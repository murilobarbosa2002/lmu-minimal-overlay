# Camadas da Arquitetura

Detalhamento das 3 camadas do sistema.

## Layer 1: Infrastructure

Responsável pela aquisição de dados do jogo.

### Responsabilidades

- Interagir com API do Windows
- Ler memória compartilhada (mmap)
- Fornecer dados mockados para desenvolvimento
- Abstrair fonte de dados

### Componentes

#### ITelemetryProvider (Interface)

Contrato abstrato para providers:

```python
from abc import ABC, abstractmethod

class ITelemetryProvider(ABC):
    @abstractmethod
    def get_data(self) -> TelemetryData:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
```

#### SharedMemoryProvider

Implementação para Windows:
- Acessa memória compartilhada do Le Mans Ultimate
- Lê estrutura binária do jogo
- Converte para `TelemetryData`

#### MockTelemetryProvider

Implementação para WSL/desenvolvimento:
- Gera dados senoidais fake
- Simula comportamento realista
- Permite desenvolver sem o jogo

### Arquivos

```
infra/
├── __init__.py
├── memory_reader.py (SharedMemoryProvider)
└── mock_provider.py (MockTelemetryProvider)
```

## Layer 2: Domain

Contém lógica de negócio e modelos de dados.

### Responsabilidades

- Definir modelos de dados
- Normalizar valores raw
- Gerenciar estados da aplicação
- Lógica de negócio pura

### Componentes

#### TelemetryData

Dataclass tipada representando estado do veículo:

```python
from dataclasses import dataclass

@dataclass
class TelemetryData:
    speed: float
    rpm: int
    throttle_pct: float
    brake_pct: float
    clutch_pct: float
    steering_angle: float
    ffb_level: float
    gear: int
    timestamp: float
```

#### Normalização

Funções para converter valores raw:

```python
def normalize_input(raw: int) -> float:
    return raw / 255.0

def normalize_rpm(rpm: int, max_rpm: int = 10000) -> float:
    return min(rpm / max_rpm, 1.0)
```

#### State Management

Gerencia estados da aplicação (Running, Edit).

### Arquivos

```
core/
├── __init__.py
├── telemetry.py (ITelemetryProvider, TelemetryData)
├── normalization.py (funções de normalização)
└── state.py (RunningState, EditState)
```

## Layer 3: Presentation

Gerencia renderização e interação com usuário.

### Responsabilidades

- Renderizar widgets com Pygame
- Gerenciar janela e transparência
- Capturar inputs do usuário
- Drag & drop de widgets

### Componentes

#### Window Manager

Controla janela e transparência:
- pywin32 para transparência no Windows
- Click-through no modo Running
- Captura mouse no modo Edit

#### Widget System

Todos widgets herdam de `Widget` base:

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
```

Widgets disponíveis:
- **Speedometer**: Velocidade e marcha
- **Pedals**: Throttle, brake, clutch
- **SteeringWheel**: Ângulo do volante
- **FFBIndicator**: Force feedback com clipping

#### States

Implementa State Pattern:
- **RunningState**: Overlay transparente, click-through
- **EditState**: Fundo visível, drag & drop

### Arquivos

```
ui/
├── __init__.py
├── window_manager.py
├── states.py
└── widgets/
    ├── __init__.py
    ├── base.py (Widget base)
    ├── speedometer.py
    ├── pedals.py
    ├── steering_wheel.py
    └── ffb_indicator.py
```

## Comunicação Entre Camadas

### Layer 1 → Layer 2

```python
provider: ITelemetryProvider = get_provider()
data: TelemetryData = provider.get_data()
```

Infrastructure fornece dados para Domain.

### Layer 2 → Layer 3

```python
for widget in widgets:
    widget.update(data)
```

Domain fornece dados normalizados para Presentation.

### Isolamento

Camadas **não** conhecem detalhes de implementação:
- UI não sabe se dados vêm de memória ou mock
- Domain não sabe como dados são renderizados
- Infrastructure não sabe o que será feito com dados

## Benefícios

### Testabilidade

Teste cada camada isoladamente:

```python
def test_widget_update():
    widget = Speedometer(0, 0)
    data = TelemetryData(speed=100.0, ...)
    widget.update(data)
    assert widget.current_speed == 100.0
```

### Extensibilidade

Adicione novo provider sem alterar UI:

```python
class NetworkTelemetryProvider(ITelemetryProvider):
    def get_data(self) -> TelemetryData:
        return fetch_from_network()
```

### Manutenibilidade

Cada camada tem responsabilidade clara e única.

## Próximos Passos

- [Design Patterns](design-patterns.md) - Patterns implementados
- [Fluxo de Dados](data-flow.md) - Trace o fluxo completo
- [API Reference](../api-reference/telemetry/index.md) - Referência detalhada
