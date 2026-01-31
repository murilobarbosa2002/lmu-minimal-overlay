import pytest
import pygame
from unittest.mock import Mock, MagicMock
from src.ui.behaviors.draggable import DraggableBehavior


class TestDraggableBehavior:
    def setup_method(self):
        self.mock_widget = Mock()
        self.mock_widget.x = 100
        self.mock_widget.y = 100
        self.mock_widget.get_rect.return_value = pygame.Rect(100, 100, 50, 50)
        self.behavior = DraggableBehavior(self.mock_widget)

    def test_initialization(self):
        assert self.behavior.widget is self.mock_widget
        assert self.behavior.is_dragging is False
        assert self.behavior.drag_offset == (0, 0)

    def test_mouse_down_hit(self):
        event = Mock()
        event.button = 1
        event.pos = (110, 110)
        
        result = self.behavior.handle_mouse_down(event)
        
        assert result is True
        assert self.behavior.is_dragging is True
        assert self.behavior.drag_offset == (100 - 110, 100 - 110)

    def test_mouse_down_miss(self):
        event = Mock()
        event.button = 1
        event.pos = (200, 200)
        
        result = self.behavior.handle_mouse_down(event)
        
        assert result is False
        assert self.behavior.is_dragging is False

    def test_mouse_down_wrong_button(self):
        event = Mock()
        event.button = 3
        event.pos = (110, 110)
        
        result = self.behavior.handle_mouse_down(event)
        
        assert result is False
        assert self.behavior.is_dragging is False

    def test_mouse_up_stops_dragging(self):
        self.behavior.is_dragging = True
        
        event = Mock()
        event.button = 1
        
        result = self.behavior.handle_mouse_up(event)
        
        assert result is False
        assert self.behavior.is_dragging is False

    def test_mouse_motion_while_dragging(self):
        self.behavior.is_dragging = True
        self.behavior.drag_offset = (-10, -10)
        
        event = Mock()
        event.pos = (150, 150)
        
        result = self.behavior.handle_mouse_motion(event)
        
        assert result is True
        self.mock_widget.set_position.assert_called_once_with(140, 140)

    def test_mouse_motion_not_dragging(self):
        self.behavior.is_dragging = False
        
        event = Mock()
        event.pos = (150, 150)
        
        result = self.behavior.handle_mouse_motion(event)
        
        assert result is False
        self.mock_widget.set_position.assert_not_called()

    def test_handle_input_mouse_down(self):
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (110, 110)
        
        result = self.behavior.handle_input(event)
        
        assert result is True
        assert self.behavior.is_dragging is True

    def test_handle_input_mouse_up(self):
        self.behavior.is_dragging = True
        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        
        result = self.behavior.handle_input(event)
        
        assert result is False
        assert self.behavior.is_dragging is False

    def test_handle_input_mouse_motion(self):
        self.behavior.is_dragging = True
        self.behavior.drag_offset = (-10, -10)
        
        event = Mock()
        event.type = pygame.MOUSEMOTION
        event.pos = (150, 150)
        
        result = self.behavior.handle_input(event)
        
        assert result is True
        self.mock_widget.set_position.assert_called_once_with(140, 140)

    def test_handle_input_other_event(self):
        event = Mock()
        event.type = pygame.KEYDOWN
        
        result = self.behavior.handle_input(event)
        
        assert result is False
