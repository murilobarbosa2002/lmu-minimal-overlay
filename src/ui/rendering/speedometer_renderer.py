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
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        top_color = (30, 35, 45, 242)
        bottom_color = (5, 5, 8, 242)
        
        for y_offset in range(height):
            ratio = y_offset / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            a = int(top_color[3] * (1 - ratio) + bottom_color[3] * ratio)
            pygame.draw.line(temp_surface, (r, g, b, a), (0, y_offset), (width, y_offset))
        
        bg_surface.blit(temp_surface, (0, 0))
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), (0, 0, width, height), border_radius=24)
        bg_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, (255, 255, 255, 30), (0, 0, width, height), width=1, border_radius=24)
        bg_surface.blit(border_surf, (0, 0))
        
        surface.blit(bg_surface, (x, y))
        
        lateral_padding = 20
        
        steering_cx = x + lateral_padding + self.steering.radius
        steering_cy = y + height // 2
        self.steering.render(surface, steering_cx, steering_cy, steering_angle, text_color)
        
        bars_total_width = self.bars.get_total_width()
        bars_x = x + width - lateral_padding - bars_total_width
        
        steering_right_edge = lateral_padding + self.steering.radius * 2
        bars_left_edge = width - lateral_padding - bars_total_width
        speed_x = x + steering_right_edge + 10
        speed_width = bars_left_edge - steering_right_edge - 20
        
        self.speed_gear.render(
            surface, speed_x, y, speed_width, height,
            speed, gear, unit, text_color, gear_color
        )
        bars_y = y + (height - 90) // 2
        self.bars.render(
            surface, bars_x, bars_y,
            throttle_pct, brake_pct, ffb_level, text_color
        )
