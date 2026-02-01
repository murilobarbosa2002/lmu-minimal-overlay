import pygame
import random
from src.core.domain.constants import (
    MAX_COLOR_VALUE,
    MIN_COLOR_VALUE,
    ALPHA_CHANNEL_INDEX,
    RED_CHANNEL_INDEX,
    GREEN_CHANNEL_INDEX,
    BLUE_CHANNEL_INDEX,
    RGBA_TUPLE_LENGTH,
    ALPHA_THRESHOLD_FOR_MASKING,
    FULL_ALPHA,
    TRANSPARENT_ALPHA,
    MASK_WHITE_COLOR,
    TRANSPARENT_COLOR,
    BORDER_WIDTH,
)


class CardBackground:
    def __init__(
        self,
        border_radius: int,
        border_color: tuple,
        gradient_top_multiplier: float,
        gradient_bottom_multiplier: float,
        default_alpha: int,
        border_glow_color: tuple = None,
        border_glow_width: int = 0,
        noise_intensity: float = 0.0,
        inner_shadow_intensity: int = 0,
        inner_shadow_size: int = 0,
    ):
        self._border_radius = border_radius
        self._border_color = border_color
        self._gradient_top_multiplier = gradient_top_multiplier
        self._gradient_bottom_multiplier = gradient_bottom_multiplier
        self._default_alpha = default_alpha
        self._border_glow_color = border_glow_color or (255, 255, 255, 0)
        self._border_glow_width = border_glow_width
        self._noise_intensity = noise_intensity
        self._inner_shadow_intensity = inner_shadow_intensity
        self._inner_shadow_size = inner_shadow_size

    def render(
        self,
        surface: pygame.Surface,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        bg_color: tuple,
    ) -> None:
        bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        red = bg_color[RED_CHANNEL_INDEX]
        green = bg_color[GREEN_CHANNEL_INDEX]
        blue = bg_color[BLUE_CHANNEL_INDEX]

        top_color = (
            min(MAX_COLOR_VALUE, int(red * self._gradient_top_multiplier)),
            min(MAX_COLOR_VALUE, int(green * self._gradient_top_multiplier)),
            min(MAX_COLOR_VALUE, int(blue * self._gradient_top_multiplier)),
        )
        bottom_color = (
            int(red * self._gradient_bottom_multiplier),
            int(green * self._gradient_bottom_multiplier),
            int(blue * self._gradient_bottom_multiplier),
        )

        alpha = (
            bg_color[ALPHA_CHANNEL_INDEX]
            if len(bg_color) == RGBA_TUPLE_LENGTH
            else self._default_alpha
        )

        for y_offset in range(height):
            gradient_ratio = y_offset / height
            current_red = int(
                top_color[RED_CHANNEL_INDEX] * (1 - gradient_ratio)
                + bottom_color[RED_CHANNEL_INDEX] * gradient_ratio
            )
            current_green = int(
                top_color[GREEN_CHANNEL_INDEX] * (1 - gradient_ratio)
                + bottom_color[GREEN_CHANNEL_INDEX] * gradient_ratio
            )
            current_blue = int(
                top_color[BLUE_CHANNEL_INDEX] * (1 - gradient_ratio)
                + bottom_color[BLUE_CHANNEL_INDEX] * gradient_ratio
            )
            pygame.draw.line(
                temp_surface,
                (current_red, current_green, current_blue, alpha),
                (MIN_COLOR_VALUE, y_offset),
                (width, y_offset),
            )

        bg_surface.blit(temp_surface, (MIN_COLOR_VALUE, MIN_COLOR_VALUE))

        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        mask.fill(TRANSPARENT_COLOR)
        pygame.draw.rect(
            mask,
            MASK_WHITE_COLOR,
            (MIN_COLOR_VALUE, MIN_COLOR_VALUE, width, height),
            border_radius=self._border_radius,
        )

        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        final_surface.fill(TRANSPARENT_COLOR)

        for y_position in range(height):
            for x_position in range(width):
                mask_alpha = mask.get_at((x_position, y_position))[ALPHA_CHANNEL_INDEX]
                if mask_alpha > ALPHA_THRESHOLD_FOR_MASKING:
                    pixel = bg_surface.get_at((x_position, y_position))
                    final_surface.set_at(
                        (x_position, y_position),
                        (
                            pixel[RED_CHANNEL_INDEX],
                            pixel[GREEN_CHANNEL_INDEX],
                            pixel[BLUE_CHANNEL_INDEX],
                            FULL_ALPHA,
                        ),
                    )

        self._apply_glassmorphism_effects(final_surface, width, height)

        surface.blit(final_surface, (position_x, position_y))

    def _apply_glassmorphism_effects(
        self, surface: pygame.Surface, width: int, height: int
    ) -> None:
        if self._noise_intensity > 0:
            self._apply_noise_texture(surface, width, height)

        if self._inner_shadow_intensity > 0:
            self._apply_inner_shadow(surface, width, height)

        if self._border_glow_width > 0:
            self._apply_border_glow(surface, width, height)

        border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            border_surf,
            self._border_color,
            (MIN_COLOR_VALUE, MIN_COLOR_VALUE, width, height),
            width=BORDER_WIDTH,
            border_radius=self._border_radius,
        )
        surface.blit(border_surf, (MIN_COLOR_VALUE, MIN_COLOR_VALUE))

    def _apply_noise_texture(
        self, surface: pygame.Surface, width: int, height: int
    ) -> None:
        noise_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        noise_surface.fill(TRANSPARENT_COLOR)

        for y_position in range(0, height, 2):
            for x_position in range(0, width, 2):
                if random.random() < self._noise_intensity:
                    noise_value = random.randint(0, 30)
                    noise_surface.set_at(
                        (x_position, y_position),
                        (noise_value, noise_value, noise_value, noise_value),
                    )

        surface.blit(noise_surface, (MIN_COLOR_VALUE, MIN_COLOR_VALUE))

    def _apply_inner_shadow(
        self, surface: pygame.Surface, width: int, height: int
    ) -> None:
        shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        shadow_surface.fill(TRANSPARENT_COLOR)

        shadow_mask = pygame.Surface((width, height), pygame.SRCALPHA)
        shadow_mask.fill(TRANSPARENT_COLOR)
        pygame.draw.rect(
            shadow_mask,
            MASK_WHITE_COLOR,
            (
                self._inner_shadow_size,
                self._inner_shadow_size,
                width - self._inner_shadow_size * 2,
                height - self._inner_shadow_size * 2,
            ),
            border_radius=max(0, self._border_radius - self._inner_shadow_size),
        )

        for y_position in range(height):
            for x_position in range(width):
                if (
                    shadow_mask.get_at((x_position, y_position))[ALPHA_CHANNEL_INDEX]
                    == 0
                ):
                    shadow_surface.set_at(
                        (x_position, y_position),
                        (0, 0, 0, self._inner_shadow_intensity),
                    )

        surface.blit(shadow_surface, (MIN_COLOR_VALUE, MIN_COLOR_VALUE))

    def _apply_border_glow(
        self, surface: pygame.Surface, width: int, height: int
    ) -> None:
        for glow_offset in range(self._border_glow_width, 0, -1):
            glow_alpha = int(
                self._border_glow_color[ALPHA_CHANNEL_INDEX]
                * (glow_offset / self._border_glow_width)
            )
            glow_color = (
                self._border_glow_color[RED_CHANNEL_INDEX],
                self._border_glow_color[GREEN_CHANNEL_INDEX],
                self._border_glow_color[BLUE_CHANNEL_INDEX],
                glow_alpha,
            )

            glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(
                glow_surface,
                glow_color,
                (MIN_COLOR_VALUE, MIN_COLOR_VALUE, width, height),
                width=glow_offset,
                border_radius=self._border_radius,
            )
            surface.blit(glow_surface, (MIN_COLOR_VALUE, MIN_COLOR_VALUE))
