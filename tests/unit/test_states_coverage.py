import pytest
from unittest.mock import Mock, call
import pygame
from src.core.states import RunningState, EditState
from src.ui.widgets.widget import Widget
from src.core.domain.telemetry_data import TelemetryData

def test_running_state_update_delegates_to_widgets():
    width, height = 100, 100
    widget1 = Mock(spec=Widget)
    widget2 = Mock(spec=Widget)
    widgets = [widget1, widget2]
    context = Mock()
    state = RunningState(context, widgets)
    
    data = Mock(spec=TelemetryData)
    state.update(data)
    
    widget1.update.assert_called_once_with(data)
    widget2.update.assert_called_once_with(data)

def test_running_state_draw_delegates_to_widgets():
    widget1 = Mock(spec=Widget)
    widgets = [widget1]
    context = Mock()
    state = RunningState(context, widgets)
    
    surface = Mock(spec=pygame.Surface)
    state.draw(surface)
    
    widget1.draw.assert_called_once_with(surface)

def test_running_state_handle_input_found():
    widget1 = Mock(spec=Widget)
    widget1.handle_input.return_value = True
    widgets = [widget1]
    context = Mock()
    state = RunningState(context, widgets)
    
    event = Mock(spec=pygame.event.Event)
    result = state.handle_input(event)
    
    assert result is True
    widget1.handle_input.assert_called_once_with(event)

def test_running_state_handle_input_not_found():
    widget1 = Mock(spec=Widget)
    widget1.handle_input.return_value = False
    widgets = [widget1]
    context = Mock()
    state = RunningState(context, widgets)
    
    event = Mock(spec=pygame.event.Event)
    result = state.handle_input(event)
    
    assert result is False

def test_edit_state_on_exit_clears_selection():
    context = Mock()
    widgets = []
    state = EditState(context, widgets)
    state.selected_widget = Mock(spec=Widget)
    
    state.on_exit()
    assert state.selected_widget is None

def test_edit_state_on_enter():
    context = Mock()
    widgets = []
    state = EditState(context, widgets)
    # Just coverage since it's empty
    state.on_enter()

def test_edit_state_update():
    context = Mock()
    widgets = []
    state = EditState(context, widgets)
    data = Mock(spec=TelemetryData)
    # Just coverage since it's empty
    state.update(data)

def test_edit_state_draw_widgets_and_selection():
    widget1 = Mock(spec=Widget)
    widget1.get_rect.return_value = pygame.Rect(0, 0, 10, 10)
    widgets = [widget1]
    context = Mock()
    state = EditState(context, widgets)
    state.selected_widget = widget1
    
    surface = Mock(spec=pygame.Surface)
    
    # We need to mock pygame.draw.rect since it requires a real surface context often
    # But here we just want to ensure it runs.
    # pygame.draw.rect might fail if video system is not initialized or surface is mock?
    # Pygame mocks usually work fine if not verifying pixels.
    # But pygame.draw.rect(surface, ...) checks surface type.
    # We might need a real surface or patch draw.
    
    # Using real surface for robustness
    real_surface = pygame.Surface((100, 100))
    state.draw(real_surface)
    
    widget1.draw.assert_called_once_with(real_surface)

def test_edit_state_handle_input_selection_hit():
    widget1 = Mock(spec=Widget)
    widget1.get_rect.return_value = pygame.Rect(0, 0, 50, 50)
    widgets = [widget1]
    context = Mock()
    state = EditState(context, widgets)
    
    # Mock event: Mouse click at 10, 10
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (10, 10), "button": 1})
    
    result = state.handle_input(event)
    
    assert result is True
    assert state.selected_widget == widget1

def test_edit_state_handle_input_selection_miss():
    widget1 = Mock(spec=Widget)
    widget1.get_rect.return_value = pygame.Rect(0, 0, 50, 50)
    widgets = [widget1]
    context = Mock()
    state = EditState(context, widgets)
    
    # Mock event: Mouse click at 100, 100 (outside)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (100, 100), "button": 1})
    
    result = state.handle_input(event)
    
    assert result is False
    assert state.selected_widget is None

def test_edit_state_handle_input_other_event():
    context = Mock()
    widgets = []
    state = EditState(context, widgets)
    
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    result = state.handle_input(event)
    assert result is False
