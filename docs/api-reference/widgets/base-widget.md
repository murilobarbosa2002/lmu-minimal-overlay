# Widget Base

Classe base abstrata para todos widgets.

## Interface

```python
class Widget(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Renderiza widget na surface."""
        pass
    
    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        """Atualiza estado com novos dados."""
        pass
    
    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Processa input. Retorna True se consumiu evento."""
        pass
    
    def get_rect(self) -> pygame.Rect:
        """Retorna retângulo de colisão."""
        pass
    
    def set_position(self, x: int, y: int) -> None:
        """Define posição do widget."""
        pass
```

## Implementação

Todos widgets devem herdar de `Widget` e implementar métodos abstratos.

Veja [Creating Widgets](creating-widgets.md).
