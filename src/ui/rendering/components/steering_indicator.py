import pygame
import math
import os

class SteeringIndicator :
    def __init__ (self ,radius :int =30 ):
        self .radius =radius 
        self .wheel_image =None
        
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
            # rotozoom provides filtered rotation (smoother)
            rotated_img = pygame.transform.rotozoom(self.wheel_image, -angle, 1.0)
            new_rect = rotated_img.get_rect(center=(cx, cy))
            surface.blit(rotated_img, new_rect)
            return

        r = self.radius
        
        color_rim = (30, 30, 30) 
        color_marker = (255, 200, 0)
        
        
        rim_points = []
        thickness = 6
        
        vals = range(30, 151, 10) 
        
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
        
        pygame.draw.line(surface, color, screen_rim_points[-1], screen_rim_points[0], thickness)
        
        
        p1 = self._rotate_point((r*0.2, 0), angle, cx, cy) 
        p2 = self._rotate_point((r-2, 0), angle, cx, cy)   
        pygame.draw.line(surface, color, p1, p2, 5) 
        
        p3 = self._rotate_point((-r*0.2, 0), angle, cx, cy) 
        p4 = self._rotate_point((-r+2, 0), angle, cx, cy)
        pygame.draw.line(surface, color, p3, p4, 5) 

        p5 = self._rotate_point((0, 0), angle, cx, cy) 
        p6 = self._rotate_point((0, r-4), angle, cx, cy) 
        pygame.draw.line(surface, color, p5, p6, 8) 
        
        pygame.draw.circle(surface, (50, 50, 50), (cx, cy), 6)
        
        marker_top = (0, -r)
        marker_bottom = (0, -r + 8)
        
        m_start = self._rotate_point(marker_top, angle, cx, cy)
        m_end = self._rotate_point(marker_bottom, angle, cx, cy)
        
        pygame.draw.line(surface, color_marker, m_start, m_end, 7)
