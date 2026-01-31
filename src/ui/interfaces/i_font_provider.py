from abc import ABC ,abstractmethod 
import pygame 
from typing import Optional 


class IFontProvider (ABC ):
    @abstractmethod 
    def get_font (self ,size :int ,bold :bool =False ,font_name :Optional [str ]=None )->pygame .font .Font :
        pass 
