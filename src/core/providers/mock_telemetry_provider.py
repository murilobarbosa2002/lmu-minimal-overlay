import time 
import time
import random
from dataclasses import replace
from src .core .providers .i_telemetry_provider import ITelemetryProvider
from src .core .domain .telemetry_data import TelemetryData
from src .core .domain .simulation .physics_engine import PhysicsEngine
from src .core .domain .simulation .track_generator import TrackGenerator
from src.core.infrastructure.config_manager import ConfigManager
from src.core.domain.constants import (
    INITIAL_INDEX,
    INITIAL_PROGRESS,
    INITIAL_TIMESTAMP,
    LERP_MAX,
    FFB_MIN,
    FFB_MAX,
    ROAD_NOISE_MIN,
    ROAD_NOISE_MAX,
    CORNER_NOISE_MIN,
    CORNER_NOISE_MAX
)


class MockTelemetryProvider (ITelemetryProvider ):
    def __init__ (self, config: ConfigManager = None):
        self ._start_time =time .time ()
        self ._last_update =time .time ()

        config = config or ConfigManager()
        conversion_config = config.get_config("conversion", {})
        self._steering_degrees_full_lock = conversion_config.get("steering_degrees_full_lock", 540.0)
        self._lateral_g_speed_divisor = conversion_config.get("lateral_g_speed_divisor", 100.0)

        self ._physics =PhysicsEngine (config)
        self ._track =TrackGenerator .generate_track ()

        self ._segment_index =INITIAL_INDEX
        self ._segment_progress =INITIAL_PROGRESS
        self ._segment_start_time =time .time ()

        defaults = config.get_defaults("telemetry")

        self .data =TelemetryData (
        speed =defaults.get("speed", 0.0),
        rpm =defaults.get("rpm", 0),
        max_rpm =defaults.get("max_rpm", 8000),
        gear =1,
        throttle_pct =defaults.get("throttle_pct", 0.0),
        brake_pct =defaults.get("brake_pct", 0.0),
        clutch_pct =defaults.get("clutch_pct", 0.0),
        steering_angle =defaults.get("steering_angle", 0.0),
        ffb_level =defaults.get("ffb_level", 0.0),
        timestamp =INITIAL_TIMESTAMP 
        )

    def _update_data (self )->None :
        current_time =time .time ()
        dt =current_time -self ._last_update 
        self ._last_update =current_time 

        segment =self ._track [self ._segment_index ]
        segment_elapsed =current_time -self ._segment_start_time 
        progress =segment_elapsed /segment .duration 

        if progress >=LERP_MAX:
            self ._segment_index =(self ._segment_index +1 )%len (self ._track )
            self ._segment_start_time =current_time 
            segment =self ._track [self ._segment_index ]
            progress =INITIAL_PROGRESS 

        self ._physics .update (dt ,segment ,progress )

        self .data .speed =self ._physics .speed 
        self .data .rpm =int (self ._physics .rpm )
        self .data .gear =self ._physics .gear 
        self .data .throttle_pct =self ._physics .throttle 
        self .data .brake_pct =self ._physics .brake 
        self .data .steering_angle =self ._physics .steering *self._steering_degrees_full_lock 

        lateral_g = self._physics.steering * (self._physics.speed / self._lateral_g_speed_divisor)
        
        road_noise = random.uniform(ROAD_NOISE_MIN, ROAD_NOISE_MAX)
        if 'CORNER' in segment.type:
             road_noise += random.uniform(CORNER_NOISE_MIN, CORNER_NOISE_MAX) * abs(self._physics.steering)
             
        self.data.ffb_level = max(FFB_MIN, min(FFB_MAX, lateral_g + road_noise))

        self .data .timestamp =current_time -self ._start_time 

    def get_data (self )->TelemetryData :
        self ._update_data ()
        return replace (self .data )

    def is_available (self )->bool :
        return True 

    def connect (self )->None :
        pass 

    def disconnect (self )->None :
        pass 

