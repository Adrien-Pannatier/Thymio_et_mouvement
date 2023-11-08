import math
from time import time

from app.config import MAX_WAIT, INDEX_FW, DIAMETER
from app.context import Context
from app.utils.module import Module
from app.utils.types import Vec2

class MotionControl(Module):

    def __init__(self, ctx: Context):
        super().__init__(ctx)
        self.ctx = ctx
        self.step = None
        self.next_step_index = None
        self.last_update = None

    def set_new_step(self, index_offset):
        if self.ctx.state.next_step_index is None:
            return
        if self.ctx.state.path is None:
            return
        
        index = min(self.ctx.state.next_step_index + index_offset, len(self.ctx.state.path) - 1)

        if index == -1:  # no more path
            return
        if self.ctx.state.path[index] is None:  # not defined waypoint problem
            return
        
        self.waypoint = self.ctx.state.path[index]
        self.ctx.state.next_step_index = index

    async def run(self):  # update function
        while True:
            await self.update_motor_control()  # update the control function

    async def update_motor_control(self):  # control function
        if self.step is None: # start WP list if WP is none
            self.set_new_step(INDEX_FW)

        command_info = self.get_and_process_step() # get step info from big brain

        if command_info is None:
            return
        (reached, speed_left_controller, speed_right_controller) = command_info

        if reached:
            if self.ctx.state.next_step_index is None:
                return
            if self.ctx.state.path is None:
                return
            self.set_new_step(INDEX_FW)

        await self.ctx.node.set_variables(  # apply the control on the wheels
            {"motor.left.target": [int(speed_left_controller)], "motor.right.target": [int(speed_right_controller)]}
        )
        
    def get_and_process_step(self):

        # get step from big brain and update forward and angular speed

        # if no position waypoint or rientation, return none
        if self.ctx.state.forward_speed is None or self.ctx.state.angular_speed is None or self.waypoint is None:
            return None 
        
        # calculate the speed of the left and right wheels
        wheel_base = 0.1  # replace with your actual wheel base
        speed_left = self.ctx.state.forward_speed - DIAMETER/2 * self.ctx.state.angular_speed
        speed_right = self.ctx.state.forward_speed + DIAMETER/2 * self.ctx.state.angular_speed

        # return the calculated speeds
        return speed_left, speed_right

        