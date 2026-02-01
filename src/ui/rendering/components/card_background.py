import pygame
from src.core.domain.constants import (
    MAX_COLOR_VALUE,
    MIN_COLOR_VALUE,
    ALPHA_CHANNEL_INDEX,
    RED_CHANNEL_INDEX,
    GREEN_CHANNEL_INDEX,
    BLUE_CHANNEL_INDEX,
    RGBA_TUPLE_LENGTH,
    ALPHA_THRESHOLD_FOR_MASKING,
    TRANSPARENT_COLOR,
    MASK_WHITE_COLOR,
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
    ):
        self._border_radius = border_radius
        self._border_color = border_color
        self._gradient_top_multiplier = gradient_top_multiplier
        self._gradient_bottom_multiplier = gradient_bottom_multiplier
        self._default_alpha = default_alpha

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
                    pixel_alpha = pixel[ALPHA_CHANNEL_INDEX]
                    final_surface.set_at(
                        (x_position, y_position),
                        (
                            pixel[RED_CHANNEL_INDEX],
                            pixel[GREEN_CHANNEL_INDEX],
                            pixel[BLUE_CHANNEL_INDEX],
                            pixel_alpha,
                        ),
                    )

        border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            border_surf,
            self._border_color,
            (MIN_COLOR_VALUE, MIN_COLOR_VALUE, width, height),
            width=BORDER_WIDTH,
            border_radius=self._border_radius,
        )
        final_surface.blit(border_surf, (MIN_COLOR_VALUE, MIN_COLOR_VALUE))

        surface.blit(final_surface, (position_x, position_y))
