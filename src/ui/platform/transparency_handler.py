import sys


class ITransparencyHandler:
    def apply_transparency(self, hwnd: int) -> None:
        pass

    def show_window(self, hwnd: int) -> None:
        pass

    def set_window_pos(self, hwnd: int, x: int, y: int) -> None:
        pass


class Win32TransparencyHandler(ITransparencyHandler):
    def __init__(self, chroma_key_color: tuple[int, int, int] = (255, 0, 128), alpha: int = 217):
        self.chroma_key_color = chroma_key_color
        self.alpha = alpha

    def apply_transparency(self, window_handle: int) -> None:
        if sys.platform != "win32":
            return

        try:
            import win32gui
            import win32con
            import win32api

            win32gui.SetWindowLong(window_handle, win32con.GWL_STYLE, win32con.WS_POPUP | win32con.WS_VISIBLE)

            ex_style = win32gui.GetWindowLong(window_handle, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(window_handle, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED)

            win32gui.SetLayeredWindowAttributes(
                window_handle, win32api.RGB(*self.chroma_key_color), 0, win32con.LWA_COLORKEY
            )

            win32gui.SetWindowPos(
                window_handle, 
                win32con.HWND_TOPMOST, 
                0, 0, 0, 0, 
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED
            )
        except ImportError:
            pass

    def show_window(self, window_handle: int) -> None:
        if sys.platform != "win32":
            return
        try:
            import win32gui
            import win32con
            flags = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE
            win32gui.SetWindowPos(window_handle, 0, 0, 0, 0, 0, flags)
        except ImportError:
            pass

    def set_window_pos(self, window_handle: int, position_x: int, position_y: int) -> None:
        if sys.platform != "win32":
            return
        try:
            import win32gui
            import win32con
            
            flags = win32con.SWP_NOZORDER | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE
            win32gui.SetWindowPos(window_handle, 0, position_x, position_y, 0, 0, flags)
        except ImportError:
            pass


class NullTransparencyHandler(ITransparencyHandler):
    def apply_transparency(self, window_handle: int) -> None:
        pass

    def show_window(self, window_handle: int) -> None:
        pass

    def set_window_pos(self, window_handle: int, position_x: int, position_y: int) -> None:
        pass
