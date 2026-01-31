import pygame 
import math 


class SteeringIndicator :
    def __init__ (self ,radius :int =30 ):
        self .radius =radius 

    def _rotate_point(self, point: tuple[float, float], angle_deg: float, cx: int, cy: int) -> tuple[int, int]:
        """Rotates a point around (cx, cy) by angle_deg."""
        x, y = point
        # Subtract center to rotate around origin (0,0)
        tx = x
        ty = y
        
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Rotation matrix
        rx = tx * cos_a - ty * sin_a
        ry = tx * sin_a + ty * cos_a
        
        # Add center back
        return int(cx + rx), int(cy + ry)

    def render (
    self ,
    surface :pygame .Surface ,
    cx :int ,
    cy :int ,
    angle :float ,
    color :tuple [int ,int ,int ]
    )->None :
        # GT Steering Wheel Shape (Flat bottom)
        # Defined as relative points (x, y) assuming radius approx 30
        r = self.radius
        
        # Basic shape components (rim thickness approx 8)
        color_rim = (30, 30, 30) # Dark rubber/alcantara 
        color_marker = (255, 200, 0) # Yellow center marker
        
        # Define the rim polygon points (relative to center 0,0)
        # Flat bottom geometry
        # Simplify: Top half arc, bottom half flat-ish
        
        # We'll draw 2 polygons: Outer and Inner, then fill area between? 
        # Easier: Draw thick lines or multiple polygons.
        # Let's draw a rotated surface or polygon points.
        
        # Let's define points for a stylized GT wheel
        points = []
        resolution = 16
        
        # Top Arc (from -135 to 135 degrees)
        for i in range(resolution + 1):
            theta = math.radians(-135 + (270 * i / resolution))
            # Screen coords: x = sin, y = -cos (inverted y)
            # But math standard: x = cos, y = sin starts at right (0 deg)
            # Let's stick to standard and rotate later
            # Top is -90 deg in pygame coords.
            # Let's use standard unit circle rotated -90
            
            # Using simple manual points for shape control
            # Top-Left (-r, -0.2r) -> Top-Arc -> Top-Right (r, -0.2r) -> Bottom-Right (0.6r, 0.8r) -> Bottom-Left ...
            pass

        # Cleaner approach: Draw separate parts rotated
        
        angle_rad = -angle # Invert since Pygame y is down, but rotation convention might differ. 
                           # Usually steering + is right. 
                           # Rotate clockwise for positive visual steering.
        
        # Create a surface for the wheel if we wanted perfect caching, but dynamic drawing is fine.
        
        # 1. Main Rim (Thick Arc)
        # We can simulate thick arc by drawing a thick circle and masking or polygon
        
        # Let's use polygons for the flat bottom shape
        outer_pts = []
        inner_pts = []
        
        # Generate points for a circle with a flat bottom
        steps = 20
        start_angle = -140 # degrees, top-left ish
        end_angle = 320    # degrees (loop around) => wait, -140 to +140 is top part (280 deg)
        # Flat bottom is between 140 and 220 deg?
        
        # Simplified: A circle with a chord cut at bottom
        # Visual range: -40 to 220? 
        
        # Let's do explicit vertex definition for a "D" shape
        # Top arch
        for i in range(steps):
             # -210 to 30 degrees (inverted y) -> Top is -90.
             # Left is -180. Right is 0.
             # Range: 30 deg (Right-Down) to 150 deg (Left-Down) is the FLAT part. 
             # So Arc is 150 deg to 390 (30) deg.
             
             deg = 150 + (240 * i / (steps - 1))
             rad_val = math.radians(deg)
             # Pygame 0 is Right, 90 is Down, 180 is Left, 270 is Up.
             # So we want Arc from roughly 30 deg (down-right) to 150 deg (down-left) to be flat/straight.
             # The REST is the arc.
             
             x = r * math.cos(rad_val)
             y = r * math.sin(rad_val)
             outer_pts.append((x, y))
             
             x_in = (r - 7) * math.cos(rad_val)
             y_in = (r - 7) * math.sin(rad_val)
             inner_pts.append((x_in, y_in))

        # Flat bottom connection
        # Connect last outer to first outer? NO.
        # We need to close the loop.
        
        # This is getting complex for a simple task. 
        # BETTER: Draw a thick circle + thick line, then rotate points.
        
        # --- IMPLEMENTATION ---
        
        # 1. Rim
        rim_points = []
        thickness = 6
        
        # Create "D" shape vertices
        # Arc part
        vals = range(30, 151, 10) # 30 to 150 is bottom part. We want the OTHER way.
        # 150 -> 390 (30)
        
        arc_start = 145
        arc_end = 395 # 35 deg
        
        step_sz = 15
        curr = arc_start
        while curr <= arc_end:
            rad2 = math.radians(curr)
            rim_points.append( (r * math.cos(rad2), r * math.sin(rad2)) )
            curr += step_sz
            
        # Add flat bottom corners explicitly if needed, but circle points cover it roughly
        
        # Rotate all rim points
        screen_rim_points = [self._rotate_point(p, angle, cx, cy) for p in rim_points]
        
        # Draw Rim as lines (open loop)
        if len(screen_rim_points) > 1:
            pygame.draw.lines(surface, color, False, screen_rim_points, thickness)
        
        # Draw Flat Bottom (connect last to first)
        pygame.draw.line(surface, color, screen_rim_points[-1], screen_rim_points[0], thickness)
        
        # 2. Center Spokes (Hub)
        # Left Spoke
        p1 = self._rotate_point((r*0.2, 0), angle, cx, cy) # Center-ish
        p2 = self._rotate_point((r-2, 0), angle, cx, cy)   # Right rim
        pygame.draw.line(surface, color, p1, p2, 5) # Right Spoke (0 deg)
        
        p3 = self._rotate_point((-r*0.2, 0), angle, cx, cy) 
        p4 = self._rotate_point((-r+2, 0), angle, cx, cy)
        pygame.draw.line(surface, color, p3, p4, 5) # Left Spoke (180 deg)

        p5 = self._rotate_point((0, 0), angle, cx, cy) 
        p6 = self._rotate_point((0, r-4), angle, cx, cy) # Down spoke (90 deg)
        pygame.draw.line(surface, color, p5, p6, 8) 
        
        # 3. Center Cap (Logo)
        pygame.draw.circle(surface, (50, 50, 50), (cx, cy), 6)
        
        # 4. Top Marker (Yellow Tape) at -90 deg (Up)
        # Position relative to center: (0, -r)
        # Rotated by angle
        
        marker_top = (0, -r)
        marker_bottom = (0, -r + 8)
        
        m_start = self._rotate_point(marker_top, angle, cx, cy)
        m_end = self._rotate_point(marker_bottom, angle, cx, cy)
        
        pygame.draw.line(surface, color_marker, m_start, m_end, 7)
