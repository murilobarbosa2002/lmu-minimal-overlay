import unittest
import json
import os
from unittest.mock import patch, mock_open
from src.core.infrastructure.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        # Reset Singleton instance before each test
        ConfigManager._instance = None
        
    def tearDown(self):
        ConfigManager._instance = None

    def test_singleton_instance(self):
        """Verify ConfigManager behaves as a Singleton."""
        instance1 = ConfigManager()
        instance2 = ConfigManager()
        self.assertIs(instance1, instance2)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_defaults_when_no_file(self, mock_file, mock_exists):
        """Verify defaults are loaded when config files do not exist."""
        mock_exists.return_value = False
        
        manager = ConfigManager()
        
        # Check if default config was loaded
        self.assertEqual(manager.get_config("version"), "1.0.0")
        
        # Check if default layout was loaded
        layout = manager.get_layout("window")
        self.assertIsInstance(layout, dict)
        self.assertEqual(layout["width"], 1920)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_existing_config(self, mock_file, mock_exists):
        """Verify existing configuration is loaded correctly."""
        mock_exists.return_value = True
        
        # Mock file content
        mock_config = json.dumps({"version": "2.0.0", "custom_key": "value"})
        mock_file.side_effect = [
            mock_open(read_data=mock_config).return_value,  # config.json
            mock_open(read_data="{}").return_value          # layout.json
        ]
        
        manager = ConfigManager()
        
        self.assertEqual(manager.get_config("version"), "2.0.0")
        self.assertEqual(manager.get_config("custom_key"), "value")

    @patch("src.core.infrastructure.config_manager.json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_config(self, mock_file, mock_json_dump):
        """Verify save_config writes to disk."""
        # Setup (mock exists to avoid initial save on init)
        with patch("os.path.exists", return_value=True):
             # Mock initial load
            with patch("json.load", return_value={}):
                manager = ConfigManager()

        manager.set_config("new_key", 123)
        manager.save_config()
        
        # Verify file was opened for writing
        mock_file.assert_called_with("config.json", 'w')
        
        # Verify json.dump was called
        # We check if the dictionary passed contains our new key
        args, _ = mock_json_dump.call_args
        self.assertEqual(args[0]["new_key"], 123)

    @patch("os.path.exists")
    def test_get_set_layout(self, mock_exists):
        """Verify get and set layout methods."""
        mock_exists.return_value = False # Force defaults
        
        # We mocking open so it doesn't fail on save
        with patch("builtins.open", mock_open()):
            manager = ConfigManager()
            
            manager.set_layout("custom_widget", {"x": 10, "y": 10})
            retrieved = manager.get_layout("custom_widget")
            
            self.assertEqual(retrieved, {"x": 10, "y": 10})

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_handles_corruption_error(self, mock_file, mock_exists):
        """Verify fallback to defaults on corrupted config."""
        mock_exists.return_value = True
        
        # Mock malformed custom content
        mock_file.side_effect = [
            mock_open(read_data="INVALID JSON").return_value,
            mock_open(read_data="{}").return_value 
        ]
        
        manager = ConfigManager()
        
        # Should fallback to default
        self.assertEqual(manager.get_config("version"), "1.0.0")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_layout_handles_corruption_error(self, mock_file, mock_exists):
        """Verify fallback to defaults on corrupted layout."""
        mock_exists.return_value = True
        
        mock_file.side_effect = [
            mock_open(read_data="{}").return_value, 
            mock_open(read_data="{ INVALID JSON").return_value
        ]
        
        manager = ConfigManager()
        
        layout = manager.get_layout("window")
        self.assertEqual(layout["width"], 1920)

    @patch("src.core.infrastructure.config_manager.json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_json_handles_io_error(self, mock_file, mock_json):
        """Verify save handles IOError silently."""
        with patch("os.path.exists", return_value=False):
            manager = ConfigManager()
            
        mock_file.side_effect = IOError("Disk full")
        
        # Should not raise
        manager.save_config()
