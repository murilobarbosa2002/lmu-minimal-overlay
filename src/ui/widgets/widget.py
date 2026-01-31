from abc import ABC, abstractmethod
import pygame
from src.core.domain.telemetry_data import TelemetryData

class Widget(ABC):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def get_rect(self) -> pygame.Rect:
        return self.rect

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        pass

    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        pass
