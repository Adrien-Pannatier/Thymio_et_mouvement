from typing import Any
from app.utils.console import *
from app.config import PIXELS_TO_METERS, GYRO_SCALING, AS_THRESH, DIAMETER, SETTINGS_PATH
import numpy as np
import time
import socket
import json

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

    def empty_buffer(self):
        # Empty the buffer
        while True:
            try:
                buffer = (self.client_socket.recv(1))
                # print(buffer)
                if buffer == b'c':
                    # print("Buffer emptied")
                    break
            except:
                # error("Could not empty buffer")
                break
            
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
        raw_y_position = 0

        while self.calibration_on:
            # Wait for message starting with "s"
            char = ""
            message = ""
            message_status = ""
            while message_status != "got":
                char = self.client_socket.recv(1).decode('utf-8')
                if char.startswith("n"):
                    message_status = "got"
                    # print(f"Received message: {message}")
                elif message_status == "start":
                    message = message + char
                elif char.startswith("s"):
                    message_status = "start"
            data_str = message[1:-1] # remove the first and last character
            try:
                data = [float(x) for x in data_str.split(',')]
            except Exception as e:
                warning(f"Exception: {e}")
                continue
            raw_y_position = raw_y_position + data[6]
            info(f"raw_y_position: {raw_y_position}")
            # time.sleep(0.1)
        
        self.client_socket.send("stop".encode('utf-8'))
        self.empty_buffer()
        # compute offset rounded to 2 decimals
        offset = round(raw_y_position / 20.00, 2)
        info(f"offset: {offset}")
        return offset
    
    def save_calibration(self, offset):
        """
        saves the calibration
        """
        # save in json file
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        settings["calibration"] = offset
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=4)

    def load_calibration(self):
        """
        loads the calibration
        """
        # check if the file exists
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        if "calibration" in settings:
            return settings["calibration"]
        else:
            return None  
        # try:
        #     with open("app/settings/calibration.txt", "r") as f:
        #         offset = f.read()
        #     return float(offset)
        # except:
        #     info("No calibration file found")
        #     return None

    def debug_start(self):
        self.client_socket.send("start".encode('utf-8'))
        self.y_position = 0
        self.x_position = 0


    def debug_step(self):
        # Wait for message starting with "s"
        char = ""
        message = ""
        message_status = ""
        while message_status != "got":
            char = self.client_socket.recv(1).decode('utf-8')
            # info(f"Received char: {char}")
            if char.startswith("n"):
                message_status = "got"
                # print(f"Received message: {message}")
            elif message_status == "start":
                message = message + char
            elif char.startswith("s"):
                message_status = "start"
        data_str = message[1:-1] # remove the first and last character
        try:
            data = [float(x) for x in data_str.split(',')]
        except Exception as e:
            warning(f"Exception: {e}")
        x_offset = data[5]
        y_offset = data[6]
        return x_offset, y_offset


    def debug_stop(self):
        # print("message over")
        self.client_socket.send("stop".encode('utf-8'))
        self.empty_buffer()
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