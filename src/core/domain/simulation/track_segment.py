from dataclasses import dataclass 

@dataclass 
class TrackSegment :
    duration :float 
    target_speed :float 
    entry_speed :float 
    type :str 
    curvature :float 
