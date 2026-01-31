import pygame
from src.ui.rendering.components import (
    SteeringIndicator,
    SpeedGearDisplay,
    IndicatorBars
)


class SpeedometerRenderer:
    """Orchestrates rendering of dashboard card components"""
    
    def __init__(self):
        self.steering = SteeringIndicator(radius=30)
        self.speed_gear = SpeedGearDisplay()
        self.bars = IndicatorBars(spacing=12)
    
    def render(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        speed: float,
        gear: int,
        unit: str,
        steering_angle: float,
        throttle_pct: float,
        brake_pct: float,
        ffb_level: float,
        bg_color: tuple,
        text_color: tuple,
        gear_color: tuple
    ) -> None:
        """Render complete dashboard card with all components"""
        # Draw background with rounded corners
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, bg_color, (0, 0, width, height), border_radius=8)
        surface.blit(bg_surface, (x, y))
        
        # Calculate section positions
        steering_width = 80
        bars_width = 130
        speed_width = width - steering_width - bars_width
        
        # Render steering indicator (LEFT)
        steering_cx = x + 40
        steering_cy = y + height // 2
        self.steering.render(surface, steering_cx, steering_cy, steering_angle, text_color)
        
        # Render speed/gear display (CENTER)
        speed_x = x + steering_width
        self.speed_gear.render(
            surface, speed_x, y, speed_width, height,
            speed, gear, unit, text_color, gear_color
        )
        
        # Render indicator bars (RIGHT)
        bars_x = x + steering_width + speed_width + 15
        bars_y = y + (height - 90) // 2
        self.bars.render(
            surface, bars_x, bars_y,
            throttle_pct, brake_pct, ffb_level, text_color
        )
