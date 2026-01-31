# Padrões de Código

Clean Code e SOLID principles.

## Type Hinting

Obrigatório em todas funções:

```python
def normalize_input(raw: int) -> float:
    return raw / 255.0
```

## Docstrings

Google Style em português:

```python
def get_data(self) -> TelemetryData:
    """Obtém dados de telemetria.
    
    Returns:
        TelemetryData com estado atual.
    """
    pass
```

## Formatação

- PEP 8
- Black
- isort

## Naming

- Variáveis: `snake_case`
- Classes: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`

Veja [.agent/rules/code_quality_standards.md](../../../.agent/rules/code_quality_standards.md).
