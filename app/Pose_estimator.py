import math
import numpy as np
from app.utils.console import *
from app.config import DIAMETER

class PoseEstimator:
    """
    Class containing the pose estimator

    @variables:
    Var position: position of the thymio
    Var orientation: orientation of the thymio
    
    @functions:
    Func __init__: initiates the class
    Func update: updates the pose of the thymio
    """

    def __init__(self, position, orientation) -> None:
        self.position = position
        self.orientation = orientation

    def update(self, speed_r_mot, speed_l_mot):
        """
        Updates the pose of the thymio

        param speed_r_mot: right wheel speed sensor in cm/s
        param speed_l_mot: left wheel speed sensor in cm/s

        return: updated position and orientation
        """

        self.position[0] += (speed_r_mot + speed_l_mot) / 2 * math.cos(self.orientation)
        self.position[1] += (speed_r_mot + speed_l_mot) / 2 * math.sin(self.orientation)
        self.orientation += (speed_r_mot - speed_l_mot) / DIAMETER

        return self.position[0], self.position[1], self.orientation