# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Changed
- **Config System**: Implemented full configuration management system (`ConfigManager`).
- **Persistence**: Window position, size, and widget layout are now persisted in `config.json` and `layout.json`.
- **UI**: DashboardCard background updated to deep blue for better aesthetics.
- **Maintenance**: Strict code cleanup - removed all comments and docstrings from `src/` directory.
- **Tests**: Achieved 100% test coverage across all codebase.

### Added
- `src/core/infrastructure/config_manager.py`: Singleton configuration manager.
- `src/core/interfaces/i_config_manager.py`: Interface for config manager.
- Unit tests for Config System.
- `docs/testing/unit-testing.md`: Documentation on testing standards.

### Fixed
- **Fonts**: Fixed "Passed a NULL pointer" error on Wine/Proton by using `io.BytesIO` streams for font loading.
- **Fonts**: Suppressed Pygame welcome message at startup.
- **Fixed**: Reddish tint in DashboardCard gradient.
- **Config**: ConfigManager handles missing or corrupted JSON files gracefully.

### Added
- `src/core/infrastructure/config_manager.py`: Singleton configuration manager.
- `src/core/interfaces/i_config_manager.py`: Interface for config manager.
- `tests/unit/ui/utils/test_fonts.py`: Comprehensive tests for FontManager static class (100% coverage).
- Unit tests for Config System.
- `docs/testing/unit-testing.md`: Documentation on testing standards.
- **BREAKING**: Removed `Pedals` widget (functionality integrated into `DashboardCard`)
- **BREAKING**: `OverlayApp` now requires dependencies via constructor injection (use `AppFactory.create()` instead of direct instantiation)
- **Architecture**: Comprehensive SOLID and Clean Architecture refactoring
- **Layout**: New compact DashboardCard (350px width) with symmetric spacing (20px) and gradient background (95% opacity)
- **Architecture**: Comprehensive SOLID and Clean Architecture refactoring across 5 phases
  - Implemented dependency injection container (`SimpleDIContainer`)
  - Extracted interfaces: `IWindowManager`, `IFontProvider`, `ITelemetryProvider`
  - Created platform-specific handlers (`Win32TransparencyHandler`, `NullTransparencyHandler`)
  - Extracted Speedometer components: `SpeedometerRenderer`, `DraggableBehavior`, `unit_converter`
  - Removed singleton pattern from `FontManager`, replaced with injectable `PygameFontProvider`
  - Created `AppFactory` for dependency wiring
- Removed all comments from production code (maintained only in tests and docs)

### Added
- `src/core/infrastructure/di_container.py`: Dependency injection container
- `src/core/infrastructure/app_factory.py`: Application factory for DI wiring
- `src/ui/interfaces/`: Interface definitions (IWindowManager, IFontProvider)
- `src/ui/platform/transparency_handler.py`: Platform-specific transparency handling
- `src/ui/behaviors/draggable.py`: Reusable drag-and-drop behavior
- `src/ui/rendering/speedometer_renderer.py`: Speedometer visual rendering
- `src/core/domain/unit_converter.py`: Pure unit conversion functions
- `src/ui/utils/pygame_font_provider.py`: Injectable font provider
- 44 new comprehensive tests (100% coverage for new modules)

### Fixed
- Test coverage improved from 98% to 99% (144 tests passing)
- Window property access in tests (changed from direct `surface` to `_surface`)

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

## [0.3.1] - Unreleased

### Added
- **UI**: Full Drag & Drop system with visual feedback (transparency change when dragging).
- **Control**: Toggle Edit Mode with `F1`.
- **Integration**: Comprehensive integration tests for drag & drop flow and persistence.
- **Assets**: Reference images for original LMU HUD (`src/assets/images/hud-default-lmu*.png`).
- **Roadmap**: Completed Phase 4 (Drag & Drop) and added Phase 5 (HUD Expansion).
- **Visuals**: Premium editing visuals:
  - **Selection**: Cyan rounded border with **dynamic breathing animation** (pulsing padding).
  - **Dragging**: Card becomes semi-transparent (180/255 opacity).

### Fixed
- **Edit Mode**: Widgets now continue to update/render telemetry data while in Edit Mode (previously paused).
- **Tests**: Achieved 100% test coverage including new integration tests and edge cases for DashboardCard.
- **Roadmap**: Detailed plan for `InputCard` refactoring and new widgets.

## [0.3.0] - 2026-01-31

### Added
- **Window**: Always-on-top functionality for Windows (`SetWindowPos` with `HWND_TOPMOST`) and Linux (`SDL_VIDEO_WINDOW_ALWAYS_ON_TOP`).
- **Tests**: Added `test_physics_engine_corner_entry` to achieve 100% coverage on physics engine.

### Changed
- **Physics**: Implemented "Human Hand" steering model with rate limiting (max 2.5 units/second).
- **Physics**: Refined damping using exponential moving average for smoother, more realistic steering.
- **Physics**: Micro-corrections now only activate under high load (Speed > 40 + Steering > 0.1).
- **Config**: Added `layout.json` to `.gitignore` (user-specific window positions).

### Fixed
- **Physics**: Eliminated unrealistic "full rotation" on initialization.
- **Tests**: Updated `test_window_init_windows_os` to include `SetWindowPos` mock verification.

## [0.2.0] - 2026-01-31

### Added
- **Visuals**: Support for custom steering wheel image (`src/assets/images/wheel-mockup.png`).
- **UI**: Percentage values added to the top of Throttle, Brake, and FFB bars (Size 16, Bold).

### Changed
- **Physics**: Improved steering simulation with reduced jitter, micro-corrections, and exponential smoothing.
- **Visuals**: Implemented `rotozoom` for high-quality, anti-aliased steering wheel rotation.
- **Visuals**: Increased Steering Indicator size (Radius 45px).
- **Layout**: Centered Speed and Gear display perfectly (Vertically and Horizontally) within the DashboardCard.
- **Layout**: Moved Indicator Bar labels (T, B, F) to the bottom for better readability.
- **Layout**: Standardized vertical spacing (5px gaps) for Indicator Bars.

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
