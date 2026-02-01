import pygame 
from src .core .application .interfaces .state import IApplicationState 
from src .core .domain .telemetry_data import TelemetryData 
from src .ui .widgets .widget import Widget 

class EditState (IApplicationState ):
    def __init__ (self ,context ,widgets :list [Widget ]):
        super ().__init__ (context )
        self .widgets =widgets 
        self .selected_widget :Widget |None =None 
        self._time_accumulator = 0.0

    def on_enter (self )->None :
        self._time_accumulator = 0.0

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
        self._time_accumulator += 0.05
        
        for widget in self .widgets :
            widget .update (data ) 

    def draw (self ,surface :pygame .Surface )->None :
        for widget in self .widgets :
            widget .draw (surface )

        if self .selected_widget :
            import math
            padding_base = 10
            padding_oscillation = 2 * math.sin(self._time_accumulator * 4) 
            current_padding = padding_base + padding_oscillation
            
            rect = self.selected_widget.get_rect()
            selection_rect = rect.inflate(current_padding * 2, current_padding * 2)
            
            pygame .draw .rect (surface ,(0 ,255 ,255 ),selection_rect ,2 ,border_radius =8 )
