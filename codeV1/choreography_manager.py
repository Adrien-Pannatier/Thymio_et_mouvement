import os
import json
from asyncio import sleep

from app.utils.console import *
from app.config import DEFAULT_SPEED_FACT, SLEEP_DURATION
from app.context import Context

class ChoreographyManager:
    def __init__(self, ctx: Context):
        super().__init__(ctx)
        self.choreography_dict = {}

    async def run(self):
        while True:
            await sleep(SLEEP_DURATION)

    def process_event(self, name, step):
        """
        when info is sent from the big brain, add it to the choreography
        """
        if name not in self.choreography_dict:
            self.create_choreography(name)
        self.add_step_to_choreography(name, step)

    def create_choreography(self, name, path=None, speed_fact=DEFAULT_SPEED_FACT):
        """
        Creates a choreography
        """
        choreography = Choreography(name, path, speed_fact)
        self.choreography_dict[name] = choreography

    def add_step_to_choreography(self, name, step):
        """
        Adds a step to the choreography
        """
        self.choreography_dict[name].data.append(step)

    def save_choreography(self, name):
        """
        Saves a choreography
        """
        # check if the choreography is complete
        if not self.choreography_dict[name].complete:
            console.print(f"[bold red]Error:[/] The choreography {name} is not complete. do you want to save it anyway? [Y/n]")
            answer = input()
            if answer == "n":
                return

        console.print(f"[bold green]Saving choreography {name}...[/]")
        with open(self.choreography_dict[name].path, "w") as file:
            json.dump(self.choreography_dict[name].data, file, indent=4)
            console.print(f"[bold green]Choreography {name} saved![/]")

    def delete_choreography(self, name):
        """
        Deletes a choreography
        """
        console.print(f"[bold red]Are you sure you want to delete the choreography {name}? [Y/n]")
        answer = input()
        if answer == "n":
            return
        console.print(f"[bold red]Deleting choreography {name}...[/]")
        os.remove(self.choreography_dict[name].path)
        console.print(f"[bold red]Choreography {name} deleted![/]")

    def displays_choreography_dict(self):
        """
        Displays the choreography dictionary
        """
        print(self.choreography_dict)

class Choreography:
    """
    Class containing the choreography

    @variables:
    Var name: name of the choreography
    Var path: path of the choreography file
    Var speed_fact: speed factor of the choreography
    Var data: data of the choreography
    Var complete: boolean indicating if the choreography is complete

    @functions:
    Func __init__: initiates the class
    Func __str__: returns the name of the choreography
    Func read_choreography: reads the choreography file and returns the list of waypoints
    Func apply_speed_fact: applies the speed factor to the choreography
    """
    def __init__(self, name, path=None, speed_fact=DEFAULT_SPEED_FACT):

        self.name = name
        self.speed_fact = speed_fact
        self.data = None
        self.complete = False
        
        if path is None:
            self.path = "app/choreographies/" + name + ".json"

        self.read_choreography()
        self.apply_speed_fact()

    def __str__(self):
        return self.name
    
    def read_choreography(self):
        """
        Reads the choreography file and returns the list of waypoints
        """
        with open(self.path, "r") as file:
            self.data = json.load(file)
    
    def apply_speed_fact(self):
        """
        Applies the speed factor to the choreography
        """
        for step in self.data:
            step["forward_speed"] *= self.speed_fact
            step["angular_speed"] *= self.speed_fact