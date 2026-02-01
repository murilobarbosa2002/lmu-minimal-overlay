from src.core.domain.telemetry_data import TelemetryData


def test_telemetry_data_full_workflow():
    raw_data = {
        "speed": 150.0,
        "rpm": 7000,
        "max_rpm": 8000,
        "gear": 4,
        "throttle_pct": 1.0,
        "brake_pct": 0.0,
        "clutch_pct": 0.0,
        "steering_angle": -180.0,
        "ffb_level": 0.8,
        "timestamp": 1234567890.0,
    }
    data = TelemetryData(**raw_data)
    assert data.speed == 150.0
    assert data.rpm == 7000
    assert data.gear == 4
    str_repr = str(data)
    assert "150.0" in str_repr
