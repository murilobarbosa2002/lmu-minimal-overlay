import random 
from typing import Dict 
from src .core .domain .simulation .track_segment import TrackSegment 
from src .core .domain .rpm_calculator import RPMCalculator
from src .core .infrastructure .config_manager import ConfigManager
from src.core.domain.constants import (
    INITIAL_SPEED,
    INITIAL_THROTTLE,
    INITIAL_BRAKE,
    INITIAL_STEERING,
    INITIAL_CLUTCH,
    LERP_MIN,
    LERP_MAX
)

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
        
        sim_config = physics_config.get("simulation", {})
        self.INITIAL_GEAR = sim_config.get("initial_gear", 1)
        self.MAX_GEAR = sim_config.get("max_gear", 6)
        self.MIN_GEAR = sim_config.get("min_gear", 1)
        self.RPM_NOISE_RANGE = sim_config.get("rpm_noise_range", 25)
        
        driver_ai = physics_config.get("driver_ai", {})
        corner_entry = driver_ai.get("corner_entry", {})
        self.BRAKE_SENSITIVITY = corner_entry.get("brake_sensitivity", 50.0)
        self.STEERING_ENTRY_FACTOR = corner_entry.get("steering_entry_factor", 0.3)
        
        corner_mid = driver_ai.get("corner_mid", {})
        self.THROTTLE_APPLICATION_POINT = corner_mid.get("throttle_application_point", 0.7)
        self.PARTIAL_THROTTLE = corner_mid.get("partial_throttle", 0.2)
        self.TRAIL_BRAKE_INTENSITY = corner_mid.get("trail_brake_intensity", 0.4)
        self.BRAKE_DECAY_RATE = corner_mid.get("brake_decay_rate", 1.5)
        
        corner_exit = driver_ai.get("corner_exit", {})
        self.MIN_THROTTLE_EXIT = corner_exit.get("min_throttle", 0.2)
        self.MAX_THROTTLE_EXIT = corner_exit.get("max_throttle", 1.0)
        
        input_response = physics_config.get("input_response", {})
        self.THROTTLE_SPEED = input_response.get("throttle_speed", 3.0)
        self.BRAKE_SPEED = input_response.get("brake_speed", 5.0)
        self.STEERING_SPEED = input_response.get("steering_speed", 2.0)
        
        steering_dynamics = physics_config.get("steering_dynamics", {})
        self.JITTER_SPEED_THRESHOLD = steering_dynamics.get("jitter_speed_threshold", 40.0)
        self.JITTER_ANGLE_THRESHOLD = steering_dynamics.get("jitter_angle_threshold", 0.1)
        self.JITTER_INTENSITY = steering_dynamics.get("jitter_intensity", 0.002)
        self.JITTER_SPEED_FACTOR = steering_dynamics.get("jitter_speed_factor", 100.0)
        self.MAX_STEER_RATE = steering_dynamics.get("max_steer_rate", 2.5)
        self.SMOOTHING_FACTOR = steering_dynamics.get("smoothing_factor", 5.0)
        
        vehicle_dynamics = physics_config.get("vehicle_dynamics", {})
        self.AERO_DRAG_COEFFICIENT = vehicle_dynamics.get("aero_drag_coefficient", 0.005)
        self.TORQUE_RPM_MIN = vehicle_dynamics.get("torque_rpm_min", 3000)
        self.TORQUE_RPM_MAX = vehicle_dynamics.get("torque_rpm_max", 7000)
        self.TORQUE_PEAK = vehicle_dynamics.get("torque_peak", 1.0)
        self.TORQUE_OFF_PEAK = vehicle_dynamics.get("torque_off_peak", 0.7)
        self.GEAR_RATIO_DIVISOR = vehicle_dynamics.get("gear_ratio_divisor", 0.5)
        self.ACCELERATION_FACTOR = vehicle_dynamics.get("acceleration_factor", 20.0)
        self.DECELERATION_FACTOR = vehicle_dynamics.get("deceleration_factor", 45.0)
        
        self .speed =INITIAL_SPEED
        self .rpm =self.IDLE_RPM
        self .gear =self.INITIAL_GEAR
        self .throttle =INITIAL_THROTTLE
        self .brake =INITIAL_BRAKE
        self .steering =INITIAL_STEERING
        self .clutch =INITIAL_CLUTCH 
        
        self._rpm_calculator = RPMCalculator(
            gear_ratios=self.GEAR_RATIOS,
            final_drive=self.FINAL_DRIVE,
            wheel_circumference=self.WHEEL_CIRCUMFERENCE,
            idle_rpm=self.IDLE_RPM,
            max_rpm=self.MAX_RPM
        )

    def _lerp (self ,start :float ,end :float ,t :float )->float :
        t =max (LERP_MIN ,min (LERP_MAX ,t ))
        return start +(end -start )*t 
    
    def update (self ,dt :float ,segment :TrackSegment ,progress :float )->None :
        target_throttle =INITIAL_THROTTLE
        target_brake =INITIAL_BRAKE
        target_steering =INITIAL_STEERING

        if segment .type =='STRAIGHT':
            target_throttle =LERP_MAX
            target_steering =INITIAL_STEERING 

        elif segment .type =='CORNER_ENTRY':
            speed_diff =self .speed -segment .target_speed 
            brake_intensity =min (1.0 ,speed_diff /self.BRAKE_SENSITIVITY )
            target_brake =brake_intensity if speed_diff >0 else INITIAL_BRAKE 
            target_steering =segment .curvature *(progress *self.STEERING_ENTRY_FACTOR )

        elif segment .type =='CORNER_MID':
            target_throttle =self.PARTIAL_THROTTLE if progress >self.THROTTLE_APPLICATION_POINT else INITIAL_THROTTLE 
            target_brake =max (INITIAL_BRAKE ,self.TRAIL_BRAKE_INTENSITY *(LERP_MAX -progress *self.BRAKE_DECAY_RATE ))
            target_steering =segment .curvature 

        elif segment .type =='CORNER_EXIT':
            target_throttle =self ._lerp (self.MIN_THROTTLE_EXIT ,self.MAX_THROTTLE_EXIT ,progress )
            target_steering =self ._lerp (segment .curvature ,INITIAL_STEERING ,progress )

        throttle_speed =self.THROTTLE_SPEED *dt 
        brake_speed =self.BRAKE_SPEED *dt 
        steer_speed =self.STEERING_SPEED *dt 

        if self .throttle <target_throttle :
            self .throttle =min (target_throttle ,self .throttle +throttle_speed )
        else :
            self .throttle =max (target_throttle ,self .throttle -throttle_speed )

        if self .brake <target_brake :
            self .brake =min (target_brake ,self .brake +brake_speed )
        else :
            self .brake =max (target_brake ,self .brake -brake_speed )

        raw_target = target_steering

        micro_correction = INITIAL_STEERING
        if self.speed > self.JITTER_SPEED_THRESHOLD and abs(self.steering) > self.JITTER_ANGLE_THRESHOLD:
            load_factor = abs(self.steering) * (self.speed / self.JITTER_SPEED_FACTOR)
            intensity = self.JITTER_INTENSITY * min(1.0, load_factor)
            micro_correction = random.uniform(-intensity, intensity)
        
        target_with_noise = raw_target + micro_correction

        max_steer_rate = self.MAX_STEER_RATE * dt 
        
        diff = target_with_noise - self.steering
        
        limited_change = max(-max_steer_rate, min(max_steer_rate, diff))
        
        alpha = self.SMOOTHING_FACTOR * dt
        self.steering += limited_change * min(1.0, alpha) 

        aero_drag =self.AERO_DRAG_COEFFICIENT *self .speed 

        torque =INITIAL_THROTTLE 
        if self.TORQUE_RPM_MIN <self .rpm <self.TORQUE_RPM_MAX :
            torque =self.TORQUE_PEAK 
        else :
            torque =self.TORQUE_OFF_PEAK 

        gear_ratio =LERP_MAX /(self .gear *self.GEAR_RATIO_DIVISOR )
        acceleration =self .throttle *self.ACCELERATION_FACTOR *torque *gear_ratio 
        deceleration =self .brake *self.DECELERATION_FACTOR 

        self .speed +=(acceleration -deceleration -aero_drag )*dt 
        self .speed =max (INITIAL_SPEED ,self .speed )

        target_rpm = self._rpm_calculator.calculate(self.speed, self.gear)
        
        if target_rpm > self.UPSHIFT_RPM and self .gear <self.MAX_GEAR :
            self .gear +=1 
            self .rpm = self._rpm_calculator.calculate(self.speed, self.gear)
        elif target_rpm < self.DOWNSHIFT_RPM and self .gear >self.MIN_GEAR :
            self .gear -=1 
            self .rpm = self._rpm_calculator.calculate(self.speed, self.gear)
        else :
            self .rpm =target_rpm +(random .random ()*self.RPM_NOISE_RANGE *2 -self.RPM_NOISE_RANGE )

        self .rpm =max (self.IDLE_RPM ,min (self.MAX_RPM ,self .rpm ))
