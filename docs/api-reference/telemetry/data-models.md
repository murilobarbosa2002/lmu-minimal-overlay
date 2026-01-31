# Data Models

Modelos de dados de telemetria.

## TelemetryData

```python
@dataclass
class TelemetryData:
    speed: float
    rpm: int
    throttle_pct: float
    brake_pct: float
    clutch_pct: float
    steering_angle: float
    ffb_level: float
    gear: int
    timestamp: float
```

## Campos

- `speed`: Velocidade em km/h
- `rpm`: Rotações por minuto
- `throttle_pct`: Throttle 0.0-1.0
- `brake_pct`: Brake 0.0-1.0
- `clutch_pct`: Clutch 0.0-1.0
- `steering_angle`: Ângulo -900 a +900
- `ffb_level`: Force feedback 0.0-1.0+
- `gear`: Marcha atual
- `timestamp`: Unix timestamp

Veja [Architecture - Layers](../../architecture/layers.md).
