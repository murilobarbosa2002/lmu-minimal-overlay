import pygame
from typing import Optional

class FontManager:
    _fonts: dict[tuple[str, int], pygame.font.Font] = {}

    @classmethod
    def get_font(cls, size: int, bold: bool = False, font_name: Optional[str] = None) -> pygame.font.Font:
        key = (font_name or "default", size)
        if key not in cls._fonts:
            if not pygame.font.get_init():
                pygame.font.init()
            
            font = pygame.font.SysFont(font_name, size, bold=bold)
            cls._fonts[key] = font
            
        return cls._fonts[key]
