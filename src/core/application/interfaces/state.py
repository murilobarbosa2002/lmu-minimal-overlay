from abc import ABC, abstractmethod
import pygame
from src.core.domain.telemetry_data import TelemetryData

class IApplicationState(ABC):
    def __init__(self, context):
        self.context = context

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        pass

    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
