import pygame
from src.ui.interfaces.i_font_provider import IFontProvider


class SpeedometerRenderer:
    def __init__(self, font_provider: IFontProvider):
        self.font_provider = font_provider
        self._bg_surface: pygame.Surface | None = None

    def create_background(self, width: int, height: int) -> pygame.Surface:
        if self._bg_surface is None:
            self._bg_surface = pygame.Surface((width, height))
            top_color = (30, 35, 45)
            bottom_color = (5, 5, 8)
            
            for y in range(height):
                ratio = y / height
                r = top_color[0] * (1 - ratio) + bottom_color[0] * ratio
                g = top_color[1] * (1 - ratio) + bottom_color[1] * ratio
                b = top_color[2] * (1 - ratio) + bottom_color[2] * ratio
                pygame.draw.line(self._bg_surface, (int(r), int(g), int(b)), (0, y), (width, y))
        
        return self._bg_surface

    def create_masked_surface(self, width: int, height: int) -> pygame.Surface:
        bg = self.create_background(width, height)
        
        masked_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        masked_surface.blit(bg, (0, 0))
        
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=24)
        masked_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, (255, 255, 255, 30), border_surf.get_rect(), width=1, border_radius=24)
        masked_surface.blit(border_surf, (0, 0))
        
        return masked_surface

    def render_gear(self, gear: int, gear_color: tuple[int, int, int]) -> pygame.Surface:
        font = self.font_provider.get_font(40, bold=True)
        gear_str = "R" if gear == -1 else "N" if gear == 0 else str(gear)
        return font.render(gear_str, True, gear_color)

    def render_speed(self, speed: int, text_color: tuple[int, int, int]) -> pygame.Surface:
        font = self.font_provider.get_font(90, bold=True)
        return font.render(f"{int(speed)}", True, text_color)
