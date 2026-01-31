from dataclasses import dataclass 

@dataclass 
class TelemetryData :
    speed :float 
    rpm :int 
    max_rpm :int 
    gear :int 
    throttle_pct :float 
    brake_pct :float 
    clutch_pct :float 
    steering_angle :float 
    ffb_level :float 
    timestamp :float 

    def __post_init__ (self )->None :
        self ._validate ()

    def _validate (self )->None :
        if not 0.0 <=self .throttle_pct <=1.0 :
            raise ValueError (f"throttle_pct deve estar entre 0.0 e 1.0, recebido: {self.throttle_pct}")
        if not 0.0 <=self .brake_pct <=1.0 :
            raise ValueError (f"brake_pct deve estar entre 0.0 e 1.0, recebido: {self.brake_pct}")
        if not 0.0 <=self .clutch_pct <=1.0 :
            raise ValueError (f"clutch_pct deve estar entre 0.0 e 1.0, recebido: {self.clutch_pct}")
        if not -900.0 <=self .steering_angle <=900.0 :
            raise ValueError (f"steering_angle deve estar entre -900 e 900, recebido: {self.steering_angle}")

    def __str__ (self )->str :
        return (
        f"TelemetryData(speed={self.speed:.1f}, rpm={self.rpm}, gear={self.gear}, "
        f"throttle={self.throttle_pct:.2f}, brake={self.brake_pct:.2f})"
        )
