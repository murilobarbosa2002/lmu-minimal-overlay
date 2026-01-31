# State Management

O sistema de gerenciamento de estados controla o comportamento global da aplicação, permitindo alternar entre modos de operação (ex: execução vs edição).

## Core Components

### StateMachine

O gerenciador central que mantém o rastreamento do estado atual e delega eventos.

```python
class StateMachine:
    def change_state(self, new_state: ApplicationState) -> None:
        """
        Transiciona para um novo estado.
        Chama on_exit() no estado antigo e on_enter() no novo.
        """
        ...

    def handle_input(self, event: pygame.event.Event) -> bool:
        """Delega para o estado atual."""
        ...

    def update(self, data: TelemetryData) -> None:
        """Delega para o estado atual."""
        ...

    def draw(self, surface: pygame.Surface) -> None:
        """Delega para o estado atual."""
        ...
```

### ApplicationState

Classe base abstrata para todos os estados.

```python
class ApplicationState(ABC):
    def __init__(self, context: StateMachine):
        self.context = context

    def on_enter(self) -> None:
        """Chamado ao entrar no estado."""
        pass

    def on_exit(self) -> None:
        """Chamado ao sair do estado."""
        pass

    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        pass

    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
```

## Estados Concretos

### RunningState

Modo padrão de operação.

- **Comportamento**: Atualiza e desenha widgets com dados de telemetria em tempo real.
- **Input**: Repassa eventos para widgets (pode interceptar hotkeys globais).

### EditState

Modo de edição de layout (Planejado/Em Progresso).

- **Comportamento**: Widgets estáticos ou com dados simulados.
- **Input**: Permite selecionar e arrastar widgets.
- **Visual**: Pode desenhar grids ou outlines de seleção.
