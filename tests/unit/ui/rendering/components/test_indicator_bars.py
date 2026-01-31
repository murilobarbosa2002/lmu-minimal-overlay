import pytest
import pygame
from src.ui.rendering.components.indicator_bars import IndicatorBars


class TestIndicatorBars:
    def setup_method(self):
        pygame.init()
        self.surface = pygame.Surface((200, 200))
        self.bars = IndicatorBars(spacing=12)
    
    def test_initialization(self):
        assert self.bars.throttle_bar is not None
        assert self.bars.brake_bar is not None
        assert self.bars.ffb_bar is not None
        assert self.bars.spacing == 12
    
    def test_render_all_bars(self):
        self.bars.render(
            surface=self.surface,
            x=50,
            y=50,
            throttle=0.8,
            brake=0.3,
            ffb=0.6,
            text_color=(255, 255, 255)
        )
        assert True
    
    def test_get_total_width(self):
        width = self.bars.get_total_width()
        # 3 bars * 18px + 2 spacings * 12px = 54 + 24 = 78
        assert width == 78
