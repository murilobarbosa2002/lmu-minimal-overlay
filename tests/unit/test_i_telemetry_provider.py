import pytest
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.domain.telemetry_data import TelemetryData


def test_cannot_instantiate_interface():
    """Abstract interface cannot be instantiated directly"""
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        ITelemetryProvider()


def test_concrete_implementation_must_implement_all_methods():
    """Concrete implementation must implement all abstract methods"""
    
    class IncompleteProvider(ITelemetryProvider):
        def get_data(self) -> TelemetryData:
            return TelemetryData(
                speed=0.0,
                rpm=0,
                max_rpm=8000,
                gear=1,
                throttle_pct=0.0,
                brake_pct=0.0,
                clutch_pct=0.0,
                steering_angle=0.0,
                ffb_level=0.0,
                timestamp=0.0
            )
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteProvider()


def test_concrete_implementation_works():
    """Complete concrete implementation should work"""
    
    class CompleteProvider(ITelemetryProvider):
        def get_data(self) -> TelemetryData:
            return TelemetryData(
                speed=100.0,
                rpm=5000,
                max_rpm=8000,
                gear=3,
                throttle_pct=0.75,
                brake_pct=0.0,
                clutch_pct=0.0,
                steering_angle=45.0,
                ffb_level=0.8,
                timestamp=1.0
            )
        
        def is_available(self) -> bool:
            return True
        
        def connect(self) -> None:
            pass
        
        def disconnect(self) -> None:
            pass
    
    provider = CompleteProvider()
    assert provider.is_available() is True
    
    data = provider.get_data()
    assert isinstance(data, TelemetryData)
    assert data.speed == 100.0
    assert data.rpm == 5000


def test_interface_has_correct_method_signatures():
    """Verifies that the interface has the correct methods"""
    assert hasattr(ITelemetryProvider, 'get_data')
    assert hasattr(ITelemetryProvider, 'is_available')
    assert hasattr(ITelemetryProvider, 'connect')
    assert hasattr(ITelemetryProvider, 'disconnect')


def test_all_methods_coverage():
    """Tests concrete implementation calling all methods for 100% coverage"""
    
    class FullCoverageProvider(ITelemetryProvider):
        def __init__(self):
            self.connected = False
        
        def get_data(self) -> TelemetryData:
            if not self.connected:
                raise RuntimeError("Provider não conectado")
            return TelemetryData(
                speed=120.0,
                rpm=6000,
                max_rpm=8000,
                gear=4,
                throttle_pct=0.8,
                brake_pct=0.0,
                clutch_pct=0.0,
                steering_angle=-30.0,
                ffb_level=0.9,
                timestamp=2.0
            )
        
        def is_available(self) -> bool:
            return True
        
        def connect(self) -> None:
            self.connected = True
        
        def disconnect(self) -> None:
            self.connected = False
    
    provider = FullCoverageProvider()
    
    assert provider.is_available() is True
    
    with pytest.raises(RuntimeError, match="Provider não conectado"):
        provider.get_data()
    
    provider.connect()
    assert provider.connected is True
    
    data = provider.get_data()
    assert isinstance(data, TelemetryData)
    assert data.speed == 120.0
    assert data.rpm == 6000
    assert data.gear == 4
    
    provider.disconnect()
    assert provider.connected is False
