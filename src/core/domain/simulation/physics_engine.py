import random 
from typing import Dict 
from src .core .domain .simulation .track_segment import TrackSegment 

class PhysicsEngine :
    def __init__ (self ):
        self .speed =0.0 
        self .rpm =800.0 
        self .gear =1 
        self .throttle =0.0 
        self .brake =0.0 
        self .steering =0.0 
        self .clutch =0.0 
        self ._gear_ratios ={1 :10 ,2 :18 ,3 :26 ,4 :34 ,5 :44 ,6 :55 }

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

        # Reduced jitter for stability
        smoothing_factor = 2.0 * dt # Increased smoothing (lower factor)
        
        jitter_intensity = 0.0
        if self.speed > 20: # Higher activation speed
             load_factor = abs(self.steering) + (self.speed / 300.0)
             # Reduced intensity multiplier from 0.02 to 0.005
             jitter_intensity = 0.005 * min(1.0, load_factor)
        
        micro_correction = random.uniform(-jitter_intensity, jitter_intensity)
        
        diff = target_steering - self.steering
        self.steering += diff * min(1.0, smoothing_factor)
        
        # Reduced micro-correction influence
        self.steering += micro_correction * 0.2 

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

        target_rpm =(self .speed /self ._gear_ratios [self .gear ])*1000 

        if target_rpm >7800 and self .gear <6 :
            self .gear +=1 
            self .rpm =(self .speed /self ._gear_ratios [self .gear ])*1000 
        elif target_rpm <3500 and self .gear >1 :
            self .gear -=1 
            self .rpm =(self .speed /self ._gear_ratios [self .gear ])*1000 
        else :
            self .rpm =target_rpm +(random .random ()*50 -25 )

        self .rpm =max (800 ,min (8200 ,self .rpm ))
