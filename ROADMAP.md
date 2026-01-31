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

- [ ] **MockTelemetryProvider**
  - [ ] Implementar geração de dados senoidais
  - [ ] Simular variação realista de speed, rpm, inputs
  - [ ] Adicionar timestamp
  - [ ] Testar com pytest

- [ ] **SharedMemoryProvider (Stub)**
  - [ ] Criar estrutura básica
  - [ ] Implementar is_available() retornando False
  - [ ] Documentar estrutura de memória do LMU (pesquisa necessária)
  - [ ] Implementação completa será feita na Fase 3

### 1.3 Layer 2: Domain

- [x] **Normalização de Dados**
  - [x] Implementar normalize_byte(value: int) -> float
  - [x] Implementar normalize_word(value: int) -> float
  - [x] Implementar denormalize_byte(value: float) -> int
  - [x] Implementar denormalize_word(value: float) -> int
  - [x] Implementar clamp(value, min, max) -> float
  - [x] Testar com pytest (100% cobertura) funções com pytest
  - [ ] Adicionar testes de edge cases

- [ ] **State Management**
  - [ ] Criar classe abstrata ApplicationState
  - [ ] Implementar RunningState
  - [ ] Implementar EditState
  - [ ] Implementar transições entre estados
  - [ ] Testar state transitions

### 1.4 Layer 3: Presentation - Base

- [ ] **Widget Base**
  - [ ] Criar classe abstrata Widget
  - [ ] Definir métodos draw(), update(), handle_input()
  - [ ] Implementar get_rect() e set_position()
  - [ ] Documentar interface completa

- [ ] **Window Manager**
  - [ ] Criar janela Pygame básica
  - [ ] Implementar detecção de plataforma (Windows vs WSL)
  - [ ] Implementar transparência no Windows (pywin32)
  - [ ] Implementar click-through no modo Running
  - [ ] Testar em ambos ambientes

---

## Fase 2: Widgets Básicos

### 2.1 Speedometer Widget

- [ ] **Implementação**
  - [ ] Criar classe Speedometer herdando de Widget
  - [ ] Implementar renderização de velocidade
  - [ ] Implementar indicador de marcha
  - [ ] Adicionar suporte para km/h e mph
  - [ ] Implementar drag & drop

- [ ] **Testes**
  - [ ] Testar atualização de dados
  - [ ] Testar renderização
  - [ ] Testar conversão km/h ↔ mph

- [ ] **Documentação**
  - [ ] Atualizar docs/api-reference/widgets/speedometer.md
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

- [ ] **main.py**
  - [ ] Implementar entry point
  - [ ] Implementar loop principal Pygame
  - [ ] Integrar TelemetryProvider
  - [ ] Integrar ConfigManager
  - [ ] Integrar Widgets
  - [ ] Implementar gerenciamento de estados
  - [ ] Implementar captura de eventos (F1, F2, ESC)
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
  - [ ] Testar em Windows com jogo
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

- [ ] **Core**
  - [ ] Testar normalização (100% cobertura)
  - [ ] Testar TelemetryData
  - [ ] Testar states

- [ ] **Infra**
  - [ ] Testar MockTelemetryProvider
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

- [ ] Atingir >80% de cobertura
- [ ] Gerar relatório de cobertura
- [ ] Documentar áreas não cobertas

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
- **Progresso**: 90% (9/10 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 2: Widgets
- **Progresso**: 0% (0/12 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 3: Configuração
- **Progresso**: 0% (0/6 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 4: Integração
- **Progresso**: 0% (0/8 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 5: Produção
- **Progresso**: 0% (0/7 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 6: Performance
- **Progresso**: 0% (0/7 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 7: Testes
- **Progresso**: 0% (0/13 tarefas)
- **Status**: ⚪ Não Iniciado

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
