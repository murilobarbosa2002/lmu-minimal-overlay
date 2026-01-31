import sys
import pygame
from src.ui.window import WindowManager
from src.core.state_machine import StateMachine
from src.core.states import RunningState, EditState
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider
from src.core.domain.telemetry_data import TelemetryData
from src.ui.widgets.speedometer import Speedometer

def main():
    # Wide/Short "card" overlay style
    window = WindowManager(title="LMU Telemetry Overlay", width=300, height=150)
    window.init()
    provider = MockTelemetryProvider()
    state_machine = StateMachine()
    
    # Center widget in the window
    speedometer = Speedometer(x=10, y=10, width=280, height=130)
    
    widgets = [speedometer]
    
    running_state = RunningState(state_machine, widgets=widgets)
    edit_state = EditState(state_machine, widgets=widgets)
    state_machine.change_state(running_state)
    
    while window.is_running:
        events = window.handle_events()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if isinstance(state_machine.current_state, RunningState):
                        state_machine.change_state(edit_state)
                    else:
                        state_machine.change_state(running_state)
                elif event.key == pygame.K_ESCAPE:
                    window.is_running = False
            state_machine.handle_input(event)
            
        try:
            data = provider.get_data()
        except Exception:
            data = None

        if data:
            state_machine.update(data)
            
        window.clear()
        if window.surface:
            state_machine.draw(window.surface)
        window.update_display()

    window.close()
    sys.exit()

if __name__ == "__main__":
    main()
