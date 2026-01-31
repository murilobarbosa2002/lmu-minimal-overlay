import pygame
from src.ui.widgets.widget import Widget
from src.core.domain.telemetry_data import TelemetryData


class DashboardCard(Widget):
    def __init__(self, x: int, y: int, width: int = 350, height: int = 130):
        super().__init__(x, y, width, height)
        self.speed = 0.0
        self.gear = 0
        self.unit = "km/h"
        self.steering_angle = 0.0
        self.throttle_pct = 0.0
        self.brake_pct = 0.0
        self.ffb_level = 0.0
        self.is_dragging = False
        self.drag_offset = (0, 0)
        
        self.bg_color = (0, 0, 0, 180)
        self.text_color = (255, 255, 255)
        self.gear_color = (255, 200, 0)

    def set_unit(self, unit: str) -> None:
        if unit in ["km/h", "mph"]:
            self.unit = unit

    def update(self, data: TelemetryData) -> None:
        raw_speed = data.speed
        if self.unit == "mph":
            raw_speed *= 0.621371
            
        self.speed = round(raw_speed)
        self.gear = data.gear
        self.steering_angle = data.steering_angle
        self.throttle_pct = data.throttle_pct
        self.brake_pct = data.brake_pct
        self.ffb_level = data.ffb_level

    def draw(self, surface: pygame.Surface) -> None:
        from src.ui.rendering.dashboard_card_renderer import DashboardCardRenderer
        
        if not hasattr(self, '_renderer'):
            self._renderer = DashboardCardRenderer()
        
        self._renderer.render(
            surface=surface,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            speed=self.speed,
            gear=self.gear,
            unit=self.unit,
            steering_angle=self.steering_angle,
            throttle_pct=self.throttle_pct,
            brake_pct=self.brake_pct,
            ffb_level=self.ffb_level,
            bg_color=self.bg_color,
            text_color=self.text_color,
            gear_color=self.gear_color
        )

    def handle_input(self, event: pygame.event.Event) -> bool:
        from src.ui.behaviors.draggable import DraggableBehavior
        
        if not hasattr(self, '_draggable'):
            self._draggable = DraggableBehavior(self)
        
        return self._draggable.handle_input(event)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
