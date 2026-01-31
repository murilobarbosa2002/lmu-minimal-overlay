# ConfigManager

Singleton de gerenciamento de configurações.

## Interface

```python
class ConfigManager(IConfigManager):
    def load_config(self) -> None:
        pass

    def save_config(self) -> None:
        pass

    def load_layout(self) -> None:
        pass

    def save_layout(self) -> None:
        pass

    def get_config(self, key: str, default: Any = None) -> Any:
        pass

    def set_config(self, key: str, value: Any) -> None:
        pass

    def get_layout(self, key: str, default: Any = None) -> Any:
        pass

    def set_layout(self, key: str, value: Any) -> None:
        pass
```

## Uso

```python
config = ConfigManager()

# Configuração (config.json)
version = config.get_config("version", "1.0.0")
config.set_config("update_interval_ms", 33)

# Layout (layout.json)
window_cfg = config.get_layout("window")
config.set_layout("widgets", widget_data_list)
```

## Singleton

Gerencia duas fontes de persistência:
- `config.json`: Configurações globais da aplicação.
- `layout.json`: Posição da janela e disposição dos widgets.

Implementa padrão Singleton via `__new__` thread-safe.

Veja [Architecture - Design Patterns](../../architecture/design-patterns.md).
