# Design Patterns

Patterns utilizados no LMU Telemetry Overlay.

## Composite Pattern

**Problema**: Tratar widgets individuais e grupos de widgets uniformemente.

**Solução**: Todos widgets implementam interface `Widget` comum.

### Implementação

```python
class Widget(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
    
    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        pass
```

Todos widgets (Speedometer, Pedals, etc) herdam de `Widget`.

## Patterns Adicionais (v0.4.0+)

### Dependency Injection

**Injeção de Dependências** com container customizado.

```python
from src.core.infrastructure.di_container import SimpleDIContainer
from src.core.infrastructure.app_factory import AppFactory

# Uso via factory
app = AppFactory.create()  # Todas dependências resolvidas
app.run()
```

**Benefícios:**
- **Testabilidade**: Mock de todas dependências
- **Desacoplamento**: Componentes independentes
- **Configurabilidade**: Fácil trocar implementações

### Strategy Pattern

**Estratégia** para comportamentos específicos de plataforma.

```python
# Diferentes handlers para transparência
class Win32TransparencyHandler:
    def apply_transparency(self, hwnd): ...

class NullTransparencyHandler:
    def apply_transparency(self, hwnd): pass
```

## SOLID Compliance

### Single Responsibility Principle

Cada classe tem uma responsabilidade única:
- `WindowManager`: Gerencia janela
- `Win32TransparencyHandler`: Aplica transparência Windows
- `SpeedometerRenderer`: Renderiza velocímetro

### Open/Closed Principle

Extensível sem modificações:
- Novos `TransparencyHandler` para outras plataformas
- Novos `Widget` sem alterar base

### Liskov Substitution Principle

Implementações substituíveis:
- `MockTelemetryProvider` ↔ `SharedMemoryProvider`
- `Win32TransparencyHandler` ↔ `NullTransparencyHandler`

### Interface Segregation Principle

Interfaces pequenas e focadas:
- `IWindowManager`: Operações de janela
- `IFontProvider`: Operações de fonte
- `ITelemetryProvider`: Operações de telemetria

### Dependency Inversion Principle

Alto nível depende de abstrações:
- `OverlayApp` depende de `IWindowManager`, não de `WindowManager`
- Uso de `AppFactory` para injeção

### Benefícios

- Adicione novos widgets sem modificar código existente
- Trate todos widgets uniformemente no loop de renderização
- Facilita composição de widgets complexos

## State Pattern

**Problema**: Comportamento da aplicação muda drasticamente entre modos.

**Solução**: Estados explícitos (RunningState, EditState).

### Implementação

```python
class ApplicationState(ABC):
    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> None:
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass

class RunningState(ApplicationState):
    def handle_input(self, event):
        pass
    
    def render(self, surface):
        pass

class EditState(ApplicationState):
    def handle_input(self, event):
        pass
    
    def render(self, surface):
        pass
```

### Estados

**RunningState**:
- Overlay transparente
- Click-through (não captura mouse)
- Apenas visualização

**EditState**:
- Fundo visível
- Captura mouse
- Permite drag & drop

### Transições

```python
if event.key == pygame.K_F1:
    if isinstance(current_state, RunningState):
        current_state = EditState()
    else:
        current_state = RunningState()
```

## Singleton Pattern

**Problema**: Configurações devem ser únicas e globalmente acessíveis.

**Solução**: ConfigManager como singleton.

### Implementação

```python
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        pass
```

### Uso

```python
config = ConfigManager()
colors = config.get_colors()
```

### Benefícios

- Configurações carregadas uma vez
- Acesso global sem variáveis globais
- Facilita testes com mock

## Adapter Pattern

**Problema**: Diferentes fontes de dados (memória, mock, rede).

**Solução**: Interface `ITelemetryProvider` abstrai fonte.

### Implementação

```python
class ITelemetryProvider(ABC):
    @abstractmethod
    def get_data(self) -> TelemetryData:
        pass

class SharedMemoryProvider(ITelemetryProvider):
    def get_data(self) -> TelemetryData:
        return self._read_from_memory()

class MockTelemetryProvider(ITelemetryProvider):
    def get_data(self) -> TelemetryData:
        return self._generate_fake_data()
```

### Benefícios

- UI não sabe fonte de dados
- Troque provider sem alterar UI
- Teste UI com dados mockados

## Observer Pattern (Futuro)

**Problema**: Polling constante é ineficiente.

**Solução**: Provider notifica quando novos dados disponíveis.

### Implementação Futura

```python
class ITelemetryProvider(ABC):
    def subscribe(self, observer: Callable[[TelemetryData], None]) -> None:
        pass
    
    def notify(self, data: TelemetryData) -> None:
        for observer in self.observers:
            observer(data)
```

Atualmente usa polling no loop principal.

## Dependency Injection

**Problema**: Acoplamento entre componentes.

**Solução**: Injetar dependências via construtor.

### Implementação

```python
class Application:
    def __init__(self, provider: ITelemetryProvider, config: ConfigManager):
        self.provider = provider
        self.config = config
```

### Benefícios

- Facilita testes com mocks
- Reduz acoplamento
- Melhora flexibilidade

## Factory Pattern

**Problema**: Criação complexa de widgets.

**Solução**: Factory para criar widgets baseado em configuração.

### Implementação

```python
class WidgetFactory:
    @staticmethod
    def create(widget_config: dict) -> Widget:
        widget_type = widget_config["type"]
        if widget_type == "Speedometer":
            return Speedometer(widget_config["x"], widget_config["y"])
        elif widget_type == "Pedals":
            return Pedals(widget_config["x"], widget_config["y"])
```

### Benefícios

- Centraliza lógica de criação
- Facilita adicionar novos tipos
- Carrega widgets de JSON facilmente

## Resumo

| Pattern | Onde Usado | Benefício |
|---------|------------|-----------|
| Composite | Widgets | Uniformidade |
| State | Modos da aplicação | Comportamento claro |
| Singleton | ConfigManager | Acesso global |
| Adapter | TelemetryProvider | Abstração de fonte |
| Dependency Injection | Application | Desacoplamento |
| Factory | Widget creation | Criação centralizada |

## Próximos Passos

- [Fluxo de Dados](data-flow.md) - Como dados fluem
- [Camadas](layers.md) - Onde patterns são aplicados
- [API Reference](../api-reference/widgets/index.md) - Implementações
