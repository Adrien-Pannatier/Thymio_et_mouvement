# todo: add color change if in mode
# from asyncio import sleep
from dataclasses import dataclass
import time
import os
import sys
from rich.padding import Padding
from rich.panel import Panel

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

        # record script choices
        self.r_asw = None

    def start_thinking(self):
        self.init()

        modules = self.init_modules()
        ui("Welcome!")
        time.sleep(1) # USER EXPERIENCE
        self.loop(modules)

    def init(self):
        """Initialise the big brain"""

        self.stop_requested = False

    def init_modules(self):
        """Initialise the modules"""
        process_controler_data = ProcessControlerData()
        choreographer = ChoreographyManager()
        motion_control = MotionControl()

        return Modules(process_controler_data, choreographer, motion_control)

    def loop(self, modules: Modules):

        while True:
            

            if self.wanted_mode == "help":
                ui("[bold white]'record'[/] to record a choreography")
                ui("[bold white]'play'[/] to play a choreography")
                ui("[bold white]'info'[/] to get information about the choreographies")
                ui("[bold white]'quit'[/] to quit the program")
                print("\n")
                ui("press enter to continue")
                input(">")
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
                if modules.motion_control.node is not None:
                    modules.motion_control.disconnect_thymio()
                sys.exit()

            elif self.wanted_mode == "No mode":
                """Print the presentation banner."""
                console.print(
                    Padding(
                        Panel(
                            "[bold green] MODE SELECTION"
                        ),
                        (1, 2),
                    ),
                    justify="left",
                )
                ui("What mode would you like to do? (you can type 'help' for more information)")
                self.wanted_mode = input(">")
            
            else:
                ui("I don't understand")
                time.sleep(1) # USER EXPERIENCE
                self.wanted_mode = "No mode"
            
            # os.system("cls")
            print("_________________________________________________________________________________________")


    def record_script(self, modules: Modules):
        """Record a choreography"""

        console.print(
            Padding(
                Panel(
                    "[bold yellow] RECORDING MODE"
                ),
                (1, 2),
            ),
            justify="left",
        )        

        # initialisation of record mode
        modules.process_controler_data.init_record()

        ui("Welcome to the recording mode!")
        time.sleep(1) # USER EXPERIENCE
        ui("What can I do for you? (you can type 'help' for more information)")
        self.r_asw = input(">")

        if self.r_asw == "help":
            ui("[bold white]'display'[/] to display the choreographies")
            ui("[bold white]'add'[/] to add a choreography")
            ui("[bold white]'remove'[/] to remove a choreography")
            ui("[bold white]'edit'[/] to edit a choreography")
            ui("[bold white]'debug'[/] to debug the record mode")
            ui("[bold white]'quit'[/] to quit the recording mode")
            ui("press enter to continue")
            input(">")
            # return to question in record mode
            return

        elif self.r_asw == "display":
            ui("Here are the choreographies:")
            modules.choreographer.displays_choreography_dict()

        elif self.r_asw == "add":
            ui("What is the name of the choreography?")
            name = input(">")
            # check if the choreography already exists
            if name in modules.choreographer.choreography_dict:
                warning("This choreography already exists")
                return
            else:
                ui("Press enter to start recording the choreography")
                input(">")
                status = console.status("Recording choreography", spinner_style="yellow")
                status.start()
                recorded_choreography = modules.process_controler_data.record()
                status.stop()
                # add the choreography to the choreography dictionary
                modules.choreographer.create_choreography(name, recorded_choreography)
                ui("Choreography created! " + name)
        
        elif self.r_asw == "remove":
            ui("What is the name of the choreography you want to remove?")
            name = input(">")
            if name == "quit":
                self.r_asw
                return
            # check if the choreography exists
            if name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            else:
                modules.choreographer.delete_choreography(name)

        elif self.r_asw == "edit":
            ui("not implemented yet")

        elif self.r_asw == "debug":
            ui("welcome to the debug mode!")
            ui("press enter to start debuging")
            input(">")
            ui("starting debuging")
            modules.process_controler_data.debug()

        else:
            ui("I don't understand")

        time.sleep(1) # USER EXPERIENCE
        ui("getting back to mode selection")
        self.r_asw = None
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

        

        
