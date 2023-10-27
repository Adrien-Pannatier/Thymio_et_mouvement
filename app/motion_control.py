import math
from time import time

from app.config import MAX_WAIT, INDEX_FW, KP_fwspeed, KI_fwspeed, KD_fwspeed, KP_anspeed, KI_anspeed, KD_anspeed 
from app.context import Context
from app.controllers import PIDController
from app.utils.module import Module
from app.utils.types import Vec2

class MotionControl(Module):

    def __init__(self, ctx: Context):
        super().__init__(ctx)
        self.ctx = ctx
        self.waypoint = None
        self.next_waypoint_index = None
        self.last_update = None

        # initialise the PID controllers
        self.pid_forward_speed_controller = PIDController(KP_fwspeed, KI_fwspeed, KD_fwspeed)
        self.pid_angular_speed_controller = PIDController(KP_anspeed, KI_anspeed, KD_anspeed)

    def setNewWaypoint(self, index_offset):
        if self.ctx.state.next_waypoint_index is None:
            return
        if self.ctx.state.path is None:
            return
        
        index = min(self.ctx.state.next_waypoint_index + index_offset, len(self.ctx.state.path) - 1)

        if index == -1:  # no more path
            return
        if self.ctx.state.path[index] is None:  # not defined waypoint problem
            return
        
        self.waypoint = self.ctx.state.path[index]
        self.ctx.state.next_waypoint_index = index

    async def run(self):  # update function
        while True:
            await self.ctx.pose_speed_update.wait(timeout=MAX_WAIT) # wait for the pose and speed update (triggered by prediction in filtering)
            await self.update_motor_control()  # update the control function

    async def update_motor_control(self):  # control function
        if self.waypoint is None: # start WP list if WP is none
            self.setNewWaypoint(INDEX_FW)

        command_info = self.controllers()
        if command_info is None:
            return
        (reached, speed_left_controller, speed_right_controller) = command_info

        if reached:
            if self.ctx.state.next_waypoint_index is None:
                return
            if self.ctx.state.path is None:
                return
            self.setNewWaypoint(INDEX_FW)

        await self.ctx.node.set_variables(  # apply the control on the wheels
            {"motor.left.target": [int(speed_left_controller)], "motor.right.target": [int(speed_right_controller)]}
        )
        
    def controllers(self):
        """
        
        """
        if self.last_update is None:
            self.last_update = time()
            return
        
        now = time()
        dt = now - self.last_update

        # if no position waypoint or rientation, return none
        if self.ctx.state.forward_speed is None or self.ctx.state.angular_speed is None or self.waypoint is None:
            return None 

        current_fwspeed = self.ctx.state.forward_speed
        current_anspeed = self.ctx.state.angular_speed

        waypoint_fwspeed = self.waypoint[0]
        waypoint_anspeed = self.waypoint[1]

        fwspeed_output = self.pid_forward_speed_controller.update(waypoint_fwspeed, current_fwspeed, dt)
        anspeed_output = self.pid_angular_speed_controller.update(waypoint_anspeed, current_anspeed, dt)

        fwspeed_command = current_fwspeed + fwspeed_output * dt
        anspeed_command = current_anspeed + anspeed_output * dt

        self.last_update = now

        # reached speed condition
        if abs(fwspeed_command - waypoint_fwspeed) < 0.1:
            if (self.ctx.state.next_waypoint_index == len(self.ctx.state.path or []) - 1):
                self.ctx.state.arrived = True
                return [True, 0, 0]
            return [True, fwspeed_command, anspeed_command]
        return [False, fwspeed_command, anspeed_command]