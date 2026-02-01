import pytest
import pygame
from src.ui.rendering.components.speed_gear_display import SpeedGearDisplay


class TestSpeedGearDisplay:
    def setup_method(self):
        pygame.init()
        self.surface = pygame.Surface((300, 200))
        self.display = SpeedGearDisplay()

    def test_initialization(self):
        assert self.display.speed_surf is None
        assert self.display.unit_surf is None
        assert self.display.gear_surf is None

    def test_render_basic(self):
        self.display.render(
            surface=self.surface,
            position_x=50,
            position_y=20,
            width=200,
            height=130,
            speed=150.0,
            gear=5,
            unit="km/h",
            rpm=6500,
            max_rpm=8000,
            text_color=(255, 255, 255),
            gear_color=(255, 200, 0),
        )
        # Should create cached surfaces
        assert self.display.speed_surf is not None
        assert self.display.unit_surf is not None
        assert self.display.gear_surf is not None

    def test_render_special_gears(self):
        # Reverse
        self.display.render(
            surface=self.surface,
            position_x=50,
            position_y=20,
            width=200,
            height=130,
            speed=5.0,
            gear=-1,
            unit="km/h",
            rpm=1500,
            max_rpm=8000,
            text_color=(255, 255, 255),
            gear_color=(255, 200, 0),
        )
        assert self.display.gear_surf is not None

        # Neutral
        self.display.render(
            surface=self.surface,
            position_x=50,
            position_y=20,
            width=200,
            height=130,
            speed=0.0,
            gear=0,
            unit="km/h",
            rpm=1500,
            max_rpm=8000,
            text_color=(255, 255, 255),
            gear_color=(255, 200, 0),
        )
        assert self.display.gear_surf is not None

    def test_invalidate_cache(self):
        # Populate cache
        self.display.render(
            surface=self.surface,
            position_x=50,
            position_y=20,
            width=200,
            height=130,
            speed=100.0,
            gear=3,
            unit="km/h",
            rpm=5000,
            max_rpm=8000,
            text_color=(255, 255, 255),
            gear_color=(255, 200, 0),
        )

        # Invalidate
        self.display.invalidate_cache()
        assert self.display.speed_surf is None
        assert self.display.unit_surf is None
        assert self.display.gear_surf is None
