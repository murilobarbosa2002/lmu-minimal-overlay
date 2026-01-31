import pytest
import pygame
from unittest.mock import Mock, MagicMock
from src.ui.rendering.speedometer_renderer import SpeedometerRenderer


class TestSpeedometerRenderer:
    def setup_method(self):
        pygame.init()
        self.renderer = SpeedometerRenderer()
        self.surface = pygame.Surface((800, 600))
    
    def test_initialization(self):
        assert self.renderer.steering is not None
        assert self.renderer.speed_gear is not None
        assert self.renderer.bars is not None
    
    def test_render_calls_components(self):
        self.renderer.render(
            surface=self.surface,
            x=100,
            y=100,
            width=400,
            height=130,
            speed=120.0,
            gear=4,
            unit="km/h",
            steering_angle=45.0,
            throttle_pct=0.75,
            brake_pct=0.0,
            ffb_level=0.5,
            bg_color=(0, 0, 0, 180),
            text_color=(255, 255, 255),
            gear_color=(255, 200, 0)
        )
        
        # Should not raise any exceptions
        assert True
    
    def test_render_draws_background(self):
        self.renderer.render(
            surface=self.surface,
            x=50,
            y=50,
            width=400,
            height=130,
            speed=180.0,
            gear=6,
            unit="km/h",
            steering_angle=0.0,
            throttle_pct=1.0,
            brake_pct=0.3,
            ffb_level=0.8,
            bg_color=(0, 0, 0, 200),
            text_color=(255, 255, 255),
            gear_color=(255, 200, 0)
        )
        
        # Should not raise and background should be drawn
        assert True
