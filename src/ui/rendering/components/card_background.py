import pygame


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

        r, g, b = bg_color[0], bg_color[1], bg_color[2]

        top_color = (
            min(255, int(r * self._gradient_top_multiplier)),
            min(255, int(g * self._gradient_top_multiplier)),
            min(255, int(b * self._gradient_top_multiplier)),
        )
        bottom_color = (
            int(r * self._gradient_bottom_multiplier),
            int(g * self._gradient_bottom_multiplier),
            int(b * self._gradient_bottom_multiplier),
        )

        alpha = bg_color[3] if len(bg_color) == 4 else self._default_alpha

        for y_offset in range(height):
            ratio = y_offset / height
            r_curr = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g_curr = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b_curr = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(
                temp_surface,
                (r_curr, g_curr, b_curr, alpha),
                (0, y_offset),
                (width, y_offset),
            )

        bg_surface.blit(temp_surface, (0, 0))

        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))
        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            (0, 0, width, height),
            border_radius=self._border_radius,
        )

        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        final_surface.fill((0, 0, 0, 0))

        for y in range(height):
            for x in range(width):
                mask_alpha = mask.get_at((x, y))[3]
                if mask_alpha > 128:
                    pixel = bg_surface.get_at((x, y))
                    final_surface.set_at((x, y), (pixel[0], pixel[1], pixel[2], 255))

        border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            border_surf,
            self._border_color,
            (0, 0, width, height),
            width=1,
            border_radius=self._border_radius,
        )
        final_surface.blit(border_surf, (0, 0))

        surface.blit(final_surface, (position_x, position_y))
