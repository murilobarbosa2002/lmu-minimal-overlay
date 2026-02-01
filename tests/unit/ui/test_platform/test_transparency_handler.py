import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ui.platform.transparency_handler import (
    Win32TransparencyHandler,
    NullTransparencyHandler,
)


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

        with patch("sys.platform", "win32"):
            with patch.dict(
                "sys.modules",
                {
                    "win32gui": mock_win32gui,
                    "win32con": mock_win32con,
                    "win32api": mock_win32api,
                },
            ):
                mock_win32con.SW_SHOW = 5
                mock_win32con.SWP_NOZORDER = 4
                mock_win32con.SWP_NOSIZE = 1
                mock_win32con.SWP_SHOWWINDOW = 64
                mock_win32con.SWP_FRAMECHANGED = 32
                mock_win32con.SWP_NOMOVE = 2
                mock_win32con.HWND_TOPMOST = -1

                # New flags
                mock_win32con.WS_POPUP = 0x80000000
                mock_win32con.WS_VISIBLE = 0x10000000
                mock_win32con.GWL_STYLE = -16

                handler.apply_transparency(12345)

                # Should be called once.
                # In apply_transparency: SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED
                expected_flags = 2 | 1 | 32

                # Verify SetWindowLong called with WS_POPUP | WS_VISIBLE
                mock_win32gui.SetWindowLong.assert_any_call(
                    12345,
                    -16,  # GWL_STYLE
                    0x80000000 | 0x10000000,  # WS_POPUP | WS_VISIBLE
                )

                mock_win32gui.SetWindowPos.assert_called_once_with(
                    12345, -1, 0, 0, 0, 0, expected_flags
                )

    def test_win32_handler_set_window_pos(self):
        handler = Win32TransparencyHandler()
        mock_win32gui = MagicMock()
        mock_win32con = MagicMock()

        # Mock constants
        mock_win32con.SWP_NOZORDER = 4
        mock_win32con.SWP_NOSIZE = 1
        mock_win32con.SWP_SHOWWINDOW = 64
        mock_win32con.SWP_FRAMECHANGED = 32
        mock_win32con.SWP_NOACTIVATE = 16  # Mock SWP_NOACTIVATE

        with patch("sys.platform", "win32"):
            with patch.dict(
                "sys.modules", {"win32gui": mock_win32gui, "win32con": mock_win32con}
            ):
                handler.set_window_pos(12345, 100, 200)

                expected_flags = 4 | 1 | 64 | 16  # Added SWP_NOACTIVATE
                mock_win32gui.SetWindowPos.assert_called_once_with(
                    12345, 0, 100, 200, 0, 0, expected_flags
                )

    def test_win32_handler_set_window_pos_import_error(self):
        handler = Win32TransparencyHandler()
        with patch("sys.platform", "win32"):
            with patch.dict("sys.modules", {"win32gui": None}):
                # Should handle import error gracefully
                handler.set_window_pos(12345, 100, 200)

    def test_win32_handler_show_window(self):
        handler = Win32TransparencyHandler()
        mock_win32gui = MagicMock()
        mock_win32con = MagicMock()

        mock_win32con.SWP_NOMOVE = 2
        mock_win32con.SWP_NOSIZE = 1
        mock_win32con.SWP_SHOWWINDOW = 64
        mock_win32con.SWP_NOACTIVATE = 16

        with patch("sys.platform", "win32"):
            with patch.dict(
                "sys.modules", {"win32gui": mock_win32gui, "win32con": mock_win32con}
            ):
                handler.show_window(12345)

                expected_flags = 2 | 1 | 64 | 16
                mock_win32gui.SetWindowPos.assert_called_once_with(
                    12345, 0, 0, 0, 0, 0, expected_flags
                )

    def test_win32_handler_show_window_import_error(self):
        handler = Win32TransparencyHandler()
        with patch("sys.platform", "win32"):
            with patch.dict("sys.modules", {"win32gui": None}):
                # Should not raise
                handler.show_window(12345)

    def test_null_handler_show_window(self):
        handler = NullTransparencyHandler()
        # Should do nothing and raise no errors
        handler.show_window(12345)

    def test_null_handler_set_window_pos(self):
        handler = NullTransparencyHandler()
        # Should do nothing and raise no errors
        handler.set_window_pos(12345, 0, 0)

    def test_null_handler_does_nothing(self):
        handler = NullTransparencyHandler()
        handler.apply_transparency(12345)
        handler.show_window(12345)

    def test_win32_handler_custom_parameters(self):
        handler = Win32TransparencyHandler(chroma_key_color=(0, 255, 0), alpha=128)

        assert handler.chroma_key_color == (0, 255, 0)
        assert handler.alpha == 128

    def test_win32_handler_on_non_windows_does_nothing(self):
        handler = Win32TransparencyHandler()

        with patch("sys.platform", "linux"):
            handler.apply_transparency(12345)
            handler.show_window(12345)
            handler.set_window_pos(12345, 0, 0)
            # Should not call any windows modules(12345)
