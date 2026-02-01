import pytest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
import pygame
from src.core.app import OverlayApp


class TestOverlayApp:
    @pytest.fixture
    def app(self):
        mock_window = Mock()
        mock_window.surface = None
        mock_window.is_running = True
        
        mock_provider = Mock()
        mock_font_provider = Mock()
        mock_config_manager = Mock()
        mock_widget_factory = Mock()
        
        mock_config_manager.get_layout.side_effect = lambda key, default=None: [] if key == "widgets" else {}
        
        return OverlayApp(
            window=mock_window,
            provider=mock_provider,
            font_provider=mock_font_provider,
            config_manager=mock_config_manager,
            widget_factory=mock_widget_factory
        )

    def test_setup_initializes_components(self, app):
        app.setup()
        
        app.window.init.assert_called_once()
        app.provider.connect.assert_called_once()
        assert len(app.widgets) == 1
        assert app.state_machine.current_state is not None
        assert app.input_handler is not None

    def test_update_fetches_data(self, app):
        app.setup()
        mock_data = Mock()
        app.provider.get_data.return_value = mock_data
        
        with patch.object(app.state_machine, 'update') as mock_update:
            app._update()
            mock_update.assert_called_once_with(mock_data)

    def test_update_handles_provider_error(self, app):
        app.setup()
        app.provider.get_data.side_effect = Exception("Provider error")
        
        with patch.object(app.state_machine, 'update') as mock_update:
            app._update()
            mock_update.assert_not_called()

    def test_update_handles_no_data(self, app):
        app.setup()
        app.provider.get_data.return_value = None
        
        with patch.object(app.state_machine, 'update') as mock_update:
            app._update()
            mock_update.assert_not_called()

    def test_handle_input_delegates(self, app):
        app.setup()
        
        with patch.object(app.input_handler, 'handle_input') as mock_handle:
            app._handle_input()
            mock_handle.assert_called_once()

    def test_handle_input_safe_without_handler(self, app):
        app.input_handler = None
        app._handle_input()

    def test_draw_renders_to_surface(self, app):
        app.setup()
        app.window.surface = Mock()
        
        with patch.object(app.state_machine, 'draw') as mock_draw:
            with patch.object(app.window, 'clear') as mock_clear:
                with patch.object(app.window, 'update_display') as mock_update:
                    app._draw()
                    
                    mock_clear.assert_called_once()
                    mock_draw.assert_called_once_with(app.window.surface)
                    mock_update.assert_called_once()

    def test_draw_skips_if_no_surface(self, app):
        app.setup()
        app.window.surface = None
        
        with patch.object(app.state_machine, 'draw') as mock_draw:
            with patch.object(app.window, 'clear') as mock_clear:
                with patch.object(app.window, 'update_display') as mock_update:
                    app._draw()
                    
                    mock_clear.assert_called_once()
                    mock_draw.assert_not_called()
                    mock_update.assert_called_once()

    @patch('sys.exit')
    def test_run_loop_execution(self, mock_exit, app):
        # Setup property mock to return True then False
        type(app.window).is_running = PropertyMock(side_effect=[True, False])
        
        with patch.object(app, 'setup') as mock_setup:
            with patch.object(app, '_handle_input') as mock_input:
                with patch.object(app, '_update') as mock_update:
                    with patch.object(app, '_draw') as mock_draw:
                        with patch.object(app.window, 'close') as mock_close:
                            app.run()
                            
                            mock_setup.assert_called_once()
                            mock_input.assert_called_once()
                            mock_update.assert_called_once()
                            mock_draw.assert_called_once()
                            mock_close.assert_called_once()
                            mock_exit.assert_called_once()
    
    def test_setup_loads_widgets_from_config(self, app):
        # Setup mock config to return valid widget data
        app.config_manager.get_layout.side_effect = lambda key, default=None: [
            {"type": "InputCard", "x": 100, "y": 200, "width": 300, "height": 100}
        ] if key == "widgets" else {}
        
        # Setup widget factory to return a widget-like mock
        mock_widget = Mock()
        mock_widget.x = 100
        mock_widget.y = 200
        app.widget_factory.create_widget.return_value = mock_widget
        
        app.setup()
        
        assert len(app.widgets) == 1
        assert app.widgets[0].x == 100
        assert app.widgets[0].y == 200

    def test_setup_loads_multiple_widgets_from_config(self, app):
        # Setup mock config to return multiple valid widgets
        app.config_manager.get_layout.side_effect = lambda key, default=None: [
            {"type": "InputCard", "x": 100, "y": 200},
            {"type": "InputCard", "x": 500, "y": 200}
        ] if key == "widgets" else {}
        
        # Setup widget factory to return different mocks
        mock_widget1 = Mock()
        mock_widget1.x = 100
        mock_widget2 = Mock()
        mock_widget2.x = 500
        
        app.widget_factory.create_widget.side_effect = [mock_widget1, mock_widget2]
        
        app.setup()
        
        assert len(app.widgets) == 2
        assert app.widgets[0].x == 100
        assert app.widgets[1].x == 500

    def test_setup_handles_invalid_widgets(self, app):
        # Setup config with one valid and one invalid widget
        app.config_manager.get_layout.side_effect = lambda key, default=None: [
            {"type": "InputCard", "x": 100, "y": 200},
            {"type": "UnknownWidget", "x": 0, "y": 0}
        ] if key == "widgets" else {}
        
        # Configure factory to raise ValueError for unknown type
        def create_side_effect(data):
            if data["type"] == "UnknownWidget":
                raise ValueError("Unknown widget type")
            mock = Mock()
            mock.x = data["x"]
            mock.y = data["y"]
            return mock
            
        app.widget_factory.create_widget.side_effect = create_side_effect
        
        app.setup()
        
        # Should populate valid widget and skip invalid one (gracefully)
        assert len(app.widgets) == 1
        assert app.widgets[0].x == 100
        # Verification that it didn't crash is implicit by reaching here

    def test_save_state(self, app):
        # Setup valid widget for setup()
        mock_widget = Mock()
        mock_widget.x = 100
        mock_widget.y = 200
        mock_widget.width = 350
        mock_widget.height = 130
        # Mock class name for serialization
        mock_widget.__class__.__name__ = "InputCard"
        
        app.config_manager.get_layout.side_effect = lambda key, default=None: [
            {"type": "InputCard", "x": 100, "y": 200}
        ] if key == "widgets" else {}
        
        app.widget_factory.create_widget.return_value = mock_widget
        
        app.setup()
        
        # Setup window props
        app.window.x = 10
        app.window.y = 20
        app.window.width = 1920
        app.window.height = 1080
        
        app.save_state()
        
        # Verify window config saved
        app.config_manager.set_layout.assert_any_call("window", {
            "x": 10, "y": 20, "width": 1920, "height": 1080, "always_on_top": True
        })
        
        # Verify widgets saved
        # We check that set_layout was called for widgets with a list containing one dict
        args = app.config_manager.set_layout.call_args_list[-1]
        assert args[0][0] == "widgets"
        assert len(args[0][1]) == 1
        assert args[0][1][0]["type"] == "InputCard"

    @patch('sys.exit')
    def test_run_saves_state_on_exit(self, mock_exit, app):
        type(app.window).is_running = PropertyMock(side_effect=[True, False])
        
        with patch.object(app, 'setup'):
            with patch.object(app, '_handle_input'):
                with patch.object(app, '_update'):
                    with patch.object(app, '_draw'):
                        with patch.object(app.window, 'close'):
                             with patch.object(app, 'save_state') as mock_save:
                                app.run()
                                mock_save.assert_called_once()
