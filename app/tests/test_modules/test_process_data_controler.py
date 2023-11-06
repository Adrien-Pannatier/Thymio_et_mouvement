import sys
sys.path.insert(0, "C:\\Users\\adrie\\Desktop\\PDS_Thymio\\001_code\\Python\\Thymio_et_mouvement")
from app.context import Context
from app.process_controler_data import ProcessControllerData

# Create an instance of the ProcessControllerData class
process_controller_data = ProcessControllerData()

# Create a loop that generates multiple sets of mock data
for i in range(10):
    # Create a variables dictionary with mock data
    variables = {
        'current_pos': [100 + i, 200 + i],  # in pixels
        'current_gyro_z': 0.05 + i,  # in rad/s
        'timestep': 0.1,  # in seconds
        'last_pos': [80 + i, 180 + i],  # in pixels
        'time': 0.1 * i  # in seconds
    }

    # Test the process_event method
    process_controller_data.process_event(variables)

    # Print the data array
    print(process_controller_data.data_array)

print("Test finished!")
print(process_controller_data.display_data_array())