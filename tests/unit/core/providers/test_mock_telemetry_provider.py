import pytest
import time
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider
from src.core.domain.simulation.track_segment import TrackSegment
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


def test_mock_provider_physics_acceleration():
    """Verify car accelerates on straights"""
    provider = MockTelemetryProvider()
    
    # Force a STRAIGHT segment
    provider._track = [TrackSegment(10.0, 300.0, 0.0, 'STRAIGHT', 0.0)]
    provider._segment_index = 0
    provider._segment_start_time = time.time()
    
    # Reset physics
    provider._physics.speed = 100.0
    provider._physics.gear = 3
    provider._physics.rpm = 4000
    provider._last_update = time.time()
    
    # Simulate 0.5s step
    time.sleep(0.01) # Ensure time diff
    provider._physics.update(0.5, provider._track[0], 0.1)
    
    # Should have throttle and acceleration
    assert provider._physics.throttle > 0.0
    assert provider._physics.speed > 100.0


def test_mock_provider_physics_braking():
    """Verify car brakes on corner entry"""
    provider = MockTelemetryProvider()
    
    # Force a BRAKING segment (Entry into slow corner)
    provider._track = [TrackSegment(5.0, 60.0, 200.0, 'CORNER_ENTRY', 0.0)]
    provider._segment_index = 0
    provider._segment_start_time = time.time()
    
    # Reset physics high speed
    provider._physics.speed = 200.0
    provider._physics.gear = 5
    provider._physics.rpm = 7000
    provider._last_update = time.time()
    
    # Simulate 0.5s step
    provider._physics.update(0.5, provider._track[0], 0.1)
    
    # Should have brake and deceleration
    assert provider._physics.brake > 0.0
    assert provider._physics.throttle == 0.0
    assert provider._physics.speed < 200.0


def test_mock_provider_steering_logic():
    """Verify steering matches curvature"""
    provider = MockTelemetryProvider()
    
    # Force a CORNER segment
    curvature = 0.8
    provider._track = [TrackSegment(5.0, 100.0, 100.0, 'CORNER_MID', curvature)]
    
    # Simulate flow
    current_time = time.time()
    provider._last_update = current_time - 0.1
    provider._segment_start_time = current_time - 2.5 # 50% progress
    
    provider.get_data()
    
    # Steering should be non-zero and match curvature direction
    assert provider.data.steering_angle > 0


def test_mock_provider_gear_shift_logic():
    """Verify automatic shifting based on RPM"""
    provider = MockTelemetryProvider()
    
    # CASE 1: Upshift
    provider._physics.speed = 200.0
    provider._physics.gear = 3
    # High RPM for gear 3
    # Ratio gear 3 is 26 speed/1000rpm -> 200/26 * 1000 = ~7692 RPM
    # We force logic loop
    provider._physics.update(0.1, TrackSegment(1.0, 300.0, 0.0, 'STRAIGHT', 0.0), 0.5)
    
    # If RPM > 7800 it shifts, let's force speed higher to trigger it
    provider._physics.speed = 210.0 # ~8076 RPM
    provider._physics.update(0.1, TrackSegment(1.0, 300.0, 0.5, 'STRAIGHT', 0.0), 0.5)
    
    assert provider._physics.gear > 3

def test_mock_provider_track_looping():
    """Verify track segments loop correctly"""
    provider = MockTelemetryProvider()
    
    # Force 1 short segment
    provider._track = [TrackSegment(1.0, 100.0, 100.0, 'STRAIGHT', 0.0)]
    provider._segment_index = 0
    provider._segment_start_time = time.time() - 1.1 # Past duration
    
    # Trigger update
    provider.get_data()
    
    # Should have advanced segment (index 0 again since len=1, but time reset)
    # Actually if len=1 it goes to 0. 
    # Let's verify _segment_start_time changed to near current time
    assert provider._segment_start_time > (time.time() - 0.5)


def test_mock_provider_data_within_ranges():
    """All values are within expected ranges"""
    provider = MockTelemetryProvider()
    data = provider.get_data()
    
    assert 0 <= data.speed <= 350
    assert 1 <= data.gear <= 6 # Updated range
    assert 0 <= data.rpm <= 10000
    assert 0.0 <= data.throttle_pct <= 1.0
    assert 0.0 <= data.brake_pct <= 1.0
    assert -900 <= data.steering_angle <= 900
