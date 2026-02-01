import random 
from typing import Dict 
from src .core .domain .simulation .track_segment import TrackSegment 
from src .core .domain .rpm_calculator import RPMCalculator
from src .core .infrastructure .config_manager import ConfigManager

class PhysicsEngine :
    def __init__ (self, config: ConfigManager = None):
        if config is None:
            config = ConfigManager()
        
        physics_config = config.get_config("physics", {})
        
        gear_ratios_config = physics_config.get("gear_ratios", {})
        self.GEAR_RATIOS = {int(k): v for k, v in gear_ratios_config.items()}
        
        self.FINAL_DRIVE = physics_config.get("final_drive", 3.5)
        self.WHEEL_CIRCUMFERENCE = physics_config.get("wheel_circumference", 1.9)
        self.IDLE_RPM = physics_config.get("idle_rpm", 1500)
        self.MAX_RPM = physics_config.get("max_rpm", 8000)
        self.REDLINE_RPM = physics_config.get("redline_rpm", 7800)
        self.UPSHIFT_RPM = physics_config.get("upshift_rpm", 7410)
        self.DOWNSHIFT_RPM = physics_config.get("downshift_rpm", 3120)
        
        self .speed =0.0 
        self .rpm =self.IDLE_RPM
        self .gear =1 
        self .throttle =0.0 
        self .brake =0.0 
        self .steering =0.0 
        self .clutch =0.0 
        
        self._rpm_calculator = RPMCalculator(
            gear_ratios=self.GEAR_RATIOS,
            final_drive=self.FINAL_DRIVE,
            wheel_circumference=self.WHEEL_CIRCUMFERENCE,
            idle_rpm=self.IDLE_RPM,
            max_rpm=self.MAX_RPM
        )

    def _lerp (self ,start :float ,end :float ,t :float )->float :
        t =max (0.0 ,min (1.0 ,t ))
        return start +(end -start )*t 
    
    def update (self ,dt :float ,segment :TrackSegment ,progress :float )->None :
        target_throttle =0.0 
        target_brake =0.0 
        target_steering =0.0 

        if segment .type =='STRAIGHT':
            target_throttle =1.0 
            target_steering =0.0 

        elif segment .type =='CORNER_ENTRY':
            speed_diff =self .speed -segment .target_speed 
            brake_intensity =min (1.0 ,speed_diff /50.0 )
            target_brake =brake_intensity if speed_diff >0 else 0.0 
            target_steering =segment .curvature *(progress *0.3 )

        elif segment .type =='CORNER_MID':
            target_throttle =0.2 if progress >0.7 else 0.0 
            target_brake =max (0.0 ,0.4 *(1.0 -progress *1.5 ))
            target_steering =segment .curvature 

        elif segment .type =='CORNER_EXIT':
            target_throttle =self ._lerp (0.2 ,1.0 ,progress )
            target_steering =self ._lerp (segment .curvature ,0.0 ,progress )

        throttle_speed =3.0 *dt 
        brake_speed =5.0 *dt 
        steer_speed =2.0 *dt 

        if self .throttle <target_throttle :
            self .throttle =min (target_throttle ,self .throttle +throttle_speed )
        else :
            self .throttle =max (target_throttle ,self .throttle -throttle_speed )

        if self .brake <target_brake :
            self .brake =min (target_brake ,self .brake +brake_speed )
        else :
            self .brake =max (target_brake ,self .brake -brake_speed )

        raw_target = target_steering

        micro_correction = 0.0
        if self.speed > 40 and abs(self.steering) > 0.1:
            load_factor = abs(self.steering) * (self.speed / 100.0)
            intensity = 0.002 * min(1.0, load_factor)
            micro_correction = random.uniform(-intensity, intensity)
        
        target_with_noise = raw_target + micro_correction

        max_steer_rate = 2.5 * dt 
        
        diff = target_with_noise - self.steering
        
        limited_change = max(-max_steer_rate, min(max_steer_rate, diff))
        
        alpha = 5.0 * dt
        self.steering += limited_change * min(1.0, alpha) 

        aero_drag =0.005 *self .speed 

        torque =0.0 
        if 3000 <self .rpm <7000 :
            torque =1.0 
        else :
            torque =0.7 

        gear_ratio =1.0 /(self .gear *0.5 )
        acceleration =self .throttle *20.0 *torque *gear_ratio 
        deceleration =self .brake *45.0 

        self .speed +=(acceleration -deceleration -aero_drag )*dt 
        self .speed =max (0.0 ,self .speed )

        target_rpm = self._rpm_calculator.calculate(self.speed, self.gear)
        
        if target_rpm > self.UPSHIFT_RPM and self .gear <6 :
            self .gear +=1 
            self .rpm = self._rpm_calculator.calculate(self.speed, self.gear)
        elif target_rpm < self.DOWNSHIFT_RPM and self .gear >1 :
            self .gear -=1 
            self .rpm = self._rpm_calculator.calculate(self.speed, self.gear)
        else :
            self .rpm =target_rpm +(random .random ()*50 -25 )

        self .rpm =max (self.IDLE_RPM ,min (self.MAX_RPM ,self .rpm ))
