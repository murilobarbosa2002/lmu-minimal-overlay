# Lógica de Negócio e Produto

Documentação completa da lógica de negócio do LMU Telemetry Overlay.

## Visão do Produto

### Problema

Pilotos de simuladores de corrida precisam de informações de telemetria em tempo real durante corridas, mas:
- Não querem alternar entre telas
- Precisam de informações visuais rápidas
- Querem personalizar o que veem
- Não querem impacto na performance do jogo

### Solução

Overlay transparente que exibe telemetria sobre o jogo sem interferir na experiência de corrida.

### Proposta de Valor

- **Transparente**: Não interfere com o jogo
- **Personalizável**: Posicione widgets onde quiser
- **Leve**: Mínimo impacto na performance
- **Informativo**: Dados críticos em tempo real

## Público-Alvo

### Primário

**Pilotos de Simulador (Le Mans Ultimate)**
- Querem melhorar performance
- Precisam de feedback visual de inputs
- Querem detectar clipping de FFB
- Buscam dados de telemetria básicos

### Secundário

**Desenvolvedores de Overlays**
- Querem contribuir com novos widgets
- Buscam arquitetura limpa e extensível
- Precisam de documentação clara

## Casos de Uso

### UC1: Monitorar Telemetria Durante Corrida

**Ator**: Piloto  
**Pré-condição**: Le Mans Ultimate rodando  
**Fluxo**:
1. Piloto inicia overlay
2. Overlay conecta à memória do jogo
3. Piloto vê telemetria em tempo real
4. Piloto ajusta pilotagem baseado em dados

**Pós-condição**: Piloto tem feedback visual contínuo

### UC2: Posicionar Widgets

**Ator**: Piloto  
**Pré-condição**: Overlay rodando  
**Fluxo**:
1. Piloto pressiona F1 (modo Edit)
2. Piloto arrasta widgets para posições desejadas
3. Piloto pressiona F1 (volta ao modo Running)
4. Layout é salvo automaticamente

**Pós-condição**: Widgets nas posições preferidas

### UC3: Detectar Clipping de FFB

**Ator**: Piloto  
**Pré-condição**: Overlay rodando  
**Fluxo**:
1. Piloto dirige com force feedback
2. FFB Indicator mostra nível de força
3. Quando FFB clippa, indicador fica vermelho
4. Piloto ajusta configurações de FFB

**Pós-condição**: Piloto sabe quando FFB está clippando

### UC4: Desenvolver Novo Widget

**Ator**: Desenvolvedor  
**Pré-condição**: Ambiente configurado  
**Fluxo**:
1. Desenvolvedor cria classe herdando de Widget
2. Implementa métodos draw(), update(), handle_input()
3. Registra widget em __init__.py
4. Adiciona ao layout.json
5. Testa com dados mockados

**Pós-condição**: Novo widget disponível

## Regras de Negócio

### RN1: Transparência

Overlay deve ser transparente no modo Running para não obstruir visão do jogo.

### RN2: Performance

Overlay não deve causar queda de FPS no jogo. Target: 60 FPS.

### RN3: Persistência

Layout de widgets deve ser salvo automaticamente ao fechar.

### RN4: Dados em Tempo Real

Telemetria deve atualizar a 60 Hz (60 vezes por segundo).

### RN5: Detecção de Clipping

FFB Indicator deve mudar de cor quando força exceder thresholds configurados.

### RN6: Modo Desenvolvimento

Deve funcionar sem o jogo rodando usando dados mockados.

### RN7: Extensibilidade

Deve ser fácil adicionar novos widgets sem modificar código existente.

## Fluxos de Dados

### Fluxo Principal: Telemetria em Tempo Real

```
Le Mans Ultimate (escreve) 
    → Shared Memory 
    → SharedMemoryProvider.get_data() 
    → TelemetryData (normalizado) 
    → Widget.update(data) 
    → Widget.draw(surface) 
    → Display
```

**Frequência**: 60 Hz  
**Latência**: ~17ms

### Fluxo Alternativo: Desenvolvimento WSL

```
time.time() (gera senoide) 
    → MockTelemetryProvider.get_data() 
    → TelemetryData (fake) 
    → Widget.update(data) 
    → Widget.draw(surface) 
    → Display
```

**Frequência**: 60 Hz  
**Latência**: ~16ms

### Fluxo de Configuração

```
config.json (disco) 
    → ConfigManager.load() 
    → Application.__init__(config) 
    → Widgets criados com config
```

**Momento**: Startup

### Fluxo de Persistência

```
User drag widget 
    → Widget.set_position(x, y) 
    → Application.on_close() 
    → ConfigManager.save_layout(widgets) 
    → layout.json (disco)
```

**Momento**: Shutdown

## Modelo de Dados

### TelemetryData

Dados de telemetria do veículo.

**Campos**:
- `speed: float` - Velocidade em km/h
- `rpm: int` - Rotações por minuto
- `throttle_pct: float` - Acelerador 0.0-1.0
- `brake_pct: float` - Freio 0.0-1.0
- `clutch_pct: float` - Embreagem 0.0-1.0
- `steering_angle: float` - Ângulo do volante -900 a +900
- `ffb_level: float` - Força do FFB 0.0-1.0+
- `gear: int` - Marcha atual
- `timestamp: float` - Unix timestamp

**Fonte**: SharedMemoryProvider ou MockTelemetryProvider

### Config

Configurações globais.

**Campos**:
- `colors: Dict[str, List[int]]` - Paleta RGB
- `thresholds: Dict[str, float]` - Limites para indicadores
- `window: Dict` - Dimensões e transparência
- `performance: Dict` - FPS target
- `telemetry: Dict` - Provider e configurações

**Fonte**: config.json

### Layout

Posições de widgets.

**Campos**:
- `widgets: List[WidgetConfig]` - Lista de widgets
  - `id: str` - Identificador único
  - `type: str` - Classe do widget
  - `x: int, y: int` - Posição
  - `width: int, height: int` - Dimensões
  - `visible: bool` - Visibilidade

**Fonte**: layout.json

## Estados da Aplicação

### RunningState

**Características**:
- Overlay transparente
- Click-through (não captura mouse)
- Apenas visualização
- Usado durante corridas

**Transição**: F1 → EditState

### EditState

**Características**:
- Fundo visível (escuro)
- Captura mouse
- Permite drag & drop
- Usado para configuração

**Transição**: F1 → RunningState

## Widgets Disponíveis

### Speedometer

**Função**: Exibir velocidade e marcha  
**Dados**: speed, gear  
**Visualização**: Números grandes + indicador de marcha

### Pedals

**Função**: Mostrar pressão dos pedais  
**Dados**: throttle_pct, brake_pct, clutch_pct  
**Visualização**: Três barras verticais coloridas

### SteeringWheel

**Função**: Mostrar ângulo do volante  
**Dados**: steering_angle  
**Visualização**: Representação circular rotativa

### FFBIndicator

**Função**: Detectar clipping de force feedback  
**Dados**: ffb_level  
**Visualização**: Barra horizontal com cores dinâmicas

## Métricas de Sucesso

### Performance

- **FPS**: Manter 60 FPS constantes
- **Latência**: <20ms da leitura à renderização
- **CPU**: <5% de uso de CPU
- **Memória**: <100MB de RAM

### Usabilidade

- **Setup**: <5 minutos para instalar e configurar
- **Aprendizado**: <2 minutos para entender interface
- **Customização**: <1 minuto para reposicionar widgets

### Qualidade

- **Cobertura de Testes**: >80%
- **Bugs Críticos**: 0
- **Documentação**: 100% das APIs documentadas

## Restrições Técnicas

### Plataforma

- **Desenvolvimento**: WSL2 Ubuntu 20.04+
- **Produção**: Windows 10/11
- **Jogo**: Le Mans Ultimate

### Tecnologias

- **Linguagem**: Python 3.9+
- **UI**: Pygame
- **Transparência**: pywin32 (Windows)
- **Memória**: mmap (built-in)

### Limitações

- Apenas Le Mans Ultimate (memória específica do jogo)
- Windows para produção (pywin32)
- 60 FPS máximo (limitação Pygame)

## Roadmap

Veja [ROADMAP.md](ROADMAP.md) para plano detalhado de desenvolvimento.
