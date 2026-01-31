from dataclasses import dataclass 

@dataclass 
class TrackSegment :
    """Defines a segment of the virtual track"""
    duration :float 
    target_speed :float 
    entry_speed :float 
    type :str 
    curvature :float 
