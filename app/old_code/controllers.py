import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    """
    Class containing the PID controller

    @variables:
    Var Kp: proportional gain
    Var Ki: integral gain
    Var Kd: derivative gain
    Var sample_time: sampling time
    Var last_error: last error
    Var integral: integral error
    
    @functions:
    Func __init__: initiates the class
    Func update: update function
    """
    def __init__(self, Kp, Ki, Kd):
        """
        Initiates the class

        param Kp: proportional gain
        param Ki: integral gain
        param Kd: derivative gain
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.last_error = 0
        self.integral = 0

    def update(self, setpoint, current_value, dt):
        """
        Updates the controller

        param setpoint: setpoint
        param current_value: current value
        """
        error = setpoint - current_value

        self.integral += error * dt
        
        derivative = (error - self.last_error) / dt
        
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        
        self.last_error = error
        
        return output