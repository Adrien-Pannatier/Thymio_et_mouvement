import json

# Define a fake process controller data
process_controller_data = {
    "data": [
        {"time": 0, "timestep": 0.1, "left_wheel_speed": 0, "right_wheel_speed": 0},
        {"time": 1, "timestep": 1, "left_wheel_speed": 5, "right_wheel_speed": 5},
        {"time": 2, "timestep": 1, "left_wheel_speed": 6, "right_wheel_speed": 6},
        {"time": 3, "timestep": 1, "left_wheel_speed": 7, "right_wheel_speed": 7},
        {"time": 4, "timestep": 1, "left_wheel_speed": 0, "right_wheel_speed": 0},
    ]
}

# Save the process controller data to a JSON file
with open('C:\\Users\\adrie\\Desktop\\PDS_Thymio\\001_code\\Python\\Thymio_et_mouvement\\choreographies\\test.json', 'w') as file:
    json.dump(process_controller_data, file, indent=4)