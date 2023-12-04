from dataclasses import dataclass
import time
import json

from app.config import *
from app.process_controler_data import ProcessControlerData
from app.choreography_manager import ChoreographyManager
from app.motion_control import MotionControl
from app.utils.console import *
from app.GUI import App
import os

@dataclass
class Modules:
    """A class to hold all the modules"""
    process_controler_data: ProcessControlerData
    choreographer: ChoreographyManager
    motion_control: MotionControl

class Gui:
    def __init__(self, modules):
        self.app = App(modules=modules)
        self.app.mainloop()
        modules.choreographer.save_settings()
        ui("Goodbye!")

class BigBrain:
    def __init__(self):

        # record script choices
        self.r_asw = None

        # editor script choice
        self.e_asw = None

    def start_thinking(self):
        self.init()

        modules = self.init_modules()
        ui("Welcome!")
        self.loop(modules)


    def init(self):
        """Initialise the big brain"""

        # create settings file if it doesn't exist
        try:
            with open(SETTINGS_PATH, "r") as file:
                pass
        except FileNotFoundError:
            # if directory not found, create it
            if not os.path.exists(SETTINGS_DIR):
                os.makedirs(SETTINGS_DIR)
            # if file not found, create it
            with open(SETTINGS_PATH, "w") as file:
                json.dump({}, file)
        self.stop_requested = False

    def init_modules(self):
        """Initialise the modules"""
        choreographer = ChoreographyManager()
        process_controler_data = ProcessControlerData()
        motion_control = MotionControl()

        return Modules(process_controler_data, choreographer, motion_control)

    def loop(self, modules: Modules):

        # start the GUI
        Gui(modules)

        # delete all temp assets in folder GUI_assets/temp_fig
        folder_path = "app\\GUI_assets\\temp_fig"
        try:
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".png"):
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)
        except:
            pass