import pygame 
from src .ui .utils .fonts import FontManager 
from src.core.infrastructure.config_manager import ConfigManager


class SpeedGearDisplay :
    def __init__ (self ):
        self .speed_surf :pygame .Surface |None =None 
        self .unit_surf :pygame .Surface |None =None 
        self .gear_surf :pygame .Surface |None =None 
        self .rpm_surf :pygame .Surface |None =None
        
        config = ConfigManager()
        theme = config.get_theme("dashboard_card")
        self._rpm_color = tuple(theme.get("rpm_color", [200, 200, 200]))
        self._rpm_font_size = theme.get("rpm_font_size", 24)

    def render (
    self ,
    surface :pygame .Surface ,
    x :int ,
    y :int ,
    width :int ,
    height :int ,
    speed :float ,
    gear :int ,
    unit :str ,
    rpm :int ,
    max_rpm :int ,
    text_color :tuple [int ,int ,int ],
    gear_color :tuple [int ,int ,int ]
    )->None :
        if self .speed_surf is None or int (speed )!=getattr (self ,'_cached_speed',None ):
            speed_font =FontManager .get_font (size =48 ,bold =True )
            self .speed_surf =speed_font .render (str (int (speed )),True ,text_color )
            self ._cached_speed =int (speed )

        if self .unit_surf is None or unit !=getattr (self ,'_cached_unit',None ):
            unit_font =FontManager .get_font (size =18 )
            self .unit_surf =unit_font .render (unit ,True ,text_color )
            self ._cached_unit =unit 

        if self .gear_surf is None or gear !=getattr (self ,'_cached_gear',None ):
            gear_font =FontManager .get_font (size =40 ,bold =True )
            gear_text ="R"if gear ==-1 else "N"if gear ==0 else str (gear )
            self .gear_surf =gear_font .render (gear_text ,True ,gear_color )
            self ._cached_gear =gear 
        
        if self .rpm_surf is None or rpm !=getattr (self ,'_cached_rpm',None ):
            rpm_font =FontManager .get_font (size =self._rpm_font_size ,bold =True )
            rpm_text =f"{rpm} RPM"
            self .rpm_surf =rpm_font .render (rpm_text ,True ,self._rpm_color )
            self ._cached_rpm =rpm

        gap = 3
        total_content_height = (
            self.gear_surf.get_height() + 
            gap + 
            self.unit_surf.get_height() + 
            gap + 
            self.speed_surf.get_height() +
            gap +
            self.rpm_surf.get_height()
        )

        start_y = y + (height - total_content_height) // 2

        gear_x =x +width //2 -self .gear_surf .get_width ()//2 
        gear_y = start_y 

        unit_x =x +width //2 -self .unit_surf .get_width ()//2 
        unit_y =gear_y +self .gear_surf .get_height ()+ gap

        speed_x =x +width //2 -self .speed_surf .get_width ()//2 
        speed_y =unit_y +self .unit_surf .get_height ()+ gap 
        
        rpm_x =x +width //2 -self .rpm_surf .get_width ()//2 
        rpm_y =speed_y +self .speed_surf .get_height ()+ gap

        surface .blit (self .gear_surf ,(gear_x ,gear_y ))
        surface .blit (self .unit_surf ,(unit_x ,unit_y ))
        surface .blit (self .speed_surf ,(speed_x ,speed_y ))
        surface .blit (self .rpm_surf ,(rpm_x ,rpm_y ))

    def invalidate_cache (self )->None :
        self .speed_surf =None 
        self .unit_surf =None 
        self .gear_surf =None 
        self .rpm_surf =None
