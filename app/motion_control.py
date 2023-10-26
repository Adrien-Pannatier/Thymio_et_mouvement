import math
from time import time

from app.config import MAX_WAIT, INDEX_FW, KP_speed, KI_speed, KD_speed, KP_orientation, KI_orientation, KD_orientation
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

        self.pid_speed_controller = PIDController(KP_speed, KI_speed, KD_speed)
        self.pid_orientation_controller = PIDController(KP_orientation, KI_orientation, KD_orientation)
    
        self.speed_history = []
        self.orientation_history = []

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
            await self.ctx.pose_update.wait(timeout=MAX_WAIT) # wait for the pose update (triggered by prediction in filtering)
            await self.update_motor_control()  # update the control function

    async def update_motor_control(self):  # control function
        if self.waypoint is None: # start WP list if WP is none
            self.setNewWaypoint(INDEX_FW)
        
    def controllers(self):
        """
        
        """
        if self.last_update is None:
            self.last_update = time()
            return
        
        now = time()
        dt = now - self.last_update

        # if no position waypoint or rientation, return none
        if self.ctx.state.position is None or self.waypoint is None or self.ctx.state.orientation is None:
            return None 

        current_position = self.ctx.state.position

        waypoint_position = Vec2(self.waypoint[0], self.waypoint[1])

        position_dif = waypoint_position - current_position

        diff_angle = math.atan2(position_dif[1], position_dif[0]) - self.ctx.state.orientation
        diff_dist = min(math.sqrt(position_dif[1] * position_dif[1] + position_dif[0] * position_dif[0]), 8) # FIND OUT WHY 8 --------------------------------------------------------------
        
        self.ctx.state.dist = diff_dist # update the distance in the state

        if abs(diff_angle) > math.pi:
            diff_angle = diff_angle - math.copysign(2 * math.pi, diff_angle)

        

        self.last_update = now