# Dashboard Card

O `DashboardCard` é o componente principal de interface do LMU Telemetry Overlay. Ele integra múltiplos indicadores em um único card compacto e eficiente.

## 📋 Características

- **Visualização Integrada**: Speed, Gear, Steering, Throttle, Brake, FFB.
- **Design Compacto**: 350x130px.
- **Alta Performance**: Renderização otimizada com caching.
- **Layout Simétrico**: Padding balanceado e alinhamento preciso.
- **Interativo**: Suporte a drag & drop.

## 🏗️ Estrutura

Composto por 4 sub-componentes:

1.  **SteeringIndicator**: Volante (Esquerda)
2.  **SpeedGearDisplay**: Velocidade e marcha (Centro)
3.  **IndicatorBars**: Throttle, Brake, FFB (Direita)
4.  **Bar**: Componente base para barras verticais

## 💻 Uso

```python
from src.ui.widgets.dashboard_card import DashboardCard

# Instanciar
card = DashboardCard(x=100, y=100)

# Atualizar dados
card.update(telemetry_data)

# Renderizar
card.draw(surface)
```

## ⚙️ Configuração

| Propriedade | Tipo | Padrão | Descrição |
|---|---|---|---|
| `unit` | str | "km/h" | Unidade de velocidade ("km/h" ou "mph") |
| `x`, `y` | int | 0 | Posição na tela |

## 🎨 Layout

```
┌────────────────────────────────────┐
│         GEAR (Yellow)              │
│   (Steering)    (Speed)      (Bars)│
│    ○           180       ║█║ ║█║ ║█║│
│                km/h      T   B   F │
└────────────────────────────────────┘
```
