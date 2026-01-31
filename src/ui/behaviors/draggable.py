import pygame


class DraggableBehavior:
    def __init__(self, widget):
        self.widget = widget
        self.is_dragging = False
        self.drag_offset = (0, 0)

    def handle_mouse_down(self, event: pygame.event.Event) -> bool:
        if event.button == 1:
            mouse_pos = event.pos
            rect = self.widget.get_rect()
            if rect.collidepoint(mouse_pos):
                self.is_dragging = True
                self.drag_offset = (self.widget.x - mouse_pos[0], self.widget.y - mouse_pos[1])
                return True
        return False

    def handle_mouse_up(self, event: pygame.event.Event) -> bool:
        if event.button == 1:
            self.is_dragging = False
        return False

    def handle_mouse_motion(self, event: pygame.event.Event) -> bool:
        if self.is_dragging:
            mouse_pos = event.pos
            new_x = mouse_pos[0] + self.drag_offset[0]
            new_y = mouse_pos[1] + self.drag_offset[1]
            self.widget.set_position(new_x, new_y)
            return True
        return False
