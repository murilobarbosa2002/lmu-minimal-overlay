# Testes

Estratégia de testes com pytest.

## Executar Testes

```bash
pytest
pytest --cov=.
pytest -v
```

## Estrutura

```
tests/
├── test_telemetry.py
├── test_widgets.py
└── test_normalization.py
```

## Exemplo

```python
def test_normalize_input():
    assert normalize_input(255) == 1.0
    assert normalize_input(0) == 0.0
```

## Cobertura

Mínimo 80%.

Veja [.agent/rules/testing_standards.md](../../../.agent/rules/testing_standards.md).
