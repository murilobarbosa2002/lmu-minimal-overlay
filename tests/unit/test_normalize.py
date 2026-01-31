import pytest
from src.core.domain.normalize import (
    normalize_byte,
    normalize_word,
    denormalize_byte,
    denormalize_word,
    clamp
)

def test_normalize_byte_valid():
    assert normalize_byte(0) == 0.0
    assert normalize_byte(127) == pytest.approx(0.498, abs=0.001)
    assert normalize_byte(255) == 1.0

def test_normalize_byte_invalid():
    with pytest.raises(ValueError, match="value deve estar entre 0 e 255"):
        normalize_byte(-1)
    with pytest.raises(ValueError, match="value deve estar entre 0 e 255"):
        normalize_byte(256)

def test_normalize_word_valid():
    assert normalize_word(0) == 0.0
    assert normalize_word(32767) == pytest.approx(0.5, abs=0.001)
    assert normalize_word(65535) == 1.0

def test_normalize_word_invalid():
    with pytest.raises(ValueError, match="value deve estar entre 0 e 65535"):
        normalize_word(-1)
    with pytest.raises(ValueError, match="value deve estar entre 0 e 65535"):
        normalize_word(65536)

def test_denormalize_byte_valid():
    assert denormalize_byte(0.0) == 0
    assert denormalize_byte(0.5) == 128
    assert denormalize_byte(1.0) == 255

def test_denormalize_byte_invalid():
    with pytest.raises(ValueError, match="value deve estar entre 0.0 e 1.0"):
        denormalize_byte(-0.1)
    with pytest.raises(ValueError, match="value deve estar entre 0.0 e 1.0"):
        denormalize_byte(1.1)

def test_denormalize_word_valid():
    assert denormalize_word(0.0) == 0
    assert denormalize_word(0.5) == 32768
    assert denormalize_word(1.0) == 65535

def test_denormalize_word_invalid():
    with pytest.raises(ValueError, match="value deve estar entre 0.0 e 1.0"):
        denormalize_word(-0.1)
    with pytest.raises(ValueError, match="value deve estar entre 0.0 e 1.0"):
        denormalize_word(1.1)

def test_clamp():
    assert clamp(0.5, 0.0, 1.0) == 0.5
    assert clamp(-0.5, 0.0, 1.0) == 0.0
    assert clamp(1.5, 0.0, 1.0) == 1.0
    assert clamp(50, 0, 100) == 50
    assert clamp(-10, 0, 100) == 0
    assert clamp(150, 0, 100) == 100

def test_clamp_invalid():
    with pytest.raises(ValueError, match="min_val deve ser menor ou igual a max_val"):
        clamp(0.5, 1.0, 0.0)

def test_round_trip_byte():
    original = 127
    normalized = normalize_byte(original)
    denormalized = denormalize_byte(normalized)
    assert denormalized == original

def test_round_trip_word():
    original = 32767
    normalized = normalize_word(original)
    denormalized = denormalize_word(normalized)
    assert denormalized == original
