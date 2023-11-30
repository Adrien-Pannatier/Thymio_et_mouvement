import math
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
        port = 2222

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
                print(buffer)
                if buffer == b'c':
                    print("Buffer emptied")
                    break
            except:
                error("Could not empty buffer")
                break
            
    def accept_connection(self):
        info("trying to accept connection")
        try:
            self.client_socket, self.client_address = self.server_socket.accept()
            info(f"Accepted connection from {self.client_address}")
            if self.client_socket != 0 and self.client_address != 0:
                return True
        except Exception as e:
            info(f"connection refused {e}")
            return False
        
    def close_connection(self):
        if self.client_socket != 0 and self.client_address != 0:
            self.client_socket.close()
        self.client_socket = 0
        self.client_address = 0
        if self.server_socket != 0:
            self.server_socket.close()

    def record_step(self):
        """
        starts the recording
        """
        data_array = []

        # send start message
        self.client_socket.send("start".encode('utf-8'))
        t, dt, gx, gy, gz, x_offset, y_offset = 0, 0, 0, 0, 0, 0, 0

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
        t = data[0]
        dt = data[1]
        gx = data[2]
        gy = data[3]
        gz = data[4]
        x_offset = data[5]
        y_offset = data[6]
        return t, dt, gx, gy, gz, x_offset, y_offset

    def process_data_array(self, data_array, calibration_const):
        debug(f"calibration_const: {calibration_const}")
        time_offset = data_array[0][0]
        position_x = 0
        position_y = 0
        positions_y = []
        processed_data_array = []
        # Extract the necessary data from the incoming wifi message
        for i in range(len(data_array)):
            time = data_array[i][0]
            timestep = data_array[i][1]
            gyro_x = data_array[i][2]
            gyro_y = data_array[i][3]
            gyro_z = data_array[i][4]
            x_offset = data_array[i][5]
            y_offset = data_array[i][6]

            debug(f"position_y: {position_y}")

            # compute position with offsets
            position_x = position_x + x_offset/calibration_const
            position_y = position_y + y_offset/calibration_const

            # Append the data to the array
            positions_y.append(position_y)

            # Compute the forward speed and angular speed
            angular_speed = math.radians(-gyro_z)
            rot_speed_x = math.radians(gyro_x)
            rot_speed_y = math.radians(gyro_y)
            tangential_speed = 1000 * (positions_y[i] - positions_y[i-1])/ timestep   # in cm/s

            # debug(f"tangential_speed: {tangential_speed} cm/s, angular_speed: {angular_speed} rad/s")

            # Apply threshold to the angular speed
            angular_speed = self.threshold_angular_speed(angular_speed) 

            # Separating speed to left and right wheels
            left_wheel_speed = tangential_speed - angular_speed * DIAMETER/2
            right_wheel_speed = tangential_speed + angular_speed * DIAMETER/2

            # round the speeds to 2 decimals
            left_wheel_speed = round(left_wheel_speed, 2)
            right_wheel_speed = round(right_wheel_speed, 2)

            # correct time
            time = time - time_offset

            # Append the data to the array but not the first term
            processed_data_array.append([time, timestep, left_wheel_speed, right_wheel_speed]) if i != 0 else None
        
        return processed_data_array

    def calibration(self):
        """
        calibrates the mock Thymio
        """
        self.client_socket.send("start".encode('utf-8'))
        info("Calibration started")

        # wait for 10 seconds
        time.sleep(10)

        info("letting the data come in")
        self.client_socket.send("stop".encode('utf-8'))

        raw_x_position = 0 
        raw_y_position = 0

        counter = 0

        while counter < 100:
            # info("treating data")
            # Wait for message starting with "s"
            char = ""
            message = ""
            message_status = ""
            while message_status != "got":
                char = self.client_socket.recv(1).decode('utf-8')
                # print(char)
                if char.startswith("c"):
                    message_status = "over"
                    message = "-leave-"
                    break
                elif char.startswith("n"):
                    # print("got")
                    message_status = "got"
                    # print(f"Received message: {message}")
                elif message_status == "start":
                    message = message + char
                elif char.startswith("s"):
                    message_status = "start"
            data_str = message[1:-1] # remove the first and last character
            debug(f"Received message: {data_str}")
            if data_str != "leave":
                counter = counter + 1
                debug(f"counter: {counter}")
                try:
                    data = [float(x) for x in data_str.split(',')]
                except Exception as e:
                    warning(f"Exception: {e}")
                    continue
                raw_y_position = raw_y_position + data[6]
            elif data_str == "leave":
                break
            # info(f"raw_y_position: {raw_y_position}")
            # time.sleep(0.1)
        
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

    def threshold_angular_speed(self, angular_speed):
        if abs(angular_speed) < AS_THRESH:
            return 0
        else:
            return angular_speed
        
    def send_stop(self):
        debug("sending stop")
        self.client_socket.send("stop".encode('utf-8'))
        time.sleep(1)
        self.client_socket.send("stop".encode('utf-8'))
        time.sleep(1)
        self.empty_buffer()
        time.sleep(1)