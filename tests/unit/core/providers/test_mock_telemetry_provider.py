import pytest
import time
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider
from src.core.domain.telemetry_data import TelemetryData


def test_mock_provider_is_available():
    """Mock provider is always available"""
    provider = MockTelemetryProvider()
    assert provider.is_available() is True


def test_mock_provider_connect_disconnect():
    """Connect and disconnect do not fail"""
    provider = MockTelemetryProvider()
    provider.connect()
    provider.disconnect()


def test_mock_provider_get_data_returns_valid_data():
    """get_data returns valid TelemetryData"""
    provider = MockTelemetryProvider()
    data = provider.get_data()
    
    assert isinstance(data, TelemetryData)
    assert data.max_rpm == 8000
    assert 1 <= data.gear <= 6
    assert 0.0 <= data.throttle_pct <= 1.0
    assert 0.0 <= data.brake_pct <= 1.0
    assert 0.0 <= data.clutch_pct <= 1.0


def test_mock_provider_data_changes_over_time():
    """Data changes over time"""
    provider = MockTelemetryProvider()
    provider.connect()
    # Initial update
    d1_speed = provider.get_data().speed
    d1_rpm = provider.get_data().rpm
    d1_timestamp = provider.get_data().timestamp
    
    # Wait a bit
    time.sleep(0.1)
    
    d2_speed = provider.get_data().speed
    d2_rpm = provider.get_data().rpm
    d2_timestamp = provider.get_data().timestamp
    
    # Data MUST change (speed increases in ACCEL state usually)
    # But if it was max speed it might not, or randomly. 
    # Our logic accelerates ~1.5 kph per tick.
    # We modify same object instance in _update_data.
    # So checking d1 vs d2 is pointless if d1 references same object.
    # We need to capture values.
    assert d1_timestamp != d2_timestamp
    assert d1_speed != d2_speed or d1_rpm != d2_rpm


def test_mock_provider_data_simulation():
    """Verify the simulation logic accelerates and shifts"""
    provider = MockTelemetryProvider()
    provider.connect()
    # Reset state manually if needed or just simulate
    
    initial_speed = provider.data.speed
    initial_gear = provider.data.gear
    
    # Run multiple updates
    import time
    time.sleep(0.1)
    provider.get_data()
    
    final_speed = provider.data.speed
    final_gear = provider.data.gear
    
    # Should have accelerated
    assert final_speed > initial_speed

def test_mock_provider_data_within_ranges():
    """All values are within expected ranges"""

    provider = MockTelemetryProvider()
    provider.connect()
    data = provider.get_data()
    
    assert 0 <= data.speed <= 350
    # Gear is roughly 0-6
    assert -1 <= data.gear <= 7
    assert 0 <= data.rpm <= 10000
    assert 0.0 <= data.throttle_pct <= 1.0
    assert 0.0 <= data.brake_pct <= 1.0

def test_mock_provider_gear_branches_coverage():
    """
    Tests all branches of the gear calculation logic manually injecting state.
    White-box testing is more appropriate here than time simulation.
    """
    provider = MockTelemetryProvider()
    
    # Init state
    provider._state = 'ACCEL'
    
    # CASE 1: Gear 1 -> 2 Shift
    # speed > 70
    provider.data.gear = 1
    provider.data.speed = 71
    provider.get_data() # Logic should update gear
    assert provider.data.gear == 2
    
    # CASE 2: Gear 2 -> 3 Shift
    # speed > 120
    provider.data.gear = 2
    provider.data.speed = 121
    provider.get_data()
    assert provider.data.gear == 3
    
    # CASE 3: Braking State Trigger
    # speed >= 280
    provider.data.gear = 6
    provider.data.speed = 280
    provider.get_data()
    assert provider._state == 'BRAKE'
    
    # CASE 4: Braking Logic / Downshift
    provider._state = 'BRAKE'
    # Gear 3 -> 2 (Downshift when speed < (120 - 10) = 110)
    provider.data.gear = 3
    provider.data.speed = 100
    provider.get_data()
    assert provider.data.gear == 2
    
    # CASE 5: Accel Reset
    # speed <= 60
    provider.data.speed = 50
    provider.get_data()
    assert provider._state == 'ACCEL'
    assert provider.data.gear == 2
