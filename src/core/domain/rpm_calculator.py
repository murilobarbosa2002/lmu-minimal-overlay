from src.core.domain.constants import KMH_TO_MS, SECONDS_TO_MINUTES, MINIMUM_SPEED_THRESHOLD, DEFAULT_GEAR_RATIO


class RPMCalculator:
    def __init__(
        self, gear_ratios: dict[int, float], final_drive: float, wheel_circumference: float, idle_rpm: int, max_rpm: int
    ):
        self._gear_ratios = gear_ratios
        self._final_drive = final_drive
        self._wheel_circumference = wheel_circumference
        self._idle_rpm = idle_rpm
        self._max_rpm = max_rpm

    def calculate(self, speed_kmh: float, gear: int) -> int:
        if gear == 0:
            return self._idle_rpm

        if gear == -1:
            speed_ms = abs(speed_kmh) / KMH_TO_MS
            gear_ratio = abs(self._gear_ratios[-1])
        else:
            speed_ms = speed_kmh / KMH_TO_MS
            gear_ratio = self._gear_ratios.get(gear, DEFAULT_GEAR_RATIO)

        if speed_ms < MINIMUM_SPEED_THRESHOLD:
            return self._idle_rpm

        rpm = (speed_ms * SECONDS_TO_MINUTES / self._wheel_circumference) * gear_ratio * self._final_drive

        return int(max(self._idle_rpm, min(self._max_rpm, rpm)))
