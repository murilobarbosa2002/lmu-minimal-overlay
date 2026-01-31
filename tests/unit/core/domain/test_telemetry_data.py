import pytest
from src.core.domain.telemetry_data import TelemetryData

def test_telemetry_data_creation():
    data = TelemetryData(
        speed=120.5,
        rpm=6000,
        max_rpm=8000,
        gear=3,
        throttle_pct=0.75,
        brake_pct=0.0,
        clutch_pct=0.0,
        steering_angle=45.0,
        ffb_level=0.5,
        timestamp=1234567890.0
    )
    assert data.speed == 120.5
    assert data.rpm == 6000
    assert data.gear == 3

def test_telemetry_data_validation_throttle():
    with pytest.raises(ValueError, match="throttle_pct deve estar entre"):
        TelemetryData(
            speed=0.0,
            rpm=0,
            max_rpm=8000,
            gear=0,
            throttle_pct=1.5,
            brake_pct=0.0,
            clutch_pct=0.0,
            steering_angle=0.0,
            ffb_level=0.0,
            timestamp=0.0
        )

def test_telemetry_data_validation_brake():
    with pytest.raises(ValueError, match="brake_pct deve estar entre"):
        TelemetryData(
            speed=0.0,
            rpm=0,
            max_rpm=8000,
            gear=0,
            throttle_pct=0.5,
            brake_pct=-0.1,
            clutch_pct=0.0,
            steering_angle=0.0,
            ffb_level=0.0,
            timestamp=0.0
        )

def test_telemetry_data_validation_clutch():
    with pytest.raises(ValueError, match="clutch_pct deve estar entre"):
        TelemetryData(
            speed=0.0,
            rpm=0,
            max_rpm=8000,
            gear=0,
            throttle_pct=0.5,
            brake_pct=0.0,
            clutch_pct=1.5,
            steering_angle=0.0,
            ffb_level=0.0,
            timestamp=0.0
        )

def test_telemetry_data_validation_steering():
    with pytest.raises(ValueError, match="steering_angle deve estar entre"):
        TelemetryData(
            speed=0.0,
            rpm=0,
            max_rpm=8000,
            gear=0,
            throttle_pct=0.5,
            brake_pct=0.0,
            clutch_pct=0.0,
            steering_angle=1000.0,
            ffb_level=0.0,
            timestamp=0.0
        )

def test_telemetry_data_str():
    data = TelemetryData(
        speed=100.0,
        rpm=5000,
        max_rpm=8000,
        gear=2,
        throttle_pct=0.5,
        brake_pct=0.2,
        clutch_pct=0.0,
        steering_angle=0.0,
        ffb_level=0.0,
        timestamp=0.0
    )
    result = str(data)
    assert "speed=100.0" in result
    assert "rpm=5000" in result
