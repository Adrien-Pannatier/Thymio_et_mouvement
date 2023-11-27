import json
import random
import os
from datetime import datetime 

# Define constraints
min_speed = 0
max_speed = 10 
max_time = 15000 # in ms
path = "app/choreographies/"
timestep = 100 # in ms
samestart = True

# check which is the highest choreography number
n = 1
while os.path.exists(path + f"random_chor_smoother_{n}.json"):
    n += 1

creation_date = str(datetime.now())

#get rid of ms
creation_date = creation_date[:-7]

last_modified = creation_date

description = f"random choreography smoother {n}"

# Create list of time steps
time_steps = []
previous_speed_left = random.randint(min_speed, max_speed)
if samestart:
    previous_speed_right = previous_speed_left
else:
    previous_speed_right = random.randint(min_speed, max_speed) 
for time in range(0, max_time, 100):
    if random.random() < 0.25:  # 25% chance of speed changes
        speed_change_left = random.randint(-1, 1)
        new_speed_left = max(min(previous_speed_left + speed_change_left, max_speed), min_speed)
        speed_change_right = random.randint(-1, 1)
        new_speed_right = max(min(previous_speed_right + speed_change_right, max_speed), min_speed)
    else:
        new_speed_left = previous_speed_left
        new_speed_right = previous_speed_right

    time_step = {
        "time": time,
        "timestep": timestep,
        "left_wheel_speed": new_speed_left,
        "right_wheel_speed": new_speed_right
    }
    time_steps.append(time_step)
    previous_speed_left = new_speed_left
    previous_speed_right = new_speed_right

# Create choreography dictionary
choreography = {
    "name": f"random_chor{n}",
    "creation_date": creation_date,
    "last_modified": last_modified,
    "description": description,
    "choreography": time_steps
}

# Write to JSON file
with open(path + f"random_chor_smoother_{n}.json", 'w') as f:
    json.dump(choreography, f)