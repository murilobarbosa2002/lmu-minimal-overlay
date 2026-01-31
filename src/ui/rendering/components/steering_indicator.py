import pygame 
import math 


class SteeringIndicator :
    def __init__ (self ,radius :int =30 ):
        self .radius =radius 

    def render (
    self ,
    surface :pygame .Surface ,
    cx :int ,
    cy :int ,
    angle :float ,
    color :tuple [int ,int ,int ]
    )->None :
        pygame .draw .circle (surface ,color ,(cx ,cy ),self .radius ,2 )
        pygame .draw .circle (surface ,color ,(cx ,cy ),3 )

        line_length =self .radius -5 
        angle_rad =-math .radians (angle )
        end_x =cx +int (line_length *math .sin (angle_rad ))
        end_y =cy +int (line_length *math .cos (angle_rad ))
        pygame .draw .line (surface ,color ,(cx ,cy ),(end_x ,end_y ),3 )
