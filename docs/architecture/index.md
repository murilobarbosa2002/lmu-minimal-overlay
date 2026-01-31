# Arquitetura

Entenda a arquitetura do LMU Telemetry Overlay.

## Visão Geral

O sistema é organizado em **4 camadas distintas** seguindo princípios **SOLID** e **Clean Architecture**:

> **Nota (v0.4.0+)**: Arquitetura refatorada com Dependency Injection, SOLID compliance, e separação de concerns. Veja [Design Patterns](design-patterns.md) para detalhes.

```
┌─────────────────────────────────────┐
│   Presentation Layer (UI)          │
│   - Pygame rendering                │
│   - Window management               │
│   - Widget system                   │
│   - Behaviors (Draggable)           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Application Layer                 │
│   - State management                │
│   - Input handling                  │
│   - Service orchestration           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Domain Layer (Core Logic)         │
│   - TelemetryData dataclass         │
│   - Normalization logic             │
│   - Unit conversion                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Infrastructure Layer              │
│   - Dependency Injection            │
│   - ITelemetryProvider interface    │
│   - Platform handlers               │
│   - SharedMemory / Mock providers   │
└─────────────────────────────────────┘
```

## Princípios Arquiteturais

### Separação de Responsabilidades

Cada camada tem responsabilidade única e bem definida.

### Desacoplamento

Camadas conhecem apenas interfaces, nunca implementações concretas.

### Inversão de Dependência

Camadas superiores dependem de abstrações, não de detalhes.

### Testabilidade

Cada camada pode ser testada isoladamente com mocks.

## Navegação

- [**Camadas**](layers.md) - Detalhamento das 3 camadas
- [**Design Patterns**](design-patterns.md) - Patterns utilizados
- [**Fluxo de Dados**](data-flow.md) - Como dados fluem pelo sistema

## Benefícios da Arquitetura

### Manutenibilidade

Código organizado e fácil de entender.

### Extensibilidade

Adicione novos widgets sem modificar core.

### Testabilidade

Teste UI sem o jogo rodando (MockProvider).

### Portabilidade

Troque implementações sem afetar outras camadas.

## Estrutura de Diretórios

## Estrutura de Diretórios

```
src/
├── main.py (entry point)
├── core/
│   ├── app.py (Application Orchestrator)
│   ├── application/ (Layer 2b: Application Services)
│   │   ├── services/ (StateMachine, InputHandler)
│   │   ├── states/ (RunningState, EditState)
│   │   └── interfaces/ (IApplicationState)
│   ├── domain/ (Layer 2a: Domain Logic)
│   │   ├── telemetry_data.py
│   │   └── normalize.py
│   └── providers/ (Layer 1: Infrastructure)
│       ├── i_telemetry_provider.py
│       ├── mock_telemetry_provider.py
│       └── shared_memory_provider.py
└── ui/ (Layer 3: Presentation)
    ├── window.py (WindowManager)
    ├── utils/ (Fonts)
    ├── rendering/
    │   ├── dashboard_card_renderer.py
    │   └── components/ (Bar, IndicatorBars, etc.)
    └── widgets/ (DashboardCard, etc.)
```

## Próximos Passos

- [Camadas](layers.md) - Entenda cada camada em detalhes
- [Design Patterns](design-patterns.md) - Patterns implementados
- [Fluxo de Dados](data-flow.md) - Trace o fluxo de dados
