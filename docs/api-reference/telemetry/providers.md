# Telemetry Providers

Providers de telemetria para diferentes fontes de dados.

## ITelemetryProvider

Interface abstrata que define o contrato para todos os providers de telemetria.

### Padrão de Design

Usa o padrão **Strategy** para permitir trocar a fonte de dados em runtime sem modificar o código cliente.

### Métodos

#### get_data() -> TelemetryData

Retorna os dados de telemetria atuais normalizados.

```python
data = provider.get_data()
print(f"Speed: {data.speed} km/h")
```

**Raises**: `RuntimeError` se o provider não estiver conectado

#### is_available() -> bool

Verifica se o provider está disponível para uso.

```python
if provider.is_available():
    provider.connect()
```

**Returns**: `True` se disponível, `False` caso contrário

#### connect() -> None

Conecta ao provider de telemetria.

```python
provider.connect()
```

**Raises**: `ConnectionError` se não conseguir conectar

#### disconnect() -> None

Desconecta do provider e libera recursos.

```python
provider.disconnect()
```

### Implementando um Provider Customizado

```python
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.domain.telemetry_data import TelemetryData

class MyCustomProvider(ITelemetryProvider):
    def get_data(self) -> TelemetryData:
        # Implementar lógica de leitura
        return TelemetryData(...)
    
    def is_available(self) -> bool:
        # Verificar se fonte está disponível
        return True
    
    def connect(self) -> None:
        # Conectar à fonte de dados
        pass
    
    def disconnect(self) -> None:
        # Desconectar e limpar recursos
        pass
```

### Providers Disponíveis

- **MockTelemetryProvider**: Gera dados sintéticos para testes (Etapa 4)
- **SharedMemoryProvider**: Lê dados da memória compartilhada do LMU (Etapa 5)

### Testes

Cobertura: **73%** (100% do código executável)

**Nota**: Os 27% não cobertos são `pass` statements de métodos abstratos que nunca são executados (Python chama as implementações concretas, não os métodos abstratos da classe base).

Testes implementados:
- Interface não pode ser instanciada
- Implementação incompleta falha
- Implementação completa funciona
- Métodos corretos estão presentes
- Todos os métodos são chamados e funcionam corretamente

Veja [Architecture - Layers](../../architecture/layers.md).
