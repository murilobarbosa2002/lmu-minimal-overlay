import pygame
from src.ui.widgets.widget import Widget
from src.core.domain.telemetry_data import TelemetryData
from src.ui.interfaces.i_font_provider import IFontProvider
from src.ui.behaviors.draggable import DraggableBehavior
from src.ui.rendering.pedals_renderer import PedalsRenderer


class Pedals(Widget):
    def __init__(self, x: int, y: int, font_provider: IFontProvider):
        super().__init__(x, y, width=120, height=180)
        self.font_provider = font_provider
        self.renderer = PedalsRenderer(bar_width=30, bar_height=150, spacing=10)
        
        self.throttle_pct = 0.0
        self.brake_pct = 0.0
        self.clutch_pct = 0.0

    def update(self, data: TelemetryData) -> None:
        self.throttle_pct = data.throttle_pct
        self.brake_pct = data.brake_pct
        self.clutch_pct = data.clutch_pct

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.render(
            surface,
            self.x,
            self.y,
            self.throttle_pct,
            self.brake_pct,
            self.clutch_pct,
            self.font_provider
        )

    def handle_input(self, event: pygame.event.Event) -> bool:
        draggable = DraggableBehavior(self)
        return draggable.handle_input(event)
