import json

# Load the JSON data from the file
with open("app\\tests\\choreography.json", "r") as json_file:
    choreography_data = json.load(json_file)

# Extract the matrix of "time," "forward_speed," and "angular_speed"
matrix = []

for step in choreography_data:
    time = step["time"]
    forward_speed = step["forward_speed"]
    angular_speed = step["angular_speed"]
    matrix.append([time, forward_speed, angular_speed])

# Print the matrix
for row in matrix:
    print(row)
