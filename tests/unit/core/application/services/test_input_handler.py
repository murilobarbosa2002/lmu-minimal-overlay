import pytest
from unittest.mock import Mock, patch
import pygame
from src.core.application.services.input_handler import InputHandler
from src.core.application.states.running_state import RunningState
from src.core.application.states.edit_state import EditState

@pytest.fixture
def input_handler_dependencies():
    state_machine = Mock()
    window = Mock()
    widgets = [Mock()]
    return state_machine, window, widgets

def test_input_handler_initialization(input_handler_dependencies):
    state_machine, window, widgets = input_handler_dependencies
    handler = InputHandler(state_machine, window, widgets)
    
    assert handler.state_machine == state_machine
    assert handler.window == window
    assert handler.widgets == widgets

def test_handle_input_delegates_to_state_machine(input_handler_dependencies):
    state_machine, window, widgets = input_handler_dependencies
    handler = InputHandler(state_machine, window, widgets)
    
    mock_event = Mock()
    mock_event.type = pygame.MOUSEBUTTONDOWN
    window.handle_events.return_value = [mock_event]
    
    handler.handle_input()
    
    state_machine.handle_input.assert_called_with(mock_event)

def test_handle_global_keys_f1_toggles_mode(input_handler_dependencies):
    state_machine, window, widgets = input_handler_dependencies
    handler = InputHandler(state_machine, window, widgets)
    
    # Setup F1 event
    mock_event = Mock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_F1
    window.handle_events.return_value = [mock_event]
    
    # Mock current state as RunningState
    state_machine.current_state = RunningState(state_machine, widgets)
    
    handler.handle_input()
    
    # Should change to EditState
    assert state_machine.change_state.call_count == 1
    args, _ = state_machine.change_state.call_args
    assert isinstance(args[0], EditState)

def test_handle_global_keys_escape_closes_window(input_handler_dependencies):
    state_machine, window, widgets = input_handler_dependencies
    handler = InputHandler(state_machine, window, widgets)
    
    mock_event = Mock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_ESCAPE
    window.handle_events.return_value = [mock_event]
    
    handler.handle_input()
    
    assert window.is_running is False

def test_toggle_mode_to_running(input_handler_dependencies):
    state_machine, window, widgets = input_handler_dependencies
    handler = InputHandler(state_machine, window, widgets)
    
    mock_event = Mock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_F1
    window.handle_events.return_value = [mock_event]
    
    # Mock current state as EditState
    state_machine.current_state = EditState(state_machine, widgets)
    
    handler.handle_input()
    
    # Should change to RunningState
    assert state_machine.change_state.call_count == 1
    args, _ = state_machine.change_state.call_args
    assert isinstance(args[0], RunningState)
