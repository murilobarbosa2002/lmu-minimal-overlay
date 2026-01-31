# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

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
