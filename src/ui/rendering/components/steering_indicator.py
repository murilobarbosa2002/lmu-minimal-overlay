import pygame
import math
import os
from src.core.infrastructure.config_manager import ConfigManager

class SteeringIndicator :
    def __init__ (self ,radius :int =None ):
        config = ConfigManager()
        theme = config.get_theme("steering_indicator")
        
        self .radius = radius if radius is not None else theme.get("radius", 30)
        self .wheel_image =None
        
        self._color_rim = tuple(theme.get("color_rim", [30, 30, 30]))
        self._color_marker = tuple(theme.get("color_marker", [255, 200, 0]))
        self._color_center = tuple(theme.get("color_center", [50, 50, 50]))
        self._tick_start = theme.get("tick_start", 30)
        self._tick_end = theme.get("tick_end", 150)
        self._tick_step = theme.get("tick_step", 10)
        
        img_path = "src/assets/images/wheel-mockup.png"
        if not os.path.exists(img_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            img_path = os.path.join(base_dir, "src/assets/images/wheel-mockup.png")
            
        if os.path.exists(img_path):
            try:
                raw_img = pygame.image.load(img_path)
                diameter = self.radius * 2
                self.wheel_image = pygame.transform.smoothscale(raw_img, (diameter, diameter))
            except Exception:
                pass 

    def _rotate_point(self, point: tuple[float, float], angle_deg: float, cx: int, cy: int) -> tuple[int, int]:
        x, y = point
        tx = x
        ty = y
        
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        
        rx = tx * cos_a - ty * sin_a
        ry = tx * sin_a + ty * cos_a
        
        
        return int(cx + rx), int(cy + ry)

    def render (
    self ,
    surface :pygame .Surface ,
    cx :int ,
    cy :int ,
    angle :float ,
    color :tuple [int ,int ,int ]
    )->None :
        if self.wheel_image:
            rotated_img = pygame.transform.rotozoom(self.wheel_image, -angle, 1.0)
            new_rect = rotated_img.get_rect(center=(cx, cy))
            surface.blit(rotated_img, new_rect)
            return

        r = self.radius
        
        
        rim_points = []
        thickness = 6
        
        vals = range(self._tick_start, self._tick_end + 1, self._tick_step) 
        
        arc_start = 145
        arc_end = 395 
        
        step_sz = 15
        curr = arc_start
        while curr <= arc_end:
            rad2 = math.radians(curr)
            rim_points.append( (r * math.cos(rad2), r * math.sin(rad2)) )
            curr += step_sz
            
        screen_rim_points = [self._rotate_point(p, angle, cx, cy) for p in rim_points]
        
        if len(screen_rim_points) > 1:
            pygame.draw.lines(surface, color, False, screen_rim_points, thickness)
        
        for v in vals:
            angle_deg = -v
            px = r * math.cos(math.radians(angle_deg))
            py = r * math.sin(math.radians(angle_deg))
            rim_points.append((px, py))

        for px, py in rim_points:
            rx, ry = self._rotate_point((px, py), angle, cx, cy)
            pygame.draw.circle(surface, self._color_rim, (rx, ry), 2)

        marker_angle_deg = 0
        marker_x = (r - 10) * math.cos(math.radians(marker_angle_deg))
        marker_y = (r - 10) * math.sin(math.radians(marker_angle_deg))
        mx, my = self._rotate_point((marker_x, marker_y), angle, cx, cy)
        pygame.draw.circle(surface, self._color_marker, (mx, my), 4)

        pygame.draw.circle(surface, self._color_center, (cx, cy), 6)
        
        marker_top = (0, -r)
        marker_bottom = (0, -r + 8)
        top_rotated = self._rotate_point(marker_top, angle, cx, cy)
        bottom_rotated = self._rotate_point(marker_bottom, angle, cx, cy)
        pygame.draw.line(surface, self._color_marker, top_rotated, bottom_rotated, 3)
