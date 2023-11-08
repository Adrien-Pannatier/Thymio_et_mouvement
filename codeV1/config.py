# == General == #
DEBUG = False
LOG_LEVEL = 6
RAISE_DEPRECATION_WARNINGS = False
POOL_SIZE = 4
SLEEP_DURATION = 0.5

# tdmclient
PROCESS_MSG_INTERVAL = 0.1  # time interval between checks if incoming messages

PHYSICAL_SIZE_CM = 110  # physical size of the scene board in cm
THYMIO_TO_CM = 4 / 100  # factor to put the thymio speed in centimetres per seconds
DIAMETER = 9.5  # wheel to wheel distance

# == Big Brain == #
UPDATE_FREQUENCY = 0.2  # frequency of big brain internal loop refresh

# == Second Thymio == #
DROP_SPEED = 50  # speed of the motors to drop the bauble
DROP_TIME = 1.5  # drop duration in seconds
HALF_TURN_SPEED = 50  # speed of the half turn
HALF_TURN_TIME = 8  # time for the thymio to do a 180° turn

# == Motion Control == #
MAX_WAIT = 0.1
INDEX_FW = 1 # follow next waypoint by index

# == Choreography manager == #
DEFAULT_SPEED_FACT = 1

# == Process controller data == #
PIXELS_TO_METERS = 0.01  # replace with actual value
GYRO_SCALING = 1  # replace with actual value
AS_THRESH = 0.05  # replace with actual value