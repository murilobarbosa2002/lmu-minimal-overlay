# Sistema de Widgets

API de componentes visuais.

## Componentes

- [Widget Base](base-widget.md) - Classe base abstrata
- [Speedometer](speedometer.md) - Velocímetro
- [Pedals](pedals.md) - Pedais
- [Steering Wheel](steering-wheel.md) - Volante
- [FFB Indicator](ffb-indicator.md) - Indicador FFB
- [Criando Widgets](creating-widgets.md) - Tutorial

## Widget Base

```python
class Widget(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
    
    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        pass
    
    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        pass
    
    def get_rect(self) -> pygame.Rect:
        pass
    
    def set_position(self, x: int, y: int) -> None:
        pass
```

## Widgets Disponíveis

- **Speedometer**: Velocidade e marcha
- **Pedals**: Throttle, brake, clutch
- **SteeringWheel**: Ângulo do volante
- **FFBIndicator**: Force feedback

## Próximos Passos

- [Widget Base](base-widget.md)
- [Criando Widgets](creating-widgets.md)
