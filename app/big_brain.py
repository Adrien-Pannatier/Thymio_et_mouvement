import math
from asyncio import sleep
from dataclasses import dataclass

from app.config import *
from app.context import Context
from app.filtering import Filtering
# from app.global_navigation import GlobalNavigation
from app.motion_control import MotionControl
from app.utils.console import *
from app.utils.types import Channel, Vec2

POSITION_THRESHOLD = 0.5

@dataclass
class Modules:
    """A class to hold all the modules"""

    filtering: Filtering
    # global_nav: GlobalNavigation
    motion_control: MotionControl


class BigBrain:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def start_thinking(self: Channel[Vec2]):
        self.init()

        modules = self.init_modules()

        with modules.filtering, modules.motion_control: 
            await self.loop(modules)

    def init(self):
        """Initialise the big brain"""

        self.stop_requested = False

    def init_modules(self):
        """Initialise the modules"""

        filtering = Filtering(self.ctx)
        # global_nav = GlobalNavigation(self.ctx)
        motion_control = MotionControl(self.ctx)

        return Modules(filtering, motion_control)

    async def loop(self, modules: Modules):

        while True:
            # update pose
            modules.filtering.predict()

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