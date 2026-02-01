import pygame
import os
import io
from typing import Optional


class FontManager:
    _fonts: dict[tuple[str, int, bool], pygame.font.Font] = {}

    @classmethod
    def get_font(cls, size: int, bold: bool = False, font_name: Optional[str] = None) -> pygame.font.Font:
        key = (font_name or "default", size, bold)
        if key not in cls._fonts:
            if not pygame.font.get_init():
                pygame.font.init()

            bold_suffix = "-Bold.ttf" if bold else "-Regular.ttf"
            font_path = os.path.join(os.getcwd(), "assets", "fonts", f"Roboto{bold_suffix}")

            if os.path.exists(font_path):
                try:
                    with open(font_path, "rb") as f:
                        font_data = io.BytesIO(f.read())

                    font = pygame.font.Font(font_data, size)
                    font.render("test", False, (0, 0, 0))
                    cls._fonts[key] = font
                    return font
                except Exception:
                    pass

            try:
                font = pygame.font.SysFont(font_name, size, bold=bold)
                cls._fonts[key] = font
                return font
            except Exception:
                font = pygame.font.Font(None, size)
                cls._fonts[key] = font
                return font

        return cls._fonts[key]
