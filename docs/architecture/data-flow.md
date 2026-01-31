# Fluxo de Dados

Como dados fluem através do sistema.

## Visão Geral

```
Game Memory → Provider → TelemetryData → Normalization → Widgets → Pygame → Display
```

## Fluxo Detalhado

### 1. Aquisição de Dados

**Produção (Windows)**:

```
Le Mans Ultimate
    ↓ (escreve)
Shared Memory
    ↓ (lê via mmap)
SharedMemoryProvider.get_data()
    ↓
TelemetryData (raw)
```

**Desenvolvimento (WSL)**:

```
time.time()
    ↓ (gera senoide)
MockTelemetryProvider.get_data()
    ↓
TelemetryData (fake)
```

### 2. Normalização

```
TelemetryData (raw values 0-255)
    ↓
normalize_input()
    ↓
TelemetryData (normalized 0.0-1.0)
```

### 3. Distribuição para Widgets

```
TelemetryData
    ↓
for widget in widgets:
    widget.update(data)
```

Cada widget extrai dados relevantes:
- Speedometer: `speed`, `gear`
- Pedals: `throttle_pct`, `brake_pct`, `clutch_pct`
- SteeringWheel: `steering_angle`
- FFBIndicator: `ffb_level`

### 4. Renderização

```
Widget.update(data)
    ↓ (atualiza estado interno)
Widget.draw(surface)
    ↓ (renderiza em Pygame Surface)
pygame.display.flip()
    ↓
Display
```

## Diagrama Completo

```
┌─────────────────────┐
│  Le Mans Ultimate   │
│   (Game Process)    │
└──────────┬──────────┘
           │ writes
           ↓
┌─────────────────────┐
│  Shared Memory      │
│   (Windows mmap)    │
└──────────┬──────────┘
           │ reads
           ↓
┌─────────────────────┐     ┌─────────────────────┐
│ SharedMemoryProvider│ OR  │ MockTelemetryProvider│
│   (Windows)         │     │   (WSL/Dev)         │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           └───────────┬───────────────┘
                       ↓
           ┌─────────────────────┐
           │   TelemetryData     │
           │   (raw values)      │
           └──────────┬──────────┘
                      │
                      ↓
           ┌─────────────────────┐
           │   Normalization     │
           │   (0-255 → 0.0-1.0) │
           └──────────┬──────────┘
                      │
                      ↓
           ┌─────────────────────┐
           │   TelemetryData     │
           │  (normalized)       │
           └──────────┬──────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ↓             ↓             ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│Speedometer│  │  Pedals  │  │ Steering │
│  Widget  │  │  Widget  │  │  Widget  │
└─────┬────┘  └─────┬────┘  └─────┬────┘
      │             │             │
      └─────────────┼─────────────┘
                    ↓
         ┌─────────────────────┐
         │  Pygame Surface     │
         │  (composited)       │
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │  Window Manager     │
         │  (transparency)     │
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │      Display        │
         └─────────────────────┘
```

## Loop Principal

```python
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_state.handle_input(event)
    
    data = provider.get_data()
    
    for widget in widgets:
        widget.update(data)
    
    surface.fill(background_color)
    
    for widget in widgets:
        widget.draw(surface)
    
    pygame.display.flip()
    clock.tick(fps_target)
```

## Frequência de Atualização

### Polling Rate

60 Hz (60 vezes por segundo) por padrão.

```python
clock.tick(60)
```

### Latência

- **Aquisição**: <1ms (leitura de memória)
- **Normalização**: <1ms (operações matemáticas simples)
- **Renderização**: ~16ms (60 FPS)

**Latência total**: ~17ms (imperceptível)

## Otimizações

### Dirty Rectangles

Apenas redesenha áreas que mudaram:

```python
dirty_rects = []
for widget in widgets:
    if widget.has_changed():
        dirty_rects.append(widget.get_rect())

pygame.display.update(dirty_rects)
```

### Caching

Widgets cacheia elementos estáticos:

```python
class Speedometer(Widget):
    def __init__(self):
        self.background = self._render_background()
    
    def draw(self, surface):
        surface.blit(self.background, self.rect)
```

### Throttling

Limite atualizações de widgets lentos:

```python
class Widget:
    def update(self, data):
        if time.time() - self.last_update < 0.1:
            return
        self._do_update(data)
```

## Fluxo de Configuração

```
config.json
    ↓
ConfigManager.load()
    ↓
Application.__init__(config)
    ↓
Widgets criados com config
```

## Fluxo de Persistência

```
User drag widget
    ↓
Widget.set_position(x, y)
    ↓
Application.on_close()
    ↓
ConfigManager.save_layout(widgets)
    ↓
layout.json
```

## Próximos Passos

- [Camadas](layers.md) - Onde cada etapa acontece
- [Design Patterns](design-patterns.md) - Patterns aplicados
- [Performance](../guides/deployment/performance.md) - Otimizações
