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
    
    data1 = provider.get_data()
    time.sleep(0.1)
    data2 = provider.get_data()
    
    assert data1.timestamp != data2.timestamp
    assert data1.speed != data2.speed or data1.rpm != data2.rpm


def test_mock_provider_data_within_ranges():
    """All values are within expected ranges"""

    provider = MockTelemetryProvider()
    
    for _ in range(10):
        data = provider.get_data()
        
        assert 0.0 <= data.speed <= 200.0
        assert 1000 <= data.rpm <= 8000
        assert 1 <= data.gear <= 6
        assert 0.0 <= data.throttle_pct <= 1.0
        assert 0.0 <= data.brake_pct <= 1.0
        assert 0.0 <= data.clutch_pct <= 1.0
        assert -900.0 <= data.steering_angle <= 900.0
        assert 0.0 <= data.ffb_level <= 1.0
        
        time.sleep(0.05)


from unittest.mock import patch

def test_mock_provider_gear_branches_coverage():
    """
    Tests all branches of the gear calculation logic using a time mock.
    
    The MockTelemetryProvider calculates the current gear based on the simulated RPM value,
    which is generated using a sine wave function driven by the current time.
    To ensure 100% code coverage and verify the logic for all gears (1 through 6),
    we mock `time.time` to return specific values that result in the required RPM ranges.
    """
    provider = MockTelemetryProvider()
    
    # RPM Calculation Formula: RPM = 4500 + 3500 * sin(0.7 * t)
    # We select specific 't' values to target each gear's RPM range.
    
    # CASE 1: Gear 4
    # Condition: 4000 <= RPM < 5000
    # At t=0, sin(0)=0, so RPM = 4500, which falls squarely into Gear 4 range.
    with patch('time.time', return_value=provider._start_time + 0):
        assert provider.get_data().gear == 4

    # CASE 2: Gear 6
    # Condition: RPM >= 6000
    # At t=1.0, 0.7 rad, sin(0.7) ~= 0.64. RPM = 4500 + 3500 * 0.64 ~= 6740.
    # This value is > 6000, so it should trigger Gear 6.
    with patch('time.time', return_value=provider._start_time + 1.0):
        data = provider.get_data()
        assert data.gear == 6
        
    # CASE 3: Gear 5
    # Condition: 5000 <= RPM < 6000
    # We need a sine value around 0.28 to get ~5500 RPM.
    # At t=0.4, 0.28 rad, sin(0.28) ~= 0.276. RPM = 4500 + 3500 * 0.276 ~= 5466.
    # This falls into Gear 5 range.
    with patch('time.time', return_value=provider._start_time + 0.4):
        data = provider.get_data()
        assert data.gear == 5
        
    # CASE 4: Gear 3
    # Condition: 3000 <= RPM < 4000
    # We need a negative sine value. At t=5.0, 3.5 rad.
    # sin(3.5) ~= -0.35. RPM = 4500 + 3500 * (-0.35) ~= 3275.
    # This falls into Gear 3 range.
    with patch('time.time', return_value=provider._start_time + 5.0):
        data = provider.get_data()
        assert data.gear == 3
        
    # CASE 5: Gear 2
    # Condition: 2000 <= RPM < 3000
    # At t=5.5, 3.85 rad. sin(3.85) ~= -0.65.
    # RPM = 4500 + 3500 * (-0.65) ~= 2225.
    # This falls into Gear 2 range.
    with patch('time.time', return_value=provider._start_time + 5.5):
        data = provider.get_data()
        assert data.gear == 2
        
    # CASE 6: Gear 1
    # Condition: RPM < 2000
    # At t=6.5, 4.55 rad. sin(4.55) ~= -0.98.
    # RPM = 4500 + 3500 * (-0.98) ~= 1070.
    # This is the lowest range, triggering Gear 1.
    with patch('time.time', return_value=provider._start_time + 6.5):
        data = provider.get_data()
        assert data.gear == 1
