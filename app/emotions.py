from tdmclient import aw
import threading
import time

class Emotion:
    def __init__(self, name, color, sensors, reactions, node, client):
        self.name = name
        self.color = color
        self.sensors = sensors
        self.reactions = reactions
        self.node = node
        self.client = client

        self.emotion_status = False
        self.sensors_values = None

        self.emotion_on = False

        self.start_emotion_thread()

    def start_emotion_thread(self):
        self.emotion_thread = threading.Thread(target=self.emotion_loop)
        self.emotion_thread.start()

    def emotion_loop(self):
        while True:
            if self.emotion_on:
                # Wait for sensor information
                aw(self.node.wait_for_variables({self.sensors}))
                aw(self.client.sleep(0.01))
                self.sensors_values = list(self.node['prox.horizontal'])
                # React to sensor information
                self.react()
            time.sleep(0.1)

    def react(self):
        # print("Reacting to sensor information")
        pass

    def start_emotion(self):
        self.emotion_on = True

    def stop_emotion(self):
        self.emotion_on = False

    def get_emotion_status(self):
        return self.emotion_status
    
    def get_emotion_sensors(self):
        return self.sensors_values

class Fear(Emotion):
    def __init__(self, node, client, fear_level):
        super().__init__(name="Fear", color="blue", sensors="prox.horizontal", reactions=["motor.left.target", "motor.right.target"], node=node, client=client)
        self.fear_level = fear_level

    def react(self):
        # print(f"getting info from {self.sensors}")
        # print(self.sensors_values)
        # when sensors triggered -> flee from the source
        # sensors weights
        w_l = [40,  20, -20, -20, -40,  30, -10, 8, 0]
        w_r = [-40, -20, -20,  20,  40, -10, 30, 0, 8]
        
        # Scale factors for sensors and constant factor
        sensor_scale = 200
        
        if self.sensors_values != [0, 0, 0, 0, 0, 0, 0]:

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
    def __init__(self, node, client, curiosity_level):
        super().__init__(name="Curiosity", color="yellow", sensors="prox.horizontal", reactions=["motor.left.target", "motor.right.target"], node=node, client=client)
        self.curiosity_level = curiosity_level

    def react(self):
        # when sensors triggered -> get closer to the source
        # sensors weights
        w_l = [-40,  -20, 20, 20, 40,  -30, 10, -8, 0]
        w_r = [40, 20, 20,  -20,  -40, 10, -30, 0, -8]

        
        # Scale factors for sensors and constant factor
        sensor_scale = 200
        
        if self.sensors_values != [0, 0, 0, 0, 0, 0, 0]:

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