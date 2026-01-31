# LMU Telemetry Overlay

Overlay de telemetria em tempo real para Le Mans Ultimate.

---

## 🚀 Quick Start

Novo no projeto? Comece aqui:

- [Instalação](getting-started/installation.md) - Configure seu ambiente
- [Quick Start](getting-started/quick-start.md) - Primeiros passos
- [Configuração](getting-started/configuration.md) - Configure o overlay

## 📚 Documentação

### Getting Started

Primeiros passos com o projeto.

- [Overview](getting-started/index.md)
- [Instalação](getting-started/installation.md)
- [Quick Start](getting-started/quick-start.md)
- [Configuração](getting-started/configuration.md)

### Architecture

Entenda a arquitetura do sistema.

- [Overview](architecture/index.md)
- [Camadas](architecture/layers.md)
- [Design Patterns](architecture/design-patterns.md)
- [Fluxo de Dados](architecture/data-flow.md)

### Guides

Guias práticos para diferentes públicos.

**Desenvolvimento:**
- [Guia de Desenvolvimento](guides/development/index.md)
- [Setup WSL](guides/development/setup-wsl.md)
- [Padrões de Código](guides/development/code-standards.md)
- [Testes](guides/development/testing.md)
- [Contribuindo](guides/development/contributing.md)

**Deploy:**
- [Overview](guides/deployment/index.md)
- [Deploy Windows](guides/deployment/windows.md)
- [Troubleshooting](guides/deployment/troubleshooting.md)
- [Performance](guides/deployment/performance.md)

**Usuário:**
- [Guia do Usuário](guides/user-guide/index.md)
- [Interface](guides/user-guide/interface.md)
- [Customização](guides/user-guide/customization.md)
- [Atalhos](guides/user-guide/keyboard-shortcuts.md)

### API Reference

Referência completa da API.

**Telemetry:**
- [Sistema de Telemetria](api-reference/telemetry/index.md)
- [Providers](api-reference/telemetry/providers.md)
- [Data Models](api-reference/telemetry/data-models.md)
- [Normalização](api-reference/telemetry/normalization.md)

**Widgets:**
- [Sistema de Widgets](api-reference/widgets/index.md)
- [Widget Base](api-reference/widgets/base-widget.md)
- [Speedometer](api-reference/widgets/speedometer.md)
- [Pedals](api-reference/widgets/pedals.md)
- [Steering Wheel](api-reference/widgets/steering-wheel.md)
- [FFB Indicator](api-reference/widgets/ffb-indicator.md)
- [Criando Widgets](api-reference/widgets/creating-widgets.md)

**Configuration:**
- [Sistema de Configuração](api-reference/configuration/index.md)
- [config.json](api-reference/configuration/config-json.md)
- [layout.json](api-reference/configuration/layout-json.md)
- [ConfigManager](api-reference/configuration/config-manager.md)

## 🎯 Características

- **Overlay Transparente**: HUD que não interfere com o jogo
- **Telemetria em Tempo Real**: Speed, RPM, inputs de pedais e volante
- **Indicador de FFB**: Visualização de força do force feedback com detecção de clipping
- **Drag & Drop**: Posicione widgets livremente na tela
- **Persistência**: Layout salvo automaticamente
- **Design Minimalista**: Interface flat UI moderna

## 🛠️ Tecnologias

- Python 3.9+
- Pygame
- pywin32 (Windows)

## 📄 Licença

MIT License
