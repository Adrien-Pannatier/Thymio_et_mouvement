from app.utils.console import *
from tdmclient import ClientAsync,aw
import time

from app.config import THYMIO_TO_CM, DEFAULT_PLAY_MODE, T, DT, LS, RS


class MotionControl():

    def __init__(self):
        self.node = None

    def init_thymio_connection(self):
        status = console.status("Connecting to Thymio driver", spinner_style="cyan")
        
        status.start()

        try:
            client = ClientAsync()
            status.update("Waiting for Thymio node")
            

            self.node = aw(client.wait_for_node())
            aw(self.node.lock())

            status.stop()

            info("Thymio node connected")
            debug(f"Node lock on {self.node}")

                # Signal the Thymio to broadcast variable changes
                # await node.watch(variables=True)

            status = None
            return True

        except ConnectionRefusedError:
            warning("Thymio driver connection refused")
            return False

        except ConnectionResetError:
            warning("Thymio driver connection closed")
            return False

        finally:
            if status is not None:
                status.stop()
                
    def disconnect_thymio(self):
        """Disconnect the Thymio driver"""
        if self.node is None:
            error("No Thymio node connected")
            return

        info("Disconnecting Thymio node")
        aw(self.node.unlock())
        self.node = None
        info("Thymio node disconnected")        
    
    def play_choreography(self, choreography, speed_factor, play_mode=DEFAULT_PLAY_MODE, nbr_repetition=0):
        """Play a choreography"""
        if self.node is None:
            error("No Thymio node connected")
            return

        if play_mode == "loop":
            self.play_loop(choreography, speed_factor)
        elif play_mode == "mult":
            info(f"Playing choreography {nbr_repetition} times")
            for i in range(nbr_repetition):
                self.play_once(choreography, speed_factor)
        else:
            error("Invalid play mode")
            return
        
    def play_loop(self, choreography, speed_factor):
        """Play a choreography in loop"""
        while True:
            self.play_once(choreography, speed_factor)

    def play_once(self, choreography, speed_factor):
        """Play a choreography once"""
        step_list = choreography.step_list
        for step in step_list:
            info(step)
            info(f"sleeping for {step[DT/speed_factor]} seconds")
            time.sleep(step[DT/speed_factor])

            left_motor_speed = step[LS]*speed_factor/THYMIO_TO_CM # convert the speed from cm/s to thymio speed
            right_motor_speed = step[RS]*speed_factor/THYMIO_TO_CM

            aw(self.node.set_variables(  # apply the control on the wheels
                {"motor.left.target": [int(left_motor_speed)], "motor.right.target": [int(right_motor_speed)]}))
            