import pygame 
from src .core .application .interfaces .state import IApplicationState 
from src .core .domain .telemetry_data import TelemetryData 
from src .ui .widgets .widget import Widget 

class EditState (IApplicationState ):
    def __init__ (self ,context ,widgets :list [Widget ]):
        super ().__init__ (context )
        self .widgets =widgets 
        self .selected_widget :Widget |None =None 

    def on_enter (self )->None :
        pass 

    def on_exit (self )->None :
        self .selected_widget =None 

    def handle_input (self ,event :pygame .event .Event )->bool :
        if event .type ==pygame .MOUSEBUTTONDOWN :
            mouse_pos =event .pos 
            self .selected_widget =None 
            for widget in self .widgets :
                if widget .get_rect ().collidepoint (mouse_pos ):
                    self .selected_widget =widget 

        handled =False 
        for widget in self .widgets :
            if widget .handle_input (event ):
                handled =True 

        return handled 

    def update (self ,data :TelemetryData )->None :
        for widget in self .widgets :
            widget .update (data ) 

    def draw (self ,surface :pygame .Surface )->None :
        for widget in self .widgets :
            widget .draw (surface )

        if self .selected_widget :
            pygame .draw .rect (surface ,(255 ,0 ,0 ),self .selected_widget .get_rect (),2 )
