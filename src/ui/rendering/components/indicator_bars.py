import pygame
from src.ui.rendering.components.bar import Bar


class IndicatorBars:
    """Composite component managing 3 bars (throttle, brake, force feedback)"""
    
    def __init__(self, spacing: int = 12):
        self.spacing = spacing
        self.throttle_bar = Bar(label="T", color=(0, 255, 0))
        self.brake_bar = Bar(label="B", color=(255, 0, 0))
        self.ffb_bar = Bar(label="F", color=(255, 165, 0))
    
    def render(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        throttle: float,
        brake: float,
        ffb: float,
        text_color: tuple[int, int, int]
    ) -> None:
        """Render all three bars horizontally"""
        current_x = x
        
        self.throttle_bar.render(surface, current_x, y, throttle, text_color)
        current_x += self.throttle_bar.width + self.spacing
        
        self.brake_bar.render(surface, current_x, y, brake, text_color)
        current_x += self.brake_bar.width + self.spacing
        
        self.ffb_bar.render(surface, current_x, y, ffb, text_color)
    
    def get_total_width(self) -> int:
        """Calculate total width needed for all bars"""
        return (self.throttle_bar.width * 3) + (self.spacing * 2)
