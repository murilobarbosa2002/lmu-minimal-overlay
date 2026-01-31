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
        flags = pygame.SRCALPHA
        if os.name == 'nt':
            flags |= pygame.NOFRAME
        else:
            flags |= pygame.RESIZABLE
        self.surface = pygame.display.set_mode((self.width, self.height), flags)
        self.is_running = True

    def set_transparent(self, transparent: bool) -> None:
        if os.name == 'nt':
            pass
        else:
            pass

    def clear(self) -> None:
        if self.surface:
            self.surface.fill((0, 0, 0, 0))

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
