import pytest
from src.core.domain.simulation.physics_engine import PhysicsEngine
from src.core.domain.simulation.track_segment import TrackSegment

def test_physics_engine_lerp():
    engine = PhysicsEngine()
    assert engine._lerp(0, 10, 0.5) == 5.0
    assert engine._lerp(0, 10, -0.5) == 0.0 # Clamping
    assert engine._lerp(0, 10, 1.5) == 10.0 # Clamping

def test_physics_engine_corner_exit():
    engine = PhysicsEngine()
    segment = TrackSegment(5.0, 200.0, 100.0, 'CORNER_EXIT', 0.5)
    
    # Progress 0.0
    engine.update(0.1, segment, 0.0)
    assert engine.throttle > 0.0
    
    # Progress 1.0
    engine.update(0.1, segment, 1.0)
    assert engine.throttle >= 1.0
    assert engine.steering == 0.0 # Should unwind to 0

def test_physics_engine_downshift():
    engine = PhysicsEngine()
    engine.speed = 40.0 # Low speed
    engine.gear = 4 # High gear
    # Ratio gear 4 is 34. RPM = 40/34 * 1000 = ~1176 RPM. Should downshift.
    
    engine.update(0.1, TrackSegment(1.0, 40.0, 40.0, 'STRAIGHT', 0.0), 0.5)
    
    assert engine.gear < 4
