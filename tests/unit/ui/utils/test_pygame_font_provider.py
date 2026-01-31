import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock
from src.ui.utils.pygame_font_provider import PygameFontProvider


class TestPygameFontProvider:
    def setup_method(self):
        pygame.init()
        self.provider = PygameFontProvider()

    def teardown_method(self):
        pygame.quit()

    def test_initialization(self):
        provider = PygameFontProvider()
        assert provider._fonts == {}

    @patch('os.path.exists')
    @patch('pygame.font.Font')
    def test_get_font_from_assets_success(self, mock_font_class, mock_exists):
        mock_exists.return_value = True
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        mock_font_class.return_value = mock_font
        
        result = self.provider.get_font(24, bold=False)
        
        assert result is mock_font
        mock_font_class.assert_called_once()

    @patch('os.path.exists')
    @patch('pygame.font.SysFont')
    def test_get_font_assets_fails_fallback_to_system(self, mock_sysfont, mock_exists):
        mock_exists.return_value = False
        mock_font = Mock()
        mock_sysfont.return_value = mock_font
        
        result = self.provider.get_font(24)
        
        assert result is mock_font
        mock_sysfont.assert_called_once()

    @patch('os.path.exists')
    @patch('pygame.font.SysFont')
    @patch('pygame.font.Font')
    def test_get_font_system_fails_fallback_to_default(self, mock_font_class, mock_sysfont, mock_exists):
        mock_exists.return_value = False
        mock_sysfont.side_effect = Exception("System font failed")
        mock_default_font = Mock()
        mock_font_class.return_value = mock_default_font
        
        result = self.provider.get_font(24)
        
        assert result is mock_default_font
        mock_font_class.assert_called_with(None, 24)

    @patch('os.path.exists')
    @patch('pygame.font.SysFont')
    def test_font_caching(self, mock_sysfont, mock_exists):
        mock_exists.return_value = False
        mock_font = Mock()
        mock_sysfont.return_value = mock_font
        
        result1 = self.provider.get_font(24, bold=False)
        result2 = self.provider.get_font(24, bold=False)
        
        assert result1 is result2
        assert mock_sysfont.call_count == 1

    @patch('os.path.exists')
    @patch('pygame.font.SysFont')
    def test_different_sizes_create_different_fonts(self, mock_sysfont, mock_exists):
        mock_exists.return_value = False
        mock_font_24 = Mock()
        mock_font_48 = Mock()
        mock_sysfont.side_effect = [mock_font_24, mock_font_48]
        
        result1 = self.provider.get_font(24)
        result2 = self.provider.get_font(48)
        
        assert result1 is not result2
        assert mock_sysfont.call_count == 2

    @patch('pygame.font.get_init')
    @patch('pygame.font.init')
    @patch('os.path.exists')
    @patch('pygame.font.Font')
    def test_font_init_called_if_needed(self, mock_font_class, mock_exists, mock_init, mock_get_init):
        mock_get_init.return_value = False
        mock_exists.return_value = False
        mock_font = Mock()
        mock_font_class.return_value = mock_font
        
        self.provider.get_font(24)
        
        mock_init.assert_called_once()

    @patch('os.path.exists')
    @patch('pygame.font.Font')
    def test_bold_font_requested(self, mock_font_class, mock_exists):
        mock_exists.return_value = True
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        mock_font_class.return_value = mock_font
        
        self.provider.get_font(24, bold=True)
        
        call_args = mock_font_class.call_args[0]
        assert "Bold" in call_args[0]

    @patch('os.path.exists')
    @patch('pygame.font.Font')
    @patch('pygame.font.SysFont')
    @patch('builtins.print')
    def test_font_load_exception_prints_error(self, mock_print, mock_sysfont, mock_font_class, mock_exists):
        mock_exists.return_value = True
        mock_font_class.side_effect = Exception("Font error")
        mock_font = Mock()
        mock_sysfont.return_value = mock_font
        
        result = self.provider.get_font(24)
        
        assert result is mock_font
        mock_print.assert_called_once()
