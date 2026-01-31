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

## Próximos Passos

- [Setup WSL](setup-wsl.md)
- [Padrões de Código](code-standards.md)
- [Testes](testing.md)
