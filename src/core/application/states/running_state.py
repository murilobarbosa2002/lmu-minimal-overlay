import pygame
from src.core.application.interfaces.state import IApplicationState
from src.core.domain.telemetry_data import TelemetryData
from src.ui.widgets.widget import Widget

class RunningState(IApplicationState):
    def __init__(self, context, widgets: list[Widget]):
        super().__init__(context)
        self.widgets = widgets

    def handle_input(self, event: pygame.event.Event) -> bool:
        return False

    def update(self, data: TelemetryData) -> None:
        for widget in self.widgets:
            widget.update(data)

    def draw(self, surface: pygame.Surface) -> None:
        for widget in self.widgets:
            widget.draw(surface)
