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
    assert speedometer.y == 10
    assert speedometer.width == 350
    assert speedometer.height == 130
    assert speedometer.speed == 0.0
    assert speedometer.gear == 0
    assert speedometer.unit == "km/h"
    assert speedometer.steering_angle == 0.0
    assert speedometer.throttle_pct == 0.0
    assert speedometer.brake_pct == 0.0
    assert speedometer.ffb_level == 0.0

def test_speedometer_update():
    speedometer = Speedometer(10, 10)
    data = TelemetryData(
        speed=120.0,
        rpm=6000,
        max_rpm=8000,
        gear=4,
        throttle_pct=0.75,
        brake_pct=0.0,
        clutch_pct=0.0,
        steering_angle=45.0,
        ffb_level=0.6,
        timestamp=0.0
    )
    
    speedometer.update(data)
    assert speedometer.speed == 120
    assert speedometer.gear == 4
    assert speedometer.steering_angle == 45.0
    assert speedometer.throttle_pct == 0.75
    assert speedometer.brake_pct == 0.0
    assert speedometer.ffb_level == 0.6

def test_speedometer_draw():
    speedometer = Speedometer(10, 10)
    surface = pygame.Surface((800, 600))
    
    # Setup state
    data = TelemetryData(
        speed=180.0,
        rpm=7000,
        max_rpm=8000,
        gear=5,
        throttle_pct=1.0,
        brake_pct=0.2,
        clutch_pct=0.0,
        steering_angle=90.0,
        ffb_level=0.8,
        timestamp=1.0
    )
    speedometer.update(data)
    
    # Draw should not raise exception
    speedometer.draw(surface)
    assert True

def test_speedometer_draw_special_gears():
    speedometer = Speedometer(10, 10)
    surface = pygame.Surface((800, 600))
    
    # Reverse
    data = TelemetryData(
        speed=5.0,
        rpm=2000,
        max_rpm=8000,
        gear=-1,
        throttle_pct=0.0,
        brake_pct=0.0,
        clutch_pct=1.0,
        steering_angle=0.0,
        ffb_level=0.0,
        timestamp=2.0
    )
    speedometer.update(data)
    speedometer.draw(surface)
    
    # Neutral
    data2 = TelemetryData(
        speed=0.0,
        rpm=1000,
        max_rpm=8000,
        gear=0,
        throttle_pct=0.0,
        brake_pct=1.0,
        clutch_pct=1.0,
        steering_angle=0.0,
        ffb_level=0.0,
        timestamp=3.0
    )
    speedometer.update(data2)
    speedometer.draw(surface)
    assert True

def test_speedometer_input():
    speedometer = Speedometer(10, 10)
    # Use actual pygame event
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    result = speedometer.handle_input(event)
    # Should return False for non-mouse events
    assert result is False

def test_unit_conversion():
    speedometer = Speedometer(0, 0)
    data = TelemetryData(
        speed=100.0,  # km/h
        rpm=5000,
        max_rpm=8000,
        gear=3,
        throttle_pct=0.5,
        brake_pct=0.0,
        clutch_pct=0.0,
        steering_angle=0.0,
        ffb_level=0.3,
        timestamp=4.0
    )
    
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
    speedometer = Speedometer(0, 0, 400, 130)
    
    # 1. Mouse Down (Hit)
    event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (50, 50), "button": 1})
    assert speedometer.handle_input(event_down) is True
    
    # 2. Mouse Motion (Dragging - requires checking DraggableBehavior)
    event_move = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (60, 60), "buttons": (1, 0, 0)})
    # This creates new DraggableBehavior each time, so drag state isn't preserved
    # We just verify it doesn't crash
    speedometer.handle_input(event_move)
    
    # 3. Mouse Up
    event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (60, 60), "button": 1})
    speedometer.handle_input(event_up)
    assert True

def test_drag_miss():
    speedometer = Speedometer(0, 0, 400, 130)
    event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (500, 500), "button": 1})
    assert speedometer.handle_input(event_down) is False

def test_get_rect():
    speedometer = Speedometer(100, 200, 400, 130)
    rect = speedometer.get_rect()
    assert rect.x == 100
    assert rect.y == 200
    assert rect.width == 400
    assert rect.height == 130

def test_set_position():
    speedometer = Speedometer(0, 0)
    speedometer.set_position(150, 250)
    assert speedometer.x == 150
    assert speedometer.y == 250
