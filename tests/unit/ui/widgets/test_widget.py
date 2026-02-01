import pytest
import pygame
from src.ui.widgets.widget import Widget
from src.core.domain.telemetry_data import TelemetryData

# Initialize pygame for Rect operations
pygame.init()

def test_cannot_instantiate_widget():
    """Abstract Widget class cannot be instantiated directly"""
    with pytest.raises(TypeError):
        Widget(0, 0, 100, 100)

def test_concrete_widget_implementation():
    """Concrete implementation of Widget works correctly"""
    
    class ConcreteWidget(Widget):
        def draw(self, surface: pygame.Surface) -> None:
            pass
            
        def update(self, data: TelemetryData) -> None:
            pass
            
        def handle_input(self, event: pygame.event.Event) -> bool:
            return False
            
    widget = ConcreteWidget(10, 20, 100, 50)
    
    assert isinstance(widget, Widget)
    assert widget.position_x == 10
    assert widget.position_y == 20
    assert widget.width == 100
    assert widget.height == 50
    assert widget.rect == pygame.Rect(10, 20, 100, 50)

def test_widget_positioning():
    """Test set_position updates coordinates and rect"""
    
    class MovableWidget(Widget):
        def draw(self, surface): pass
        def update(self, data): pass
        def handle_input(self, event): return False
        
    widget = MovableWidget(0, 0, 50, 50)
    widget.set_position(100, 100)
    
    assert widget.position_x == 100
    assert widget.position_y == 100
    assert widget.rect.x == 100
    assert widget.rect.y == 100
    assert widget.get_rect() == widget.rect
