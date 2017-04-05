"""
This library provides functions to do validation works
"""
from constants import *

def is_valid_block_width(var):
	if is_integer(var) and var >= MIN_BLOCK_WIDTH and var <= MAX_BLOCK_WIDTH:
		return True
	else:
		return False

def is_integer(var):
	return isinstance(var, int)

def is_floating(var):
	return isinstance(var, float)

def is_valid_num_soldier(var):
	if is_integer(var) and var >= MIN_NUM_SOLDIER and var <= MAX_NUM_SOLDIER:
		return True
	else:
		return False

def is_valid_total_num_soldier(var):
	if is_integer(var) and var <= MAX_TOTAL_NUM_SOLDIER:
		return True
	else:
		return False

def is_valid_damage(var):
	if is_floating(var) and var >= MIN_DAMAGE and var <= MAX_DAMAGE:
		return True
	else:
		return False

def is_valid_escape_fixed_rate(var):
	if is_integer(var) and var >= MIN_ESCAPE_FIXED_RATE and var <= MAX_ESCAPE_FIXED_RATE:
		return True
	else:
		return False

def is_valid_threshold(var):
	if is_integer(var) and var >= MIN_ESCAPE_THRESHOLD and var <= MAX_ESCAPE_THRESHOLD:
		return True
	else:
		return False

		