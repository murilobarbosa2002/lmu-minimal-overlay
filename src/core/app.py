import sys
import pygame
from src.ui.window import WindowManager
from src.core.application.services.state_machine import StateMachine
from src.core.application.states.running_state import RunningState
from src.core.application.states.edit_state import EditState
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider
from src.ui.widgets.speedometer import Speedometer

class OverlayApp:
    def __init__(self):
        self.window = WindowManager(title="LMU Telemetry Overlay", width=1920, height=1080)
        self.provider = MockTelemetryProvider()
        self.state_machine = StateMachine()
        self.widgets = []

    def setup(self):
        self.window.init()
        speedometer = Speedometer(x=1500, y=850, width=280, height=130)
        self.widgets = [speedometer]
        running_state = RunningState(self.state_machine, widgets=self.widgets)
        edit_state = EditState(self.state_machine, widgets=self.widgets)
        self.state_machine.change_state(running_state)

    def _handle_input(self):
        events = self.window.handle_events()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_global_keys(event)
            self.state_machine.handle_input(event)

    def _handle_global_keys(self, event):
        if event.key == pygame.K_F1:
            self._toggle_mode()
        elif event.key == pygame.K_ESCAPE:
            self.window.is_running = False

    def _toggle_mode(self):
        if isinstance(self.state_machine.current_state, RunningState):
            self.state_machine.change_state(EditState(self.state_machine, self.widgets))
        else:
            self.state_machine.change_state(RunningState(self.state_machine, self.widgets))

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
