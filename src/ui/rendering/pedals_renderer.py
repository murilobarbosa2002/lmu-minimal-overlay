import pygame
from typing import Tuple
from src.ui.interfaces.i_font_provider import IFontProvider


class PedalsRenderer:
    def __init__(self, bar_width: int = 30, bar_height: int = 150, spacing: int = 10):
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.spacing = spacing
        self.throttle_color = (0, 255, 100)
        self.brake_color = (255, 50, 50)
        self.clutch_color = (100, 150, 255)
        self.bg_color = (40, 40, 40)
        self.border_color = (80, 80, 80)

    def render(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        throttle_pct: float,
        brake_pct: float,
        clutch_pct: float,
        font_provider: IFontProvider
    ) -> None:
        pedals = [
            (throttle_pct, self.throttle_color, "T"),
            (brake_pct, self.brake_color, "B"),
            (clutch_pct, self.clutch_color, "C")
        ]
        
        for i, (pct, color, label) in enumerate(pedals):
            bar_x = x + i * (self.bar_width + self.spacing)
            self._draw_bar(surface, bar_x, y, pct, color, font_provider, label)

    def _draw_bar(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        percentage: float,
        color: Tuple[int, int, int],
        font_provider: IFontProvider,
        label: str
    ) -> None:
        clamped_pct = max(0.0, min(1.0, percentage))
        
        pygame.draw.rect(surface, self.bg_color, (x, y, self.bar_width, self.bar_height))
        pygame.draw.rect(surface, self.border_color, (x, y, self.bar_width, self.bar_height), 2)
        
        fill_height = int(self.bar_height * clamped_pct)
        if fill_height > 0:
            fill_y = y + self.bar_height - fill_height
            pygame.draw.rect(surface, color, (x, fill_y, self.bar_width, fill_height))
        
        font = font_provider.get_font(14)
        label_text = font.render(label, True, (200, 200, 200))
        label_rect = label_text.get_rect(centerx=x + self.bar_width // 2, top=y + self.bar_height + 5)
        surface.blit(label_text, label_rect)
        
        pct_text = font.render(f"{int(clamped_pct * 100)}%", True, (200, 200, 200))
        pct_rect = pct_text.get_rect(centerx=x + self.bar_width // 2, bottom=y - 5)
        surface.blit(pct_text, pct_rect)
