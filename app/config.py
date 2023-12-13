# == General == #
DEBUG = False
LOG_LEVEL = 7
RAISE_DEPRECATION_WARNINGS = False

# tdmclient
THYMIO_TO_CM = 4 / 100  # factor to put the thymio speed in centimetres per seconds
DIAMETER = 9.5  # wheel to wheel distance

# == Motion Control == #
DEFAULT_PLAY_MODE = "once"
T = 0 # time index
DT = 1 # delta time index
LS = 2 # left wheel speed index
RS = 3 # right wheel speed index

# == Choreography manager == #
DEFAULT_SPEED_FACT = 1
DEFAULT_PATH_CHOREO = "C:/Users/adrie/Desktop/PDS_Thymio/001_code/Python/Thymio_et_mouvement/app/choreographies/"
DEFAULT_PATH_SEQUENCE = "C:/Users/adrie/Desktop/PDS_Thymio/001_code/Python/Thymio_et_mouvement/app/sequences/"

# == Process controller data == #
GYRO_SCALING = 20 
AS_THRESH = 0.05  
TIMEOUT_CONNECTION = 50  # seconds
RECORDING_DURATION = 20  # seconds 
DATA_PROCESSING_DURATION = 7 # seconds

# == canvas config == #
LENGTH_IN_PIX = 358
OFFSET_STARTGRAPH = 75
WIDTH_BAR = 3
OFFSET_ENDGRAPH = LENGTH_IN_PIX + OFFSET_STARTGRAPH
LEFTBAR_X0 = OFFSET_STARTGRAPH
LEFTBAR_Y0 = 0
LEFTBAR_X1 = LEFTBAR_X0 + WIDTH_BAR
LEFTBAR_Y1 = 1000
RIGHTBAR_X0 = OFFSET_ENDGRAPH - WIDTH_BAR
RIGHTBAR_Y0 = 0
RIGHTBAR_X1 = OFFSET_ENDGRAPH
RIGHTBAR_Y1 = 1000
BARSTART_COLOR = "#5e9949"
BAREND_COLOR = "#e74748"

# == settings == #
SETTINGS_DIR = "C:/Users/adrie/Desktop/PDS_Thymio/001_code/Python/Thymio_et_mouvement/app/settings"
SETTINGS_PATH = "C:/Users/adrie/Desktop/PDS_Thymio/001_code/Python/Thymio_et_mouvement/app/settings/settings.json"