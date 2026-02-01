import time
from src.core.providers.mock_telemetry_provider import MockTelemetryProvider


def test_mock_provider_workflow():
    """Workflow completo: connect → get_data → disconnect"""
    provider = MockTelemetryProvider()

    assert provider.is_available() is True

    provider.connect()

    data1 = provider.get_data()
    assert data1.speed >= 0.0
    assert data1.rpm >= 800

    time.sleep(0.1)

    data2 = provider.get_data()
    assert data2.timestamp > data1.timestamp

    provider.disconnect()
