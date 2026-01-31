from src .core .providers .i_telemetry_provider import ITelemetryProvider 
from src .core .domain .telemetry_data import TelemetryData 

SHARED_MEMORY_NAME ="$LMuTelem$"


class SharedMemoryProvider (ITelemetryProvider ):
    def is_available (self )->bool :
        return False 

    def connect (self )->None :
        raise NotImplementedError ("SharedMemoryProvider not implemented in Phase 1")

    def disconnect (self )->None :
        pass 

    def get_data (self )->TelemetryData :
        raise RuntimeError ("Provider not connected")
