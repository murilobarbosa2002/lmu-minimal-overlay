import pytest
import pygame
from src.ui.rendering.components.steering_indicator import SteeringIndicator


class TestSteeringIndicator:
    def setup_method(self):
        pygame.init()
        self.surface = pygame.Surface((200, 200))
        self.indicator = SteeringIndicator(radius=30)
    
    def test_initialization(self):
        assert self.indicator.radius == 30
    
    def test_render_center_angle(self):
        self.indicator.render(
            surface=self.surface,
            cx=100,
            cy=100,
            angle=0.0,
            color=(255, 255, 255)
        )
        assert True
    
    def test_render_left_angle(self):
        self.indicator.render(
            surface=self.surface,
            cx=100,
            cy=100,
            angle=-90.0,
            color=(255, 255, 255)
        )
        assert True
    
    def test_render_right_angle(self):
        self.indicator.render(
            surface=self.surface,
            cx=100,
            cy=100,
            angle=90.0,
            color=(255, 255, 255)
        )
        assert True
    
    def test_render_full_rotation(self):
        # Test 360 degree rotation
        for angle in range(0, 360, 45):
            self.indicator.render(
                surface=self.surface,
                cx=100,
                cy=100,
                angle=float(angle),
                color=(255, 255, 255)
            )
        assert True
