from math import pi

BLUE_ARMY = 0
RED_ARMY = 1

ADD_BLOCK_MODE = 0
DEPLOY_BLUE_ARMY_MODE = 1
DEPLOY_RED_ARMY_MODE = 2

ADD_BLOCK_OUTLINE = "green"
ADD_BLOCK_RECT_WIDTH = 80

DEPLOY_BLUE_ARMY_OUTLINE = "blue"
DEPLOY_RED_ARMY_OUTLINE = "red"
DEPLOY_ARMY_RECT_WIDTH = 60

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
PLACE_TEXT = "Press 'ESC' Button to Exit..."


MIN_BLOCK_WIDTH=40
MAX_BLOCK_WIDTH=100
MIN_NUM_SOLDIER = 1
MAX_NUM_SOLDIER = 100
MAX_TOTAL_NUM_SOLDIER = 200
MIN_DAMAGE = 1
MAX_DAMAGE = 100
MIN_ESCAPE_FIXED_RATE = 0
MAX_ESCAPE_FIXED_RATE = 100
MIN_ESCAPE_THRESHOLD = 0
MAX_ESCAPE_THRESHOLD = 100
INCORRECT_BLOCK_WIDTH_TEXT = "Block width must be an integer between 40 and 100. Please Re-Enter..."
INCORRECT_NUM_SOLDIER_TEXT = "Number of soldiers must be an integer between 1 and 200. Please Re-Enter..."
INCORRECT_DAMAGE_TEXT = "Damage must be an floating number between 1 and 100. Please Re-Enter..."
INCORRECT_ESCAPE_FIXED_RATE_TEXT = "Escape fixed rate must be an integer between 0 and 100. Please Re-Enter..."
INCORRECT_ESCAPE_THRESHOLD_TEXT = "Escape threhold must be an integer between 0 and 100. Please Re-Enter..."
OVER_MAX_NUM_SOLDIER_TEXT = "Total number of soldiers in an army cannot exceed 200. Please Re-Enter..."
NOT_ENOUGH_SOLDIER_TEXT = "Number of soldiers of both armies should be greater than 0 to start the simulation..."

SOLDIER_ITEM_TAG = "soldier"
BLOCK_ITEM_TAG = "block"

SECTION_TITLE_BG = 'lightgrey'

BATTLEFIELD_WIDTH = 600
SOLDIER_WIDTH=6


MENU_WIDTH = 35
MESSAGE_WRAP_LENGTH = 310
MESSAGE_FONT_SIZE = 16
WARNING_BG_COLOR = 'red'
MESSAGE_BG_COLOR = 'green'

INFO_MESSAGE_TYPE = 0
WARNING_MESSAGE_TYPE = 1

MAX_HEALTH_POINT = 100
MAX_NUM_ROUND = 1000
SOLDIER_MOVE_SPEED = 5

ROTATE_RADIAN = pi/8

MAX_NUM_THREADS = 8

SABER_ATTACK_RANGE = 8

DECTION_RANGE = 300