import pytest
from unittest.mock import Mock
import pygame
from src.ui.rendering.pedals_renderer import PedalsRenderer


class TestPedalsRenderer:
    def setup_method(self):
        pygame.init()
        self.surface = pygame.Surface((400, 300))
        self.renderer = PedalsRenderer(bar_width=30, bar_height=150, spacing=10)
        self.mock_font_provider = Mock()
        self.mock_font = Mock()
        self.mock_font_provider.get_font.return_value = self.mock_font
        
        mock_text_surface = pygame.Surface((50, 20))
        self.mock_font.render.return_value = mock_text_surface

    def test_init_sets_dimensions(self):
        assert self.renderer.bar_width == 30
        assert self.renderer.bar_height == 150
        assert self.renderer.spacing == 10

    def test_init_sets_colors(self):
        assert self.renderer.throttle_color == (0, 255, 100)
        assert self.renderer.brake_color == (255, 50, 50)
        assert self.renderer.clutch_color == (100, 150, 255)

    def test_render_draws_three_bars(self):
        self.renderer.render(self.surface, 10, 10, 0.5, 0.7, 0.3, self.mock_font_provider)
        
        assert self.mock_font_provider.get_font.call_count >= 3

    def test_render_with_zero_percentages(self):
        self.renderer.render(self.surface, 10, 10, 0.0, 0.0, 0.0, self.mock_font_provider)
        
        assert self.mock_font.render.call_count >= 6

    def test_render_with_full_percentages(self):
        self.renderer.render(self.surface, 10, 10, 1.0, 1.0, 1.0, self.mock_font_provider)
        
        assert self.mock_font.render.call_count >= 6

    def test_render_clamps_percentages(self):
        self.renderer.render(self.surface, 10, 10, 1.5, -0.5, 0.5, self.mock_font_provider)
        
        render_calls = [call[0][0] for call in self.mock_font.render.call_args_list]
        assert "100%" in render_calls
        assert "0%" in render_calls
        assert "50%" in render_calls

    def test_draw_bar_renders_labels(self):
        self.renderer._draw_bar(self.surface, 10, 10, 0.5, (255, 0, 0), self.mock_font_provider, "T")
        
        render_calls = [call[0][0] for call in self.mock_font.render.call_args_list]
        assert "T" in render_calls
        assert "50%" in render_calls

    def test_custom_dimensions(self):
        custom_renderer = PedalsRenderer(bar_width=40, bar_height=200, spacing=15)
        
        assert custom_renderer.bar_width == 40
        assert custom_renderer.bar_height == 200
        assert custom_renderer.spacing == 15
