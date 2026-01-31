import pygame 
from src .core .application .services .state_machine import StateMachine 
from src .core .application .states .running_state import RunningState 
from src .core .application .states .edit_state import EditState 
from src .ui .window import WindowManager 

class InputHandler :
    def __init__ (self ,state_machine :StateMachine ,window :WindowManager ,widgets :list ):
        self .state_machine =state_machine 
        self .window =window 
        self .widgets =widgets 

    def handle_input (self )->None :
        events =self .window .handle_events ()
        for event in events :
            if event .type ==pygame .KEYDOWN :
                self ._handle_global_keys (event )
            self .state_machine .handle_input (event )

    def _handle_global_keys (self ,event :pygame .event .Event )->None :
        if event .key ==pygame .K_F1 :
            self ._toggle_mode ()
        elif event .key ==pygame .K_ESCAPE :
            self .window .is_running =False 

    def _toggle_mode (self )->None :
        if isinstance (self .state_machine .current_state ,RunningState ):
            self .state_machine .change_state (EditState (self .state_machine ,self .widgets ))
        else :
            self .state_machine .change_state (RunningState (self .state_machine ,self .widgets ))
