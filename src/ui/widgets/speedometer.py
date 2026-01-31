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
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 160), s.get_rect(), border_radius=15)
        surface.blit(s, (self.x, self.y))
        
        if self.speed_surf is None:
            font = FontManager.get_font(90, bold=True)
            self.speed_surf = font.render(f"{int(self.speed)}", True, self.text_color)
            
        speed_rect = self.speed_surf.get_rect(center=(self.x + self.width // 2, self.y + 95))
        surface.blit(self.speed_surf, speed_rect)
        
        if self.gear_surf is None:
            font = FontManager.get_font(40, bold=True)
            gear_str = "R" if self.gear == -1 else "N" if self.gear == 0 else str(self.gear)
            self.gear_surf = font.render(gear_str, True, self.gear_color)
            
        gear_rect = self.gear_surf.get_rect(center=(self.x + self.width // 2, self.y + 30))
        surface.blit(self.gear_surf, gear_rect)

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
