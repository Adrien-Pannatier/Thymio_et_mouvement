import math
from asyncio import sleep
from dataclasses import dataclass

from app.config import *
from app.context import Context
from app.process_controler_data import ProcessControlerData
from app.choreography_manager import ChoreographyManager
from app.motion_control import MotionControl
from app.utils.console import *
from app.utils.types import Channel, Vec2

POSITION_THRESHOLD = 0.5

@dataclass
class Modules:
    """A class to hold all the modules"""
    process_controler_data: ProcessControlerData
    choreographer: ChoreographyManager
    motion_control: MotionControl


class BigBrain:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def start_thinking(self: Channel[Vec2]):
        self.init()

        modules = self.init_modules()

        with modules.process_controler_data, modules.choreographer, modules.motion_control: 
            await self.loop(modules)

    def init(self):
        """Initialise the big brain"""

        self.stop_requested = False

    def init_modules(self):
        """Initialise the modules"""
        process_controler_data = ProcessControlerData(self.ctx)
        choreographer = ChoreographyManager(self.ctx)
        motion_control = MotionControl(self.ctx)

        return Modules(process_controler_data, choreographer, motion_control)

    async def loop(self, modules: Modules):

        while True:
        # if in record choreography mode
            # get choreography name
            # get speeds from process controler data 
            # add step to the choreography

        # if in play choreography mode
            # get wanted choreography name
            # get choreography step
            # send step to motion control

            # trigger state update
            self.ctx.state.changed() 

            # end of path is reached message
            if self.ctx.state.arrived == True:
                self.ctx.state.end = None
                self.ctx.state.path = None
                self.ctx.state.arrived = False
                console.info("End of path reached")
                self.ctx.state.changed() # trigger state update

            self.ctx.debug_update = False
            await sleep(UPDATE_FREQUENCY) # stop at the end of the path