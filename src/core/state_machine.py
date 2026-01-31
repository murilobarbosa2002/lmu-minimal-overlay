from abc import ABC, abstractmethod
import pygame
from src.core.domain.telemetry_data import TelemetryData

class ApplicationState(ABC):
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


class StateMachine:
    def __init__(self):
        self.current_state: ApplicationState | None = None

    def change_state(self, new_state: ApplicationState) -> None:
        if self.current_state:
            self.current_state.on_exit()
        
        self.current_state = new_state
        
        if self.current_state:
            self.current_state.on_enter()

    def handle_input(self, event: pygame.event.Event) -> bool:
        if self.current_state:
            return self.current_state.handle_input(event)
        return False

    def update(self, data: TelemetryData) -> None:
        if self.current_state:
            self.current_state.update(data)

    def draw(self, surface: pygame.Surface) -> None:
        if self.current_state:
            self.current_state.draw(surface)
