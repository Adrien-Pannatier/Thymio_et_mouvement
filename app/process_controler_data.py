from app.context import Context
from app.utils.console import *
from app.config import PIXELS_TO_METERS, GYRO_SCALING, AS_THRESH
import numpy as np

class ProcessControllerData():

    # def __init__(self, ctx: Context):
    #     super().__init__(ctx)
    #     self.data_array = []
    #     self.time = 0
    def __init__(self):
        self.data_array = []
        self.time = 0

    def process_event(self, test_variables={}):
        try:
            # Extract the necessary data from the variables dictionary
            # current_pos = []
            # current_gyro_z = []
            # timestep = []
            # last_pos = []
            # Extract the necessary data from the variables dictionary
            current_pos = test_variables['current_pos']
            current_gyro_z = test_variables['current_gyro_z']
            timestep = test_variables['timestep']
            last_pos = test_variables['last_pos']

            # Compute the forward speed and angular speed
            forward_speed, angular_speed = self.compute_speeds(current_pos, current_gyro_z, timestep, last_pos)

            # Apply threshold to the angular speed
            angular_speed = self.threshold_angular_speed(angular_speed) 

            # Append the data to the array
            self.time = self.time + timestep
            self.append_to_array(self.time, forward_speed, angular_speed)

        except KeyError:
            print("KeyError: One or more necessary variables are missing.")

        except Exception as e:
            print(f"Exception: {e}")

    def compute_speeds(self, current_pos, current_gyro_z, timestep, last_pos):
        # Convert position from pixels to meters
        current_pos_meters = [pos * PIXELS_TO_METERS for pos in current_pos]
        last_pos_meters = [pos * PIXELS_TO_METERS for pos in last_pos]

        # Calculate the change in position and gyroscope Z
        delta_pos = np.array(current_pos_meters) - np.array(last_pos_meters)
        angular_speed = current_gyro_z

        # Calculate the forward speed and angular speed
        forward_speed = delta_pos / timestep

        return forward_speed, angular_speed

    def threshold_angular_speed(self, angular_speed):
        if abs(angular_speed) < AS_THRESH:
            return 0
        else:
            return angular_speed

    def append_to_array(self, time, forward_speed, angular_speed):
        # Append a new row to the array
        self.data_array.append([time, forward_speed[0], forward_speed[1], angular_speed])

    def clear_data_array(self):
        self.data_array.clear()

    def display_data_array(self):
        print(self.data_array)

    def reset_time(self):
        self.time = 0
    
    def reset_process(self):
        self.clear_data_array()
        self.reset_time()