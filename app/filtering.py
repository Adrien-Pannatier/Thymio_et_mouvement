import math
from asyncio import sleep

from app.config import SLEEP_DURATION, THYMIO_TO_CM
from app.context import Context
from app.Pose_estimator import PoseEstimator
from app.utils.module import Module
from app.utils.types import Vec2


class Filtering(Module):
    """
    Class containing the pose estimator

    @variables:
    Var ctx: context of the application
    Var estimator: estimator of the pose

    @functions:
    Func __init__: initiates the class
    # Func run: runs the module
    Func process_event: callback function for sensor update
    Func predict: predict the next position of the thymio
    """

    def __init__(self, ctx: Context):
        super().__init__(ctx)

        self.estimator = PoseEstimator((0,0), math.pi/2) # initial position of the thymio 0,0 facing north

    async def run(self):
        while True:
            await sleep(SLEEP_DURATION)

    def process_event(self, variables):
        """
        When variables from sensors are updated, estimate position

        param: variables from Thymio censors
        """
        [vl] = variables["motor.left.speed"]
        [vr] = variables["motor.right.speed"]

        vl = vl * THYMIO_TO_CM
        vr = vr * THYMIO_TO_CM

        self.predict(vl, vr)

        self.ctx.pose_speed_update.trigger()
        self.ctx.state.changed()

    def predict(self, vl, vr):
        """ 
        Predicts the next position of the thymio and updates the state

        param vl: left wheel speed sensor in cm/s
        param vr: right wheel speed sensor in cm/s
        """
        pose_x_est, pose_y_est, orientation_est = self.estimator.update(vl, vr)

        self.ctx.state.position = (pose_x_est, pose_y_est)
        self.ctx.state.orientation = orientation_est