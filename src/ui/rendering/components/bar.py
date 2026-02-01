import pygame 
from src .ui .utils .fonts import FontManager 
from src.core.infrastructure.config_manager import ConfigManager


class Bar :
    def __init__ (
    self ,
    label :str ,
    color :tuple [int ,int ,int ],
    width :int =None ,
    height :int =None 
    ):
        config = ConfigManager()
        theme = config.get_theme("bar")
        
        self .label =label 
        self .color =color 
        self .width = width if width is not None else theme.get("width", 18)
        self .height = height if height is not None else theme.get("height", 70)
        self .bidirectional =False
        
        self._bg_color = tuple(theme.get("bg_color", [40, 40, 40]))
        self._border_radius = theme.get("border_radius", 3)
        self._centerline_color = tuple(theme.get("centerline_color", [100, 100, 100]))
        self._padding = theme.get("padding", 5)
        self._font_size_value = theme.get("font_size_value", 16)
        self._font_size_label = theme.get("font_size_label", 14) 

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

        pct_value = int(abs(value) * 100)
        value_str = f"{pct_value}%"
        value_font = FontManager.get_font(size=self._font_size_value, bold=True) 
        value_surf = value_font.render(value_str, True, text_color)
        value_x = x + self.width // 2 - value_surf.get_width() // 2
        surface.blit(value_surf, (value_x, y))

        bar_y = y + value_surf.get_height() + self._padding

        label_font = FontManager.get_font(size=self._font_size_label, bold=True)
        label_surf = label_font.render(self.label, True, text_color)
        label_x = x + self.width // 2 - label_surf.get_width() // 2
        
        label_y = bar_y + self.height + self._padding 
        surface.blit(label_surf, (label_x, label_y))

 
        bg_rect =pygame .Rect (x ,bar_y ,self .width ,self .height )

        pygame .draw .rect (surface ,self._bg_color ,bg_rect ,border_radius =self._border_radius )

        if not self.bidirectional:
            fill_height =int (self .height *value )
            if fill_height >0 :
                fill_rect =pygame .Rect (
                x ,
                bar_y +self .height -fill_height ,
                self .width ,
                fill_height 
                )
                pygame .draw .rect (surface ,self .color ,fill_rect ,border_radius =self._border_radius )
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
                g = max(0, 255 - int(abs_val * 510))
                b = 0
                color = (r, g, b)
                
                pygame.draw.rect(surface, color, fill_rect, border_radius=self._border_radius)
            
            pygame.draw.line(surface, self._centerline_color, (x, center_y), (x + self.width, center_y), 1)
