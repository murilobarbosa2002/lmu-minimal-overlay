import sys
import pygame
from src.ui.interfaces.i_window_manager import IWindowManager
from src.ui.interfaces.i_font_provider import IFontProvider
from src.core.application.services.state_machine import StateMachine
from src.core.application.states.running_state import RunningState
from src.core.application.states.edit_state import EditState
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.ui.widgets.speedometer import Speedometer
from src.ui.widgets.pedals import Pedals
from src.core.application.services.input_handler import InputHandler


class OverlayApp:
    def __init__(
        self, 
        window: IWindowManager, 
        provider: ITelemetryProvider,
        font_provider: IFontProvider
    ):
        self.window = window
        self.provider = provider
        self.font_provider = font_provider
        self.state_machine = StateMachine()
        self.widgets = []
        self.input_handler = None

    def setup(self) -> None:
        self.window.init()
        self.provider.connect()
        self.widgets = [
            Speedometer(x=1700, y=50, width=280, height=130),
            Pedals(x=1700, y=300, font_provider=self.font_provider)
        ]
        running_state = RunningState(self.state_machine, widgets=self.widgets)
        edit_state = EditState(self.state_machine, widgets=self.widgets)
        self.state_machine.change_state(running_state)
        self.input_handler = InputHandler(self.state_machine, self.window, self.widgets)

    def _handle_input(self):
        if self.input_handler:
            self.input_handler.handle_input()

    def _update(self):
        try:
            data = self.provider.get_data()
        except Exception:
            data = None
        if data:
            self.state_machine.update(data)

    def _draw(self):
        self.window.clear()
        if self.window.surface:
            self.state_machine.draw(self.window.surface)
        self.window.update_display()

    def run(self):
        self.setup()
        while self.window.is_running:
            self._handle_input()
            self._update()
            self._draw()
        self.window.close()
        sys.exit()
