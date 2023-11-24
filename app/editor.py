from app.config import T

class Editor():

    def __init__(self):
        pass

    def trim_choreography(self, choreography, trim_start, trim_end):
        """Trim the choreography"""
        "the trim instructions are in percentage of the choreography duration"
        step_list = choreography.step_list
        new_step_list = []
        for step in step_list:
            if step[T] >= trim_start and step[T] <= trim_end:
                new_step_list.append(step)
        choreography.step_list = new_step_list
        return choreography
    

        