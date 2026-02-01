import pygame
from src.ui.rendering.components.speed_gear_display import SpeedGearDisplay
from src.ui.rendering.components.steering_indicator import SteeringIndicator
from src.ui.rendering.components.indicator_bars import IndicatorBars
from src.core.infrastructure.config_manager import ConfigManager


class DashboardCardRenderer:
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
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        r, g, b = bg_color[0], bg_color[1], bg_color[2]

        top_color = (
            min(255, int(r * self._gradient_top_multiplier)),
            min(255, int(g * self._gradient_top_multiplier)),
            min(255, int(b * self._gradient_top_multiplier)),
        )
        bottom_color = (
            int(r * self._gradient_bottom_multiplier),
            int(g * self._gradient_bottom_multiplier),
            int(b * self._gradient_bottom_multiplier),
        )

        alpha = bg_color[3] if len(bg_color) == 4 else self._default_alpha

        for y_offset in range(height):
            ratio = y_offset / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(temp_surface, (r, g, b, alpha), (0, y_offset), (width, y_offset))

        bg_surface.blit(temp_surface, (0, 0))
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(mask, self._mask_color, (0, 0, width, height), border_radius=self._border_radius)
        bg_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            border_surf, self._border_color, (0, 0, width, height), width=1, border_radius=self._border_radius
        )
        bg_surface.blit(border_surf, (0, 0))

        surface.blit(bg_surface, (position_x, position_y))

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
