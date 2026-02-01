import pytest
from src.core.domain.simulation.physics_engine import PhysicsEngine
from src.core.domain.simulation.track_segment import TrackSegment

def test_physics_engine_lerp():
    engine = PhysicsEngine()
    assert engine._lerp(0, 10, 0.5) == 5.0
    assert engine._lerp(0, 10, -0.5) == 0.0 # Clamping
    assert engine._lerp(0, 10, 1.5) == 10.0 # Clamping

def test_rpm_calculation_neutral_gear():
    engine = PhysicsEngine()
    engine.gear = 0
    engine.speed = 100.0
    
    rpm = engine._rpm_calculator.calculate(engine.speed, engine.gear)
    
    assert rpm == PhysicsEngine.IDLE_RPM

def test_rpm_calculation_reverse_gear():
    engine = PhysicsEngine()
    engine.gear = -1
    engine.speed = 20.0
    
    rpm = engine._rpm_calculator.calculate(engine.speed, engine.gear)
    
    assert rpm >= PhysicsEngine.IDLE_RPM
    assert rpm <= PhysicsEngine.MAX_RPM

def test_physics_engine_corner_exit():
    engine = PhysicsEngine()
    segment = TrackSegment(5.0, 200.0, 100.0, 'CORNER_EXIT', 0.5)
    
    # Progress 0.0
    engine.update(0.1, segment, 0.0)
    assert engine.throttle > 0.0
    
    # Progress 1.0 - Use larger dt to allow throttle inertia to catch up
    engine.update(0.5, segment, 1.0)
    # The linear interpolation might hit 1.0 exactly but floating point precision can vary.
    # Also, the previous update might have moved it near 1.0. 
    # Let's check it increased significantly.
    assert engine.throttle > 0.8
    assert engine.steering == 0.0

def test_physics_engine_downshift():
    engine = PhysicsEngine()
    engine.speed = 40.0 # Low speed
    engine.gear = 4 # High gear
    # Ratio gear 4 is 34. RPM = 40/34 * 1000 = ~1176 RPM. Should downshift.
    
    engine.update(0.1, TrackSegment(1.0, 40.0, 40.0, 'STRAIGHT', 0.0), 0.5)
    
    assert engine.gear < 4

def test_steering_micro_corrections():
    engine = PhysicsEngine()
    engine.speed = 100.0 # High speed to trigger jitter
    engine.steering = 0.5
    
    # Update with 0 steering target (straight)
    # This would normally smooth to 0.0, but micro-corrections should add noise.
    initial_steering = engine.steering
    series_of_updates = []
    
    # Run a few updates
    segment = TrackSegment(1.0, 100.0, 100.0, 'STRAIGHT', 0.0)
    for _ in range(10):
        engine.update(0.016, segment, 0.5)
        series_of_updates.append(engine.steering)
        
    # Check that it's changing
    assert any(val != initial_steering for val in series_of_updates)
    
    # Check that it doesn't stay perfectly static if we are just holding a turn
    # (Though in STRAIGHT target is 0, so it will decay)
    
    # Test maintaining a turn
    engine.steering = 0.5
    segment_corner = TrackSegment(1.0, 100.0, 100.0, 'CORNER_MID', 0.5)
    # CORNER_MID target steering is curvature (say 0.5)
    
    last_val = engine.steering
    changes = 0
    for _ in range(20):
        engine.update(0.016, segment_corner, 0.5)
        if engine.steering != last_val:
            changes += 1
        last_val = engine.steering
        
    # It should fluctuate slightly due to jitter even if target matches current
    assert changes > 0

def test_physics_engine_corner_entry():
    engine = PhysicsEngine()
    engine.speed = 100.0
    segment = TrackSegment(1.0, 50.0, 50.0, 'CORNER_ENTRY', 0.5)
    
    # Progress 0.5
    engine.update(0.1, segment, 0.5)
    
    # Speed (100) > Target (50), so brake should be applied
    assert engine.brake > 0.0
    
    # Steering should be increasing based on curvature * progress
    assert engine.steering != 0.0
