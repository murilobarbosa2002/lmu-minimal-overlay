from src.core.app import OverlayApp
from src.core.infrastructure.di_container import SimpleDIContainer
from src.ui.window import WindowManager
from src.ui.interfaces.i_window_manager import IWindowManager
from src.ui.interfaces.i_font_provider import IFontProvider
from src.ui.utils.pygame_font_provider import PygameFontProvider
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider
from src.ui.widgets.dashboard_card import DashboardCard
from src.core.application.services.state_machine import StateMachine
from src.core.application.states.running_state import RunningState
from src.core.application.states.edit_state import EditState
from src.core.application.services.input_handler import InputHandler


class AppFactory:
    @staticmethod
    def create(use_mock_provider: bool = True) -> OverlayApp:
        container = SimpleDIContainer()
        
        container.register(
            IFontProvider,
            lambda c: PygameFontProvider(),
            singleton=True
        )
        
        container.register(
            IWindowManager,
            lambda c: WindowManager(title="LMU Telemetry Overlay", width=1920, height=1080),
            singleton=True
        )
        
        container.register(
            ITelemetryProvider,
            lambda c: MockTelemetryProvider(),
            singleton=True
        )
        
        window = container.resolve(IWindowManager)
        provider = container.resolve(ITelemetryProvider)
        font_provider = container.resolve(IFontProvider)
        
        app = OverlayApp(window=window, provider=provider, font_provider=font_provider)
        
        return app
