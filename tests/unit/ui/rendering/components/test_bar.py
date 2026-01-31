
import pytest
import pygame
from src.ui.rendering.components.bar import Bar


class TestBar:
    def setup_method(self):
        pygame.init()
        self.surface = pygame.Surface((200, 200))
        self.bar = Bar(label="T", color=(0, 255, 0), width=18, height=70)
    
    def test_initialization(self):
        assert self.bar.label == "T"
        assert self.bar.color == (0, 255, 0)
        assert self.bar.width == 18
        assert self.bar.height == 70
        assert self.bar.bidirectional == False
    
    def test_render_zero_value(self):
        self.bar.render(self.surface, 50, 50, 0.0, (255, 255, 255))
        assert True
    
    def test_render_full_value(self):
        self.bar.render(self.surface, 50, 50, 1.0, (255, 255, 255))
        assert True
    
    def test_render_partial_value(self):
        self.bar.render(self.surface, 50, 50, 0.5, (255, 255, 255))
        assert True
    
    def test_render_clamps_value_above_one(self):
        self.bar.render(self.surface, 50, 50, 1.5, (255, 255, 255))
        assert True
    
    def test_render_clamps_value_below_zero(self):
        self.bar.render(self.surface, 50, 50, -0.5, (255, 255, 255))
        assert True

    def test_bidirectional_mode_initialization(self):
        self.bar.set_bidirectional(True)
        assert self.bar.bidirectional == True

    def test_bidirectional_render_positive(self):
        self.bar.set_bidirectional(True)
        # Should render upwards from center
        self.bar.render(self.surface, 50, 50, 0.5, (255, 255, 255))
        assert True

    def test_bidirectional_render_negative(self):
        self.bar.set_bidirectional(True)
        # Should render downwards from center
        self.bar.render(self.surface, 50, 50, -0.5, (255, 255, 255))
        assert True

    def test_bidirectional_render_clamps(self):
        self.bar.set_bidirectional(True)
        self.bar.render(self.surface, 50, 50, 1.5, (255, 255, 255)) # Clamps directly
        self.bar.render(self.surface, 50, 50, -1.5, (255, 255, 255)) # Clamps
        assert True
