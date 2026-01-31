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


## MockTelemetryProvider

Provider para testes que gera dados sintéticos realistas baseados em funções senoidais.
Útil para desenvolvimento sem o simulador rodando.

### Uso

```python
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider
import time

provider = MockTelemetryProvider()
provider.connect()  # No-op

while True:
    data = provider.get_data()
    print(f"RPM: {data.rpm}, Speed: {data.speed:.1f}")
    time.sleep(0.1)
```

### Dados Gerados

Todos os dados variam suavemente ao longo do tempo (baseado em `time.time()`):

- **Speed**: 0 a 200 km/h
- **RPM**: 1000 a 8000
- **Gear**: 1 a 6 (calculado baseado no RPM)
- **Inputs**: Throttle/Brake (0.0 a 1.0), Steering (-900° a +900°)
- **FFB**: 0.0 a 1.0

### Testes

Cobertura: **100%**

Testes implementados:
- Workflow completo (connect/get/disconnect)
- Validação de ranges de todos os campos
- Cobertura de todas as marchas (1-6)
- Consistência temporal dos dados

Veja [Architecture - Layers](../../architecture/layers.md).
