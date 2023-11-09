# todo: add color change if in mode
from asyncio import sleep
from dataclasses import dataclass
import time
import os

from app.config import *
from app.process_controler_data import ProcessControlerData
from app.choreography_manager import ChoreographyManager
from app.motion_control import MotionControl
from app.utils.console import *

POSITION_THRESHOLD = 0.5

@dataclass
class Modules:
    """A class to hold all the modules"""
    process_controler_data: ProcessControlerData
    choreographer: ChoreographyManager
    motion_control: MotionControl


class BigBrain:
    def __init__(self):
        self.wanted_mode = "No mode"

    async def start_thinking(self):
        self.init()

        modules = self.init_modules()
        ui("Welcome!")
        time.sleep(1) # USER EXPERIENCE
        await self.loop(modules)

    def init(self):
        """Initialise the big brain"""

        self.stop_requested = False

    def init_modules(self):
        """Initialise the modules"""
        process_controler_data = ProcessControlerData()
        choreographer = ChoreographyManager()
        motion_control = MotionControl()

        return Modules(process_controler_data, choreographer, motion_control)

    async def loop(self, modules: Modules):

        while True:

            if self.wanted_mode == "No mode":
                ui("What mode would you like to do? (you can type 'help' for more information)")
                self.wanted_mode = input(">")

            elif self.wanted_mode == "help":
                ui("'record' to record a choreography")
                ui("'play' to play a choreography")
                ui("'info' to get information about the choreographies")
                ui("'quit' to quit the program")
                time.sleep(1) # USER EXPERIENCE
                self.wanted_mode = "No mode"

            elif self.wanted_mode == "record":
                self.record_script(modules)

            elif self.wanted_mode == "play":
                self.play_script(modules)

            elif self.wanted_mode == "info":
                self.info_script(modules)

            elif self.wanted_mode == "quit":
                ui("Goodbye!")
                return
            
            else:
                ui("I don't understand")
                time.sleep(1) # USER EXPERIENCE
                self.wanted_mode = "No mode"
            
            # os.system("cls")
            print("_________________________________________________________________________________________")


    def record_script(self, modules: Modules):
        """Record a choreography"""

        # initialisation of record mode
        modules.process_controler_data.init_record()
        print("_________________________________________________________________________________________")
        info("RECORDING MODE")
        print("_________________________________________________________________________________________")
        ui("Welcome to the recording mode!")
        time.sleep(1) # USER EXPERIENCE
        ui("What can I do for you? (you can type 'help' for more information)")
        answer = input(">")

        if answer == "help":
            ui("'display' to display the choreographies")
            ui("'add' to add a choreography")
            ui("'remove' to remove a choreography")
            ui("'edit' to edit a choreography")
            time.sleep(1) # USER EXPERIENCE
            # return to question in record mode

        elif answer == "display":
            ui("Here are the choreographies:")
            modules.choreographer.displays_choreography_dict()

        elif answer == "add":
            ui("What is the name of the choreography?")
            name = input(">")
            # check if the choreography already exists
            if name in modules.choreographer.choreography_dict:
                warning("This choreography already exists")
                return
            else:
                status = console.status("Recording choreography", spinner_style="yellow")
                status.start()
                recorded_choreography = modules.process_controler_data.record()
                status.stop()
                # add the choreography to the choreography dictionary
                modules.choreographer.create_choreography(name, recorded_choreography)
                ui("Choreography created! " + name)
        
        elif answer == "remove":
            ui("What is the name of the choreography you want to remove?")
            name = input(">")
            # check if the choreography exists
            if name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            else:
                modules.choreographer.delete_choreography(name)

        elif answer == "edit":
            ui("not implemented yet")

        else:
            ui("I don't understand")
        
        self.wanted_mode = "No mode"

    def play_script(self, modules: Modules):
        """Play a choreography"""

        # initialisation of play mode
        modules.motion_control.init_thymio_connection()

        ui("Do you want to play a choreography or a sequence? [choreography/sequence]")
        answer = input(">")

        if answer == "choreography":
            ui("What is the name of the choreography you want to play?")
            name = input(">")
            # check if the choreography exists
            if name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            else:
                ui("In what mode do you want to play the choreography? [loop/once]")
                play_mode = input(">")
                # check if the play mode exists
                if play_mode not in ["loop", "once"]:
                    warning("This play mode does not exist")
                    return
                ui("What is the speed factor of the choreography? [1-10]")
                speed_factor = input(">")
                # check if the speed factor is valid
                try:
                    speed_factor = int(speed_factor)
                except ValueError:
                    warning("This speed factor is not valid")
                    return
                if speed_factor not in range(1, 11):
                    warning("This speed factor is not valid")
                    return

                # play the choreography
                modules.motion_control.play_choreography(modules.choreographer.choreography_dict[name], speed_factor, play_mode)

        elif answer == "sequence":
            ui("not implemented yet")
            pass

        self.wanted_mode = "No mode"

    def info_script(self, modules):
        """Info about the choreographies"""
        ui("The choreographies available are the following:")
        modules.choreographer.displays_choreography_dict()
        time.sleep(1) # USER EXPERIENCE
        
        # check if choreographies exist
        if len(modules.choreographer.choreography_dict) == 0:
            ui("There are no choreographies")
            self.wanted_mode = "No mode"
            time.sleep(1) # USER EXPERIENCE
            return
        
        ui("Do you want to know more about a choreography? [Y/n]")
        answer = input(">")

        if answer == "y":
            ui("What is the name of the choreography you want to know more about?")
            name = input(">")
            # check if the choreography exists
            if name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            else:
                ui("Here is the choreography " + name)
                choreography_name, speed_factor, path = modules.choreographer.choreography_dict[name].get_info()
                ui("Name: " + choreography_name)
                ui("Speed factor: " + str(speed_factor))
                ui("Path: " + path)
        
        self.wanted_mode = "No mode"

        

        
