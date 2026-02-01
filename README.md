# LMU Telemetry Overlay

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Overlay de telemetria em tempo real para Le Mans Ultimate. HUD transparente que exibe dados de telemetria e inputs sem interferir na experiência de corrida.

![LMU Telemetry Overlay](docs/assets/screenshot-placeholder.png)
![LMU Telemetry Overlay](docs/assets/screenshot-placeholder.png)
> *Screenshot: DashboardCard integrado com volante, velocidade/marcha e barras de input*

## 🎯 Características

- **Overlay Transparente**: HUD que não interfere com o jogo
- **Telemetria em Tempo Real**: Speed, RPM, inputs de pedais e volante (60 Hz)
- **Display de RPM**: Exibição realista de RPM com simulação baseada em relações de marcha
- **Indicador de FFB**: Visualização de força do force feedback com detecção de clipping
- **Zero Magic Numbers**: 66+ constantes em `constants.py`, todos os valores configuráveis
- **100% Configurável**: Todos os parâmetros visuais e físicos via `config.json`
- **Física Configurável**: Relações de marcha, final drive, RPM limits personalizáveis
- **Suporte Multi-Carro**: Configure diferentes tipos de carro (LMP2, GT3, F1)
- **Sistema de Temas**: Crie temas personalizados modificando cores, dimensões e estilos
- **Drag & Drop**: Posicione widgets livremente na tela
- **Persistência**: Layout e configurações salvos automaticamente
- **Design Minimalista**: Interface flat UI moderna
- **Desenvolvimento WSL**: Funciona sem o jogo usando dados mockados
- **100% Test Coverage**: 217 testes unitários e de integração
- **Agent Rules**: Políticas de código documentadas em `.agent/rules.md`

## 🚀 Quick Start

### Desenvolvimento (WSL)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/lmu-minimal-overlay.git
cd lmu-minimal-overlay

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Execute
python main.py
```

### Produção (Windows)

```bash
# Instale dependências Windows
pip install -r requirements-windows.txt

# Execute
python main.py
```

**Nota**: Le Mans Ultimate deve estar rodando para telemetria real.

## 📋 Requisitos

- **Python 3.9+**
- **Pygame** para renderização
- **pywin32** (apenas Windows) para transparência
- **Le Mans Ultimate** (para produção)

## 📚 Documentação

Documentação completa disponível em [GitHub Pages](https://murilobarbosa2002.github.io/lmu-minimal-overlay/getting-started/installation.html):

- [**Getting Started**](docs/getting-started/index.md) - Instalação e primeiros passos
- [**Architecture**](docs/architecture/index.md) - Arquitetura e design patterns
- [**Guides**](docs/guides/index.md) - Guias de desenvolvimento, deploy e uso
- [**API Reference**](docs/api-reference/index.md) - Referência completa da API
- [**PRODUCT.md**](docs/PRODUCT.md) - Lógica de negócio e produto
- [**ROADMAP.md**](ROADMAP.md) - Roadmap de desenvolvimento

## 🎮 Widgets Disponíveis

| Widget | Descrição | Dados |
|--------|-----------|-------|
| **DashboardCard** | Dashboard compacto integrado | Speed, RPM, Gear, Steering, Throttle, Brake, FFB |
|--------|-----------|-------|
| **DashboardCard** | Card principal integrado | Speed, Gear, Steering, Pedals, FFB |
| **FPS Counter** | Contador de quadros | FPS atual |

## ⌨️ Atalhos

| Atalho | Ação |
|--------|------|
| `F1` | Alternar entre modo Running e Edit |
| `F2` | Mostrar/ocultar FPS counter |
| `ESC` | Fechar overlay |

## 🏗️ Arquitetura

Sistema organizado em **3 camadas** seguindo princípios **SOLID** e **Clean Code**:

```
┌─────────────────────────────────────┐
│   Layer 3: Presentation (UI)       │
│   - Pygame rendering                │
│   - Widget system                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Layer 2: Domain (Core Logic)     │
│   - TelemetryData                   │
│   - Normalization                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Layer 1: Infrastructure           │
│   - ITelemetryProvider              │
│   - SharedMemory / Mock             │
└─────────────────────────────────────┘
```

**Design Patterns**: Composite, State, Singleton, Adapter

Veja [Architecture](docs/architecture/index.md) para detalhes.

## 🛠️ Desenvolvimento

### Setup

```bash
# WSL/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure X Server para Pygame
export DISPLAY=:0
```

### Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=.

# Validar código
mypy .
black .
flake8 .
```

### Padrões de Código

- **Type Hints**: Obrigatório em todas funções
- **Docstrings**: Google Style em português
- **Formatação**: PEP 8, Black, isort
- **Commits**: Padrão Commitizen em português

Veja [Development Guide](docs/guides/development/index.md).

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

### Workflow

1. Fork o repositório
2. Crie branch (`git checkout -b feat/nova-feature`)
3. Commit (padrão Commitizen): `git commit -m "feat(widgets): adiciona widget de temperatura"`
4. Push (`git push origin feat/nova-feature`)
5. Abra Pull Request

## 📝 Roadmap

Veja [ROADMAP.md](ROADMAP.md) para plano completo de desenvolvimento.

**Status Atual**: Fase 3 - Configuração (Completo)

**Próximas Fases**:
- Fase 4: Integração (Em progresso)
- Fase 5: Produção Windows
- Fase 6: Otimizações e Performance

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Comunidade Le Mans Ultimate
- Desenvolvedores de overlays de simuladores
- Contribuidores do projeto

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/lmu-minimal-overlay/issues)
- **Documentação**: [GitHub Pages](https://seu-usuario.github.io/lmu-minimal-overlay/)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/lmu-minimal-overlay/discussions)

---

**Desenvolvido com ❤️ para a comunidade de sim racing**
