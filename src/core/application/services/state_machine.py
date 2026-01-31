import pygame 
from src .core .application .interfaces .state import IApplicationState 
from src .core .domain .telemetry_data import TelemetryData 

class StateMachine :
    def __init__ (self ):
        self .current_state :IApplicationState |None =None 

    def change_state (self ,new_state :IApplicationState )->None :
        if self .current_state :
            self .current_state .on_exit ()

        self .current_state =new_state 

        if self .current_state :
            self .current_state .on_enter ()

    def handle_input (self ,event :pygame .event .Event )->bool :
        if self .current_state :
            return self .current_state .handle_input (event )
        return False 

    def update (self ,data :TelemetryData )->None :
        if self .current_state :
            self .current_state .update (data )

    def draw (self ,surface :pygame .Surface )->None :
        if self .current_state :
            self .current_state .draw (surface )
