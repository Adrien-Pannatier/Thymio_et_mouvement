# to add: sequence manager

import os
import json
import numpy as np

from app.utils.console import *
from app.config import DEFAULT_SPEED_FACT, SLEEP_DURATION, DEFAULT_PATH

class ChoreographyManager:
    def __init__(self):
        self.choreography_dict = {}
        self.load_choreography_dict()

    def create_choreography(self, name, data_array, description="", path=DEFAULT_PATH, speed_fact=DEFAULT_SPEED_FACT):
        """
        Creates a choreography
        """
        choreography = Choreography(name, data_array, description, path, speed_fact)
        self.choreography_dict[name] = choreography
        self.save_choreography_dict(name)

    def load_choreography_dict(self, path=DEFAULT_PATH):
        """
        Loads the choreography dictionary
        """
        for file in os.listdir(path):
            if file.endswith(".json"):
                name, _ = os.path.splitext(file)
                # print(name)
                # step_list = []
                with open(path + file, "r") as file:
                    data = json.load(file)
                #     for step in data:
                #         step_list.append(step)
                step_list = np.array([[item['time'], item['timestep'], item['left_wheel_speed'], item['right_wheel_speed']] for item in data['data']])
                # print(step_list)
                if name not in self.choreography_dict:
                    self.choreography_dict[name] = Choreography(name, step_list, path=path)
    
    def save_choreography_dict(self, path=DEFAULT_PATH):
        """
        Saves the choreography dictionary
        """
        for choreography in self.choreography_dict.values():
            with open(path + choreography.name + ".json", "w") as file:
                if not os.path.isfile(path + choreography.name + ".json"):
                    json.dump(choreography.data, file, indent=4)

    def delete_choreography(self, name):
        """
        Deletes a choreography
        """
        ui(f"[bold red]Are you sure you want to delete the choreography [/][white]{name}[/][bold red]? [Y/n][/]")
        answer = input(">")
        if answer == "n":
            return
        ui(f"[bold orange]Deleting choreography [/][white]{name}[/][bold orange]...[/]")
        os.remove(self.choreography_dict[name].path)
        del self.choreography_dict[name]
        ui(f"[bold green]Choreography [/][white]{name}[/][bold green] deleted![/]")

    def displays_choreography_dict(self):
        """
        Displays the choreography dictionary names
        """
        verbose(f"[bold green]Choreographies:[/]")
        i = 1
        for choreography in self.choreography_dict:
            console.print(f"           {i} - {choreography}")
            i = i + 1

        # print(self.choreography_dict)

class Choreography:
    """
    Class containing the choreography

    @variables:
    Var name: name of the choreography
    Var description: description of the choreography
    Var step_list: array of the choreography data
    Var path: path of the choreography file
    Var speed_fact: speed factor of the choreography
    Var data: data of the choreography
    Var complete: boolean indicating if the choreography is complete

    @functions:
    Func __init__: initiates the class
    Func __str__: returns the name of the choreography
    Func get_info: returns the info of the choreography
    """
    def __init__(self, name, step_list, description="", path=DEFAULT_PATH, speed_fact=DEFAULT_SPEED_FACT):
        self.name = name
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
        return self.name, self.description, self.speed_fact, self.path
    
class Sequence:
    def __init__(self, name, choregraphy_list):
        self.name = name
        self.choregraphy_list = choregraphy_list

    def __str__(self):
        return self.name
    
    def get_info(self):
        """
        Returns the info of the sequence
        """
        return self.name, self.choregraphy_list