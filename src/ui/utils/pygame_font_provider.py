import pygame 
import os 
from typing import Optional 
from src .ui .interfaces .i_font_provider import IFontProvider 


class PygameFontProvider (IFontProvider ):
    def __init__ (self ):
        self ._fonts :dict [tuple [str ,int ,bool ],pygame .font .Font ]={}

    def get_font (self ,size :int ,bold :bool =False ,font_name :Optional [str ]=None )->pygame .font .Font :
        key =(font_name or "default",size ,bold )
        if key not in self ._fonts :
            if not pygame .font .get_init ():
                pygame .font .init ()

            bold_suffix ="-Bold.ttf"if bold else "-Regular.ttf"
            font_path =os .path .join (os .getcwd (),"assets","fonts",f"Roboto{bold_suffix}")

            if os .path .exists (font_path ):
                try :
                    font =pygame .font .Font (font_path ,size )
                    font .render ("test",False ,(0 ,0 ,0 ))
                    self ._fonts [key ]=font 
                    return font 
                except Exception as e :
                    print (f"Failed to load font {font_path}: {e}")

            try :
                font =pygame .font .SysFont (font_name ,size ,bold =bold )
                self ._fonts [key ]=font 
                return font 
            except Exception :
                font =pygame .font .Font (None ,size )
                self ._fonts [key ]=font 
                return font 

        return self ._fonts [key ]
