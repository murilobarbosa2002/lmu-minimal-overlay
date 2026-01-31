import pytest
from src.core.providers.shared_memory_provider import SharedMemoryProvider
from src.core.providers.i_telemetry_provider import ITelemetryProvider

def test_shared_memory_provider_implements_interface():
    """Verify that SharedMemoryProvider implements ITelemetryProvider"""
    assert issubclass(SharedMemoryProvider, ITelemetryProvider)
    provider = SharedMemoryProvider()
    assert isinstance(provider, ITelemetryProvider)

def test_shared_memory_provider_is_not_available():
    """Verify that is_available always returns False for stub"""
    provider = SharedMemoryProvider()
    assert provider.is_available() is False

def test_shared_memory_provider_connect_raises_error():
    """Verify that connect raises NotImplementedError"""
    provider = SharedMemoryProvider()
    with pytest.raises(NotImplementedError):
        provider.connect()

def test_shared_memory_provider_get_data_raises_error():
    """Verify that get_data raises RuntimeError (not connected)"""
    provider = SharedMemoryProvider()
    with pytest.raises(RuntimeError):
        provider.get_data()
