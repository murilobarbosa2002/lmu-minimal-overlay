from typing import Dict, Type
from src.ui.widgets.widget import Widget
from src.ui.widgets.input_card import InputCard


class WidgetFactory:
    def __init__(self):
        self._registry: Dict[str, Type[Widget]] = {}
        self._register_default_widgets()

    def _register_default_widgets(self) -> None:
        self.register("InputCard", InputCard)

    def register(self, widget_type: str, widget_class: Type[Widget]) -> None:
        self._registry[widget_type] = widget_class

    def create_widget(self, widget_data: dict) -> Widget:
        widget_type = widget_data.get("type")

        if widget_type not in self._registry:
            raise ValueError(f"Unknown widget type: {widget_type}")

        widget_class = self._registry[widget_type]

        position_x = widget_data.get("position_x", 0)
        position_y = widget_data.get("position_y", 0)
        width = widget_data.get("width", 350)
        height = widget_data.get("height", 130)

        return widget_class(
            position_x=position_x, position_y=position_y, width=width, height=height
        )
