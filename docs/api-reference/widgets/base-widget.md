# Widget Base

Classe base abstrata para todos widgets do overlay. Define o contrato de renderização e comportamento.

## Estrutura da Classe

### Atributos

- `x` (int): Posição X na tela.
- `y` (int): Posição Y na tela.
- `width` (int): Largura do widget.
- `height` (int): Altura do widget.
- `rect` (pygame.Rect): Retângulo de colisão e renderização.

### Interface

```python
class Widget(ABC):
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Inicializa o widget.
        
        Args:
            x (int): Posição X inicial.
            y (int): Posição Y inicial.
            width (int): Largura.
            height (int): Altura.
        """
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Renderiza o widget na superfície alvo.
        
        Args:
            surface (pygame.Surface): Superfície do Pygame onde o widget será desenhado.
        """
        pass
    
    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        """
        Atualiza o estado interno do widget baseado nos dados de telemetria.
        
        Args:
            data (TelemetryData): Snapshot mais recente da telemetria.
        """
        pass
    
    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        """
        Processa eventos de entrada (cliques, teclado, etc).
        
        Args:
            event (pygame.event.Event): Evento do Pygame.
            
        Returns:
            bool: True se o evento foi consumido pelo widget, False caso contrário.
        """
        pass
    
    def get_rect(self) -> pygame.Rect:
        """
        Retorna o retângulo de colisão do widget.
        
        Returns:
            pygame.Rect: Retângulo atual (x, y, width, height).
        """
        return self.rect
    
    def set_position(self, x: int, y: int) -> None:
        """
        Atualiza a posição do widget.
        
        Args:
            x (int): Nova posição X.
            y (int): Nova posição Y.
        """
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
```

## Implementação

Todos widgets devem herdar de `Widget` e implementar métodos abstratos.

Veja [Creating Widgets](creating-widgets.md).
