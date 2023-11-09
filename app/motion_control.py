from asyncio import create_task, sleep
from app.utils.console import *
from tdmclient import ClientAsync

from app.config import PROCESS_MSG_INTERVAL, DEFAULT_PLAY_MODE, T, DT, LS, RS


class MotionControl():

    def __init__(self):
        self.node = None

    async def init_thymio_connection(self):
        status = console.status("Connecting to Thymio driver", spinner_style="cyan")
        
        status.start()

        try:
            with ClientAsync() as client:
                status.update("Waiting for Thymio node")

                # Start processing Thymio driver messages
                create_task(process_messages(client))

                with await client.lock() as node:
                    status.stop()

                    # Construct the application context
                    self.node = node

                    info("Thymio node connected")
                    debug(f"Node lock on {node}")

                    # Signal the Thymio to broadcast variable changes
                    await node.watch(variables=True)

                    status = None

        except ConnectionRefusedError:
            warning("Thymio driver connection refused")

        except ConnectionResetError:
            warning("Thymio driver connection closed")

        finally:
            if status is not None:
                status.stop()
                
    def play_choreography(self, choreography, speed_factor, play_mode=DEFAULT_PLAY_MODE):
        """Play a choreography"""
        if self.node is None:
            error("No Thymio node connected")
            return

        if play_mode == "loop":
            self.play_loop(choreography, speed_factor)
        elif play_mode == "once":
            self.play_once(choreography, speed_factor)
        else:
            error("Invalid play mode")
            return
        
    def play_loop(self, choreography, speed_factor, speed_mode):
        """Play a choreography in loop"""
        while True:
            self.play_once(choreography, speed_factor, speed_mode)

    async def play_once(self, choreography, speed_factor, speed_mode):
        """Play a choreography once"""
        for step in choreography:
            left_motor_speed = step[LS]*speed_factor
            right_motor_speed = step[RS]*speed_factor

            await self.node.set_variables(  # apply the control on the wheels
                {"motor.left.target": [int(left_motor_speed)], "motor.right.target": [int(right_motor_speed)]})
            
            sleep(step[DT])
        
async def process_messages(client: ClientAsync):
    """Process waiting messages from the Thymio driver."""

    try:
        while True:
            client.process_waiting_messages()
            await sleep(PROCESS_MSG_INTERVAL)

    except Exception:
        pass

        