from src .core .app import OverlayApp 
from src .core .infrastructure .di_container import SimpleDIContainer 
from src .ui .window import WindowManager 
from src .ui .interfaces .i_window_manager import IWindowManager 
from src .ui .interfaces .i_font_provider import IFontProvider 
from src .ui .utils .pygame_font_provider import PygameFontProvider 
from src .core .providers .i_telemetry_provider import ITelemetryProvider 
from src .core .providers .mock_telemetry_provider import MockTelemetryProvider 
from src .core .interfaces .i_config_manager import IConfigManager 
from src .core .infrastructure .config_manager import ConfigManager 
from src .ui .factories .widget_factory import WidgetFactory 
from src .core .application .services .state_machine import StateMachine 
from src .core .application .states .running_state import RunningState 
from src .core .application .states .edit_state import EditState 
from src .core .application .services .input_handler import InputHandler 


class AppFactory :
    @staticmethod 
    def create (use_mock_provider :bool =True )->OverlayApp :
        container =SimpleDIContainer ()

        container .register (
        IFontProvider ,
        lambda c :PygameFontProvider (),
        singleton =True 
        )

        container .register (
        IWindowManager ,
        lambda c: WindowManager(
            title=c.resolve(IConfigManager).get_config("window", {}).get("title", "LMU Telemetry Overlay"),
            width=c.resolve(IConfigManager).get_config("window", {}).get("default_width", 1920),
            height=c.resolve(IConfigManager).get_config("window", {}).get("default_height", 1080)
        ),
        singleton =True 
        )

        container .register (
        ITelemetryProvider ,
        lambda c :MockTelemetryProvider (),
        singleton =True 
        )

        container .register (
        IConfigManager ,
        lambda c :ConfigManager (),
        singleton =True 
        )

        window =container .resolve (IWindowManager )
        provider =container .resolve (ITelemetryProvider )
        font_provider =container .resolve (IFontProvider )
        config_manager =container .resolve (IConfigManager )
        widget_factory =WidgetFactory ()

        app =OverlayApp (
            window =window ,
            provider =provider ,
            font_provider =font_provider ,
            config_manager =config_manager ,
            widget_factory =widget_factory 
        )

        return app 
