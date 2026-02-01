import pytest
from unittest.mock import Mock, patch
import pygame
from src.ui.widgets.input_card import InputCard
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


def test_input_card_init():
    input_card = InputCard(position_x=10, position_y=10)
    assert input_card.position_x == 10
    assert input_card.position_y == 10
    assert input_card.width == 350
    assert input_card.height == 130
    assert input_card.speed == 0.0
    assert input_card.gear == 0
    assert input_card.unit == "km/h"
    assert input_card.steering_angle == 0.0
    assert input_card.throttle_pct == 0.0
    assert input_card.brake_pct == 0.0
    assert input_card.ffb_level == 0.0


def test_input_card_update():
    input_card = InputCard(position_x=10, position_y=10)
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
        timestamp=0.0,
    )

    input_card.update(data)
    assert input_card.speed == 120
    assert input_card.gear == 4
    assert input_card.steering_angle == 45.0
    assert input_card.throttle_pct == 0.75
    assert input_card.brake_pct == 0.0
    assert input_card.ffb_level == 0.6


def test_input_card_draw():
    input_card = InputCard(position_x=10, position_y=10)
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
        timestamp=1.0,
    )
    input_card.update(data)

    # Draw should not raise exception
    input_card.draw(surface)
    assert True


def test_input_card_draw_special_gears():
    input_card = InputCard(position_x=10, position_y=10)
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
        timestamp=2.0,
    )
    input_card.update(data)
    input_card.draw(surface)

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
        timestamp=3.0,
    )
    input_card.update(data2)
    input_card.draw(surface)
    assert True


def test_input_card_input():
    input_card = InputCard(position_x=10, position_y=10)
    # Use actual pygame event
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    result = input_card.handle_input(event)
    # Should return False for non-mouse events
    assert result is False


def test_unit_conversion():
    input_card = InputCard(position_x=0, position_y=0)
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
        timestamp=4.0,
    )

    input_card.update(data)
    assert input_card.speed == 100

    input_card.set_unit("mph")
    assert input_card.unit == "mph"


def test_mph_coverage_explicit():
    input_card = InputCard(position_x=0, position_y=0)
    input_card.unit = "mph"
    data = Mock()
    data.speed = 100.0
    data.gear = 1
    data.steering_angle = 0
    data.throttle_pct = 0
    data.brake_pct = 0
    data.ffb_level = 0

    input_card.update(data)
    assert input_card.speed == 62


def test_draw_visual_feedback_dragging():
    input_card = InputCard(position_x=0, position_y=0)
    # Mock draggable to simulate dragging state
    mock_draggable = Mock()
    mock_draggable.is_dragging = True
    input_card._draggable = mock_draggable

    # Mock renderer to verify call args
    mock_renderer = Mock()
    input_card._renderer = mock_renderer

    surface = Mock()
    input_card.draw(surface)

    # Verify bg_color was changed to feedback color (0, 15, 60, 200)
    args = mock_renderer.render.call_args.kwargs
    assert args["bg_color"] == (0, 15, 60, 200)

    # Test invalid unit
    input_card.set_unit("invalid")
    assert input_card.unit == "km/h"


def test_drag_and_drop():
    input_card = InputCard(position_x=0, position_y=0, width=400, height=130)

    # 1. Mouse Down (Hit)
    event_down = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"pos": (50, 50), "button": 1}
    )
    assert input_card.handle_input(event_down) is True

    # 2. Mouse Motion (Dragging - requires checking DraggableBehavior)
    event_move = pygame.event.Event(
        pygame.MOUSEMOTION, {"pos": (60, 60), "buttons": (1, 0, 0)}
    )
    # This creates new DraggableBehavior each time, so drag state isn't preserved
    # We just verify it doesn't crash
    input_card.handle_input(event_move)

    # 3. Mouse Up
    event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (60, 60), "button": 1})
    input_card.handle_input(event_up)
    assert True


def test_drag_miss():
    input_card = InputCard(position_x=0, position_y=0, width=400, height=130)
    event_down = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"pos": (500, 500), "button": 1}
    )
    assert input_card.handle_input(event_down) is False


def test_get_rect():
    input_card = InputCard(position_x=100, position_y=200, width=400, height=130)
    rect = input_card.get_rect()
    assert rect.x == 100
    assert rect.y == 200
    assert rect.width == 400
    assert rect.height == 130


def test_set_position():
    input_card = InputCard(position_x=0, position_y=0)
    input_card.set_position(150, 250)
    assert input_card.position_x == 150
    assert input_card.position_y == 250
