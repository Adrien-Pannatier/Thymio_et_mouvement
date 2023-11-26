# to add: sequence manager

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


from app.utils.console import *
from app.config import DEFAULT_SPEED_FACT, SLEEP_DURATION, DEFAULT_PATH_CHOREO, DEFAULT_PATH_SEQUENCE

class ChoreographyManager:
    def __init__(self):
        self.choreography_dict = {}
        self.sequence_dict = {}
        self.check_repo()
        self.load_choreography_dict()
        self.load_sequence_dict()
        self.sort_choreography_dict()
        self.sort_sequence_dict()

    def check_repo(self):
        # checks if the choreography and sequence folders exist
        if not os.path.isdir(DEFAULT_PATH_CHOREO):
            os.mkdir(DEFAULT_PATH_CHOREO)
            info("Choreography folder created")
        if not os.path.isdir(DEFAULT_PATH_SEQUENCE):
            os.mkdir(DEFAULT_PATH_SEQUENCE)
            info("Sequence folder created")

    def update_database(self):
        """
        Updates the database
        """
        self.load_choreography_dict()
        self.load_sequence_dict()
        self.sort_choreography_dict()
        self.sort_sequence_dict()
        info("Database updated")

    # CHOREOGRAPHY FUNCTIONS
    def create_choreography(self, name, data_array, description="", path=DEFAULT_PATH_CHOREO, speed_fact=DEFAULT_SPEED_FACT):
        """
        Creates a choreography
        """
        choreography = Choreography(name, data_array, description, path, speed_fact)
        self.choreography_dict[name] = choreography
        self.save_choreography_dict()

    def load_choreography_dict(self, path=DEFAULT_PATH_CHOREO):
        """
        Loads the choreography dictionary
        """
        for file in os.listdir(path):
            if file.endswith(".json"):
                name, _ = os.path.splitext(file)
                # print(name)
                # step_list = []
                try: 
                    with open(path + file, "r") as file:
                        data = json.load(file)
                    creation_date = data['creation_date']
                    last_modified = data['last_modified']
                    description = data['description']
                    step_list = np.array([[item['time'], item['timestep'], item['left_wheel_speed'], item['right_wheel_speed']] for item in data['choreography']])
                except KeyError:
                    error(f"choreography [bold white]{name}[/] is corrupted")
                    return

                # print(step_list)
                if name not in self.choreography_dict:
                    self.choreography_dict[name] = Choreography(name, creation_date, last_modified, step_list, description, path=path)
    
    def save_choreography_dict(self, path=DEFAULT_PATH_CHOREO):
        """
        Saves the choreography dictionary
        """
        for choreography in self.choreography_dict.values():
            data_to_save = {}
            data_to_save['name'] = choreography.name
            data_to_save['creation_date'] = choreography.creation_date
            data_to_save['last_modified'] = choreography.last_modified
            data_to_save['description'] = choreography.description
            data_to_save['choreography'] = [{'time': item[0], 'timestep': item[1], 'left_wheel_speed': item[2], 'right_wheel_speed': item[3]} for item in choreography.step_list]

            with open(path + choreography.name + ".json", "w") as file:
                # if not os.path.isfile(path + choreography.name + ".json"):
                print("saving")
                json.dump(data_to_save, file, indent=4)

    def save_choreography(self, name, path=DEFAULT_PATH_CHOREO):
        """
        Saves the choreography
        """
        choreography = self.choreography_dict[name]
        data_to_save = {}
        data_to_save['name'] = choreography.name
        data_to_save['creation_date'] = choreography.creation_date
        data_to_save['last_modified'] = (str(datetime.now()))[:-7]
        data_to_save['description'] = choreography.description
        data_to_save['choreography'] = [{'time': item[0], 'timestep': item[1], 'left_wheel_speed': item[2], 'right_wheel_speed': item[3]} for item in choreography.step_list]

        with open(path + choreography.name + ".json", "w") as file:
            # if not os.path.isfile(path + choreography.name + ".json"):
            print("saving")
            json.dump(data_to_save, file, indent=4)

    def delete_choreography(self, name):
        """
        Deletes a choreography
        """
        os.remove(self.choreography_dict[name].path)
        del self.choreography_dict[name]

    def displays_choreography_dict(self):
        """
        Displays the choreography dictionary names
        """
        verbose(f"[bold green]Choreographies:[/]")
        i = 1
        for choreography in self.choreography_dict:
            console.print(f"           {i} - {choreography}")
            i = i + 1

        # check if the choreography dictionary is empty
        if len(self.choreography_dict) == 0:
            console.print(f"           [bold white]No choreography saved[/]")

        # print(self.choreography_dict)

    def sort_choreography_dict(self):
        # sorts the choreography dictionary by creation date
        self.choreography_dict = {k: v for k, v in sorted(self.choreography_dict.items(), key=lambda item: item[1].creation_date)}
    
    # SEQUENCE FUNCTIONS
    def create_sequence(self, name, creation_date, description, sequence_l=[], path=DEFAULT_PATH_SEQUENCE):
        """
        Creates a sequence
        """
        sequence = Sequence(name, creation_date, description, sequence_l, path)
        self.sequence_dict[name] = sequence
        self.save_sequence_dict()

    def load_sequence_dict(self, path=DEFAULT_PATH_SEQUENCE):
        """
        Loads the sequence dictionary
        """
        for file in os.listdir(path):
            if file.endswith(".json"):
                name, _ = os.path.splitext(file)
            try:
                with open(path + file, "r") as file:
                    data = json.load(file)
                creation_date = data['creation_date']
                description = data['description']
                sequence_l = data['sequence_order']

                if name not in self.sequence_dict:
                    self.sequence_dict[name] = Sequence(name, creation_date=creation_date, description=description, sequence_l=sequence_l, path=path)
            except KeyError:
                error(f"sequence [bold white]{name}[/] is corrupted")
                pass
    
    def save_sequence_dict(self, path=DEFAULT_PATH_SEQUENCE):
        """
        Saves the sequence dictionary
        """
        for sequence in self.sequence_dict.values():
            data_to_save = {}
            data_to_save['name'] = sequence.name
            data_to_save['creation_date'] = sequence.creation_date
            data_to_save['description'] = sequence.description
            data_to_save['sequence_order'] = sequence.sequence_l
            if not os.path.isfile(path + sequence.name + ".json"):
                with open(path + sequence.name + ".json", "w") as file:
                    print("saving")
                    json.dump(data_to_save, file, indent=4)
    
    def delete_sequence(self, name):
        """
        Deletes a sequence
        """
        os.remove(self.sequence_dict[name].path)
        del self.sequence_dict[name]

    def displays_sequence_dict(self):
        """
        Displays the sequence dictionary names
        """
        verbose(f"[bold green]Sequences:[/]")
        if len(self.sequence_dict) == 0:
            console.print(f"           [bold white]No sequence saved[/]")
            return
        i = 1
        for sequence in self.sequence_dict:
            console.print(f"           {i} - {sequence}")
            i = i + 1

        # print(self.sequence_dict)

    def sort_sequence_dict(self):
        # sorts the sequence dictionary by creation date
        self.sequence_dict = {k: v for k, v in sorted(self.sequence_dict.items(), key=lambda item: item[1].creation_date)}

# CLASSES

class Choreography:
    """
    Class containing the choreography

    @variables:
    Var name: name of the choreography
    Var creation_date: date of creation of the choreography
    Var last_modified: date of last modification of the choreography
    Var description: description of the choreography
    Var step_list: array of the choreography data
    Var path: path of the choreography file
    Var speed_fact: speed factor of the choreography

    @functions:
    Func __init__: initiates the class
    Func __str__: returns the name of the choreography
    Func get_info: returns the info of the choreography
    Func graph_speeds: graphs the speeds of the choreography
    """
    def __init__(self, name, creation_date, last_modified, step_list, description="", path=DEFAULT_PATH_CHOREO, speed_fact=DEFAULT_SPEED_FACT):
        self.name = name
        self.creation_date = creation_date
        self.last_modified = last_modified
        self.step_list = step_list
        self.description = description
        self.path = path + name + ".json"
        self.speed_fact = speed_fact

    def __str__(self):
        return self.name
    
    def get_info(self):
        """
        Returns the info of the choreography
        """
        return self.name, self.creation_date, self.last_modified, self.description, self.speed_fact, self.path
    
    def get_last_time(self):
        """
        Returns the last time of the choreography
        """
        return self.step_list[-1,0]
    
    def graph_speeds(self):
        """
        Graphs the speeds of the choreography
        """
        ax = plt.gca()
        plt.plot(self.step_list[:,0], self.step_list[:,2], label="left wheel speed")
        plt.plot(self.step_list[:,0], self.step_list[:,3], label="right wheel speed")
        # plt.xlabel("time (s)")
        # plt.ylabel("speed (m/s)")
        # plt.legend()
        ax.set(ylabel=None)
        ax.set(yticklabels=[])
        ax.set(yticks=[])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_facecolor("#dbdbdb")
        plt.gcf().set_size_inches(10, 5)
        # plt.show()
        plt.savefig(f"app/GUI_assets/temp_fig/{self.name}_light_graph.png")
        # change background color
        ax.set_facecolor('#2b2b2b')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.set(ylabel=None)
        # plt.xlabel("time (s)", color='white')
        # plt.ylabel("speed (m/s)", color='white')
        plt.savefig(f"app/GUI_assets/temp_fig/{self.name}_dark_graph.png", transparent=True)   
        plt.clf()
        plt.close()

    def trim(self, start_time, end_time):
        """
        Trims the choreography
        """
        start_index = np.where(self.step_list[:,0] == start_time)[0][0]
        end_index = np.where(self.step_list[:,0] == end_time)[0][0]
        self.step_list = self.step_list[start_index:end_index+1,:]
        # shift the axis
        self.step_list[:,0] = self.step_list[:,0] - start_time
    
class Sequence:
    """
    Class containing the sequence

    @variables:
    Var name: name of the sequence
    Var creation_date: date of creation of the sequence
    Var description: description of the sequence
    Var sequence_l: list of the choreography names
    Var path: path of the sequence file

    @functions:
    Func __init__: initiates the class
    Func __str__: returns the name of the sequence
    Func get_info: returns the info of the sequence
    Func empty: empties the sequence
    """
    def __init__(self, name, creation_date, description="", sequence_l=[], path=DEFAULT_PATH_SEQUENCE):
        self.name = name
        self.creation_date = creation_date
        self.sequence_l = sequence_l
        self.description = description
        self.path = path + name + ".json"

    def __str__(self):
        return self.name
    
    def get_info(self):
        """
        Returns the info of the sequence
        """
        return self.name, self.creation_date, self.description, self.path, self.sequence_l
    
    def empty(self):
        """
        Empties the sequence
        """
        self.sequence_l = []
