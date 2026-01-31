# Sistema de Configuração

API de configuração e persistência.

## Componentes

- [config.json](config-json.md) - Configurações globais
- [layout.json](layout-json.md) - Posições de widgets
- [ConfigManager](config-manager.md) - Singleton de configuração

## ConfigManager

```python
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def get(self, key: str) -> Any:
        pass
    
    def save_layout(self, widgets: List[Widget]) -> None:
        pass
```

## Arquivos

- **config.json**: Cores, thresholds, performance
- **layout.json**: Posições e visibilidade

## Próximos Passos

- [config.json](config-json.md)
- [layout.json](layout-json.md)
- [ConfigManager](config-manager.md)
