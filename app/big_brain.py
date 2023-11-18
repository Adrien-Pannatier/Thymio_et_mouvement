from dataclasses import dataclass
import time
import sys
from rich.padding import Padding
from rich.panel import Panel

from app.config import *
from app.process_controler_data import ProcessControlerData
from app.choreography_manager import ChoreographyManager
from app.motion_control import MotionControl
from app.editor import Editor
from app.utils.console import *

@dataclass
class Modules:
    """A class to hold all the modules"""
    process_controler_data: ProcessControlerData
    choreographer: ChoreographyManager
    motion_control: MotionControl
    editor: Editor


class BigBrain:
    def __init__(self):
        self.wanted_mode = "First time"

        # record script choices
        self.r_asw = None

        # editor script choice
        self.e_asw = None

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
        editor = Editor()

        return Modules(process_controler_data, choreographer, motion_control, editor)

    def loop(self, modules: Modules):
        console.print(
            Padding(
                Panel(
                    "[bold deep_pink4] MODE SELECTION "
                ),
                (1, 2),
            ), 
            justify="left",
        )
        time.sleep(1) # USER EXPERIENCE
        ui("Hi! I'm UI, your personal assistant. I am not a real AI, but I can help you with the program.\n"
            + SPC + "Now you are in the mode selection mode, here you can choose between different modes.")
        time.sleep(1) # USER EXPERIENCE
        print("\n")
        ui("[bold deep_pink4]Here are the modes available:[/]\n"
        + SPC + "[bold white]'record'[/] to record a choreography\n"
        + SPC + "[bold white]'play'[/] to play a choreography\n"
        + SPC + "[bold white]'editor'[/] to edit choreographies, create sequences and more\n"
        + SPC + "[bold white]'info'[/] to get information about the choreographies\n"
        + SPC + "[bold white]'quit'[/] to quit the program")
        time.sleep(1) # USER EXPERIENCE
        print("\n")
        ui("Which mode would you like to select?")
        self.wanted_mode = input(">")
        print("_________________________________________________________________________________________")

        while True:

            if self.wanted_mode == "record":
                self.record_script(modules)

            elif self.wanted_mode == "play":
                self.play_script(modules)

            elif self.wanted_mode == "editor":
                self.editor_script(modules)

            elif self.wanted_mode == "info":
                self.info_script(modules)

            elif self.wanted_mode == "quit":
                # ui("Goodbye!")
                console.print('''[cyan]　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
　　　　　　　　　　　　 　◇　　　　　　　　　　　　　　　　
　　　　　　　　　　　　　ｉ　　　　　　　　　　　　　　　　
　　　　　　　　　　　　　＼　　　　　　　　　　　　　　　　
　　　　　　　　　　　　　　╲　　　　　　　　　　　　　　　
　　　　　　　　　　　　　　〔　　　　　　　　　　　　　　　
　　　　　　　　　　　　╭～⌒ ～╮　　　　　　　　　　　　　
　　　　　　　　　　　　│　　　│　　　　　　　　　　　　　
　　　　　　　　　　　　│　　　│　　　　　　Goodbye!　　　　
　　　　　　　　　 　　╭⌒ ╮  ╭⌒ ╮　　　   /　　　　　　　　
　　　　　　　　　 　　│Ｏ│  │Ｏ│　　　　/　　　　　　
　　　　　　　　　 　　╰╮ ╯  ╰ ╭╯　　　　　　　　　　　　
　　　　　　　　　　　　│   o  │　　　　　　　　　　　　　
　　　　　　　　　　　　│      │　　　　　　　　　　　　　
　　　　　　　　　　　　│　  　│　　　　　　　　　　　　　
　　　　　　　　　▕︸︸︸︸︸︸︸︸︸－～　　　　　　　　　
　　　　　　　　　︷　　　　　　 　 ▕－～╲　　　　　　　　
　　　　　　　　╱＞〉　⌒╮　　 　    ▕　  　╲╲　　　　　　　
　　　　　　　╱╱  ▕　〈　ノ　       ▕　    ╲╲　　　　　　
　 　　　　　╱╱ 　▕　　︶　　 　    ▕　　　　╲╲　　　　　[/]''')
                time.sleep(3) # USER EXPERIENCE
                # if modules.motion_control.node is not None:
                #     modules.motion_control.disconnect_thymio()
                sys.exit()

            elif self.wanted_mode == "No mode":
                """Print the presentation banner."""
                console.print(
                    Padding(
                        Panel(
                            "[bold deep_pink4] MODE SELECTION "
                        ),
                        (1, 2),
                    ), 
                    justify="left",
                )
                ui("Welcome back to the mode selection mode!")
                time.sleep(1) # USER EXPERIENCE
                print("\n")
                ui("[bold deep_pink4]Here are the modes available:[/]\n"
                + SPC + "[bold white]'record'[/] to record a choreography\n"
                + SPC + "[bold white]'play'[/] to play a choreography\n"
                + SPC + "[bold white]'editor'[/] to edit choreographies, create sequences and more\n"
                + SPC + "[bold white]'info'[/] to see what sequences and choreographies exist in detail\n"
                + SPC + "[bold white]'quit'[/] to quit the program")
                time.sleep(1) # USER EXPERIENCE
                print("\n")
                ui("Which mode would you like to select?")
                self.wanted_mode = input(">")
                print("_________________________________________________________________________________________")

            
            else:
                ui("I don't understand")
                time.sleep(1) # USER EXPERIENCE
                self.wanted_mode = "No mode"
            
            # os.system("cls")
            print("_________________________________________________________________________________________")


    def record_script(self, modules: Modules):
        """Record a choreography"""

        if self.r_asw == "display":
            ui("Here are the choreographies:")
            modules.choreographer.displays_choreography_dict()
            time.sleep(1)
            ui("press enter to get back to record mode")
            input(">")
            print("_________________________________________________________________________________________")
            self.r_asw = None
            pass

        elif self.r_asw == "add":
            ui("What is the name of the choreography?")
            name = input(">")
            print("_________________________________________________________________________________________")
            # check if the choreography already exists
            if name in modules.choreographer.choreography_dict:
                warning("This choreography already exists")
                return
            else:
                ui("Press enter to start recording the choreography")
                input(">")
                print("_________________________________________________________________________________________")
                status = console.status("Recording choreography", spinner_style="yellow")
                status.start()
                recorded_choreography = modules.process_controler_data.record()
                status.stop()
                # add the choreography to the choreography dictionary
                modules.choreographer.create_choreography(name, recorded_choreography)
                ui("Choreography created! " + name)
            self.r_asw = None

        elif self.r_asw == "debug":
            ui("welcome to the debug mode!")
            ui("press enter to start debuging")
            input(">")
            print("_________________________________________________________________________________________")
            ui("starting debuging")
            modules.process_controler_data.debug()
            self.r_asw = None

        elif self.r_asw == "quit":
            self.r_asw = None
            self.wanted_mode = "No mode"
            ui("getting back to mode selection")
            return
        
        elif self.r_asw == None:
            console.print(
                Padding(
                    Panel(
                        "[bold gold1] RECORDING MODE"
                    ),
                    (1, 2),
                ),
                justify="left",
            )
            time.sleep(1) # USER EXPERIENCE
            ui("You are in the recording mode, here you can record new choreographies using the fake thymio. \n"
                + "           You can also manage the different choreographies")
            time.sleep(1) # USER EXPERIENCE
            print("\n")
            ui("[bold gold1]Welcome to the recording mode! here is what I can do for you:[/]\n"
            + SPC + "[bold white]'display'[/] to display the choreographies\n"
            + SPC + "[bold white]'add'[/] to add a choreography\n"
            + SPC + "[bold white]'debug'[/] to debug the record mode\n"
            + SPC + "[bold white]'quit'[/] to quit the recording mode")
            print("\n")

            # initialisation of record mode
            modules.process_controler_data.init_record()
            time.sleep(1) # USER EXPERIENCE
            ui("What can I do for you?")
            self.r_asw = input(">")
            print("_________________________________________________________________________________________")

        else:
            ui("I don't understand")

        time.sleep(1) # USER EXPERIENCE

    def play_script(self, modules: Modules):
        """Play a choreography"""

        console.print(
            Padding(
                Panel(
                    "[bold chartreuse3]PLAY MODE"
                ),
                (1, 2),
            ),
            justify="left",
        )      
        time.sleep(1) # USER EXPERIENCE
        ui("[bold chartreuse3]Welcome to the play mode![/]\n"
        + SPC + "here is what I can do for you:\n"
        + SPC + "[bold white]'choreography'[/] to play a choreography\n"
        + SPC + "[bold white]'sequence'[/] to play a sequence\n"
        + SPC + "[bold white]'quit'[/] to quit the play mode")

        # initialisation of play mode
        if modules.motion_control.node is None:
            if not modules.motion_control.init_thymio_connection():
                ui("Do you want to try again? [Y/n]")
                try_asw = input(">")
                print("_________________________________________________________________________________________")
                if try_asw == "y":
                    pass
                else:
                    self.wanted_mode = "No mode"
                    return

        ui(f"Do you want to play a choreography or a sequence?")
        answer = input(">")
        print("_________________________________________________________________________________________")

        if answer == "choreography":
            modules.choreographer.displays_choreography_dict() # display choreographies
            ui("What is the name of the choreography you want to play?")
            name = input(">")
            print("_________________________________________________________________________________________")
            # check if the name is a number
            if name.isdigit():
                name = self.nbr_to_choreography_name(modules, name)

            # check if the choreography exists
            if name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            else:
                ui("In what mode do you want to play the choreography? /loop/mult/once/")
                play_mode = input(">")
                print("_________________________________________________________________________________________")
                # check if the play mode exists
                if play_mode not in ["loop", "mult", "once"]:
                    warning("This play mode does not exist")
                    return
                if play_mode == "mult":
                    ui("How many times do you want to play the choreography?")
                    nbr_repetition = input(">")
                    print("_________________________________________________________________________________________")

                    # check if the number of repetition is valid
                    try:
                        nbr_repetition = int(nbr_repetition)
                    except ValueError:
                        warning("This number of repetition is not valid")
                        return
                ui(f"What is the speed factor of the choreography? [{MIN_SPEED_FACTOR}-{MAX_SPEED_FACTOR}]")
                speed_factor = input(">")
                print("_________________________________________________________________________________________")

                # check if the speed factor is valid
                try:
                    speed_factor = int(speed_factor)
                except ValueError:
                    warning("This speed factor is not valid")
                    return
                if speed_factor not in range(MIN_SPEED_FACTOR, MAX_SPEED_FACTOR + 1):
                    warning("This speed factor is not valid")
                    return

                # play the choreography
                modules.motion_control.play_choreography(modules.choreographer.choreography_dict[name], speed_factor, play_mode, nbr_repetition)
                ui("Choreography played!")
                

        elif answer == "sequence":
            ui("not implemented yet")
            pass

        elif answer == "quit":
            ui("getting back to mode selection")
            self.wanted_mode = "No mode"
            return

        else:
            ui("I don't understand")
            time.sleep(1) # USER EXPERIENCE
    
        self.wanted_mode = "No mode"
        if modules.motion_control.node is not None:
                    modules.motion_control.disconnect_thymio()

    def editor_script(self, modules: Modules):
        """Edit choreographies"""
        console.print(
            Padding(
                Panel(
                    "[bold dark_cyan] EDITOR MODE"
                ),
                (1, 2),
            ),
            justify="left",
        )      
        time.sleep(1) # USER EXPERIENCE
        ui("Welcome to the editor! In the editor mode, you can edit choreographies, create sequences and more")
        print("\n")
        time.sleep(1) # USER EXPERIENCE
        ui("[bold dark_cyan]Here are the commands available:[/]\n"
        + SPC + "[bold white]'delete chor'[/] to delete a choreography\n"
        + SPC + "[bold white]'create seq'[/] to create a sequence\n"
        + SPC + "[bold white]'delete seq'[/] to delete a sequence\n"
        + SPC + "[bold white]'quit'[/] to quit the editor")
        print("\n")
        time.sleep(1) # USER EXPERIENCE
        ui("What can I do for you?")
        self.e_asw = input(">")
        print("_________________________________________________________________________________________")

        if self.e_asw == "disp chor":
            ui("Here are the choreographies:")
            modules.choreographer.displays_choreography_dict()
            time.sleep(1)
            return
        elif self.e_asw == "disp seq":
            ui("Here are the sequences:")
            modules.choreographer.displays_sequence_dict()
            time.sleep(1)
            return
        elif self.e_asw == "delete chor":
            modules.choreographer.displays_choreography_dict()
            ui("What is the name/number of the choreography you want to delete?")
            name = input(">")
            print("_________________________________________________________________________________________")
            if name == "quit":
                self.r_asw = None
                return
            # check if the choreography exists
            if name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            else:
                modules.choreographer.delete_choreography(name)
                ui("Press enter to get back to editor mode")
                input(">")
                print("_________________________________________________________________________________________")
            self.e_asw = None

        elif self.e_asw == "create seq":
            sequence_order = []
            ui("How do you want to name your sequence?")
            name = input(">")
            print("_________________________________________________________________________________________")
            # check if the sequence already exists
            if name in modules.choreographer.sequence_dict:
                warning("This sequence already exists")
                return
            else:
                ui("Could you describe the sequence a bit?")
                description = input(">")
                print("_________________________________________________________________________________________")
                correct_seq = False
                while correct_seq == False:
                    ui("What is the sequence order? (type the numbers of the choreographies you want to add\n"
                    + SPC + "to the sequence, separated by a '>' sign)\n"
                    + SPC + "Example: 1>2>3>4\n"
                    + SPC + "Here are the choreographies available:")
                    modules.choreographer.displays_choreography_dict()
                    ui("once you are done, press enter")
                    sequence_order_str = input(">")
                    print("_________________________________________________________________________________________")
                    if sequence_order_str == "quit":
                        return
                    try: 
                        sequence_order = sequence_order_str.split(">")
                        sequence_order = [int(i) for i in sequence_order]
                        # check if the choreographies exist
                        for chor in sequence_order:
                            if chor not in range(1, len(modules.choreographer.choreography_dict) + 1):
                                raise ValueError
                        correct_seq = True
                    except ValueError:
                        warning("This sequence order is not valid\n")
                        pass
                modules.choreographer.create_sequence(name, description, sequence_order)
                info("Sequence created!")
                print("\n")
                ui("Press enter to get back to the editor")
                input(">")
                print("_________________________________________________________________________________________")
                time.sleep(1)
        elif self.e_asw == "delete seq":
            ui("Here are the sequences:")
            modules.choreographer.displays_sequence_dict()
            ui("What is the name/number of the sequence you want to delete?")
            name = input(">")
            print("_________________________________________________________________________________________")
            if name == "quit":
                self.e_asw = None
                return
            # check if name is a number
            if name.isdigit():
                name = self.nbr_to_sequence_name(modules, name)
            # check if the sequence exists
            if name not in modules.choreographer.sequence_dict:
                warning("This sequence does not exist")
                return
            else:
                modules.choreographer.delete_sequence(name)
                ui("Press enter to get back to editor mode")
                input(">")
                print("_________________________________________________________________________________________")
            self.e_asw = None
            return
        elif self.e_asw == "quit":
            self.wanted_mode = "No mode"
            self.e_asw = None
            ui("getting back to mode selection")
            return        
        else:
            ui("I don't understand")
            time.sleep(1) # USER EXPERIENCE
            return

    def info_script(self, modules):
        """Info about the choreographies and sequences"""
        ui("The choreographies and sequences available are the following:")
        print("\n")
        modules.choreographer.displays_choreography_dict()
        print("\n")
        time.sleep(1) # USER EXPERIENCE
        modules.choreographer.displays_sequence_dict()
        print("\n")
        time.sleep(1) # USER EXPERIENCE

        ui("Which do you want to know more about? example: 'c1' for choreography 1, 'sname_sequence1' for sequence 'name_sequence1'")
        entry = input(">")
        print("_________________________________________________________________________________________")

        answer = entry[0] 
        name = entry[1:] 

        if answer == "c":
            # check if the name is a number
            if name.isdigit():
                name = self.nbr_to_choreography_name(modules, name)
            
            # check if the choreography exists
            if name == None or name == "quit":
                pass
                
            elif name not in modules.choreographer.choreography_dict:
                warning("This choreography does not exist")
                return
            
            else:
                ui("Here is the choreography " + name)
                choreography_name, description, speed_factor, path = modules.choreographer.choreography_dict[name].get_info()
                ui(f"Name:           [white]{choreography_name}[/]")
                ui(f"Description:    [white]{description}[/]")
                ui(f"Speed factor:   [white]{str(speed_factor)}[/]")
                ui(f"Path:           [white]{path}[/]")
                ui("Press enter to get back to mode selection")
                input(">")
                print("_________________________________________________________________________________________")
            self.wanted_mode = "No mode"
            ui("getting back to mode selection")
            
        elif answer == "s":
            ui("If you want more information about a sequence, type the name/number of the sequence")
            name = input(">")
            print("_________________________________________________________________________________________")
            # check if the name is a number
            if name.isdigit():
                name = self.nbr_to_sequence_name(modules, name)

            # check if the sequence exists
            if name == None or name == "quit":
                pass
            elif name not in modules.choreographer.sequence_dict:
                warning("This sequence does not exist")
                return
            
            else:
                ui("Here is the sequence " + name)
                sequence_name, description, path, sequence_order = modules.choreographer.sequence_dict[name].get_info()
                print("\n")
                ui(f"Name:           [white]{sequence_name}[/]")
                ui(f"Description:    [white]{description}[/]")
                ui(f"Path:           [white]{path}[/]")
                ui(f"Sequence order: [white]{sequence_order}[/]")
                print("\n")
                ui("Press enter to get back to mode selection")
                input(">")
                print("_________________________________________________________________________________________")
            self.wanted_mode = "No mode"
            ui("getting back to mode selection")

        elif answer == "quit":
            self.wanted_mode = "No mode"
            ui("getting back to mode selection")
            
        else :
            ui("I don't understand")
        time.sleep(1)

    def nbr_to_choreography_name(self,modules, name):
        """Convert a number to a choreography name"""
        try:
            nbr = int(name)
            if nbr > len(modules.choreographer.choreography_dict):
                raise ValueError
            name = list(modules.choreographer.choreography_dict.keys())[nbr-1]
            return name
        except ValueError:
            warning("This choreography does not exist")
            return None
            
    def nbr_to_sequence_name(self,modules, name):
        """Convert a number to a sequence name"""
        try:
            nbr = int(name)
            if nbr > len(modules.choreographer.sequence_dict):
                raise ValueError
            name = list(modules.choreographer.sequence_dict.keys())[nbr-1]
            return name
        except ValueError:
            warning("This sequence does not exist")
            return None
