import pygame
import sys
from src.ui.interfaces.i_window_manager import IWindowManager
from src.ui.platform.transparency_handler import ITransparencyHandler, Win32TransparencyHandler, NullTransparencyHandler


class WindowManager(IWindowManager):
    def __init__(
        self, 
        title: str = "LMU Overlay", 
        width: int = 800, 
        height: int = 600,
        transparency_handler: ITransparencyHandler | None = None
    ):
        self.title = title
        self.width = width
        self.height = height
        self._surface: pygame.Surface | None = None
        self._is_running = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        if transparency_handler is None:
            self.transparency_handler = (
                Win32TransparencyHandler() if sys.platform == "win32" 
                else NullTransparencyHandler()
            )
        else:
            self.transparency_handler = transparency_handler

    def init(self) -> None:
        pygame.init()
        pygame.display.set_caption(self.title)
        flags = pygame.SRCALPHA | pygame.NOFRAME
        self._surface = pygame.display.set_mode((self.width, self.height), flags)
        
        if sys.platform == "win32":
            hwnd = pygame.display.get_wm_info()["window"]
            self.transparency_handler.apply_transparency(hwnd)

        self._is_running = True

    def clear(self) -> None:
        if self._surface:
            self._surface.fill((255, 0, 128))

    def update_display(self) -> None:
        pygame.display.flip()
        self.clock.tick(self.fps)

    def handle_events(self) -> list[pygame.event.Event]:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self._is_running = False
        return events

    def close(self) -> None:
        self._is_running = False
        pygame.quit()

    @property
    def surface(self) -> pygame.Surface | None:
        return self._surface

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool) -> None:
        self._is_running = value

