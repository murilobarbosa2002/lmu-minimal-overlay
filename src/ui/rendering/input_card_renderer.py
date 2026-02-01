import pygame
from src.ui.rendering.components.speed_gear_display import SpeedGearDisplay
from src.ui.rendering.components.steering_indicator import SteeringIndicator
from src.ui.rendering.components.indicator_bars import IndicatorBars
from src.ui.rendering.components.card_background import CardBackground
from src.core.infrastructure.config_manager import ConfigManager


class InputCardRenderer:
    def __init__(self):
        config = ConfigManager()
        theme = config.get_theme("dashboard_card")

        self.speed_gear = SpeedGearDisplay()
        self.steering = SteeringIndicator()
        self.bars = IndicatorBars()

        self._border_radius = theme.get("border_radius", 24)
        self._border_color = tuple(theme.get("border_color", [255, 255, 255, 30]))
        self._mask_color = tuple(theme.get("mask_color", [255, 255, 255]))
        self._lateral_padding = theme.get("lateral_padding", 20)
        self._gradient_top_multiplier = theme.get("gradient_top_multiplier", 1.2)
        self._gradient_bottom_multiplier = theme.get("gradient_bottom_multiplier", 0.8)
        self._default_alpha = theme.get("default_alpha", 240)
        
        self.background = CardBackground(
            border_radius=self._border_radius,
            border_color=self._border_color,
            mask_color=self._mask_color,
            gradient_top_multiplier=self._gradient_top_multiplier,
            gradient_bottom_multiplier=self._gradient_bottom_multiplier,
            default_alpha=self._default_alpha
        )

        self._speed_gear_left_margin = theme.get("speed_gear_left_margin", 10)
        self._speed_gear_horizontal_margin = theme.get("speed_gear_horizontal_margin", 20)
        self._bars_height = theme.get("bars_height", 90)

    def render(
        self,
        surface: pygame.Surface,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        speed: float,
        gear: int,
        unit: str,
        rpm: int,
        max_rpm: int,
        steering_angle: float,
        throttle_pct: float,
        brake_pct: float,
        ffb_level: float,
        bg_color: tuple,
        text_color: tuple,
        gear_color: tuple,
    ) -> None:
        self.background.render(surface, position_x, position_y, width, height, bg_color)

        steering_cx = position_x + self._lateral_padding + self.steering.radius
        steering_cy = position_y + height // 2
        self.steering.render(surface, steering_cx, steering_cy, steering_angle, text_color)

        bars_total_width = self.bars.get_total_width()
        bars_x = position_x + width - self._lateral_padding - bars_total_width

        steering_right_edge = self._lateral_padding + self.steering.radius * 2
        bars_left_edge = width - self._lateral_padding - bars_total_width
        speed_gear_x = position_x + steering_right_edge + self._speed_gear_left_margin
        speed_gear_w = bars_left_edge - steering_right_edge - self._speed_gear_horizontal_margin
        speed_gear_y = position_y
        speed_gear_h = height

        self.speed_gear.render(
            surface,
            speed_gear_x,
            speed_gear_y,
            speed_gear_w,
            speed_gear_h,
            speed,
            gear,
            unit,
            rpm,
            max_rpm,
            text_color,
            gear_color,
        )

        bars_y = position_y + (height - self._bars_height) // 2
        self.bars.render(surface, bars_x, bars_y, throttle_pct, brake_pct, ffb_level, text_color)
