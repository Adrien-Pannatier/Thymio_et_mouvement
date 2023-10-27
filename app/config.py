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
KP_speed = 1
KI_speed = 0.1
KD_speed = 0.1
KP_orientation = 1
KI_orientation = 0.1
KD_orientation = 0.1

# == Choreography manager == #
DEFAULT_SPEED_FACT = 1