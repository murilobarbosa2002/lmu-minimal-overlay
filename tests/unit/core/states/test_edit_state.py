import pytest
from unittest.mock import Mock, MagicMock, patch
import pygame
from src.core.application.states.edit_state import EditState

class TestEditState:
    @pytest.fixture
    def edit_state(self):
        context = Mock()
        widgets = []
        return EditState(context, widgets)

    def test_initialization(self, edit_state):
        assert edit_state.widgets == []
        assert edit_state.selected_widget is None

    def test_handle_input_selects_widget(self):
        # Setup
        context = Mock()
        widget1 = Mock()
        widget1.get_rect.return_value = pygame.Rect(0, 0, 100, 100)
        widget2 = Mock()
        widget2.get_rect.return_value = pygame.Rect(200, 0, 100, 100)
        
        state = EditState(context, [widget1, widget2])
        
        # Click on widget 1
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (50, 50)
        
        state.handle_input(event)
        
        assert state.selected_widget == widget1

    def test_handle_input_deselects_clicked_outside(self):
        # Setup
        context = Mock()
        widget1 = Mock()
        widget1.get_rect.return_value = pygame.Rect(0, 0, 100, 100)
        
        state = EditState(context, [widget1])
        state.selected_widget = widget1
        
        # Click outside
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (200, 200)
        
        state.handle_input(event)
        
        assert state.selected_widget is None

    def test_handle_input_delegates_to_widgets(self):
        context = Mock()
        widget = Mock()
        widget.handle_input.return_value = True
        
        state = EditState(context, [widget])
        
        event = MagicMock()
        state.handle_input(event)
        
        widget.handle_input.assert_called_with(event)

    @patch('pygame.draw.rect')
    def test_draw_renders_widgets_and_selection(self, mock_draw_rect):
        context = Mock()
        widget = Mock()
        widget.get_rect.return_value = pygame.Rect(0, 0, 100, 100)
        state = EditState(context, [widget])
        state.selected_widget = widget
        
        surface = Mock()
        
        state.draw(surface)
            
        widget.draw.assert_called_with(surface)
        mock_draw_rect.assert_called_once()

    def test_update_propagates_data_to_widgets(self):
        context = Mock()
        widget = Mock()
        state = EditState(context, [widget])
        
        data = Mock()
        state.update(data)
        
        widget.update.assert_called_with(data)
