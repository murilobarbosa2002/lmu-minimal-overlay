# Criando Widgets

Tutorial para criar novos widgets.

## Passo 1: Criar Arquivo

```python
# ui/widgets/meu_widget.py
from ui.widgets.base import Widget
from core.telemetry import TelemetryData
import pygame

class MeuWidget(Widget):
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 100, 50)
    
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
    
    def update(self, data: TelemetryData) -> None:
        pass
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False
    
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def set_position(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y
```

## Passo 2: Registrar

```python
# ui/widgets/__init__.py
from .meu_widget import MeuWidget
```

## Passo 3: Adicionar ao Layout

```json
{
  "widgets": [
    {
      "id": "meu_widget",
      "type": "MeuWidget",
      "x": 100,
      "y": 100
    }
  ]
}
```

Veja [Widget Base](base-widget.md).
