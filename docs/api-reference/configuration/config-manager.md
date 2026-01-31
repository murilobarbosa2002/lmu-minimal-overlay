# ConfigManager

Singleton de gerenciamento de configurações.

## Interface

```python
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def get(self, key: str) -> Any:
        """Obtém valor de configuração."""
        pass
    
    def get_colors(self) -> Dict[str, List[int]]:
        """Obtém paleta de cores."""
        pass
    
    def save_layout(self, widgets: List[Widget]) -> None:
        """Salva layout de widgets."""
        pass
    
    def reload(self) -> None:
        """Recarrega configurações."""
        pass
```

## Uso

```python
config = ConfigManager()
colors = config.get_colors()
ffb_threshold = config.get("thresholds.ffb_clipping")
```

## Singleton

Apenas uma instância existe. Chamadas subsequentes retornam mesma instância.

Veja [Architecture - Design Patterns](../../architecture/design-patterns.md).
