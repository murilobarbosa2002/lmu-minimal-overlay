# Data Models

Modelos de dados de telemetria.

## TelemetryData

Dataclass que representa dados de telemetria normalizados do jogo.

### Campos

```python
@dataclass
class TelemetryData:
    speed: float
    rpm: int
    max_rpm: int
    gear: int
    throttle_pct: float
    brake_pct: float
    clutch_pct: float
    steering_angle: float
    ffb_level: float
    timestamp: float
```

### Descrição dos Campos

- `speed`: Velocidade em km/h
- `rpm`: RPM atual do motor
- `max_rpm`: RPM máximo do motor
- `gear`: Marcha atual (0 = neutro, -1 = ré)
- `throttle_pct`: Acelerador normalizado (0.0 a 1.0)
- `brake_pct`: Freio normalizado (0.0 a 1.0)
- `clutch_pct`: Embreagem normalizada (0.0 a 1.0)
- `steering_angle`: Ângulo do volante em graus (-900 a 900)
- `ffb_level`: Nível de force feedback (0.0+)
- `timestamp`: Timestamp Unix dos dados

### Validações

A dataclass valida automaticamente os seguintes ranges:

- `throttle_pct`: Deve estar entre 0.0 e 1.0
- `brake_pct`: Deve estar entre 0.0 e 1.0
- `clutch_pct`: Deve estar entre 0.0 e 1.0
- `steering_angle`: Deve estar entre -900 e 900 graus

Valores fora desses ranges levantam `ValueError` com mensagem descritiva.

### Uso

```python
from src.core.domain.telemetry_data import TelemetryData

data = TelemetryData(
    speed=120.5,
    rpm=6000,
    max_rpm=8000,
    gear=3,
    throttle_pct=0.75,
    brake_pct=0.0,
    clutch_pct=0.0,
    steering_angle=45.0,
    ffb_level=0.5,
    timestamp=1234567890.0
)

print(data)
```

### Criação a partir de Dicionário

```python
raw_data = {
    "speed": 150.0,
    "rpm": 7000,
    "max_rpm": 8000,
    "gear": 4,
    "throttle_pct": 1.0,
    "brake_pct": 0.0,
    "clutch_pct": 0.0,
    "steering_angle": -180.0,
    "ffb_level": 0.8,
    "timestamp": 1234567890.0
}

data = TelemetryData(**raw_data)
```

### Representação String

O método `__str__` retorna uma representação compacta para debug:

```python
str(data)
```

Output:
```
TelemetryData(speed=120.5, rpm=6000, gear=3, throttle=0.75, brake=0.00)
```

### Testes

Cobertura: **100%**

Testes implementados:
- Criação com dados válidos
- Validação de throttle fora do range
- Validação de brake fora do range
- Validação de clutch fora do range
- Validação de steering fora do range
- Representação string
- Workflow completo (E2E)

## Funções de Normalização

Funções utilitárias para converter valores brutos em valores normalizados (0.0-1.0).

### normalize_byte

Normaliza valores de 8 bits (0-255) para 0.0-1.0.

```python
from src.core.domain.normalize import normalize_byte

throttle_raw = 200
throttle_normalized = normalize_byte(throttle_raw)
```

### normalize_word

Normaliza valores de 16 bits (0-65535) para 0.0-1.0.

```python
from src.core.domain.normalize import normalize_word

steering_raw = 32767
steering_normalized = normalize_word(steering_raw)
```

### denormalize_byte

Converte valores normalizados (0.0-1.0) para 8 bits (0-255).

```python
from src.core.domain.normalize import denormalize_byte

throttle_normalized = 0.75
throttle_raw = denormalize_byte(throttle_normalized)
```

### denormalize_word

Converte valores normalizados (0.0-1.0) para 16 bits (0-65535).

```python
from src.core.domain.normalize import denormalize_word

steering_normalized = 0.5
steering_raw = denormalize_word(steering_normalized)
```

### clamp

Limita um valor entre um mínimo e máximo.

```python
from src.core.domain.normalize import clamp

value = clamp(1.5, 0.0, 1.0)
```

### Validações

Todas as funções validam os ranges de entrada:
- `normalize_byte`: 0-255
- `normalize_word`: 0-65535
- `denormalize_byte`: 0.0-1.0
- `denormalize_word`: 0.0-1.0
- `clamp`: min_val ≤ max_val

Valores fora do range levantam `ValueError`.

### Testes

Cobertura: **100%**

Testes implementados:
- Normalização de bytes válidos
- Normalização de words válidos
- Desnormalização válida
- Validação de ranges inválidos
- Clamp com valores dentro e fora do range
- Round-trip (normalize → denormalize)

Veja [Architecture - Layers](../../architecture/layers.md).
