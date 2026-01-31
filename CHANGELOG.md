# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Script `run_windows.bat` com auto-instalação de Python e Chocolatey
- Guia de instalação para Windows (`docs/guides/windows-setup.md`)
- Verificação de ambiente Windows/Linux com fallback robusto
- TelemetryData dataclass com validação de ranges
- Testes unitários para TelemetryData (100% cobertura)
- Teste E2E para TelemetryData
- Agent rule para explicar antes de commit com execução de testes
- Funções de normalização (normalize_byte, normalize_word, denormalize_byte, denormalize_word, clamp)
- Testes unitários para funções de normalização (100% cobertura)
- Teste E2E para funções de normalização
- Interface ITelemetryProvider (ABC)
- Testes unitários para ITelemetryProvider
- MockTelemetryProvider com dados senoidais realistas
- Testes unitários para MockTelemetryProvider (100% cobertura)
- Teste E2E para MockTelemetryProvider
- SharedMemoryProvider (Stub) para estrutura futura de memória compartilhada
- Documentação da estrutura de memória do rFactor 2 / LMU
- Classe abstrata `Widget` (Foundation UI)
- Documentação detalhada da API Widget (atributos e interface)
- Testes unitários para `Widget` (100% cobertura)
- Testes de edge cases para funções de normalização (NaN, Inf, tipos inválidos)
- Sistema de State Management (`StateMachine`, `RunningState`, `EditState`)
- Testes unitários para State Management (100% cobertura)
- `WindowManager` com suporte a configurações específicas de SO e validação
- `main.py` com loop de aplicação integrado
- Documentação do Window Manager
- Widget `Speedometer` funcional com cache de renderização
- Utilitário `FontManager`
- Atualização em `main.py` para exibir o velocímetro
- Refatoração SRP: Criação de `OverlayApp` e limpeza de `main.py`
- Arquitetura SOLID: Reestruturação de `src/core` em `application/services/states`
- Limpeza de Código: Remoção de comentários e docstrings em `src/`

### Fixed
- Layout do Widget Speedometer (sobreposição de marcha/velocidade)
- Sincronização de drag & drop (área de colisão vs visual)
- Tratamento de input no RunningState (bloqueio de interação acidental)
- Compatibilidade de testes com mudanças de lógica (100% pass)
- Script de setup para suportar caminhos UNC (WSL network paths)

### Planejado

- Implementação de ITelemetryProvider
- Implementação de TelemetryData
- Implementação de MockTelemetryProvider
- Implementação de widgets básicos
- Sistema de configuração

## [0.1.0] - 2026-01-31

### Adicionado

- Estrutura inicial do projeto
- Documentação completa em `docs/`
  - Getting Started (instalação, quick start, configuração)
  - Architecture (camadas, design patterns, fluxo de dados)
  - Guides (development, deployment, user guide)
  - API Reference (telemetry, widgets, configuration)
- PRODUCT.md com lógica de negócio
- ROADMAP.md com plano de desenvolvimento (10 fases, ~90 tarefas)
- README.md com overview do projeto
- requirements.txt e requirements-windows.txt
- CONTRIBUTING.md com guia de contribuição
- CHANGELOG.md (este arquivo)
- .gitignore configurado
- Configuração Jekyll para GitHub Pages
- 13 arquivos de rules do Antigravity em `.agent/rules/`

### Estrutura de Documentação

- 40 arquivos Markdown organizados em 4 seções temáticas
- Navegação completa com índices em cada nível
- Links cruzados entre páginas relacionadas
- Toda documentação em português brasileiro

### Commits

- `chore(config): adiciona .gitignore`
- `docs(config): configura Jekyll para GitHub Pages`
- `docs(getting-started): adiciona seção getting started`
- `docs(architecture): adiciona documentação de arquitetura`
- `docs(guides): adiciona guias práticos`
- `docs(api): adiciona referência completa da API`
- `docs(product): adiciona documentação de produto`
- `docs(roadmap): adiciona roadmap detalhado do projeto`

## Tipos de Mudanças

- `Added` - Novas funcionalidades
- `Changed` - Mudanças em funcionalidades existentes
- `Deprecated` - Funcionalidades que serão removidas
- `Removed` - Funcionalidades removidas
- `Fixed` - Correções de bugs
- `Security` - Correções de segurança

[Unreleased]: https://github.com/seu-usuario/lmu-minimal-overlay/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/seu-usuario/lmu-minimal-overlay/releases/tag/v0.1.0
