from abc import ABC, abstractmethod
import pygame
from src.core.domain.telemetry_data import TelemetryData


class Widget(ABC):
    def __init__(self, position_x: int, position_y: int, width: int, height: int):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(position_x, position_y, width, height)

    def set_position(self, position_x: int, position_y: int) -> None:
        self.position_x = position_x
        self.position_y = position_y
        self.rect.x = position_x
        self.rect.y = position_y

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
