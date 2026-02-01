import pygame
from src.core.application.interfaces.state import IApplicationState
from src.core.domain.telemetry_data import TelemetryData
from src.ui.widgets.widget import Widget
from src.core.infrastructure.config_manager import ConfigManager


class EditState(IApplicationState):
    def __init__(self, context, widgets: list[Widget]):
        super().__init__(context)
        self.widgets = widgets
        self.selected_widget: Widget | None = None
        self._time_accumulator = 0.0

        config = ConfigManager()
        theme = config.get_theme("edit_mode")

        self._selection_color = tuple(theme.get("selection_color", [0, 255, 255]))
        self._selection_border_width = theme.get("selection_border_width", 2)
        self._selection_border_radius = theme.get("selection_border_radius", 8)
        self._padding_base = (
            theme.get("padding_min", 8) + theme.get("padding_max", 12)
        ) / 2
        self._padding_oscillation = (
            theme.get("padding_max", 12) - theme.get("padding_min", 8)
        ) / 2

    def on_enter(self) -> None:
        self._time_accumulator = 0.0

    def on_exit(self) -> None:
        self.selected_widget = None

    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.selected_widget = None
            for widget in self.widgets:
                if widget.get_rect().collidepoint(mouse_pos):
                    self.selected_widget = widget

        handled = False
        for widget in self.widgets:
            if widget.handle_input(event):
                handled = True

        return handled

    def update(self, data: TelemetryData) -> None:
        self._time_accumulator += 0.05

        for widget in self.widgets:
            widget.update(data)

    def draw(self, surface: pygame.Surface) -> None:
        for widget in self.widgets:
            widget.draw(surface)

        if self.selected_widget:
            import math

            padding_oscillation = self._padding_oscillation * math.sin(
                self._time_accumulator * 4
            )
            current_padding = self._padding_base + padding_oscillation

            rect = self.selected_widget.get_rect()
            selection_rect = rect.inflate(current_padding * 2, current_padding * 2)

            pygame.draw.rect(
                surface,
                (*self._selection_color, 255),
                selection_rect,
                self._selection_border_width,
                border_radius=self._selection_border_radius,
            )
