import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.ui.rendering.components.steering_indicator import SteeringIndicator


class TestSteeringIndicator:
    def setup_method(self):
        pygame.init()
        self.surface = pygame.Surface((200, 200))
        # Default indicator for basic tests (might load image if present)
        # We will override for specific coverage
        self.indicator = SteeringIndicator(radius=30)

    def test_initialization(self):
        assert self.indicator.radius == 30

    def test_init_loads_image_if_exists(self):
        with patch("os.path.exists", return_value=True):
            with patch("pygame.image.load", return_value=pygame.Surface((10, 10))):
                with patch(
                    "pygame.transform.smoothscale",
                    return_value=pygame.Surface((60, 60)),
                ):
                    ind = SteeringIndicator()
                    assert ind.wheel_image is not None

    def test_init_fallback_if_missing(self):
        with patch("os.path.exists", return_value=False):
            ind = SteeringIndicator()
            assert ind.wheel_image is None

    def test_init_exception_handling(self):
        with patch("os.path.exists", return_value=True):
            with patch("pygame.image.load", side_effect=Exception("Load failed")):
                ind = SteeringIndicator()
                assert ind.wheel_image is None

    def test_render_with_image(self):
        # Force indicator to have an image
        self.indicator.wheel_image = pygame.Surface((60, 60))

        with patch(
            "pygame.transform.rotozoom", return_value=pygame.Surface((60, 60))
        ) as mock_rotozoom:
            self.indicator.render(self.surface, 100, 100, 45.0, (255, 255, 255))
            # Verify rotozoom called with negative angle and scale 1.0
            mock_rotozoom.assert_called_with(self.indicator.wheel_image, -45.0, 1.0)

    def test_render_fallback_vector(self):
        # Force indicator to NOT have an image
        self.indicator.wheel_image = None

        # Should run without error and draw lines/circles
        self.indicator.render(self.surface, 100, 100, 0.0, (255, 255, 255))
        assert True

    def test_render_full_rotation_vector(self):
        self.indicator.wheel_image = None
        for angle in range(0, 360, 45):
            self.indicator.render(
                surface=self.surface,
                cx=100,
                cy=100,
                angle=float(angle),
                color=(255, 255, 255),
            )
        assert True
