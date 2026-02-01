import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock
from src.ui.utils.fonts import FontManager
import io


class TestFontManager:
    def setup_method(self):
        # Reset cache before each test
        FontManager._fonts = {}
        pygame.init()

    def teardown_method(self):
        FontManager._fonts = {}
        pygame.quit()

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("pygame.font.Font")
    def test_get_font_success(self, mock_font_class, mock_exists, mock_open):
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = b"fontdata"
        mock_open.return_value.__enter__.return_value = mock_file

        mock_font = Mock()
        mock_font.render.return_value = Mock()
        mock_font_class.return_value = mock_font

        result = FontManager.get_font(24)

        assert result is mock_font
        # Verify called with BytesIO
        call_args = mock_font_class.call_args
        assert isinstance(call_args[0][0], io.BytesIO)
        assert call_args[0][0].getvalue() == b"fontdata"

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("pygame.font.SysFont")
    def test_get_font_fallback_to_sysfont(self, mock_sysfont, mock_exists, mock_open):
        mock_exists.return_value = False
        mock_font = Mock()
        mock_sysfont.return_value = mock_font

        result = FontManager.get_font(24)

        assert result is mock_font
        mock_sysfont.assert_called_once()  # Should try sysfont if file doesn't exist

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("pygame.font.Font")
    @patch("pygame.font.SysFont")
    @patch("builtins.print")
    def test_font_load_exception(
        self, mock_print, mock_sysfont, mock_font_class, mock_exists, mock_open
    ):
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Simulate loading error
        mock_font_class.side_effect = Exception("File load error")

        # Fallback to sysfont
        mock_sysfont.return_value = Mock()

        FontManager.get_font(24)

        # Error is suppressed
        mock_print.assert_not_called()

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("pygame.font.Font")
    @patch("pygame.font.SysFont")
    def test_get_font_all_fails_default(
        self, mock_sysfont, mock_font_class, mock_exists, mock_open
    ):
        mock_exists.return_value = False
        # Sysfont fails too
        mock_sysfont.side_effect = Exception("Sysfont error")

        mock_default_font = Mock()
        # Default font uses Font(None, size)
        mock_font_class.return_value = mock_default_font

        result = FontManager.get_font(24)

        assert result is mock_default_font

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("pygame.font.SysFont")
    def test_font_caching(self, mock_sysfont, mock_exists, mock_open):
        mock_exists.return_value = False
        mock_font = Mock()
        mock_sysfont.return_value = mock_font

        # First call
        result1 = FontManager.get_font(24)
        # Second call
        result2 = FontManager.get_font(24)

        assert result1 is result2
        assert mock_sysfont.call_count == 1

    @patch("pygame.font.get_init")
    @patch("pygame.font.init")
    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("pygame.font.SysFont")
    def test_font_init_called(
        self, mock_sysfont, mock_exists, mock_open, mock_init, mock_get_init
    ):
        mock_exists.return_value = False
        mock_get_init.return_value = False  # Force init
        mock_sysfont.return_value = Mock()

        FontManager.get_font(24)

        mock_init.assert_called_once()
