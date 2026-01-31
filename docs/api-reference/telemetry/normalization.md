# Normalização

Funções de normalização de dados.

## normalize_input

```python
def normalize_input(raw: int) -> float:
    """Normaliza input 0-255 para 0.0-1.0."""
    return raw / 255.0
```

## normalize_rpm

```python
def normalize_rpm(rpm: int, max_rpm: int = 10000) -> float:
    """Normaliza RPM baseado em máximo."""
    return min(rpm / max_rpm, 1.0)
```

## normalize_steering

```python
def normalize_steering(angle: float) -> float:
    """Normaliza ângulo -900/+900 para -1.0/+1.0."""
    return angle / 900.0
```

## kmh_to_mph

```python
def kmh_to_mph(speed_kmh: float) -> float:
    """Converte km/h para mph."""
    return speed_kmh * 0.621371
```

Veja [Architecture - Layers](../../architecture/layers.md).
