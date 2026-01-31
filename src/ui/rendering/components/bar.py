import pygame 
from src .ui .utils .fonts import FontManager 


class Bar :
    def __init__ (
    self ,
    label :str ,
    color :tuple [int ,int ,int ],
    width :int =18 ,
    height :int =70 
    ):

        self .label =label 
        self .color =color 
        self .width =width 
        self .height =height
        self .bidirectional =False 

    def set_bidirectional(self, enabled: bool) -> None:
        self.bidirectional = enabled

    def render (
    self ,
    surface :pygame .Surface ,
    x :int ,
    y :int ,
    value :float ,
    text_color :tuple [int ,int ,int ]
    )->None :
        if not self.bidirectional:
            value =max (0.0 ,min (1.0 ,value ))
        else:
            value =max (-1.0 ,min (1.0 ,value ))

        # Percentage Value (Top)
        pct_value = int(abs(value) * 100)
        value_str = f"{pct_value}%"
        value_font = FontManager.get_font(size=10, bold=True) 
        value_surf = value_font.render(value_str, True, text_color)
        value_x = x + self.width // 2 - value_surf.get_width() // 2
        surface.blit(value_surf, (value_x, y))

        bar_y = y + 20

        # Label (Bottom) - Prepared for later use
        label_font = FontManager.get_font(size=14, bold=True)
        label_surf = label_font.render(self.label, True, text_color)
        label_x = x + self.width // 2 - label_surf.get_width() // 2
        label_y = bar_y + self.height + 4 
        surface.blit(label_surf, (label_x, label_y))

 
        bg_rect =pygame .Rect (x ,bar_y ,self .width ,self .height )

        pygame .draw .rect (surface ,(40 ,40 ,40 ),bg_rect ,border_radius =3 )

        if not self.bidirectional:
            fill_height =int (self .height *value )
            if fill_height >0 :
                fill_rect =pygame .Rect (
                x ,
                bar_y +self .height -fill_height ,
                self .width ,
                fill_height 
                )
                pygame .draw .rect (surface ,self .color ,fill_rect ,border_radius =3 )
        else:
            center_y = bar_y + (self.height // 2)
            half_height = self.height // 2
            
            fill_height = int(half_height * abs(value))
            
            if fill_height > 0:
                if value > 0:
                    fill_rect = pygame.Rect(
                        x, 
                        center_y - fill_height, 
                        self.width, 
                        fill_height
                    )
                else:
                    fill_rect = pygame.Rect(
                        x, 
                        center_y, 
                        self.width, 
                        fill_height
                    )
                
                abs_val = abs(value)
                r = min(255, int(abs_val * 510))
                g = min(255, int((1 - abs_val) * 510)) if abs_val > 0.5 else 255
                b = 0
                color = (r, g, b)
                
                pygame.draw.rect(surface, color, fill_rect, border_radius=3)
            
            pygame.draw.line(surface, (100, 100, 100), (x, center_y), (x + self.width, center_y), 1)
