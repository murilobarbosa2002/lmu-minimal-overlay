import pygame
import os
import sys

class WindowManager:
    def __init__(self, title: str = "LMU Overlay", width: int = 800, height: int = 600):
        self.title = title
        self.width = width
        self.height = height
        self.surface: pygame.Surface | None = None
        self.is_running = False
        self.clock = pygame.time.Clock()
        self.fps = 60

    def init(self) -> None:
        pygame.init()
        pygame.display.set_caption(self.title)
        flags = pygame.SRCALPHA | pygame.NOFRAME
        self.surface = pygame.display.set_mode((self.width, self.height), flags)
        
        if sys.platform == "win32":
            try:
                import win32gui
                import win32con
                import win32api
                
                hwnd = pygame.display.get_wm_info()["window"]
                
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED)
                
                win32gui.SetLayeredWindowAttributes(
                    hwnd, 
                    win32api.RGB(255, 0, 128), 
                    217, 
                    win32con.LWA_COLORKEY | win32con.LWA_ALPHA
                )
            except ImportError:
                pass

        self.is_running = True

    def clear(self) -> None:
        if self.surface:
            self.surface.fill((255, 0, 128))

    def update_display(self) -> None:
        pygame.display.flip()
        self.clock.tick(self.fps)

    def handle_events(self) -> list[pygame.event.Event]:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
        return events

    def close(self) -> None:
        self.is_running = False
        pygame.quit()
