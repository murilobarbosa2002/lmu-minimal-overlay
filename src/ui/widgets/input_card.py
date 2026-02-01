import pygame
from src.ui.widgets.widget import Widget
from src.core.domain.telemetry_data import TelemetryData
from src.core.infrastructure.config_manager import ConfigManager
from src.core.domain.constants import (
    INITIAL_SPEED,
    INITIAL_STEERING,
    INITIAL_THROTTLE,
    INITIAL_BRAKE,
    KM_TO_MILES,
)


class InputCard(Widget):
    def __init__(
        self, position_x: int, position_y: int, width: int = None, height: int = None
    ):
        config = ConfigManager()
        theme = config.get_theme("dashboard_card")
        defaults = config.get_defaults("telemetry")

        self.position_x = position_x
        self.position_y = position_y
        self.width = width if width is not None else theme.get("width", 350)
        self.height = height if height is not None else theme.get("height", 130)
        super().__init__(self.position_x, self.position_y, self.width, self.height)

        self.speed = defaults.get("speed", INITIAL_SPEED)
        self.gear = defaults.get("gear", 1)
        self.rpm = defaults.get("rpm", 1500)
        self.max_rpm = defaults.get("max_rpm", 8000)
        self.unit = defaults.get("unit", "km/h")
        self.steering_angle = defaults.get("steering_angle", INITIAL_STEERING)
        self.throttle_pct = defaults.get("throttle_pct", INITIAL_THROTTLE)
        self.brake_pct = defaults.get("brake_pct", INITIAL_BRAKE)
        self.ffb_level = defaults.get("ffb_level", INITIAL_THROTTLE)
        self.is_dragging = False
        self.drag_offset = (0, 0)

        self.bg_color = tuple(theme.get("bg_color", [10, 20, 30, 242]))
        self.text_color = tuple(theme.get("text_color", [255, 255, 255]))
        self.gear_color = tuple(theme.get("gear_color", [255, 200, 0]))
        self._drag_color = tuple(theme.get("bg_color_dragging", [25, 35, 50, 180]))

    def set_unit(self, unit: str) -> None:
        if unit in ["km/h", "mph"]:
            self.unit = unit

    def update(self, data: TelemetryData) -> None:
        raw_speed = data.speed
        if self.unit == "mph":
            raw_speed *= KM_TO_MILES

        self.speed = round(raw_speed)
        self.gear = data.gear
        self.rpm = data.rpm
        self.max_rpm = data.max_rpm
        self.steering_angle = data.steering_angle
        self.throttle_pct = data.throttle_pct
        self.brake_pct = data.brake_pct
        self.ffb_level = data.ffb_level

    def draw(self, surface: pygame.Surface) -> None:
        from src.ui.rendering.input_card_renderer import InputCardRenderer

        if not hasattr(self, "_renderer"):
            self._renderer = InputCardRenderer()

        current_bg_color = self.bg_color
        if hasattr(self, "_draggable") and self._draggable.is_dragging:
            current_bg_color = self._drag_color

        self._renderer.render(
            surface=surface,
            position_x=self.position_x,
            position_y=self.position_y,
            width=self.width,
            height=self.height,
            speed=self.speed,
            gear=self.gear,
            unit=self.unit,
            rpm=self.rpm,
            max_rpm=self.max_rpm,
            steering_angle=self.steering_angle,
            throttle_pct=self.throttle_pct,
            brake_pct=self.brake_pct,
            ffb_level=self.ffb_level,
            bg_color=current_bg_color,
            text_color=self.text_color,
            gear_color=self.gear_color,
        )

    def handle_input(self, event: pygame.event.Event) -> bool:
        from src.ui.behaviors.draggable import DraggableBehavior

        if not hasattr(self, "_draggable"):
            self._draggable = DraggableBehavior(self)

        return self._draggable.handle_input(event)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.position_x, self.position_y, self.width, self.height)

    def set_position(self, position_x: int, position_y: int) -> None:
        self.position_x = position_x
        self.position_y = position_y
