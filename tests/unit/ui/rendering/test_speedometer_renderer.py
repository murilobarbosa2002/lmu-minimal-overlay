import pytest
import pygame
from unittest.mock import Mock, MagicMock
from src.ui.rendering.speedometer_renderer import SpeedometerRenderer


class TestSpeedometerRenderer:
    def setup_method(self):
        pygame.init()
        self.mock_font_provider = Mock()
        self.renderer = SpeedometerRenderer(self.mock_font_provider)

    def teardown_method(self):
        pygame.quit()

    def test_initialization(self):
        assert self.renderer.font_provider is self.mock_font_provider
        assert self.renderer._bg_surface is None

    def test_create_background(self):
        surface = self.renderer.create_background(200, 150)
        
        assert surface is not None
        assert surface.get_width() == 200
        assert surface.get_height() == 150
        assert self.renderer._bg_surface is surface

    def test_create_background_cached(self):
        surface1 = self.renderer.create_background(200, 150)
        surface2 = self.renderer.create_background(200, 150)
        
        assert surface1 is surface2

    def test_create_masked_surface(self):
        surface = self.renderer.create_masked_surface(200, 150)
        
        assert surface is not None
        assert surface.get_width() == 200
        assert surface.get_height() == 150

    def test_render_gear_normal(self):
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        self.mock_font_provider.get_font.return_value = mock_font
        
        result = self.renderer.render_gear(3, (255, 200, 0))
        
        self.mock_font_provider.get_font.assert_called_once_with(40, bold=True)
        mock_font.render.assert_called_once_with("3", True, (255, 200, 0))

    def test_render_gear_reverse(self):
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        self.mock_font_provider.get_font.return_value = mock_font
        
        result = self.renderer.render_gear(-1, (255, 200, 0))
        
        mock_font.render.assert_called_once_with("R", True, (255, 200, 0))

    def test_render_gear_neutral(self):
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        self.mock_font_provider.get_font.return_value = mock_font
        
        result = self.renderer.render_gear(0, (255, 200, 0))
        
        mock_font.render.assert_called_once_with("N", True, (255, 200, 0))

    def test_render_speed(self):
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        self.mock_font_provider.get_font.return_value = mock_font
        
        result = self.renderer.render_speed(125, (255, 255, 255))
        
        self.mock_font_provider.get_font.assert_called_once_with(90, bold=True)
        mock_font.render.assert_called_once_with("125", True, (255, 255, 255))

    def test_render_speed_converts_to_int(self):
        mock_font = Mock()
        mock_font.render.return_value = Mock()
        self.mock_font_provider.get_font.return_value = mock_font
        
        result = self.renderer.render_speed(125.7, (255, 255, 255))
        
        mock_font.render.assert_called_once_with("125", True, (255, 255, 255))
