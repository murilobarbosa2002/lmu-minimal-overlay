import pygame
from src.ui.widgets.widget import Widget
from src.core.domain.telemetry_data import TelemetryData
from src.ui.utils.fonts import FontManager

class Speedometer(Widget):
    def __init__(self, x: int, y: int, width: int = 200, height: int = 150):
        super().__init__(x, y, width, height)
        self.speed = 0.0
        self.gear = 0
        self.unit = "km/h"
        self.is_dragging = False
        self.drag_offset = (0, 0)
        
        self.bg_color = (0, 0, 0, 128)
        self.text_color = (255, 255, 255)
        self.gear_color = (255, 200, 0)
        
        self.speed_surf: pygame.Surface | None = None
        self.gear_surf: pygame.Surface | None = None
        self.unit_surf: pygame.Surface | None = None

    def set_unit(self, unit: str) -> None:
        if unit in ["km/h", "mph"] and unit != self.unit:
            self.unit = unit
            self.unit_surf = None
            self.speed_surf = None

    def update(self, data: TelemetryData) -> None:
        raw_speed = data.speed
        if self.unit == "mph":
            raw_speed *= 0.621371
            
        new_speed = round(raw_speed)
        new_gear = data.gear
        
        if new_speed != int(self.speed):
            self.speed = new_speed
            self.speed_surf = None
            
        if new_gear != self.gear:
            self.gear = new_gear
            self.gear_surf = None

    def draw(self, surface: pygame.Surface) -> None:

        if not hasattr(self, '_bg_surface'):
            self._bg_surface = pygame.Surface((self.width, self.height))
            top_color = (30, 35, 45)
            bottom_color = (5, 5, 8)
            
            for y in range(self.height):
                ratio = y / self.height
                r = top_color[0] * (1 - ratio) + bottom_color[0] * ratio
                g = top_color[1] * (1 - ratio) + bottom_color[1] * ratio
                b = top_color[2] * (1 - ratio) + bottom_color[2] * ratio
                pygame.draw.line(self._bg_surface, (int(r), int(g), int(b)), (0, y), (self.width, y))
                
        masked_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        masked_surface.blit(self._bg_surface, (0, 0))
        
        mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=24)
        masked_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        border_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, (255, 255, 255, 30), border_surf.get_rect(), width=1, border_radius=24)
        masked_surface.blit(border_surf, (0, 0))
        
        surface.blit(masked_surface, (self.x, self.y))

        if self.gear_surf is None:
            font = FontManager.get_font(40, bold=True)
            gear_str = "R" if self.gear == -1 else "N" if self.gear == 0 else str(self.gear)
            self.gear_surf = font.render(gear_str, True, self.gear_color)
            
        gear_rect = self.gear_surf.get_rect(centerx=self.x + self.width // 2, top=self.y + 20)
        surface.blit(self.gear_surf, gear_rect)

        if self.speed_surf is None:
            font = FontManager.get_font(90, bold=True)
            self.speed_surf = font.render(f"{int(self.speed)}", True, self.text_color)
            
        speed_rect = self.speed_surf.get_rect(centerx=self.x + self.width // 2, bottom=self.y + self.height - 10)
        surface.blit(self.speed_surf, speed_rect)



    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                rect = self.get_rect()
                if rect.collidepoint(mouse_pos):
                    self.is_dragging = True
                    self.drag_offset = (self.x - mouse_pos[0], self.y - mouse_pos[1])
                    return True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_pos = event.pos
                new_x = mouse_pos[0] + self.drag_offset[0]
                new_y = mouse_pos[1] + self.drag_offset[1]
                self.set_position(new_x, new_y)
                return True
                
        return False
