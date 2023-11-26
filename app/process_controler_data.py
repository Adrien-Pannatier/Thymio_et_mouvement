from typing import Any
from app.utils.console import *
from app.config import PIXELS_TO_METERS, GYRO_SCALING, AS_THRESH, DIAMETER
import numpy as np
import time
import socket

class ProcessControlerData:
     
    def __init__(self):
        self.recording_state = False
        self.server_socket = None
        self.record_length = 5 # seconds
        self.calibration_on = False

    def init_record(self):
        """
        connects to the mock Thymio
        """
        # Set the IP address and port to match Arduino configuration
        host = '0.0.0.0'  # Listen on all available network interfaces
        port = 8888

        try:
            # Create a socket and bind it to the address
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(1)
            info(f"Listening on {host}:{port}...")
        
            self.client_socket = 0
            self.client_address = 0

        except OSError: # A vérifier ----------------------------------------------------------------------------
            warning(f"[bold red]Error:[/] The mock Thymio is not running. Please run it and try again.")
            
    def accept_connection(self):
        try:
            self.client_socket, self.client_address = self.server_socket.accept()
            info(f"Accepted connection from {self.client_address}")
            if self.client_socket != 0 and self.client_address != 0:
                return True
        except:
            return False
        
    def close_connection(self):
        if self.client_socket != 0 and self.client_address != 0:
            self.client_socket.close()
        self.client_socket = 0
        self.client_address = 0
        if self.server_socket != 0:
            self.server_socket.close()

    def record(self):
        """
        starts the recording
        """
        data_array = []

        self.recording_state = True

        client_socket, client_address = self.server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_socket.send("start".encode('utf-8'))
        
        while self.recording_state:
            data_str = client_socket.recv(37).decode('utf-8')
            print(f"Received data is: {data_str}")
            data = [float(x) for x in data_str.split(',')]
            data_array.append(data)

            if data[0] >= self.record_length:
                print("Recording stopped")
                self.recording_state = False

        client_socket.send("stop".encode('utf-8'))
        client_socket.close()

        output = self.process_data_array(data_array)

        return output

    def process_data_array(self, data_array):
        processed_data_array = []
        try:
            # Extract the necessary data from the incoming wifi message
            for i in range(len(data_array)):
                time = data_array[i][0]
                timestep = data_array[i][0] - data_array[i-1][0]
                current_pos = data_array[i][1:3]
                current_gyro_z = data_array[i][3]
                last_pos = data_array[i-1][1:3]

                # Compute the forward speed and angular speed
                forward_speed, angular_speed = self.compute_speeds(current_pos, current_gyro_z, timestep, last_pos)

                # Apply threshold to the angular speed
                angular_speed = self.threshold_angular_speed(angular_speed) 

                # Tangential speed
                tangential_speed = np.sqrt(forward_speed[0]**2 + forward_speed[1]**2)

                # Separating speed to left and right wheels
                left_wheel_speed = tangential_speed - angular_speed * DIAMETER/2
                right_wheel_speed = tangential_speed + angular_speed * DIAMETER/2

                # Append the data to the array
                processed_data_array.append([time, timestep, left_wheel_speed, right_wheel_speed])   
            
            return processed_data_array

        except KeyError:
            warning("KeyError: One or more necessary variables are missing.")

        except Exception as e:
            warning(f"Exception: {e}")

    def calibration(self):
        """
        calibrates the mock Thymio
        """
        self.client_socket.send("start".encode('utf-8'))
        info("Calibration started")

        raw_x_position = 0 

        while self.calibration_on:
            data_str = self.client_socket.recv(37).decode('utf-8')
            if len(data_str) > 35:
                # print(f"Received data: {data_str}")    
                # separate data
                data = [str(x) for x in data_str.split(',')]
                # print(f"recieved x offset: {data[5]}, recieved y offset: {data[6]}")
                try:
                    raw_x_position = raw_x_position + float(data[5])
                except:
                    pass
        self.client_socket.send("stop".encode('utf-8'))
        # compute offset rounded to 2 decimals
        offset = round(raw_x_position / 20.00, 2)

        return offset
    
    def save_calibration(self, offset):
        """
        saves the calibration
        """
        with open("app/settings/calibration.txt", "w") as f:
            f.write(str(offset))

    def load_calibration(self):
        """
        loads the calibration
        """
        # check if the file exists
        try:
            with open("app/settings/calibration.txt", "r") as f:
                offset = f.read()
            return float(offset)
        except:
            info("No calibration file found")
            return None

    def debug_start(self):
        self.client_socket.send("start".encode('utf-8'))

    def debug_step(self):
        data_str = self.client_socket.recv(37).decode('utf-8')
        if len(data_str) > 35:
            data = [str(x) for x in data_str.split(',')]
            # get x and y offsets
            try: 
                x_offset = float(data[5])
            except:
                x_offset = 0.00
            try:
                y_offset = float(data[6])
            except:
                y_offset = 0.00
            # print(f"x offset: {x_offset}")
            # print(f"y offset: {y_offset}")
            return x_offset, y_offset
        return None, None


    def debug_stop(self):
        # print("message over")
        self.client_socket.send("stop".encode('utf-8'))
        time.sleep(1)

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