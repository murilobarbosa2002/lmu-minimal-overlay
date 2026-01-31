# Guia de Desenvolvimento

Aprenda a desenvolver e contribuir para o LMU Telemetry Overlay.

## Começando

- [Setup WSL](setup-wsl.md) - Configure ambiente de desenvolvimento
- [Padrões de Código](code-standards.md) - Clean Code e SOLID
- [Testes](testing.md) - Estratégia de testes
- [Contribuindo](contributing.md) - Como contribuir

## Estrutura do Projeto

```
lmu-minimal-overlay/
├── main.py
├── core/
│   ├── telemetry.py
│   ├── normalization.py
│   └── state.py
├── infra/
│   ├── memory_reader.py
│   └── mock_provider.py
├── ui/
│   ├── window_manager.py
│   ├── states.py
│   └── widgets/
├── config/
│   ├── settings.py
│   ├── config.json
│   └── layout.json
└── tests/
```

## Quick Reference

### Executar Testes

```bash
pytest
pytest --cov=.
```

### Validar Código

```bash
mypy .
black .
flake8 .
```

### Criar Novo Widget

1. Crie arquivo em `ui/widgets/`
2. Herde de `Widget` base
3. Implemente métodos obrigatórios
4. Registre em `__init__.py`
5. Adicione testes

## Navegação

- [Setup WSL](setup-wsl.md)
- [Padrões de Código](code-standards.md)
- [Testes](testing.md)
- [Contribuindo](contributing.md)
- [Dependency Injection](#dependency-injection)

## Dependency Injection

### Usando AppFactory

Forma recomendada de criar a aplicação:

```python
from src.core.infrastructure.app_factory import AppFactory

app = AppFactory.create()  # DI automático
app.run()
```

### Registro Customizado

Para testes ou configurações específicas:

```python
from src.core.infrastructure.di_container import SimpleDIContainer

container = SimpleDIContainer()

# Registrar singleton
container.register(
    IFontProvider,
    lambda c: PygameFontProvider(),
    singleton=True
)

# Resolver serviço
font_provider = container.resolve(IFontProvider)
```

### Testing com DI

```python
from unittest.mock import Mock

def test_app():
    mock_window = Mock(spec=IWindowManager)
    mock_provider = Mock(spec=ITelemetryProvider)
    mock_fonts = Mock(spec=IFontProvider)
    
    app = OverlayApp(
        window=mock_window,
        provider=mock_provider,
        font_provider=mock_fonts
    )
    
    app.setup()
    # Testes com mocks...
```
