import sys 
from typing import Optional 


class ITransparencyHandler :
    def apply_transparency (self ,hwnd :int )->None :
        pass 


class Win32TransparencyHandler (ITransparencyHandler ):
    def __init__ (self ,chroma_key_color :tuple [int ,int ,int ]=(255 ,0 ,128 ),alpha :int =217 ):
        self .chroma_key_color =chroma_key_color 
        self .alpha =alpha 

    def apply_transparency (self ,hwnd :int )->None :
        if sys .platform !="win32":
            return 

        try :
            import win32gui 
            import win32con 
            import win32api 

            ex_style =win32gui .GetWindowLong (hwnd ,win32con .GWL_EXSTYLE )
            win32gui .SetWindowLong (hwnd ,win32con .GWL_EXSTYLE ,ex_style |win32con .WS_EX_LAYERED )

            win32gui .SetLayeredWindowAttributes (
            hwnd ,
            win32api .RGB (*self .chroma_key_color ),
            self .alpha ,
            win32con .LWA_COLORKEY |win32con .LWA_ALPHA 
            )
        except ImportError :
            pass 


class NullTransparencyHandler (ITransparencyHandler ):
    def apply_transparency (self ,hwnd :int )->None :
        pass 
