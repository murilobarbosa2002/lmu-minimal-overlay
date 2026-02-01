from dataclasses import dataclass
from src.core.domain.constants import (
    PERCENTAGE_MIN,
    PERCENTAGE_MAX,
    STEERING_ANGLE_MIN,
    STEERING_ANGLE_MAX,
)


@dataclass
class TelemetryData:
    speed: float
    gear: int
    rpm: int
    max_rpm: int
    throttle_pct: float
    brake_pct: float
    clutch_pct: float
    steering_angle: float
    ffb_level: float
    timestamp: float

    def __post_init__(self):
        if not PERCENTAGE_MIN <= self.throttle_pct <= PERCENTAGE_MAX:
            raise ValueError(
                f"throttle_pct deve estar entre {PERCENTAGE_MIN} e {PERCENTAGE_MAX}, recebido: {self.throttle_pct}"
            )
        if not PERCENTAGE_MIN <= self.brake_pct <= PERCENTAGE_MAX:
            raise ValueError(
                f"brake_pct deve estar entre {PERCENTAGE_MIN} e {PERCENTAGE_MAX}, recebido: {self.brake_pct}"
            )
        if not PERCENTAGE_MIN <= self.clutch_pct <= PERCENTAGE_MAX:
            raise ValueError(
                f"clutch_pct deve estar entre {PERCENTAGE_MIN} e {PERCENTAGE_MAX}, recebido: {self.clutch_pct}"
            )
        if not STEERING_ANGLE_MIN <= self.steering_angle <= STEERING_ANGLE_MAX:
            raise ValueError(
                f"steering_angle deve estar entre {STEERING_ANGLE_MIN} e {STEERING_ANGLE_MAX}, recebido: {self.steering_angle}"
            )

    def __str__(self) -> str:
        return (
            f"TelemetryData(speed={self.speed:.1f}, rpm={self.rpm}, gear={self.gear}, "
            f"throttle={self.throttle_pct:.2f}, brake={self.brake_pct:.2f})"
        )
