import time
import math
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.domain.telemetry_data import TelemetryData


class MockTelemetryProvider(ITelemetryProvider):
    def __init__(self):
        self._start_time = time.time()
        self._last_update = time.time()
        self._state = 'ACCEL'
        
        self.data = TelemetryData(
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

    def _update_data(self) -> None:
        current_time = time.time()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        shift_points = {1: 70, 2: 120, 3: 160, 4: 200, 5: 240, 6: 285}
        
        current_speed = self.data.speed
        current_gear = self.data.gear
        
        if self._state == 'ACCEL':
            accel_rate = 30.0 * dt
            current_speed += accel_rate
            
            if current_gear < 6:
                if current_speed > shift_points.get(current_gear, 999):
                    current_gear += 1
            
            if current_speed >= 280:
                self._state = 'BRAKE'
                
        else:
            decel_rate = 60.0 * dt
            current_speed -= decel_rate
            
            if current_gear > 1:
                prev_gear_max = shift_points.get(current_gear - 1, 0)
                if current_speed < (prev_gear_max - 10):
                    current_gear -= 1
            
            if current_speed <= 60:
                self._state = 'ACCEL'
                current_gear = 2
                
        current_speed = max(0, min(current_speed, 300))
        
        self.data.speed = current_speed
        self.data.gear = int(current_gear)
        
        self.data.rpm = int(4000 + (current_speed % 40) * 100) 
        
        self.data.throttle_pct = 1.0 if self._state == 'ACCEL' else 0.0
        self.data.brake_pct = 1.0 if self._state == 'BRAKE' else 0.0
        
        self.data.timestamp = current_time - self._start_time

    def get_data(self) -> TelemetryData:
        self._update_data()
        from dataclasses import replace
        return replace(self.data)

    def is_available(self) -> bool:
        return True

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass
