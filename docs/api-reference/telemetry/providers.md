# Telemetry Providers

Implementações de ITelemetryProvider.

## ITelemetryProvider

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

## SharedMemoryProvider

Produção Windows.

```python
provider = SharedMemoryProvider()
if provider.connect():
    data = provider.get_data()
```

## MockTelemetryProvider

Desenvolvimento WSL.

```python
provider = MockTelemetryProvider()
provider.connect()
data = provider.get_data()
```

Veja [Architecture - Layers](../../architecture/layers.md).
