import pygame
from src.ui.utils.fonts import FontManager


class Bar:
    """Individual vertical bar component"""
    
    def __init__(
        self,
        label: str,
        color: tuple[int, int, int],
        width: int = 18,
        height: int = 70
    ):
        self.label = label
        self.color = color
        self.width = width
        self.height = height
    
    def render(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        value: float,
        text_color: tuple[int, int, int]
    ) -> None:
        """Render the bar at given position with value (0.0-1.0)"""
        # Clamp value
        value = max(0.0, min(1.0, value))
        
        # Render label
        label_font = FontManager.get_font(size=14, bold=True)
        label_surf = label_font.render(self.label, True, text_color)
        label_x = x + self.width // 2 - label_surf.get_width() // 2
        surface.blit(label_surf, (label_x, y))
        
        # Bar position (below label)
        bar_y = y + 20
        bg_rect = pygame.Rect(x, bar_y, self.width, self.height)
        
        # Draw background (dark)
        pygame.draw.rect(surface, (40, 40, 40), bg_rect, border_radius=3)
        
        # Draw fill (from bottom up)
        fill_height = int(self.height * value)
        if fill_height > 0:
            fill_rect = pygame.Rect(
                x,
                bar_y + self.height - fill_height,
                self.width,
                fill_height
            )
            pygame.draw.rect(surface, self.color, fill_rect, border_radius=3)
