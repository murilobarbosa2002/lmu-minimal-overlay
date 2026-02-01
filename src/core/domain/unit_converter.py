from src.core.domain.constants import KM_TO_MILES, MILES_TO_KM


def km_to_mph(speed_kph: float) -> float:
    return speed_kph * KM_TO_MILES


def mph_to_km(speed_mph: float) -> float:
    return speed_mph * MILES_TO_KM
