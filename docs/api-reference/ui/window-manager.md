# Window Manager

O `WindowManager` é responsável por gerenciar a janela da aplicação, abstraindo as especificidades da biblioteca gráfica (Pygame) e do sistema operacional.

## Responsabilidades

- Inicialização do Pygame e da janela.
- Configuração de flags de janela (Border, Transparency, click-through).
- Abstração do loop de eventos.
- Gerenciamento de FPS e atualização de display.

## Interface

```python
class WindowManager:
    def __init__(self, title: str = "LMU Overlay", width: int = 800, height: int = 600):
        """
        Inicializa o gerenciador.
        Args:
            title: Título da janela.
            width: Largura inicial.
            height: Altura inicial.
        """
        ...

    def init(self) -> None:
        """
        Inicializa o subsistema de vídeo e cria a janela.
        Aplica flags específicas de SO (ex: NOFRAME no Windows).
        """
        ...

    def set_transparent(self, transparent: bool) -> None:
        """
        Define o modo de transparência/click-through.
        
        Args:
            transparent: Se True, ativa modo transparente (overlay).
        """
        ...

    def clear(self) -> None:
        """Limpa a tela com cor transparente (0,0,0,0)."""
        ...

    def update_display(self) -> None:
        """Atualiza o display (flip) e mantém o framerate."""
        ...

    def handle_events(self) -> list[pygame.event.Event]:
        """
        Processa e retorna eventos do Pygame.
        Trata automaticamente o evento QUIT.
        """
        ...

    def close(self) -> None:
        """Fecha a janela e encerra o Pygame."""
        ...
```

## Flags de Sistema

- **Windows**: Usa `pygame.NOFRAME` para remover bordas. Transparência via Win32 API (Stub na versão atual).
- **Linux**: Usa `pygame.RESIZABLE` para permitir redimensionamento durante desenvolvimento.
