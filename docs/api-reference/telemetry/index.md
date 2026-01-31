# Sistema de Telemetria

API de aquisição e normalização de dados.

## Componentes

- [Providers](providers.md) - ITelemetryProvider, SharedMemory, Mock
- [Data Models](data-models.md) - TelemetryData
- [Normalização](normalization.md) - Funções de normalização

## Interface ITelemetryProvider

```python
class ITelemetryProvider(ABC):
    @abstractmethod
    def get_data(self) -> TelemetryData:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
```

## Implementações

- **SharedMemoryProvider**: Produção Windows
- **MockTelemetryProvider**: Desenvolvimento WSL

## Próximos Passos

- [Providers](providers.md)
- [Data Models](data-models.md)
- [Normalização](normalization.md)
