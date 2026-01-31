from src.core.domain.normalize import normalize_byte, normalize_word, clamp

def test_normalize_workflow():
    raw_throttle = 200
    raw_brake = 100
    raw_steering = 32767
    
    throttle_normalized = normalize_byte(raw_throttle)
    brake_normalized = normalize_byte(raw_brake)
    steering_normalized = normalize_word(raw_steering)
    
    assert 0.0 <= throttle_normalized <= 1.0
    assert 0.0 <= brake_normalized <= 1.0
    assert 0.0 <= steering_normalized <= 1.0
    
    throttle_clamped = clamp(throttle_normalized, 0.0, 1.0)
    brake_clamped = clamp(brake_normalized, 0.0, 1.0)
    
    assert throttle_clamped == throttle_normalized
    assert brake_clamped == brake_normalized
    
    assert throttle_normalized > brake_normalized
    assert abs(steering_normalized - 0.5) < 0.01
