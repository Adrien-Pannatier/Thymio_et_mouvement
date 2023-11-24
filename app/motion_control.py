from app.utils.console import *
import tdmclient
from tdmclient import ClientAsync,aw
import time

from app.config import THYMIO_TO_CM, DEFAULT_PLAY_MODE, T, DT, LS, RS


class MotionControl():

    def __init__(self):
        self.node = None
        self.choreography_status = "stop" # start, pause, stop
        self.completion_percentage = 0

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

            status = None
            return True

        except ConnectionRefusedError:
            warning("Thymio driver connection refused")
            return False

        except ConnectionResetError:
            warning("Thymio driver connection closed")
            return False
        
        except Exception as e:
            error(f"Unexpected error: {e}")
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
        aw(self.node.stop())
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
                last_dt = self.play_once(choreography, speed_factor)
            time.sleep(last_dt)

        else:
            error("Invalid play mode")
            return

    def stop_motors(self):
        """Stop the motors"""
        if self.node is None:
            error("No Thymio node connected")
            return

        info("Stopping motors")
        aw(self.node.set_variables(  # apply the control on the wheels
            {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))

    def play_loop(self, choreography, speed_factor):
        """Play a choreography in loop"""
        for i in range(10): # MODIFY TO INFINITE LOOP -----------------------------------------------------------------------------
            last_dt = self.play_once(choreography, speed_factor)
        time.sleep(last_dt)
        aw(self.node.set_variables(  # apply the control on the wheels
            {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))

    def play_once(self, choreography, speed_factor):
        """Play a choreography once"""
        step_list = choreography.step_list
        end_time = step_list[-1][T]
        last_dt = step_list[-1][DT]
        if self.choreography_status == "play":
            for step in step_list:
                # info(step)    
                # info(f"sleeping for {step[DT]/speed_factor} seconds")
                time.sleep(step[DT]/speed_factor)

                left_motor_speed = step[LS]*speed_factor/THYMIO_TO_CM # convert the speed from cm/s to thymio speed
                right_motor_speed = step[RS]*speed_factor/THYMIO_TO_CM

                aw(self.node.set_variables(  # apply the control on the wheels
                    {"motor.left.target": [int(left_motor_speed)], "motor.right.target": [int(right_motor_speed)]}))
                
                # info(f"step {step[T]} / {end_time}")
                self.completion_percentage = step[T]/end_time

                if self.choreography_status == "pause":
                    info("Choreography paused")
                    aw(self.node.set_variables(  # apply the control on the wheels
                        {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))
                    while self.choreography_status == "pause":
                        time.sleep(0.1)
                        if self.choreography_status == "stop":
                            self.completion_percentage = 0
                            info("Choreography stopped")
                            return last_dt
                        elif self.choreography_status == "play":
                            info("Choreography resumed")
                            break

                elif self.choreography_status == "stop":
                    info("Choreography stopped")
                    self.completion_percentage = 0
                    aw(self.node.set_variables(  # apply the control on the wheels
                        {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))
                    return last_dt
            # self.choreography_status = "stop"
            self.completion_percentage = 0
        
        return last_dt
        
        
            