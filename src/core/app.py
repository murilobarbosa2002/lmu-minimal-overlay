import sys 
import pygame 
from src .ui .interfaces .i_window_manager import IWindowManager 
from src .ui .interfaces .i_font_provider import IFontProvider 
from src .core .application .services .state_machine import StateMachine 
from src .core .application .services .input_handler import InputHandler 
from src .core .application .states .running_state import RunningState 
from src .core .application .states .edit_state import EditState 
from src .core .providers .i_telemetry_provider import ITelemetryProvider 
from src .core .interfaces .i_config_manager import IConfigManager 
from src .ui .factories .widget_factory import WidgetFactory 


class OverlayApp :
    def __init__ (
    self ,
    window :IWindowManager ,
    provider :ITelemetryProvider ,
    font_provider :IFontProvider ,
    config_manager :IConfigManager ,
    widget_factory :WidgetFactory 
    ):
        self .window =window 
        self .provider =provider 
        self .font_provider =font_provider 
        self .config_manager =config_manager 
        self .widget_factory =widget_factory 
        self .state_machine =StateMachine ()
        self .widgets =[]
        self .input_handler =None 

    def setup (self )->None :
        win_cfg =self .config_manager .get_layout ("window",{})
        x =win_cfg .get ("x",0 )
        y =win_cfg .get ("y",0 )
        self .window .set_position (x ,y )
        
        self .window .init ()
        self .provider .connect ()
        
        self .widgets =[]
        widgets_data =self .config_manager .get_layout ("widgets",[])
        
        if not widgets_data :
            new_widgets_data =[{
                "type":"DashboardCard",
                "x":1700 ,
                "y":50 ,
                "width":350 ,
                "height":130 
            }]
            self .config_manager .set_layout ("widgets",new_widgets_data )
            widgets_data =new_widgets_data 
        
        for w_data in widgets_data :
            try :
                widget =self .widget_factory .create_widget (w_data )
                self .widgets .append (widget )
            except ValueError :
                pass
        running_state =RunningState (self .state_machine ,widgets =self .widgets )
        edit_state =EditState (self .state_machine ,widgets =self .widgets )
        self .state_machine .change_state (running_state )
        self .input_handler =InputHandler (self .state_machine ,self .window ,self .widgets )

    def _handle_input (self ):
        if self .input_handler :
            self .input_handler .handle_input ()

    def _update (self ):
        try :
            data =self .provider .get_data ()
        except Exception :
            data =None 
        if data :
            self .state_machine .update (data )

    def _draw (self ):
        self .window .clear ()
        if self .window .surface :
            self .state_machine .draw (self .window .surface )
        self .window .update_display ()

    def save_state (self )->None :
        if hasattr (self .window ,'x')and hasattr (self .window ,'y'):
             win_cfg ={
                 "x":self .window .x ,
                 "y":self .window .y ,
                 "width":getattr (self .window ,'width',1920 ),
                 "height":getattr (self .window ,'height',1080 ),
                 "always_on_top":True 
             }
             self .config_manager .set_layout ("window",win_cfg )

        widgets_data =[]
        for widget in self .widgets :
            w_data ={
                "type":type (widget ).__name__ ,
                "x":widget .x ,
                "y":widget .y ,
                "width":widget .width ,
                "height":widget .height 
            }
            widgets_data .append (w_data )
        
        self .config_manager .set_layout ("widgets",widgets_data )

    def run (self ):
        self .setup ()
        while self .window .is_running :
            self ._handle_input ()
            self ._update ()
            self ._draw ()
        self .save_state ()
        self .window .close ()
        sys .exit ()
