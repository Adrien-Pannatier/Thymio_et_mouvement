from tdmclient import aw
import threading

class Emotion:
    def __init__(self, name, color, sensors, reactions, node):
        self.name = name
        self.color = color
        self.sensors = sensors
        self.reactions = reactions
        self.node = node

        self.emotion_status = False
        self.sensors_values = None

        self.start_emotion_thread()

    def start_emotion_thread(self):
        self.emotion_thread = threading.Thread(target=self.emotion_loop)
        self.emotion_thread.start()

    def emotion_loop(self):
        while True:
            # Wait for sensor information
            self.sensors_values = aw(self.node.wait_for_variables(self.sensors))
            # React to sensor information
            self.react()

    def react(self):
        pass

    def get_emotion_status(self):
        return self.emotion_status

class Fear(Emotion):
    def __init__(self, node, fear_level):
        super().__init__(node=node)
        self.name = "Fear"
        self.color = "blue"
        self.sensors = ["prox.horizontal"]
        self.reactions = ["motor.left.target", "motor.right.target"]
        self.fear_level = fear_level

    def react(self):
        # when sensors triggered -> flee from the source
        # sensors weights
        w_l = [40,  20, -20, -20, -40,  30, -10, 8, 0]
        w_r = [-40, -20, -20,  20,  40, -10, 30, 0, 8]
        
        # Scale factors for sensors and constant factor
        sensor_scale = 200
        
        if self.sensors_values != None:

            self.emotion_status = True

            # Compute scaled sensor values
            for i in range(len(self.sensors_values)):
                self.sensors_values[i] = self.sensors_values[i] // sensor_scale
            
            # Initialize motor powers
            motor_output_left = 0
            motor_output_right = 0    
            
            for i in range(len(self.sensors_values)):    
                # Compute outputs of neurons and set motor powers
                motor_output_left = motor_output_left + self.sensors_values[i] * w_l[i] * self.fear_level
                motor_output_right = motor_output_right + self.sensors_values[i] * w_r[i] * self.fear_level

            # Set motor powers
            aw(self.node.set_variables(  # apply the control on the wheels
                {"motor.left.target": [motor_output_left], "motor.right.target": [motor_output_right]}))

        else:
            self.emotion_status = False

class Curiosity(Emotion):
    def __init__(self, node, curiosity_level):
        super().__init__(node=node)
        self.name = "Curiosity"
        self.color = "yellow"
        self.sensors = ["prox.horizontal"]
        self.reactions = ["motor.left.target", "motor.right.target"]
        self.curiosity_level = curiosity_level

    def react(self):
        # when sensors triggered -> get closer to the source
        # sensors weights
        w_l = -[40,  20, -20, -20, -40,  30, -10, 8, 0]
        w_r = -[-40, -20, -20,  20,  40, -10, 30, 0, 8]

        
        # Scale factors for sensors and constant factor
        sensor_scale = 200
        
        if self.sensors_values != None:

            self.emotion_status = True

            # Compute scaled sensor values
            for i in range(len(self.sensors_values)):
                self.sensors_values[i] = self.sensors_values[i] // sensor_scale
            
            # Initialize motor powers
            motor_output_left = 0
            motor_output_right = 0    
            
            for i in range(len(self.sensors_values)):    
                # Compute outputs of neurons and set motor powers
                motor_output_left = motor_output_left + self.sensors_values[i] * w_l[i] * self.curiosity_level
                motor_output_right = motor_output_right + self.sensors_values[i] * w_r[i] * self.curiosity_level

            # Set motor powers
            aw(self.node.set_variables(  # apply the control on the wheels
                {"motor.left.target": [motor_output_left], "motor.right.target": [motor_output_right]}))

        else:
            self.emotion_status = False