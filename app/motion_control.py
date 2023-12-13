from app.utils.console import *
from tdmclient import ClientAsync,aw
import time

from app.config import THYMIO_TO_CM, DEFAULT_PLAY_MODE, T, DT, LS, RS

class MotionControl():

    def __init__(self):
        self.node = None
        self.client = None
        self.choreography_status = "stop" # start, pause, stop
        self.completion_percentage = 0

    def init_thymio_connection(self):
        try:
            self.client = ClientAsync()
            self.node = aw(self.client.wait_for_node())
            aw(self.node.lock())
            info("Thymio node connected")
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

    def disconnect_thymio(self):
        """Disconnect the Thymio driver"""
        if self.node is None:
            error("No Thymio node connected")
            return
        info("Disconnecting Thymio node")
        aw(self.node.stop())
        aw(self.client.sleep(0.1))
        aw(self.node.unlock())
        aw(self.client.sleep(0.1))
        self.node = None
        info("Thymio node disconnected")        
    
    def play_choreography(self, choreography, speed_factor, play_mode=DEFAULT_PLAY_MODE, nbr_repetition=0, emotion=None):
        """
        Play a choreography

        @params:
        choreography: choreography object, contains the steps to play
        speed_factor: float, speed factor to apply to the choreography
        play_mode: string, "once" or "loop"
        nbr_repetition: int, number of times to repeat the choreography
        emotion: emotion object, emotion to detect
        """
        if self.node is None:
            error("No Thymio node connected")
            return

        if play_mode == "loop":
            self.play_loop(choreography, speed_factor, emotion)
        elif play_mode == "mult":
            info(f"Playing choreography {nbr_repetition} times")
            for i in range(nbr_repetition):
                last_dt = self.play_once(choreography, speed_factor, emotion)
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

    def play_loop(self, choreography, speed_factor, emotion):
        """Play a choreography in loop"""
        for i in range(50): 
            last_dt = self.play_once(choreography, speed_factor, emotion)
        time.sleep(last_dt/1000)
        aw(self.node.set_variables(  # apply the control on the wheels
            {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))

    def play_once(self, choreography, speed_factor, emotion):
        """Play a choreography once"""
        step_list = choreography.step_list
        end_time = step_list[-1][T]/1000
        last_dt = step_list[-1][DT]/1000
        if self.choreography_status == "play":
            for step in step_list:
                time.sleep(step[DT]/1000/speed_factor) #step in ms 
                left_motor_speed = step[LS]*speed_factor/THYMIO_TO_CM # convert the speed from cm/s to thymio speed
                right_motor_speed = step[RS]*speed_factor/THYMIO_TO_CM
                if emotion is not None:
                    emotion.start_emotion()
                    if emotion.get_emotion_status() == True:
                        self.choreography_status = "pause"
            
                if self.choreography_status == "pause":
                    info("Choreography paused")
                    aw(self.node.set_variables(  # apply the control on the wheels
                        {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))
                    while self.choreography_status == "pause":
                        time.sleep(0.1)
                        if emotion is not None and not self.pause_by_button:
                            if emotion.get_emotion_status() == False:
                                self.choreography_status = "play"
                                emotion.stop_emotion()
                                break
                        if self.choreography_status == "stop":
                            self.completion_percentage = 0
                            info("Choreography stopped")
                            emotion.stop_emotion() if emotion is not None else None
                            return last_dt
                        elif self.choreography_status == "play" and self.pause_by_button == True:
                            info("Choreography resumed")
                            self.pause_by_button = False
                            break
                elif self.choreography_status == "stop":
                    info("Choreography stopped")
                    self.completion_percentage = 0
                    aw(self.node.set_variables(  # apply the control on the wheels
                        {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))
                    emotion.stop_emotion() if emotion is not None else None
                    return last_dt
                aw(self.node.set_variables(  # apply the control on the wheels
                    {"motor.left.target": [int(left_motor_speed)], "motor.right.target": [int(right_motor_speed)]}))                
                self.completion_percentage = step[T]/1000/end_time
            self.completion_percentage = 0
        emotion.stop_emotion() if emotion is not None else None
        return last_dt
        
        
            