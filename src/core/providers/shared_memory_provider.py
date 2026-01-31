from src.core.providers.i_telemetry_provider import ITelemetryProvider
from src.core.domain.telemetry_data import TelemetryData

# LMU uses standard rFactor 2 shared memory map name
SHARED_MEMORY_NAME = "$LMuTelem$"


class SharedMemoryProvider(ITelemetryProvider):
    def is_available(self) -> bool:
        """
        Check if shared memory is available.
        
        For this stub implementation (Phase 1), it always returns False.
        """
        return False

    def connect(self) -> None:
        raise NotImplementedError("SharedMemoryProvider not implemented in Phase 1")

    def disconnect(self) -> None:
        pass

    def get_data(self) -> TelemetryData:
        raise RuntimeError("Provider not connected")
