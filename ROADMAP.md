# Roadmap - LMU Telemetry Overlay

Roadmap detalhado de desenvolvimento do projeto. Este documento é atualizado continuamente conforme o progresso.

**Última atualização**: 2026-01-31 (v0.3.0)

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

- [x] **MockTelemetryProvider (Physics-Lite)**
  - [x] Implementar `PhysicsEngine` com inércia e arrasto
  - [x] Implementar `TrackGenerator` com segmentos técnicos
  - [x] Simular Trail Braking e input smoothing
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

### 2.1 DashboardCard (antigo Speedometer)

- [x] **Implementação**
  - [x] Criar classe DashboardCard herdando de Widget
  - [x] Integrar Speed, Gear, Steering, Pedals, FFB
  - [x] Implementar layout simétrico e compacto (350px)
  - [x] Implementar drag & drop

- [x] **Testes**
  - [x] Testar atualização de todos dados (162 testes total)
  - [x] Testar renderização otimizada
  - [x] 100% Cobertura

- [x] **Documentação**
  - [x] Atualizar API reference
  - [x] Adicionar screenshots

### 2.2 Pedals Widget (Removido)

- [x] **Status**: Integrado ao DashboardCard para design mais limpo e compacto.

### 2.3 Steering Wheel Widget (Integrado)

- [x] **Status**: Integrado ao DashboardCard.

### 2.4 FFB Indicator Widget (Integrado)

- [x] **Status**: Integrado ao DashboardCard.

---

## Fase 3: Sistema de Configuração

### 3.1 ConfigManager

- [x] **Implementação**
  - [x] Implementar Singleton pattern
  - [x] Implementar carregamento de config.json
  - [x] Implementar carregamento de layout.json
  - [x] Implementar salvamento de layout
  - [x] Adicionar validação de configurações
  - [x] Implementar valores padrão
  - [x] Implementar backup automático

- [x] **Testes**
  - [x] Testar singleton (apenas uma instância)
  - [x] Testar carregamento de JSON
  - [x] Testar salvamento de layout
  - [x] Testar validação
  - [x] Testar valores padrão

- [x] **Documentação**
  - [x] Atualizar docs/api-reference/configuration/config-manager.md

### 3.2 Arquivos de Configuração

- [x] **config.json**
  - [x] Criar estrutura padrão
  - [x] Documentar todas opções
  - [x] Adicionar exemplos

- [x] **layout.json**
  - [x] Criar estrutura padrão
  - [x] Definir posições padrão de widgets
  - [x] Documentar estrutura

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
  - [x] Implementar salvamento ao fechar

- [x] **Testes de Integração**
  - [x] Testar fluxo completo de dados
  - [x] Testar transições de estado
  - [x] Testar drag & drop (F1 toggle, persistência)
  - [x] Testar persistência de layout

### 4.2 Drag & Drop System (Concluído)

- [x] **Implementação**
  - [x] Detectar clique em widget
  - [x] Implementar arrastar widget
  - [x] Implementar soltar widget
  - [x] Salvar nova posição
  - [x] Feedback visual durante drag (transparência/cor)

- [x] **Testes**
  - [x] Testar detecção de colisão
  - [x] Testar movimento de widget
  - [x] Testar salvamento de posição

### 4.3 Expansão de Widgets
- [ ] **Refatoração UI**
  - [ ] Renomear `DashboardCard` para `InputCard`
  - [ ] Renomear `DashboardCardRenderer` para `InputCardRenderer`
  - [ ] Criar sistema de cards múltiplos
- [ ] **Novos Widgets**
  - [ ] **Fuel & Energy Card**: Barra de Combustível, Energia (ERS/Bateria)
  - [ ] **Car Status Card**: Óleo, Água, Pneus (4x), Freios
- [ ] **Integração Real**: Conectar novos widgets ao `TelemetryData`

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
  - [x] Testar SharedMemoryProvider
  - [x] Testar ITelemetryProvider interface

- [x] **UI**
  - [x] Testar cada widget isoladamente
  - [x] Testar Widget base
  - [x] Testar window manager

- [x] **Config**
  - [x] Testar ConfigManager
  - [x] Testar carregamento/salvamento

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
- **Progresso**: 100% (12/12 tarefas)
- **Status**: 🟢 Completo

### Fase 3: Configuração
- **Progresso**: 100% (6/6 tarefas)
- **Status**: 🟢 Completo

### Fase 4: Integração
- **Progresso**: 75% (6/8 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 6: Produção (Anterior Fase 5)
- **Progresso**: 30% (2/7 tarefas)
- **Status**: 🟡 Em Progresso

### Fase 7: Performance (Anterior Fase 6)
- **Progresso**: 0% (0/7 tarefas)
- **Status**: ⚪ Não Iniciado

### Fase 7: Testes
- **Progresso**: 90% (12/13 tarefas)
- **Status**: 🟢 Avançado

### Fase 8: Documentação
- **Progresso**: 92% (12/13 tarefas)
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
