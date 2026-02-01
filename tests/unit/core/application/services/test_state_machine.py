import pytest
from unittest.mock import Mock
from src.core.application.services.state_machine import StateMachine
from src.core.application.interfaces.state import IApplicationState as ApplicationState
from src.core.application.states.running_state import RunningState
from src.core.application.states.edit_state import EditState
from src.core.domain.telemetry_data import TelemetryData
import pygame

# Initialize pygame for events/surface
pygame.init()


class MockState(ApplicationState):
    def __init__(self, context):
        super().__init__(context)
        self.entered = False
        self.exited = False
        self.updated = False
        self.drawn = False
        self.input_handled = False

    def on_enter(self):
        self.entered = True

    def on_exit(self):
        self.exited = True

    def update(self, data):
        self.updated = True

    def draw(self, surface):
        self.drawn = True

    def handle_input(self, event):
        self.input_handled = True
        return True


def test_state_machine_initialization():
    sm = StateMachine()
    assert sm.current_state is None


def test_state_transition():
    sm = StateMachine()
    state1 = MockState(sm)
    state2 = MockState(sm)

    # Initial transition
    sm.change_state(state1)
    assert sm.current_state == state1
    assert state1.entered is True
    assert state1.exited is False

    # Transition to new state
    sm.change_state(state2)
    assert sm.current_state == state2
    assert state1.exited is True
    assert state2.entered is True


def test_state_delegation():
    sm = StateMachine()
    state = MockState(sm)
    sm.change_state(state)

    dummy_data = Mock(spec=TelemetryData)
    dummy_surface = Mock(spec=pygame.Surface)
    dummy_event = pygame.event.Event(pygame.USEREVENT)

    sm.update(dummy_data)
    assert state.updated is True

    sm.draw(dummy_surface)
    assert state.drawn is True

    handled = sm.handle_input(dummy_event)
    assert state.input_handled is True
    assert handled is True


def test_running_state_initialization():
    sm = StateMachine()
    widgets = []
    state = RunningState(sm, widgets)
    assert state.widgets == []


def test_edit_state_selection_stub():
    # Only creating instances to verify imports and basic structure
    sm = StateMachine()
    widgets = []
    state = EditState(sm, widgets)
    assert state.selected_widget is None


def test_state_machine_handle_input_no_state():
    sm = StateMachine()
    # Should return False safely
    assert sm.handle_input(Mock()) is False


def test_state_machine_update_no_state():
    sm = StateMachine()
    # Should not raise error
    sm.update(Mock())


def test_state_machine_draw_no_state():
    sm = StateMachine()
    # Should not raise error
    sm.draw(Mock())
