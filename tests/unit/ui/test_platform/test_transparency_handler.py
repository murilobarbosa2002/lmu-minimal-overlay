import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ui.platform.transparency_handler import Win32TransparencyHandler, NullTransparencyHandler


class TestWin32TransparencyHandler:
    def test_win32_handler_applies_transparency_successfully(self):
        handler = Win32TransparencyHandler()
        
        mock_win32gui = MagicMock()
        mock_win32con = MagicMock()
        mock_win32api = MagicMock()
        
        mock_win32api.RGB.return_value = 0xFF0080
        mock_win32con.GWL_EXSTYLE = -20
        mock_win32con.WS_EX_LAYERED = 0x80000
        mock_win32con.LWA_COLORKEY = 1
        mock_win32con.LWA_ALPHA = 2
        mock_win32gui.GetWindowLong.return_value = 0
        
        with patch('sys.platform', 'win32'):
            with patch.dict('sys.modules', {
                'win32gui': mock_win32gui,
                'win32con': mock_win32con,
                'win32api': mock_win32api
            }):
                handler.apply_transparency(12345)
                
                mock_win32gui.GetWindowLong.assert_called_once()
                mock_win32gui.SetWindowLong.assert_called_once()
                mock_win32gui.SetLayeredWindowAttributes.assert_called_once()

    def test_null_handler_does_nothing(self):
        handler = NullTransparencyHandler()
        handler.apply_transparency(12345)

    def test_win32_handler_custom_parameters(self):
        handler = Win32TransparencyHandler(chroma_key_color=(0, 255, 0), alpha=128)
        
        assert handler.chroma_key_color == (0, 255, 0)
        assert handler.alpha == 128

    def test_win32_handler_on_non_windows_does_nothing(self):
        handler = Win32TransparencyHandler()
        
        with patch('sys.platform', 'linux'):
            handler.apply_transparency(12345)
