from src.core.domain.constants import (
    BYTE_MAX,
    WORD_MAX,
    NORMALIZED_MIN,
    NORMALIZED_MAX
)


def normalize_byte(value: int) -> float:
    if not 0 <= value <= BYTE_MAX:
        raise ValueError(f"value deve estar entre 0 e {BYTE_MAX}, recebido: {value}")
    return value / BYTE_MAX


def normalize_word(value: int) -> float:
    if not 0 <= value <= WORD_MAX:
        raise ValueError(f"value deve estar entre 0 e {WORD_MAX}, recebido: {value}")
    return value / WORD_MAX


def denormalize_byte(value: float) -> int:
    if not NORMALIZED_MIN <= value <= NORMALIZED_MAX:
        raise ValueError(f"value deve estar entre {NORMALIZED_MIN} e {NORMALIZED_MAX}, recebido: {value}")
    return round(value * BYTE_MAX)


def denormalize_word(value: float) -> int:
    if not NORMALIZED_MIN <= value <= NORMALIZED_MAX:
        raise ValueError(f"value deve estar entre {NORMALIZED_MIN} e {NORMALIZED_MAX}, recebido: {value}")
    return round(value * WORD_MAX)


def clamp(value: float, min_val: float, max_val: float) -> float:
    if min_val > max_val:
        raise ValueError(f"min_val deve ser menor ou igual a max_val, recebido: min={min_val}, max={max_val}")
    return max(min_val, min(max_val, value))
