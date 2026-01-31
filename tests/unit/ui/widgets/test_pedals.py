import pytest
from unittest.mock import Mock, patch
import pygame
from src.ui.widgets.pedals import Pedals
from src.core.domain.telemetry_data import TelemetryData


class TestPedals:
    def setup_method(self):
        pygame.init()
        self.mock_font_provider = Mock()
        self.mock_font = Mock()
        self.mock_font_provider.get_font.return_value = self.mock_font
        
        mock_text_surface = pygame.Surface((50, 20))
        self.mock_font.render.return_value = mock_text_surface
        
        self.pedals = Pedals(x=100, y=200, font_provider=self.mock_font_provider)

    def test_init_sets_position(self):
        assert self.pedals.x == 100
        assert self.pedals.y == 200

    def test_init_sets_dimensions(self):
        assert self.pedals.width == 120
        assert self.pedals.height == 180

    def test_init_creates_renderer(self):
        assert self.pedals.renderer is not None
        assert self.pedals.renderer.bar_width == 30

    def test_init_sets_default_values(self):
        assert self.pedals.throttle_pct == 0.0
        assert self.pedals.brake_pct == 0.0
        assert self.pedals.clutch_pct == 0.0

    def test_update_sets_throttle(self):
        data = TelemetryData(
            speed=100.0, rpm=5000, max_rpm=8000, gear=3,
            throttle_pct=0.75, brake_pct=0.0, clutch_pct=0.0,
            steering_angle=0.0, ffb_level=0.5, timestamp=0.0
        )
        self.pedals.update(data)
        
        assert self.pedals.throttle_pct == 0.75

    def test_update_sets_brake(self):
        data = TelemetryData(
            speed=100.0, rpm=5000, max_rpm=8000, gear=3,
            throttle_pct=0.0, brake_pct=0.50, clutch_pct=0.0,
            steering_angle=0.0, ffb_level=0.5, timestamp=0.0
        )
        self.pedals.update(data)
        
        assert self.pedals.brake_pct == 0.50

    def test_update_sets_clutch(self):
        data = TelemetryData(
            speed=100.0, rpm=5000, max_rpm=8000, gear=3,
            throttle_pct=0.0, brake_pct=0.0, clutch_pct=0.25,
            steering_angle=0.0, ffb_level=0.5, timestamp=0.0
        )
        self.pedals.update(data)
        
        assert self.pedals.clutch_pct == 0.25

    def test_update_sets_all_values(self):
        data = TelemetryData(
            speed=100.0, rpm=5000, max_rpm=8000, gear=3,
            throttle_pct=0.8, brake_pct=0.2, clutch_pct=0.5,
            steering_angle=0.0, ffb_level=0.5, timestamp=0.0
        )
        self.pedals.update(data)
        
        assert self.pedals.throttle_pct == 0.8
        assert self.pedals.brake_pct == 0.2
        assert self.pedals.clutch_pct == 0.5

    @patch('src.ui.rendering.pedals_renderer.PedalsRenderer.render')
    def test_draw_calls_renderer(self, mock_render):
        surface = pygame.Surface((800, 600))
        self.pedals.throttle_pct = 0.6
        self.pedals.brake_pct = 0.4
        self.pedals.clutch_pct = 0.2
        
        self.pedals.draw(surface)
        
        mock_render.assert_called_once_with(
            surface, 100, 200, 0.6, 0.4, 0.2, self.mock_font_provider
        )

    @patch('src.ui.widgets.pedals.DraggableBehavior')
    def test_handle_input_creates_draggable(self, mock_behavior_class):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (100, 200), 'button': 1})
        mock_behavior = Mock()
        mock_behavior.handle_input.return_value = True
        mock_behavior_class.return_value = mock_behavior
        
        result = self.pedals.handle_input(event)
        
        mock_behavior_class.assert_called_once_with(self.pedals)
        mock_behavior.handle_input.assert_called_once_with(event)
        assert result is True

    def test_get_rect_returns_correct_bounds(self):
        rect = self.pedals.get_rect()
        
        assert rect.x == 100
        assert rect.y == 200
        assert rect.width == 120
        assert rect.height == 180
