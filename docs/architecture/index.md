# Arquitetura

Entenda a arquitetura do LMU Telemetry Overlay.

## Visão Geral

O sistema é organizado em **3 camadas distintas** seguindo princípios **SOLID** e **Clean Code**:

```
┌─────────────────────────────────────┐
│   Layer 3: Presentation (UI)       │
│   - Pygame rendering                │
│   - Window management               │
│   - Widget system                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Layer 2: Domain (Core Logic)     │
│   - TelemetryData dataclass         │
│   - Normalization logic             │
│   - State management                │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Layer 1: Infrastructure           │
│   - ITelemetryProvider interface    │
│   - SharedMemoryProvider (Windows)  │
│   - MockTelemetryProvider (WSL)     │
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

```
lmu-minimal-overlay/
├── main.py (entry point)
├── core/ (Layer 2: Domain)
│   ├── telemetry.py
│   ├── normalization.py
│   └── state.py
├── infra/ (Layer 1: Infrastructure)
│   ├── memory_reader.py
│   └── mock_provider.py
└── ui/ (Layer 3: Presentation)
    ├── window_manager.py
    ├── states.py
    └── widgets/
```

## Próximos Passos

- [Camadas](layers.md) - Entenda cada camada em detalhes
- [Design Patterns](design-patterns.md) - Patterns implementados
- [Fluxo de Dados](data-flow.md) - Trace o fluxo de dados
