import numpy as np

from utils.types import Step

PIXELS_TO_METERS = 0.01  # replace with actual value
ANGULAR_SPEED_THRESH = 0.1  # replace with actual value

def compute_speeds(current_pos, current_gyro_z, dt, last_pos):
    # Convert position from pixels to meters
    current_pos_meters = [pos * PIXELS_TO_METERS for pos in current_pos]
    last_pos_meters = [pos * PIXELS_TO_METERS for pos in last_pos]

    # Calculate the change in position and gyroscope Z
    delta_pos = np.array(current_pos_meters) - np.array(last_pos_meters)
    angular_speed = angular_speed_threshold(current_gyro_z)

    # Calculate the forward speed and angular speed
    forward_speed = delta_pos / dt

    return Step(0, forward_speed[0], forward_speed[1], angular_speed)

def angular_speed_threshold(angular_speed):
    if abs(angular_speed) < ANGULAR_SPEED_THRESH:
        return 0
    else:
        return angular_speed
    
# Test the compute_speeds function
current_pos = [100, 200]  # in pixels
last_pos = [80, 180]  # in pixels
current_gyro_z = 0.05  # in rad/s
dt = 0.1  # in seconds

forward_speed, angular_speed = compute_speeds(current_pos, current_gyro_z, dt, last_pos)

print(f"Forward speed: {forward_speed} m/s")
print(f"Angular speed: {angular_speed} rad/s")