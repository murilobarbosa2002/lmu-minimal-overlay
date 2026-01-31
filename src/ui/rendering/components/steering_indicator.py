import pygame
import math


class SteeringIndicator:
    """Component for displaying steering wheel angle"""
    
    def __init__(self, radius: int = 30):
        self.radius = radius
    
    def render(
        self,
        surface: pygame.Surface,
        cx: int,
        cy: int,
        angle: float,
        color: tuple[int, int, int]
    ) -> None:
        """Render steering wheel indicator at center (cx, cy) with angle in degrees"""
        # Draw outer circle
        pygame.draw.circle(surface, color, (cx, cy), self.radius, 2)
        
        # Draw center dot
        pygame.draw.circle(surface, color, (cx, cy), 3)
        
        # Draw angle indicator line
        line_length = self.radius - 5
        angle_rad = -math.radians(angle)  # Negative for correct rotation direction
        end_x = cx + int(line_length * math.sin(angle_rad))
        end_y = cy + int(line_length * math.cos(angle_rad))
        pygame.draw.line(surface, color, (cx, cy), (end_x, end_y), 3)
