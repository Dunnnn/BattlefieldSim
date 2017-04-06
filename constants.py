from math import pi

BLUE_ARMY = 0
RED_ARMY = 1

ADD_BLOCK_MODE = 0
DEPLOY_BLUE_ARMY_MODE = 1
DEPLOY_RED_ARMY_MODE = 2

ADD_BLOCK_OUTLINE = "green"

DEPLOY_BLUE_ARMY_OUTLINE = "blue"
DEPLOY_RED_ARMY_OUTLINE = "red"

# In num of cells
DEPLOY_ARMY_RECT_WIDTH = 5

BLUE_ARMY_ITEM_COLOR = "blue"
RED_ARMY_ITEM_COLOR = "red"

MACHINE_GUN_OPTION = 0
SWORD_OPTION = 1
SNIPER_GUN_OPTION = 2

WEAKEST_TARGET_OPTION = 0
VULNERABLE_TARGET_OPTION = 1
RANDOM_TARGET_OPTION = 2

FIXED_RATE_OPTION = 0
THRESHOLD_OPTION = 1
LINEAR_OPTION = 2

WELCOME_TEXT = "Welcome to Sim Battlefield!"
SIMULATION_END_TEXT = "Clear result to start another battle..."
PLACE_TEXT = "Press 'ESC' Button to Exit..."


# In num of cells
MIN_BLOCK_WIDTH = 3
# In num of cells
MAX_BLOCK_WIDTH = 11
MIN_NUM_SOLDIER = 1
MAX_NUM_SOLDIER = 25
MAX_TOTAL_NUM_SOLDIER = 100
MIN_DAMAGE = 1
MAX_DAMAGE = 100
MIN_ESCAPE_FIXED_RATE = 0
MAX_ESCAPE_FIXED_RATE = 100
MIN_ESCAPE_THRESHOLD = 0
MAX_ESCAPE_THRESHOLD = 100
INCORRECT_BLOCK_WIDTH_TEXT = "Block width must be an odd integer between 3 and 11. Please Re-Enter..."
INCORRECT_NUM_SOLDIER_TEXT = "Number of soldiers must be an integer between 1 and 25. Please Re-Enter..."
INCORRECT_DAMAGE_TEXT = "Damage must be an floating number between 1 and 100. Please Re-Enter..."
INCORRECT_ESCAPE_FIXED_RATE_TEXT = "Escape fixed rate must be an integer between 0 and 100. Please Re-Enter..."
INCORRECT_ESCAPE_THRESHOLD_TEXT = "Escape threhold must be an integer between 0 and 100. Please Re-Enter..."
OVER_MAX_NUM_SOLDIER_TEXT = "Total number of soldiers in an army cannot exceed 200. Please Re-Enter..."
NOT_ENOUGH_SOLDIER_TEXT = "Number of soldiers of both armies should be greater than 0 to start the simulation..."

SOLDIER_ITEM_TAG = "soldier"
BLOCK_ITEM_TAG = "block"

SECTION_TITLE_BG = 'lightgrey'

# In pixels
BATTLEFIELD_WIDTH = 600
# In pixels
SOLDIER_WIDTH = 20
CELL_WIDTH = SOLDIER_WIDTH

# In num of cells
BATTLEFIELD_MAP_WIDTH = BATTLEFIELD_WIDTH / CELL_WIDTH

# In pixels
MENU_WIDTH = 35
# In pixels
MESSAGE_WRAP_LENGTH = 310
# In pixels
MESSAGE_FONT_SIZE = 16
WARNING_BG_COLOR = 'red'
MESSAGE_BG_COLOR = 'green'

INFO_MESSAGE_TYPE = 0
WARNING_MESSAGE_TYPE = 1

MAX_HEALTH_POINT = 100
MAX_NUM_ROUND = 1000

ROTATE_RADIAN = pi/8

MAX_NUM_THREADS = 64

SABER_ATTACK_RANGE = 1

DEBUG_MODE = False

HELP_FILE = "help.txt"