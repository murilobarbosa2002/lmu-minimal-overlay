import time
import math
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.domain.telemetry_data import TelemetryData


class MockTelemetryProvider(ITelemetryProvider):
    def __init__(self):
        self._start_time = time.time()

    def get_data(self) -> TelemetryData:
        t = time.time() - self._start_time
        
        speed = 100 + 100 * math.sin(t * 0.5)
        rpm_base = 4500 + 3500 * math.sin(t * 0.7)
        rpm = int(max(1000, min(8000, rpm_base)))
        
        if rpm < 2000:
            gear = 1
        elif rpm < 3000:
            gear = 2
        elif rpm < 4000:
            gear = 3
        elif rpm < 5000:
            gear = 4
        elif rpm < 6000:
            gear = 5
        else:
            gear = 6
        
        throttle_pct = max(0.0, min(1.0, 0.5 + 0.5 * math.sin(t * 0.8)))
        brake_pct = max(0.0, min(1.0, 0.5 - 0.5 * math.sin(t * 0.8)))
        clutch_pct = 0.0
        steering_angle = 450 * math.sin(t * 0.3)
        ffb_level = 0.5 + 0.5 * abs(math.sin(t * 0.3))
        
        return TelemetryData(
            speed=speed,
            rpm=rpm,
            max_rpm=8000,
            gear=gear,
            throttle_pct=throttle_pct,
            brake_pct=brake_pct,
            clutch_pct=clutch_pct,
            steering_angle=steering_angle,
            ffb_level=ffb_level,
            timestamp=t
        )

    def is_available(self) -> bool:
        return True

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass
