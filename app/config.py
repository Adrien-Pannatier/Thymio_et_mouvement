# == General == #
DEBUG = False
LOG_LEVEL = 7
RAISE_DEPRECATION_WARNINGS = False
SLEEP_DURATION = 0.5

# tdmclient
PROCESS_MSG_INTERVAL = 0.1  # time interval between checks if incoming messages
THYMIO_TO_CM = 4 / 100  # factor to put the thymio speed in centimetres per seconds
DIAMETER = 9.5  # wheel to wheel distance

# == Big Brain == #
UPDATE_FREQUENCY = 0.2  # frequency of big brain internal loop refresh

# == Motion Control == #
DEFAULT_PLAY_MODE = "once"
T = 0 # time index
DT = 1 # delta time index
LS = 2 # left wheel speed index
RS = 3 # right wheel speed index
MIN_SPEED_FACTOR = -20
MAX_SPEED_FACTOR = 20

# == Choreography manager == #
DEFAULT_SPEED_FACT = 1
DEFAULT_PATH = "choreographies/"

# == Process controller data == #
PIXELS_TO_METERS = 0.01  # replace with actual value
GYRO_SCALING = 1  # replace with actual value
AS_THRESH = 0.05  # replace with actual value