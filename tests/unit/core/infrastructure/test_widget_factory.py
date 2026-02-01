import pytest
from src.ui.factories.widget_factory import WidgetFactory
from src.ui.widgets.dashboard_card import DashboardCard
from src.ui.widgets.widget import Widget


def test_widget_factory_initialization():
    factory = WidgetFactory()
    assert factory is not None
    assert hasattr(factory, '_registry')


def test_default_widgets_registered():
    factory = WidgetFactory()
    widget_data = {"type": "DashboardCard", "x": 100, "y": 200}
    widget = factory.create_widget(widget_data)
    
    assert isinstance(widget, DashboardCard)
    assert widget.x == 100
    assert widget.y == 200


def test_create_widget_with_all_parameters():
    factory = WidgetFactory()
    widget_data = {
        "type": "DashboardCard",
        "x": 500,
        "y": 300,
        "width": 400,
        "height": 150
    }
    widget = factory.create_widget(widget_data)
    
    assert widget.x == 500
    assert widget.y == 300
    assert widget.width == 400
    assert widget.height == 150


def test_create_widget_with_default_values():
    factory = WidgetFactory()
    widget_data = {"type": "DashboardCard"}
    widget = factory.create_widget(widget_data)
    
    assert widget.x == 0
    assert widget.y == 0
    assert widget.width == 350
    assert widget.height == 130


def test_unknown_widget_type_raises_error():
    factory = WidgetFactory()
    widget_data = {"type": "UnknownWidget"}
    
    with pytest.raises(ValueError, match="Unknown widget type: UnknownWidget"):
        factory.create_widget(widget_data)


def test_register_custom_widget():
    class CustomWidget(Widget):
        def __init__(self, position_x=0, position_y=0, width=100, height=100):
            super().__init__(x, y, width, height)
        
        def draw(self, surface):
            pass
        
        def update(self, data):
            pass
        
        def handle_input(self, event):
            pass
    
    factory = WidgetFactory()
    factory.register("CustomWidget", CustomWidget)
    
    widget_data = {"type": "CustomWidget", "x": 50, "y": 75}
    widget = factory.create_widget(widget_data)
    
    assert isinstance(widget, CustomWidget)
    assert widget.x == 50
    assert widget.y == 75
