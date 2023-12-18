from dataclasses import dataclass
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
    def __init__(self, modules, application_path):
        self.application_path = application_path
        self.app = App(modules=modules, application_path=application_path)
        self.app.mainloop()
        modules.choreographer.save_settings()
        ui("Goodbye!")

class BigBrain:
    def __init__(self, application_path):
        self.application_path = application_path

    def start_thinking(self):
        self.init()
        modules = self.init_modules()
        ui("Welcome!")
        self.loop(modules)


    def init(self):
        """Initialise the big brain"""
        # create settings file if it doesn't exist
        try:
            with open(self.application_path + SETTINGS_PATH, "r") as file:
                pass
        except FileNotFoundError:
            # if directory not found, create it
            if not os.path.exists(self.application_path + SETTINGS_DIR):
                os.makedirs(self.application_path + SETTINGS_DIR)
            # if file not found, create it
            with open(self.application_path + SETTINGS_PATH, "w") as file:
                json.dump({}, file)
        self.stop_requested = False

    def init_modules(self):
        """Initialise the modules"""
        choreographer = ChoreographyManager(app_path=self.application_path)
        process_controler_data = ProcessControlerData(app_path=self.application_path)
        motion_control = MotionControl()

        return Modules(process_controler_data, choreographer, motion_control)

    def loop(self, modules: Modules):

        # start the GUI
        Gui(modules, self.application_path)

        # delete all temp assets in folder GUI_assets/temp_fig
        folder_path = self.application_path + "app\\GUI_assets\\temp_fig"
        try:
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".png"):
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)
        except:
            pass