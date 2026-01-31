import time
import random
from dataclasses import replace
from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.domain.telemetry_data import TelemetryData
from src.core.domain.simulation.physics_engine import PhysicsEngine
from src.core.domain.simulation.track_generator import TrackGenerator


class MockTelemetryProvider(ITelemetryProvider):
    def __init__(self):
        self._start_time = time.time()
        self._last_update = time.time()
        
        self._physics = PhysicsEngine()
        self._segments = TrackGenerator.generate_track()
        
        self._segment_index = 0
        self._segment_start_time = time.time()
        
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
        
        segment = self._segments[self._segment_index]
        segment_elapsed = current_time - self._segment_start_time
        progress = segment_elapsed / segment.duration
        
        if progress >= 1.0:
            self._segment_index = (self._segment_index + 1) % len(self._segments)
            self._segment_start_time = current_time
            segment = self._segments[self._segment_index]
            progress = 0.0
            
        self._physics.update(dt, segment, progress)
        
        self.data.speed = self._physics.speed
        self.data.rpm = int(self._physics.rpm)
        self.data.gear = self._physics.gear
        self.data.throttle_pct = self._physics.throttle
        self.data.brake_pct = self._physics.brake
        self.data.steering_angle = self._physics.steering * 540.0
        
        g_force = abs(self._physics.steering * self._physics.speed * 0.05)
        road_noise = random.random() * 0.05
        raw_ffb = (g_force * 0.8) + (2.0 if self._physics.steering != 0 and 'CORNER' in segment.type else 0.0) * 0.1
        self.data.ffb_level = min(1.0, raw_ffb + road_noise)
        
        self.data.timestamp = current_time - self._start_time

    def get_data(self) -> TelemetryData:
        self._update_data()
        return replace(self.data)

    def is_available(self) -> bool:
        return True

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

