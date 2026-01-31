import pytest
from unittest.mock import Mock, patch
import pygame
from src.ui.widgets.speedometer import Speedometer
from src.ui.utils.fonts import FontManager
from src.core.domain.telemetry_data import TelemetryData

# Initialize font module for tests
pygame.font.init()

def test_font_manager_singleton_behavior():
    font1 = FontManager.get_font(20)
    font2 = FontManager.get_font(20)
    assert font1 is font2

def test_font_manager_different_sizes():
    font1 = FontManager.get_font(20)
    font2 = FontManager.get_font(30)
    assert font1 is not font2

def test_speedometer_init():
    speedometer = Speedometer(x=10, y=10)
    assert speedometer.x == 10
    assert speedometer.speed == 0.0
    assert speedometer.speed_surf is None

def test_speedometer_update_cache_invalidation():
    speedometer = Speedometer(10, 10)
    data = Mock(spec=TelemetryData)
    data.speed = 100.0
    data.gear = 4
    
    # First update
    speedometer.update(data)
    assert speedometer.speed == 100
    assert speedometer.gear == 4
    
    # Mock cache population
    speedometer.speed_surf = Mock()
    speedometer.gear_surf = Mock()
    
    # Update with same data
    speedometer.update(data)
    assert speedometer.speed_surf is not None
    
    # Update with new data
    data.speed = 101.0
    speedometer.update(data)
    assert speedometer.speed_surf is None # Should invalidate

def test_speedometer_draw():
    speedometer = Speedometer(10, 10)
    surface = pygame.Surface((200, 200))
    
    # Setup state
    data = Mock(spec=TelemetryData)
    data.speed = 120.0
    data.gear = 5
    speedometer.update(data)
    
    # Draw
    speedometer.draw(surface)
    
    # Verify surfaces created
    assert speedometer.speed_surf is not None
    assert speedometer.gear_surf is not None

def test_speedometer_draw_special_gears():
    speedometer = Speedometer(10, 10)
    surface = pygame.Surface((200, 200))
    
    # Reverse
    data = Mock(spec=TelemetryData)
    data.speed = 0
    data.gear = -1
    speedometer.update(data)
    speedometer.draw(surface)
    
    # Neutral
    data.gear = 0
    speedometer.update(data)
    speedometer.draw(surface)

def test_speedometer_input():
    speedometer = Speedometer(10, 10)
    # Ignored event
    assert speedometer.handle_input(Mock(type=pygame.KEYDOWN)) is False

def test_unit_conversion():
    speedometer = Speedometer(0, 0)
    data = Mock(spec=TelemetryData)
    data.speed = 100.0 # km/h
    data.gear = 1
    
    speedometer.update(data)
    assert speedometer.speed == 100
    
    speedometer.set_unit("mph")
    assert speedometer.unit == "mph"
    
    speedometer.update(data)
    # 100 km/h * 0.621371 = 62.1371 -> 62
    assert speedometer.speed == 62
    
    # Test invalid unit
    speedometer.set_unit("invalid")
    assert speedometer.unit == "mph"

def test_drag_and_drop():
    speedometer = Speedometer(0, 0, 100, 100)
    
    # 1. Mouse Down (Hit)
    event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (50, 50), "button": 1})
    assert speedometer.handle_input(event_down) is True
    assert speedometer.is_dragging is True
    assert speedometer.drag_offset == (-50, -50)
    
    # 2. Mouse Motion (Dragging)
    event_move = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (60, 60), "buttons": (1, 0, 0)})
    assert speedometer.handle_input(event_move) is True
    # New pos should be mouse_pos + offset
    # 60 + (-50) = 10
    assert speedometer.x == 10
    assert speedometer.y == 10
    
    # 3. Mouse Up (Drop)
    event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (60, 60), "button": 1})
    speedometer.handle_input(event_up)
    assert speedometer.is_dragging is False

def test_drag_miss():
    speedometer = Speedometer(0, 0, 100, 100)
    event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (200, 200), "button": 1})
    assert speedometer.handle_input(event_down) is False
    assert speedometer.is_dragging is False

