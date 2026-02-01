import pygame
from src.ui.rendering.components.bar import Bar
from src.core.infrastructure.config_manager import ConfigManager


class IndicatorBars:
    def __init__(self, spacing: int = None):
        config = ConfigManager()
        theme = config.get_theme("indicator_bars")

        self.spacing = spacing if spacing is not None else theme.get("spacing", 12)

        throttle_color = tuple(theme.get("throttle_color", [0, 255, 0]))
        brake_color = tuple(theme.get("brake_color", [255, 0, 0]))
        ffb_color = tuple(theme.get("ffb_color", [255, 165, 0]))

        self.throttle_bar = Bar(label="T", color=throttle_color)
        self.brake_bar = Bar(label="B", color=brake_color)
        self.ffb_bar = Bar(label="F", color=ffb_color)
        self.ffb_bar.set_bidirectional(True)

    def render(
        self,
        surface: pygame.Surface,
        position_x: int,
        position_y: int,
        throttle: float,
        brake: float,
        ffb: float,
        text_color: tuple[int, int, int],
    ) -> None:
        current_x = position_x

        self.throttle_bar.render(surface, current_x, position_y, throttle, text_color)
        current_x += self.throttle_bar.width + self.spacing

        self.brake_bar.render(surface, current_x, position_y, brake, text_color)
        current_x += self.brake_bar.width + self.spacing

        self.ffb_bar.render(surface, current_x, position_y, ffb, text_color)

    def get_total_width(self) -> int:
        return (self.throttle_bar.width * 3) + (self.spacing * 2)
