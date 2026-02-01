# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [0.6.0] - 2026-02-01

### Adicionado
- **Display de RPM**: RPM agora exibido abaixo da velocidade com fonte e cor configuráveis
- **Simulação Realista de RPM**: Cálculo baseado em relações de marcha estilo LMP2
- **Física Configurável**: Todas as constantes de física agora em `config.json`
- **RPMCalculator**: Nova classe de domínio para cálculo de RPM reutilizável
- **Suporte Multi-Carro**: Configuração permite diferentes tipos de carro (LMP2, GT3, F1)

### Modificado
- **Volante Maior**: Raio aumentado de 45px para 60px (33% maior)
- **PhysicsEngine**: Refatorado para usar RPMCalculator e carregar configuração
- **Arquitetura**: Melhor separação de responsabilidades (SRP)

### Técnico
- **100% Coverage**: Alcançado 100% de cobertura de testes (217 testes)
- **Código Limpo**: Removido diretório vazio `/src/infra`
- **Performance**: Limpeza de `__pycache__` do repositório

---

## [0.5.0] - 2026-02-01

### Adicionado
- **Configuração Completa**: Sistema de configuração centralizado consolidado
- **Guia de Configuração**: Documentação completa em `configuration-complete.md`

### Corrigido
- **Opacidade**: Correção no tratamento de opacidade em componentes de renderização
- **Config Duplicado**: Consolidação de arquivos de configuração duplicados

---

## [Unreleased]

### Changed - Centralização Completa de Configuração (2026-02-01)

#### **Zero Valores Hardcoded Alcançado** 🎯
- **Refatoração Completa**: Eliminados TODOS os 31+ valores hardcoded do código de produção
- **100% Configurável**: Todos os parâmetros visuais agora controlados via `config.json`
- **Sistema de Temas Pronto**: Suporte completo para esquemas de cores e presets visuais personalizados

#### **Schema Estendido do ConfigManager**
- Adicionada seção `window`: título, dimensões padrão
- Adicionado tema `steering_indicator`: cores (aro, marcador, centro), raio, parâmetros de marcação
- Adicionado tema `bar`: dimensões, cores, padding, tamanhos de fonte, border radius
- Adicionado tema `indicator_bars`: espaçamento, cores throttle/brake/FFB
- Adicionado tema `edit_mode`: cor de seleção, propriedades de borda, ranges de animação
- Aprimorado tema `dashboard_card`: cores de borda, cor de máscara, padding lateral

#### **Refatoração de Componentes** (6 componentes, 31+ valores)
1. **SteeringIndicator** (7 valores)
   - Cores: aro, marcador, centro
   - Dimensões: raio
   - Ranges de marcação: início, fim, passo
   
2. **Bar** (8 valores)
   - Dimensões: largura, altura
   - Cores: fundo, linha central
   - Estilo: border_radius, padding
   - Fontes: tamanho do valor, tamanho do label

3. **IndicatorBars** (4 valores)
   - Layout: espaçamento
   - Cores: throttle, brake, FFB

4. **DashboardCardRenderer** (4 valores)
   - Estilo: border_radius, lateral_padding
   - Cores: border_color, mask_color

5. **EditState** (5 valores)
   - Cores: selection_color
   - Estilo: border_width, border_radius
   - Animação: padding_min, padding_max

6. **WindowManager** (3 valores)
   - Janela: título, largura_padrão, altura_padrão

### Changed - Atualizações Anteriores
- **Sistema de Configuração**: Implementado sistema completo de gerenciamento de configuração (`ConfigManager`).
- **Persistência**: Posição da janela, tamanho e layout de widgets agora persistidos em `config.json` e `layout.json`.
- **UI**: Background do DashboardCard atualizado para azul profundo para melhor estética.
- **Manutenção**: Limpeza rigorosa de código - removidos todos comentários e docstrings do diretório `src/`.
- **Testes**: Alcançada cobertura de 100% em toda a base de código.

### Added
- `src/core/infrastructure/config_manager.py`: Gerenciador de configuração singleton.
- `src/core/interfaces/i_config_manager.py`: Interface para gerenciador de configuração.
- Testes unitários para Sistema de Configuração.
- `docs/testing/unit-testing.md`: Documentação sobre padrões de testes.
- `docs/guides/user-guide/configuration-complete.md`: Guia completo de configuração.

### Fixed
- **Fontes**: Corrigido erro "Passed a NULL pointer" no Wine/Proton usando streams `io.BytesIO` para carregamento de fontes.
- **Fontes**: Suprimida mensagem de boas-vindas do Pygame na inicialização.
- **Corrigido**: Tonalidade avermelhada no gradiente do DashboardCard.
- **Config**: ConfigManager trata arquivos JSON ausentes ou corrompidos graciosamente.

### Added (Continuação)
- `src/core/infrastructure/config_manager.py`: Gerenciador de configuração singleton.
- `src/core/interfaces/i_config_manager.py`: Interface para gerenciador de configuração.
- `tests/unit/ui/utils/test_fonts.py`: Testes abrangentes para classe estática FontManager (100% cobertura).
- Testes unitários para Sistema de Configuração.
- `docs/testing/unit-testing.md`: Documentação sobre padrões de testes.
- **BREAKING**: Removido widget `Pedals` (funcionalidade integrada ao `DashboardCard`)
- **BREAKING**: `OverlayApp` agora requer dependências via injeção de construtor (use `AppFactory.create()` ao invés de instanciação direta)
- **Arquitetura**: Refatoração abrangente SOLID e Clean Architecture em 5 fases
  - Implementado container de injeção de dependência (`SimpleDIContainer`)
  - Extraídas interfaces: `IWindowManager`, `IFontProvider`, `ITelemetryProvider`
  - Criados handlers específicos de plataforma (`Win32TransparencyHandler`, `NullTransparencyHandler`)
  - Extraídos componentes do Speedometer: `SpeedometerRenderer`, `DraggableBehavior`, `unit_converter`
  - Removido padrão singleton do `FontManager`, substituído por `PygameFontProvider` injetável
  - Criado `AppFactory` para conexão de dependências
- **Layout**: Novo DashboardCard compacto (350px largura) com espaçamento simétrico (20px) e background gradiente (95% opacidade)
- Removidos todos comentários do código de produção (mantidos apenas em testes e docs)

### Added (Módulos de Infraestrutura)
- `src/core/infrastructure/di_container.py`: Container de injeção de dependência
- `src/core/infrastructure/app_factory.py`: Factory de aplicação para conexão DI
- `src/ui/interfaces/`: Definições de interface (IWindowManager, IFontProvider)
- `src/ui/platform/transparency_handler.py`: Tratamento de transparência específico de plataforma
- `src/ui/behaviors/draggable.py`: Comportamento de drag-and-drop reutilizável
- `src/ui/rendering/speedometer_renderer.py`: Renderização visual do velocímetro
- `src/core/domain/unit_converter.py`: Funções puras de conversão de unidades
- `src/ui/utils/pygame_font_provider.py`: Provedor de fontes injetável
- 44 novos testes abrangentes (100% cobertura para novos módulos)

### Fixed (Melhorias de Testes e Compatibilidade)
- Cobertura de testes melhorada de 98% para 99% (144 testes passando)
- Acesso a propriedades de janela em testes (mudado de `surface` direto para `_surface`)

### Added (Funcionalidades Iniciais)
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

### Fixed (Correções de Layout e Compatibilidade)
- Layout do Widget Speedometer (sobreposição de marcha/velocidade)
- Sincronização de drag & drop (área de colisão vs visual)
- Tratamento de input no RunningState (bloqueio de interação acidental)
- Compatibilidade de testes com mudanças de lógica (100% pass)
- Script de setup para suportar caminhos UNC (WSL network paths)

### Planejado

- Implementação de ITelemetryProvider

---

## [0.4.0] - 2026-02-01

### Added
- **UI**: Sistema completo de Drag & Drop com feedback visual (mudança de transparência ao arrastar).
- **Controle**: Alternar Modo de Edição com `F1`.
- **Integração**: Testes de integração abrangentes para fluxo de drag & drop e persistência.
- **Assets**: Imagens de referência para HUD original do LMU (`src/assets/images/hud-default-lmu*.png`).
- **Roadmap**: Completada Fase 4 (Drag & Drop) e adicionada Fase 5 (Expansão HUD).
- **Visuais**: Visuais premium de edição:
  - **Seleção**: Borda arredondada ciano com **animação de respiração dinâmica** (padding pulsante).
  - **Arrastando**: Card fica semi-transparente (180/255 opacidade).

### Fixed
- **Opacidade**: Corrigido bug onde conteúdo do card herdava transparência do background. Background agora respeita alpha do `bg_color` independentemente.
- **Cores**: Refinado background do card para corresponder preferência do usuário (Azul-Preto Escuro) e gradiente dinâmico baseado na cor de entrada.
- **Cor de Arrasto**: Mudada cor de feedback de arrasto para `(25, 35, 50, 180)` para evitar tonalidade rosada.
- **Modo de Edição**: Widgets agora continuam a atualizar/renderizar dados de telemetria enquanto no Modo de Edição (anteriormente pausado).
- **Testes**: Alcançada cobertura de 100% incluindo novos testes de integração e casos extremos para DashboardCard.
- **Roadmap**: Plano detalhado para refatoração de `InputCard` e novos widgets.

## [0.3.0] - 2026-01-31

### Added
- **Janela**: Funcionalidade always-on-top para Windows (`SetWindowPos` com `HWND_TOPMOST`) e Linux (`SDL_VIDEO_WINDOW_ALWAYS_ON_TOP`).
- **Testes**: Adicionado `test_physics_engine_corner_entry` para alcançar 100% de cobertura no motor de física.

### Changed
- **Física**: Implementado modelo de direção "Mão Humana" com limitação de taxa (máx 2.5 unidades/segundo).
- **Física**: Refinado amortecimento usando média móvel exponencial para direção mais suave e realista.
- **Física**: Micro-correções agora ativam apenas sob alta carga (Velocidade > 40 + Direção > 0.1).
- **Config**: Adicionado `layout.json` ao `.gitignore` (posições de janela específicas do usuário).

### Fixed
- **Física**: Eliminada "rotação completa" irrealista na inicialização.
- **Testes**: Atualizado `test_window_init_windows_os` para incluir verificação de mock `SetWindowPos`.

## [0.2.0] - 2026-01-31

### Added
- **Visuais**: Suporte para imagem personalizada de volante (`src/assets/images/wheel-mockup.png`).
- **UI**: Valores percentuais adicionados ao topo das barras de Throttle, Brake e FFB (Tamanho 16, Negrito).

### Changed
- **Física**: Simulação de direção melhorada com jitter reduzido, micro-correções e suavização exponencial.
- **Visuais**: Implementado `rotozoom` para rotação de volante de alta qualidade e anti-aliasing.
- **Visuais**: Aumentado tamanho do Indicador de Direção (Raio 45px).
- **Layout**: Centralizado display de Velocidade e Marcha perfeitamente (Vertical e Horizontalmente) dentro do DashboardCard.
- **Layout**: Movidos labels das Barras Indicadoras (T, B, F) para baixo para melhor legibilidade.
- **Layout**: Padronizado espaçamento vertical (gaps de 5px) para Barras Indicadoras.

### Added (Arquitetura e Infraestrutura)
- `src/core/infrastructure/config_manager.py`: Gerenciador de configuração singleton.
- `src/core/interfaces/i_config_manager.py`: Interface para gerenciador de configuração.
- `tests/unit/ui/utils/test_fonts.py`: Testes abrangentes para classe estática FontManager (100% cobertura).
- Testes unitários para Sistema de Configuração.
- `docs/testing/unit-testing.md`: Documentação sobre padrões de testes.
- **BREAKING**: Removido widget `Pedals` (funcionalidade integrada ao `DashboardCard`)
- **BREAKING**: `OverlayApp` agora requer dependências via injeção de construtor (use `AppFactory.create()` ao invés de instanciação direta)
- **Arquitetura**: Refatoração abrangente SOLID e Clean Architecture
- **Layout**: Novo DashboardCard compacto (350px largura) com espaçamento simétrico (20px) e background gradiente (95% opacidade)
- **Arquitetura**: Refatoração abrangente SOLID e Clean Architecture em 5 fases
  - Implementado container de injeção de dependência (`SimpleDIContainer`)
  - Extraídas interfaces: `IWindowManager`, `IFontProvider`, `ITelemetryProvider`
  - Criados handlers específicos de plataforma (`Win32TransparencyHandler`, `NullTransparencyHandler`)
  - Extraídos componentes do Speedometer: `SpeedometerRenderer`, `DraggableBehavior`, `unit_converter`
  - Removido padrão singleton do `FontManager`, substituído por `PygameFontProvider` injetável
  - Criado `AppFactory` para conexão de dependências
- Removidos todos comentários do código de produção (mantidos apenas em testes e docs)

### Added (Novos Módulos)
- `src/core/infrastructure/di_container.py`: Container de injeção de dependência
- `src/core/infrastructure/app_factory.py`: Factory de aplicação para conexão DI
- `src/ui/interfaces/`: Definições de interface (IWindowManager, IFontProvider)
- `src/ui/platform/transparency_handler.py`: Tratamento de transparência específico de plataforma
- `src/ui/behaviors/draggable.py`: Comportamento de drag-and-drop reutilizável
- `src/ui/rendering/speedometer_renderer.py`: Renderização visual do velocímetro
- `src/core/domain/unit_converter.py`: Funções puras de conversão de unidades
- `src/ui/utils/pygame_font_provider.py`: Provedor de fontes injetável
- 44 novos testes abrangentes (100% cobertura para novos módulos)

### Fixed
- Cobertura de testes melhorada de 98% para 99% (144 testes passando)
- Acesso a propriedades de janela em testes (mudado de `surface` direto para `_surface`)
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
- **Opacity**: Fixed bug where card content inherited background transparency. Background now respects `bg_color` alpha independently.
- **Colors**: Refined card background to match user preference (Dark Bluish-Black) and dynamic gradient based on input color.
- **Drag Color**: Changed drag feedback color to `(25, 35, 50, 180)` to avoid pinkish hue.
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
