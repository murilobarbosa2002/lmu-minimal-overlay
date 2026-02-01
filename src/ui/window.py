import sys
import os
import pygame
import logging
import time
from typing import Optional

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class IWindowManager:
    pass


from src.ui.platform.transparency_handler import (
    ITransparencyHandler,
    Win32TransparencyHandler,
    NullTransparencyHandler,
)


from src.core.domain.constants import (
    PLATFORM_WIN32,
    ENV_SDL_VIDEO_WINDOW_POS,
    OFFSCREEN_COORD,
    DWM_SYNC_DELAY,
    WINDOW_FLUSH_CYCLES,
    DEFAULT_WINDOW_TITLE,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_FPS,
    DEFAULT_WINDOW_X,
    DEFAULT_WINDOW_Y,
)


class WindowManager(IWindowManager):
    def __init__(
        self,
        title: str = DEFAULT_WINDOW_TITLE,
        width: int = DEFAULT_WINDOW_WIDTH,
        height: int = DEFAULT_WINDOW_HEIGHT,
        transparency_handler: Optional[ITransparencyHandler] = None,
    ):

        self.title = title
        self.width = width
        self.height = height
        self.fps = DEFAULT_WINDOW_FPS
        self.is_running = False
        self._surface: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()

        if transparency_handler:
            self.transparency_handler = transparency_handler
        else:
            if sys.platform == PLATFORM_WIN32:
                from src.ui.platform.transparency_handler import (
                    Win32TransparencyHandler,
                )

                self.transparency_handler = Win32TransparencyHandler()
            else:
                from src.ui.platform.transparency_handler import NullTransparencyHandler

                self.transparency_handler = NullTransparencyHandler()

        self.window_position_x = DEFAULT_WINDOW_X
        self.window_position_y = DEFAULT_WINDOW_Y

    def set_position(self, position_x: int, position_y: int) -> None:
        self.window_position_x = position_x
        self.window_position_y = position_y
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (position_x, position_y)

    def init(self) -> None:
        logger.debug("Initializing WindowManager...")

        if sys.platform != PLATFORM_WIN32:
            os.environ["SDL_VIDEO_WINDOW_ALWAYS_ON_TOP"] = "1"
        else:
            logger.debug(f"Setting {ENV_SDL_VIDEO_WINDOW_POS} to off-screen")
            os.environ[ENV_SDL_VIDEO_WINDOW_POS] = (
                f"{OFFSCREEN_COORD},{OFFSCREEN_COORD}"
            )

        logger.debug("Calling pygame.init()")
        pygame.init()
        pygame.display.set_caption(self.title)

        flags = pygame.SRCALPHA | pygame.NOFRAME
        if sys.platform == PLATFORM_WIN32:
            flags |= pygame.HIDDEN

        logger.debug(f"Creating window with flags: {flags}")
        self._surface = pygame.display.set_mode((self.width, self.height), flags)

        if sys.platform == PLATFORM_WIN32:
            window_handle = pygame.display.get_wm_info()["window"]
            logger.debug(
                f"Window handle obtained: {window_handle}. Forcing off-screen..."
            )
            self.transparency_handler.set_window_pos(
                window_handle, OFFSCREEN_COORD, OFFSCREEN_COORD
            )

            logger.debug("Applying transparency...")
            self.transparency_handler.apply_transparency(window_handle)

        pygame.event.pump()

        logger.debug("Flushing buffers...")
        for _ in range(WINDOW_FLUSH_CYCLES):
            self.clear()
            pygame.display.flip()

        if sys.platform == PLATFORM_WIN32:
            logger.debug(f"Waiting {DWM_SYNC_DELAY}s for DWM to apply transparency...")
            time.sleep(DWM_SYNC_DELAY)
            logger.debug(
                f"Moving window to visible position ({self.window_position_x}, {self.window_position_y}) and showing..."
            )

            window_handle = pygame.display.get_wm_info()["window"]
            self.transparency_handler.set_window_pos(
                window_handle, self.window_position_x, self.window_position_y
            )
            self.transparency_handler.show_window(window_handle)

        self.is_running = True
        logger.debug("WindowManager initialization complete.")

    def clear(self) -> None:
        if self._surface:
            if sys.platform == PLATFORM_WIN32:
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
