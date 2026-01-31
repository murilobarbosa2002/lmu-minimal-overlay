# Roadmap - LMU Telemetry Overlay

Roadmap detalhado de desenvolvimento do projeto. Este documento é atualizado continuamente conforme o progresso.

**Última atualização**: 2026-01-31

---

## Fase 1: Fundação e Infraestrutura

### 1.1 Estrutura do Projeto

- [x] Criar estrutura de diretórios (core/, infra/, ui/, config/)
- [x] Configurar .gitignore
- [x] Criar requirements.txt e requirements-windows.txt
- [x] Configurar estrutura de documentação GitHub Docs
- [x] Criar documentação de produto (PRODUCT.md)
- [x] Criar roadmap (ROADMAP.md)
- [x] Criar setup.py e pytest.ini
- [x] Criar main.py como entry point

### 1.2 Layer 1: Infrastructure

- [x] **ITelemetryProvider (Interface)**
  - [x] Definir interface abstrata com métodos get_data(), is_available(), connect(), disconnect()
  - [x] Adicionar type hints completos
  - [x] Documentar com docstrings em português

- [x] **TelemetryData (Dataclass)**
  - [x] Criar dataclass com todos campos tipados
  - [x] Adicionar validação de dados
  - [x] Implementar método __str__ para debug

- [x] **MockTelemetryProvider**
  - [x] Implementar geração de dados senoidais
  - [x] Simular variação realista de speed, rpm, inputs
  - [x] Adicionar timestamp
  - [x] Testar com pytest (100% cobertura)

- [x] **SharedMemoryProvider (Stub)**
  - [x] Criar estrutura básica
  - [x] Implementar is_available() retornando False
  - [x] Documentar estrutura de memória do LMU (pesquisa necessária)
  - [ ] Implementação completa será feita na Fase 3

### 1.3 Layer 2: Domain

- [x] **Normalização de Dados**
  - [x] Implementar normalize_byte(value: int) -> float
  - [x] Implementar normalize_word(value: int) -> float
  - [x] Implementar denormalize_byte(value: float) -> int
  - [x] Implementar denormalize_word(value: float) -> int
  - [x] Implementar clamp(value, min, max) -> float
  - [x] Testar com pytest (100% cobertura) funções com pytest
  - [x] Adicionar testes de edge cases

- [x] **State Management**
  - [x] Criar classe abstrata ApplicationState
  - [x] Implementar RunningState
  - [x] Implementar EditState
  - [x] Implementar transições entre estados
  - [x] Testar state transitions

### 1.4 Layer 3: Presentation - Base

- [x] **Widget Base**
  - [x] Criar classe abstrata Widget
  - [x] Definir métodos draw(), update(), handle_input()
  - [x] Implementar get_rect() e set_position()
  - [x] Documentar interface completa

- [x] **Window Manager**
  - [x] Criar janela Pygame básica
  - [x] Implementar detecção de plataforma (Windows vs WSL)
  - [x] Implementar transparência no Windows (pywin32 stub)
  - [x] Implementar click-through no modo Running (stub)
  - [x] Testar em ambos ambientes

---

## Fase 2: Widgets Básicos

### 2.1 Speedometer Widget

- [x] **Implementação**
  - [x] Criar classe Speedometer herdando de Widget
  - [x] Implementar renderização de velocidade
  - [x] Implementar indicador de marcha
  - [x] Adicionar suporte para km/h e mph (km/h fixo inicial)
  - [x] Implementar drag & drop

- [x] **Testes**
  - [x] Testar atualização de dados
  - [x] Testar renderização
  - [x] Testar conversão km/h ↔ mph

- [x] **Documentação**
  - [x] Atualizar docs/api-reference/widgets/speedometer.md
  - [ ] Adicionar screenshots

### 2.2 Pedals Widget

- [ ] **Implementação**
  - [ ] Criar classe Pedals herdando de Widget
  - [ ] Implementar três barras verticais
  - [ ] Adicionar cores configuráveis (verde, vermelho, azul)
  - [ ] Implementar animação suave
  - [ ] Implementar drag & drop

- [ ] **Testes**
  - [ ] Testar atualização de dados
  - [ ] Testar renderização de barras
  - [ ] Testar cores

- [ ] **Documentação**
  - [ ] Atualizar docs/api-reference/widgets/pedals.md
  - [ ] Adicionar screenshots

### 2.3 Steering Wheel Widget

- [ ] **Implementação**
  - [ ] Criar classe SteeringWheel herdando de Widget
  - [ ] Implementar representação circular
  - [ ] Implementar rotação baseada em ângulo
  - [ ] Adicionar indicador de centro
  - [ ] Implementar drag & drop

- [ ] **Testes**
  - [ ] Testar rotação -900 a +900
  - [ ] Testar renderização
  - [ ] Testar normalização de ângulo

- [ ] **Documentação**
  - [ ] Atualizar docs/api-reference/widgets/steering-wheel.md
  - [ ] Adicionar screenshots

### 2.4 FFB Indicator Widget

- [ ] **Implementação**
  - [ ] Criar classe FFBIndicator herdando de Widget
  - [ ] Implementar barra horizontal
  - [ ] Implementar cores dinâmicas (verde, amarelo, vermelho)
  - [ ] Adicionar thresholds configuráveis
  - [ ] Implementar drag & drop

- [ ] **Testes**
  - [ ] Testar mudança de cor baseada em threshold
  - [ ] Testar detecção de clipping
  - [ ] Testar configuração de thresholds

- [ ] **Documentação**
  - [ ] Atualizar docs/api-reference/widgets/ffb-indicator.md
  - [ ] Adicionar screenshots

---

## Fase 3: Sistema de Configuração

### 3.1 ConfigManager

- [ ] **Implementação**
  - [ ] Implementar Singleton pattern
  - [ ] Implementar carregamento de config.json
  - [ ] Implementar carregamento de layout.json
  - [ ] Implementar salvamento de layout
  - [ ] Adicionar validação de configurações
  - [ ] Implementar valores padrão
  - [ ] Implementar backup automático

- [ ] **Testes**
  - [ ] Testar singleton (apenas uma instância)
  - [ ] Testar carregamento de JSON
  - [ ] Testar salvamento de layout
  - [ ] Testar validação
  - [ ] Testar valores padrão

- [ ] **Documentação**
  - [ ] Atualizar docs/api-reference/configuration/config-manager.md

### 3.2 Arquivos de Configuração

- [ ] **config.json**
  - [ ] Criar estrutura padrão
  - [ ] Documentar todas opções
  - [ ] Adicionar exemplos

- [ ] **layout.json**
  - [ ] Criar estrutura padrão
  - [ ] Definir posições padrão de widgets
  - [ ] Documentar estrutura

---

## Fase 4: Integração e Loop Principal

### 4.1 Application Main

- [x] **main.py**
  - [x] Implementar entry point
  - [x] Implementar loop principal Pygame
  - [x] Integrar TelemetryProvider
  - [x] Integrar ConfigManager (Parcial)
  - [x] Integrar Widgets
  - [x] Implementar gerenciamento de estados
  - [x] Implementar captura de eventos (F1, F2, ESC)
  - [ ] Implementar salvamento ao fechar

- [ ] **Testes de Integração**
  - [ ] Testar fluxo completo de dados
  - [ ] Testar transições de estado
  - [ ] Testar drag & drop
  - [ ] Testar persistência de layout

### 4.2 Drag & Drop System

- [ ] **Implementação**
  - [ ] Detectar clique em widget
  - [ ] Implementar arrastar widget
  - [ ] Implementar soltar widget
  - [ ] Salvar nova posição
  - [ ] Feedback visual durante drag

- [ ] **Testes**
  - [ ] Testar detecção de colisão
  - [ ] Testar movimento de widget
  - [ ] Testar salvamento de posição

---

## Fase 5: Produção Windows

### 5.1 SharedMemoryProvider Completo

- [ ] **Pesquisa**
  - [ ] Pesquisar estrutura de memória do Le Mans Ultimate
  - [ ] Documentar offsets de memória
  - [ ] Identificar nome do mmap

- [ ] **Implementação**
  - [ ] Implementar leitura de memória compartilhada
  - [ ] Implementar parsing de estrutura binária
  - [ ] Implementar conversão para TelemetryData
  - [ ] Adicionar tratamento de erros

- [ ] **Testes**
  - [ ] Testar com Le Mans Ultimate rodando
  - [ ] Validar dados lidos
  - [ ] Testar reconexão após crash do jogo

### 5.2 Detecção Automática de Provider

- [ ] **Implementação**
  - [ ] Detectar plataforma (Windows vs Linux)
  - [ ] Verificar disponibilidade de shared memory
  - [ ] Fallback para MockProvider se necessário
  - [ ] Logging claro de qual provider está ativo

- [ ] **Testes**
  - [x] Testar em Windows com jogo (Script de automação criado)
  - [ ] Testar em Windows sem jogo
  - [ ] Testar em WSL

---

## Fase 6: Otimizações e Performance

### 6.1 Renderização Otimizada

- [ ] **Dirty Rectangles**
  - [ ] Implementar sistema de dirty rectangles
  - [ ] Apenas redesenhar áreas alteradas
  - [ ] Medir ganho de performance

- [ ] **Caching**
  - [ ] Cachear elementos estáticos de widgets
  - [ ] Pré-renderizar backgrounds
  - [ ] Medir ganho de performance

- [ ] **Throttling**
  - [ ] Implementar throttling para widgets lentos
  - [ ] Configurar frequência de atualização por widget

### 6.2 Profiling

- [ ] **Medições**
  - [ ] Medir FPS médio
  - [ ] Medir latência de dados
  - [ ] Medir uso de CPU
  - [ ] Medir uso de memória

- [ ] **Otimizações**
  - [ ] Identificar bottlenecks
  - [ ] Otimizar código crítico
  - [ ] Validar melhorias

---

## Fase 7: Testes Completos

### 7.1 Testes Unitários

- [x] **Core**
  - [x] Testar normalização (100% cobertura)
  - [x] Testar TelemetryData
  - [x] Testar states

- [x] **Infra**
  - [x] Testar MockTelemetryProvider
  - [ ] Testar SharedMemoryProvider
  - [ ] Testar ITelemetryProvider interface

- [ ] **UI**
  - [ ] Testar cada widget isoladamente
  - [ ] Testar Widget base
  - [ ] Testar window manager

- [ ] **Config**
  - [ ] Testar ConfigManager
  - [ ] Testar carregamento/salvamento

### 7.2 Testes de Integração

- [ ] Testar fluxo completo de telemetria
- [ ] Testar persistência de configurações
- [ ] Testar drag & drop end-to-end
- [ ] Testar transições de estado

### 7.3 Testes E2E

- [ ] Testar aplicação completa em WSL
- [ ] Testar aplicação completa em Windows
- [ ] Testar com Le Mans Ultimate rodando
- [ ] Testar cenários de erro

### 7.4 Cobertura

- [x] Atingir >80% de cobertura (100% Atingido)
- [x] Gerar relatório de cobertura
- [x] Documentar áreas não cobertas (Nenhuma)

---

## Fase 8: Documentação Final

### 8.1 Documentação Técnica

- [ ] Revisar toda documentação em docs/
- [ ] Adicionar screenshots de todos widgets
- [ ] Adicionar diagramas Mermaid
- [ ] Atualizar exemplos de código
- [ ] Revisar links cruzados

### 8.2 README Principal

- [x] Criar README.md na raiz
- [x] Adicionar badges (build, coverage, license)
- [ ] Adicionar screenshots do overlay
- [x] Adicionar quick start
- [x] Adicionar links para documentação

### 8.3 CHANGELOG

- [x] Criar CHANGELOG.md
- [x] Documentar todas mudanças
- [x] Seguir formato Keep a Changelog
- [x] Versionar seguindo SemVer

### 8.4 CONTRIBUTING

- [x] Criar CONTRIBUTING.md
- [x] Workflow de contribuição
- [x] Padrões de código
- [x] Checklist de PR

---

## Fase 9: Deploy e Distribuição

### 9.1 Empacotamento

- [ ] Criar script de build
- [ ] Testar instalação limpa
- [ ] Criar instalador Windows (opcional)
- [ ] Documentar processo de instalação

### 9.2 CI/CD

- [ ] Configurar GitHub Actions
- [ ] Automatizar testes em cada commit
- [ ] Automatizar validação de código (mypy, black, flake8)
- [ ] Automatizar geração de relatório de cobertura

### 9.3 Release

- [ ] Criar tag v1.0.0
- [ ] Criar release no GitHub
- [ ] Adicionar binários (se aplicável)
- [ ] Anunciar release

---

## Phase 3: Code Quality & Architecture (IN PROGRESS)
**Status**: ✅ **COMPLETED** (January 2026)

### Completed
- ✅ **Architecture Refactoring** (v0.4.0)
  - ✅ Dependency injection container implementation
  - ✅ SOLID principles compliance across codebase
  - ✅ Clean Architecture patterns (interfaces, handlers, services)
  - ✅ Removed singleton patterns (FontManager → PygameFontProvider)
  - ✅ Platform-specific code separation (Win32TransparencyHandler)
  - ✅ Component extraction (SpeedometerRenderer, DraggableBehavior)
  - ✅ 99% test coverage (144 tests passing)
- ✅ **Code Cleanup**: Removed all comments from production code
- ✅ **Testing Infrastructure**: 100% coverage on new modules

### In Progress
- 🔄 **Documentation Updates**: Architecture diagrams and integration guides

---

## Fase 10: Funcionalidades Futuras

### 10.1 Novos Widgets

- [ ] **Tire Temperature Widget**
  - [ ] Pesquisar dados disponíveis
  - [ ] Implementar visualização
  - [ ] Testar

- [ ] **Lap Time Widget**
  - [ ] Implementar cronômetro
  - [ ] Mostrar último lap
  - [ ] Mostrar melhor lap

- [ ] **Fuel Widget**
  - [ ] Mostrar combustível restante
  - [ ] Calcular voltas restantes
  - [ ] Alertar quando baixo

### 10.2 Melhorias de UX

- [ ] **Temas**
  - [ ] Implementar sistema de temas
  - [ ] Criar tema claro e escuro
  - [ ] Permitir temas customizados

- [ ] **Hotkeys Customizáveis**
  - [ ] Permitir configurar atalhos
  - [ ] Salvar em config.json

- [ ] **Widget Presets**
  - [ ] Criar layouts pré-definidos
  - [ ] Permitir salvar/carregar presets

### 10.3 Suporte a Outros Jogos

- [ ] Pesquisar estrutura de memória de outros sims
- [ ] Implementar providers para outros jogos
- [ ] Testar compatibilidade

---

## Métricas de Progresso

### Fase 1: Fundação
- **Progresso**: 100% (10/10 tarefas)
- **Status**: 🟢 Completo

### Fase 2: Widgets
- **Progresso**: 33% (4/12 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 3: Configuração
- **Progresso**: 0% (0/6 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 4: Integração
- **Progresso**: 50% (4/8 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 5: Produção
- **Progresso**: 30% (2/7 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 6: Performance
- **Progresso**: 0% (0/7 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 7: Testes
- **Progresso**: 70% (9/13 tarefas)
- **Status**: 🟢 Avançado

### Fase 8: Documentação
- **Progresso**: 85% (11/13 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 9: Deploy
- **Progresso**: 0% (0/7 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 10: Futuro
- **Progresso**: 0% (0/9 tarefas)
- **Status**: ⚪ Planejamento

---

## Legenda

- [x] Concluído
- [ ] Pendente
- 🟢 Completo
- 🟡 Em Progresso
- ⚪ Não Iniciado
- 🔴 Bloqueado

---

## Notas

Este roadmap é um documento vivo e deve ser atualizado conforme o projeto evolui. Cada tarefa concluída deve ser marcada com [x] e a data de conclusão documentada no commit.
