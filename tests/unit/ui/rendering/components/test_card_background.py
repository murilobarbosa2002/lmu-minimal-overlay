import pytest
import pygame
from unittest.mock import Mock, call, patch
from src.ui.rendering.components.card_background import CardBackground

class TestCardBackground:
    def setup_method(self):
        pygame.init()
        self.background = CardBackground(
            border_radius=20,
            border_color=(255, 255, 255, 50),
            mask_color=(255, 255, 255),
            gradient_top_multiplier=1.2,
            gradient_bottom_multiplier=0.8,
            default_alpha=200
        )
        self.surface = pygame.Surface((800, 600))
    
    def test_render_draws_gradient(self):
        with patch('pygame.draw.line') as mock_line:
            self.background.render(
                self.surface,
                position_x=0, position_y=0,
                width=100, height=50,
                bg_color=(100, 100, 100, 255)
            )
            # Should draw 50 lines (height)
            assert mock_line.call_count == 50
    
    def test_render_uses_alpha(self):
        with patch('pygame.draw.line') as mock_line:
            self.background.render(
                self.surface,
                position_x=0, position_y=0,
                width=100, height=50,
                bg_color=(0, 0, 0, 123)
            )
            # Verify alpha
            args = mock_line.call_args_list[0].args
            color = args[1]
            assert color[3] == 123

    def test_render_applies_mask_and_border(self):
        with patch('pygame.draw.rect') as mock_rect:
            self.background.render(
                self.surface,
                position_x=0, position_y=0,
                width=100, height=50,
                bg_color=(0, 0, 0, 255)
            )
            # 1 for mask, 1 for border
            assert mock_rect.call_count == 2
