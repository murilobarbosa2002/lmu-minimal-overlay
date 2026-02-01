import pygame
import sys
import os
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IWindowManager:
    pass
from src.ui.platform.transparency_handler import ITransparencyHandler, Win32TransparencyHandler, NullTransparencyHandler


class WindowManager(IWindowManager):
    def __init__(
        self,
        title: str = "LMU Overlay",
        width: int = 800,
        height: int = 600,
        transparency_handler: ITransparencyHandler | None = None,
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
                Win32TransparencyHandler() if sys.platform == "win32" else NullTransparencyHandler()
            )
        else:
            self.transparency_handler = transparency_handler

        self.x = 0
        self.y = 0

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (x, y)

    def init(self) -> None:
        logger.debug("Initializing WindowManager...")
        if sys.platform != "win32":
            os.environ["SDL_VIDEO_WINDOW_ALWAYS_ON_TOP"] = "1"
        else:
            logger.debug("Setting SDL_VIDEO_WINDOW_POS to off-screen")
            os.environ['SDL_VIDEO_WINDOW_POS'] = "-32000,-32000"

        logger.debug("Calling pygame.init()")
        pygame.init()
        pygame.display.set_caption(self.title)
        
        flags = pygame.SRCALPHA | pygame.NOFRAME
        if sys.platform == "win32":
            flags |= pygame.HIDDEN
            
        logger.debug(f"Creating window with flags: {flags}")
        self._surface = pygame.display.set_mode((self.width, self.height), flags)

        if sys.platform == "win32":
            hwnd = pygame.display.get_wm_info()["window"]
            logger.debug(f"Window handle obtained: {hwnd}. Forcing off-screen...")
            self.transparency_handler.set_window_pos(hwnd, -32000, -32000)
            
            logger.debug("Applying transparency...")
            self.transparency_handler.apply_transparency(hwnd)
        
        pygame.event.pump()

        logger.debug("Flushing buffers...")
        for _ in range(2):
            self.clear()
            pygame.display.flip()

        if sys.platform == "win32":
            logger.debug("Waiting 100ms for DWM to apply transparency...")
            time.sleep(0.1)
            logger.debug(f"Moving window to visible position ({self.x}, {self.y}) and showing...")
            hwnd = pygame.display.get_wm_info()["window"]
            self.transparency_handler.set_window_pos(hwnd, self.x, self.y)
            self.transparency_handler.show_window(hwnd)

        self._is_running = True
        logger.debug("WindowManager initialization complete.")

    def clear(self) -> None:
        if self._surface:
            if sys.platform == "win32":
                self._surface.fill((255, 0, 128))
            else:
                self._surface.fill((0, 0, 0, 0))

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
