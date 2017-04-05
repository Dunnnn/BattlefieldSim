import copy
import numpy as np
import functools
import random
import threading
from math import sin, cos, atan2, sqrt, pi

from util_lib import *
from constants import * 

class Singleton(type):
	"""
	This class is for keeping only one instance for the same mode.
	Two modes are the same if the mode type and values are the same.
	"""
	_instances = []
	def __call__(cls, *args, **kwargs):
		new_instance = super(Singleton, cls).__call__(*args, **kwargs)
		index = None

		try:
			index =  cls._instances.index(new_instance)
			return cls._instances[index]
		except ValueError:
			cls._instances.append(new_instance)
			return new_instance

class Battle():
	def __init__(self, army_a, army_b, battlefield_map):
		self.army_a = army_a
		self.army_b = army_b
		self.battlefield_map = battlefield_map
		self.max_round = MAX_NUM_ROUND

		self.start()

	def start(self):
		self.current_round = 0
		self.survivor_record = np.zeros((2, self.max_round+1))
		self.survivor_record[0, 0] = self.army_a.size()
		self.survivor_record[1, 1] = self.army_b.size()

	def move_round(self):
		self.army_a.move(self.army_b, self.battlefield_map)
		self.army_b.move(self.army_a, self.battlefield_map)

	def cast_move(self):
		self.army_a.cast_move()
		self.army_b.cast_move()

	def attack_round(self):
		self.army_a.attack(self.army_b)
		self.army_b.attack(self.army_a)

	def cast_damage_round(self):
		self.army_a.cast_damage()
		self.army_b.cast_damage()

	def remove_death(self):
		self.army_a.remove_death()
		self.army_b.remove_death()

	def record_round(self):
		self.survivor_record[0, self.current_round] = self.army_a.size()
		self.survivor_record[1, self.current_round] = self.army_b.size()

	def next_round(self):
		self.current_round += 1
		self.move_round()
		self.cast_move()
		self.attack_round()
		self.cast_damage_round()
		self.remove_death()
		self.record_round()

	def is_battle_over(self):
		if self.army_a.size() == 0 or self.army_b.size() == 0 or self.current_round >= self.max_round:
			return True
		else:
			return False

	def get_battle_record(self):
		return self.survivor_record[:, :self.current_round+1]

	def clear(self):
		self.army_a.clear()
		self.army_b.clear()

class Army(): 
    def __init__(self, army_item_color, army_id, rotate_radian=ROTATE_RADIAN):
    	self.soldier_list = []
    	self.soldier_factory = SoldierFactory()
    	self.army_item_color = army_item_color
    	self.army_id = army_id
    	self.rotate_radian = rotate_radian

    def add_soldiers(self, num_soldiers, center_x, center_y, damage, weapon_type, attack_target_mode, march_target_mode, escape_behavior_mode, escape_fixed_rate=None, escape_threshold=None):
    	relative_pos_indices = np.random.choice((int)(DEPLOY_ARMY_RECT_WIDTH / SOLDIER_WIDTH)**2, size=num_soldiers, replace=False)
    	x_pos = np.floor((relative_pos_indices/(DEPLOY_ARMY_RECT_WIDTH / SOLDIER_WIDTH))) * SOLDIER_WIDTH + SOLDIER_WIDTH / 2
    	y_pos = (relative_pos_indices%(DEPLOY_ARMY_RECT_WIDTH / SOLDIER_WIDTH)) * SOLDIER_WIDTH + SOLDIER_WIDTH / 2

    	start_x = center_x - DEPLOY_ARMY_RECT_WIDTH / 2
    	start_y = center_y - DEPLOY_ARMY_RECT_WIDTH / 2
    	
    	abs_x_coord_array = start_x + x_pos
    	abs_y_coord_array = start_y + y_pos


    	for i in range(len(abs_x_coord_array)):
    		soldier = self.soldier_factory.generate_soldier(x=abs_x_coord_array[i], y=abs_y_coord_array[i],\
    			damage=damage, weapon_type=weapon_type, attack_target_mode=attack_target_mode,\
    			march_target_mode=march_target_mode, escape_behavior_mode=escape_behavior_mode,\
    			escape_fixed_rate=escape_fixed_rate, escape_threshold=escape_threshold)
    		
    		self.soldier_list.append(soldier)

    def move(self, enemy_army, battlefield_map):
    	"""
    	This function only stores the deltax and deltay to move in the Soldier Object. Movement will be
		executed in cast_move()
    	"""
    	friend_center = self.center()
    	enemy_center = enemy_army.center()

    	sema = threading.BoundedSemaphore(MAX_NUM_THREADS)

    	threads = []
    	for soldier in self.soldier_list:
    		sema.acquire()
    		t=threading.Thread(target=soldier.move, args=(self, friend_center, enemy_army, enemy_center, battlefield_map, sema))
    		t.start()
    		threads.append(t)

    def cast_move(self):
    	for soldier in self.soldier_list:
    		soldier.x = soldier.x + soldier.to_move_x
    		soldier.y = soldier.y + soldier.to_move_y
    		soldier.to_move_x = 0
    		soldier.to_move_y = 0
    		
    def attack(self, enemy_army):
    	"""
    	This function only stores the total damage in the enemy Soldier Object. Attack will be
		executed in cast_move()
    	"""
    	for soldier in self.soldier_list:
    		soldier.attack(enemy_army)

    def cast_damage(self):
    	for soldier in self.soldier_list:
    		soldier.health_point = soldier.health_point - soldier.damage_to_bear
    		soldier.damage_to_bear = 0

    def remove_death(self):
    	for soldier in self.soldier_list:
    		if soldier.is_dead():
    			self.soldier_list.remove(soldier)

    def center(self):
    	total_x = 0
    	total_y = 0
    	for soldier in self.soldier_list:
    		total_x += soldier.x
    		total_y += soldier.y
    	return total_x/self.size(), total_y/self.size()

    def get_soldiers(self):
    	return self.soldier_list
    			
    def size(self):
    	return len(self.soldier_list)

    def clear(self):
    	self.soldier_list.clear()

class SoldierFactory():
	def generate_soldier(self, x, y, damage, weapon_type, attack_target_mode, march_target_mode, escape_behavior_mode, escape_fixed_rate=None, escape_threshold=None):
		if attack_target_mode == WEAKEST_TARGET_OPTION:
			attack_target_mode = WeakestTargetMode()
		elif attack_target_mode == VULNERABLE_TARGET_OPTION:
			attack_target_mode = VulnerableTargetMode()
		elif attack_target_mode == RANDOM_TARGET_OPTION:
			attack_target_mode = RandomTargetMode()

		if march_target_mode == WEAKEST_TARGET_OPTION:
			march_target_mode = WeakestTargetMode()
		elif march_target_mode == VULNERABLE_TARGET_OPTION:
			march_target_mode = VulnerableTargetMode()
		elif march_target_mode == RANDOM_TARGET_OPTION:
			march_target_mode = RandomTargetMode()

		if escape_behavior_mode == FIXED_RATE_OPTION:
			escape_behavior_mode = FixedRateEscapeMode(escape_fixed_rate)
		elif escape_behavior_mode == THRESHOLD_OPTION:
			escape_behavior_mode = ThresholdEscapeMode(escape_threshold)
		elif escape_behavior_mode == LINEAR_OPTION:
			escape_behavior_mode = LinearEscapeMode()

		if weapon_type == MACHINE_GUN_OPTION:
			return Ranger(x=x, y=y, damage=damage, attack_target_mode=attack_target_mode, march_target_mode=march_target_mode, escape_behavior_mode=escape_behavior_mode)
		elif weapon_type == SWORD_OPTION:
			return Saber(x=x, y=y, damage=damage, attack_target_mode=attack_target_mode, march_target_mode=march_target_mode, escape_behavior_mode=escape_behavior_mode)
		elif weapon_type == SNIPER_GUN_OPTION:
			return Sniper(x=x, y=y, damage=damage, attack_target_mode=attack_target_mode, march_target_mode=march_target_mode, escape_behavior_mode=escape_behavior_mode)

class Soldier():
	def __init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode):
		self.x = x
		self.y = y
		self.damage = damage
		self.attack_target_mode = attack_target_mode
		self.march_target_mode = march_target_mode
		self.escape_behavior_mode = escape_behavior_mode
		self.health_point = MAX_HEALTH_POINT
		self.damage_to_bear = 0
		self.to_move_x = 0
		self.to_move_y = 0

	def attack(self, enemy_army):
		enemy = self.attack_target_mode.choose_target(self, enemy_army)
		hit_rate = self.hit_rate(enemy)
		if np.random.random_sample() <= hit_rate:
			enemy.damage_to_bear += self.damage

	def move(self, friend_army, friend_center, enemy_army, enemy_center, battlefield_map, sema):
		escape = self.escape_behavior_mode.if_escape(self)

		if escape:
			self.escape(friend_army, friend_center, enemy_army, enemy_center, battlefield_map)
		else:
			self.march(friend_army, enemy_army, battlefield_map)

		sema.release()

	def march(self, friend_army, enemy_army, battlefield_map):
		pass

	def escape(self, friend_army, friend_center, enemy_army, enemy_center, battlefield_map):
		target_x, target_y = 2 * np.array(list(friend_center)) - np.array(list(enemy_center))
		self.to_move_x, self.to_move_y = self.caculate_movement(self.x, self.y, target_x, target_y, friend_army, enemy_army, battlefield_map)

	def caculate_movement(self, start_x, start_y, target_x, target_y, friend_army, enemy_army, battlefield_map):
		start_point = Point(start_x, start_y)
		target_point = Point(target_x, target_y)
		connection_line_segment = LineSegment(start_point, target_point)

		if connection_line_segment.get_mod() <= SOLDIER_MOVE_SPEED:
			dir_x, dir_y = np.array(list(connection_line_segment.get_direction())) * SOLDIER_MOVE_SPEED
			connection_line_segment = LineSegment(start_point, Point(start_x + dir_x, start_y + dir_y))

		block_list = battlefield_map.get_block_list()

		rotated = 0

		# If the movement goes cross any block, then rotate
		while (connection_line_segment.if_cross_any_block(block_list)) and rotated < 2 * pi:
			connection_line_segment = connection_line_segment.rotate_clockwise(friend_army.rotate_radian)
			rotated += ROTATE_RADIAN

		# If the final result still cross block, then stay still
		if connection_line_segment.if_cross_any_block(block_list):
			return 0, 0
		
		to_move_x, to_move_y =  np.array(list(connection_line_segment.get_direction())) * SOLDIER_MOVE_SPEED 

		# Check if cross border
		target_point = Point(start_x + to_move_x, start_y + to_move_y)
		connection_line_segment = LineSegment(start_point, target_point)

		rotated = 0

		while (connection_line_segment.if_cross_border() or connection_line_segment.if_cross_any_block(block_list)) and rotated < 2 * pi:
			connection_line_segment = connection_line_segment.rotate_clockwise(ROTATE_RADIAN)
			rotated += ROTATE_RADIAN

		if connection_line_segment.if_cross_border() or connection_line_segment.if_cross_any_block(block_list):
			return 0, 0

		to_move_x, to_move_y =  np.array(list(connection_line_segment.get_direction())) * SOLDIER_MOVE_SPEED

		#dest_x = start_x + to_move_x
		#dest_y = start_y + to_move_y
		#dest_circle = Circle(dest_x, dest_y, SOLDIER_WIDTH / 2)

		#for soldier in friend_army.get_soldiers() + enemy_army.get_soldiers():
		#	soldier_circle = Circle(soldier.x, soldier.y, SOLDIER_WIDTH / 2)
		#	if soldier_circle.if_cross_circle(dest_circle):
		#		return 0, 0

		return to_move_x, to_move_y

	def hit_rate(self, enemy):
		pass

	def is_dead(self):
		if self.health_point < 0:
			return True
		else:
			return False

class Ranger(Soldier):
	def __init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode):
		Soldier.__init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode)

	def hit_rate(self, enemy):
		return 0

	def march(self, friend_army, enemy_army, battlefield_map):
		target = self.march_target_mode.choose_target(self, enemy_army)
		target_x = target.x
		target_y = target.y
		self.to_move_x, self.to_move_y = self.caculate_movement(self.x, self.y, target_x, target_y, friend_army, enemy_army, battlefield_map)

class Saber(Soldier):
	def __init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode):
		Soldier.__init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode)

	def hit_rate(self, enemy):
		point_self = Point(self.x, self.y)
		point_enemy = Point(enemy.x ,enemy.y)
		dist = point_self.dist(point_enemy)
		if dist <= SABER_ATTACK_RANGE:
			return 1
		else:
			return 0

	def march(self, friend_army, enemy_army, battlefield_map):
		target = self.march_target_mode.choose_target(self, enemy_army)
		target_x = target.x
		target_y = target.y
		self.to_move_x, self.to_move_y = self.caculate_movement(self.x, self.y, target_x, target_y, friend_army, enemy_army, battlefield_map)

class Sniper(Soldier):
	def __init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode):
		Soldier.__init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode)
	
	def hit_rate(self, enemy):
		return 0

	def march(self, friend_army, enemy_army, battlefield_map):
		target = self.march_target_mode.choose_target(self, enemy_army)
		target_x = 2 * self.x - target.x
		target_y = 2 * self.y - target.y
		self.to_move_x, self.to_move_y = self.caculate_movement(self.x, self.y, target_x, target_y, friend_army, enemy_army, battlefield_map)

class BehaviorMode(metaclass=Singleton):
	def __eq__(self, other):
		if type(other) is type(self):
			return self.__dict__ == other.__dict__
    
		return NotImplemented

	def __ne__(self, other):
		if type(other) is type(self):
			return not self.__eq__(other)

		return NotImplemented

	def __hash__(self):
		"""Override the default hash behavior (that returns the id or the object)"""
		return hash(tuple(sorted(self.__dict__.items())))

class TargetMode(BehaviorMode):
	def __init__(self):
		pass

	def choose_target(self, decider, enemy_army):
		pass

class WeakestTargetMode(TargetMode):
	def __init__(self):
		pass

	def choose_target(self, decider, enemy_army):
		weakest = random.choice(enemy_army.get_soldiers())
		for enemy in enemy_army.get_soldiers():
			if enemy.health_point < weakest.health_point:
				weakest = enemy

		return weakest

class VulnerableTargetMode(TargetMode):
	def __init__(self):
		pass

	def choose_target(self, decider, enemy_army):
		"""Hacky way to decide the most vulnerable enemy"""
		vulnerable = random.choice(enemy_army.get_soldiers())
		if isinstance(decider, Sniper):
			for enemy in enemy_army.get_soldiers():
				enemy_pos = Point(enemy.x, enemy.y)
				decider_pos = Point(decider.x, decider.y)
				if decider_pos.dist(enemy) > decider_pos.dist(vulnerable):
					vulnerable = enemy
		else:
			for enemy in enemy_army.get_soldiers():
				enemy_pos = Point(enemy.x, enemy.y)
				decider_pos = Point(decider.x, decider.y)
				if decider_pos.dist(enemy) < decider_pos.dist(vulnerable):
					vulnerable = enemy

		return vulnerable


class RandomTargetMode(TargetMode):
	def __init__(self):
		pass

	def choose_target(self, decider, enemy_army):
		return random.choice(enemy_army.get_soldiers())

class EscapeBehaviorMode(BehaviorMode):
	def __init__(self):
		pass

	def if_escape(self, decider):
		if np.random.random_sample() <= self.escape_rate(decider):
			return True
		else:
			return False

class FixedRateEscapeMode(EscapeBehaviorMode):
	def __init__(self, escape_fixed_rate):
		self.escape_fixed_rate = escape_fixed_rate/100

	def escape_rate(self, decider):
		return self.escape_fixed_rate

class ThresholdEscapeMode(EscapeBehaviorMode):
	def __init__(self, escape_threshold):
		self.escape_threshold = escape_threshold

	def escape_rate(self, decider):
		if decider.health_point <= self.escape_threshold:
			return 1
		else:
			return 0

class LinearEscapeMode(EscapeBehaviorMode):
	def __init__(self):
		pass

	def escape_rate(self, decider):
		return 1 - decider.health_point/100

class Block():
	def __init__(self, x, y, width):
		self.x = x
		self.y = y
		self.width = width

class BattlefieldMap():
	def __init__(self):
		self.block_list = []

	def add_block(self, x, y, width):
		self.block_list.append(Block(x, y, width))

	def get_block_list(self):
		return self.block_list

	def clear(self):
		self.block_list.clear()

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def dist(self, other_point):
		delta_x = self.x - other_point.x
		delta_y = self.y - other_point.y
		return sqrt(delta_x**2 + delta_y**2)

class Circle():
	def __init__(self, center_x, center_y, radius):
		self.center_x = center_x
		self.center_y = center_y
		self.radius = radius

	def if_cross_circle(self, other_circle):
		delta_x = self.center_x - other_circle.center_x
		delta_y = self.center_y - other_circle.center_y
		dist = sqrt(delta_x**2 + delta_y**2)

		if dist < (self.radius + other_circle.radius):
			return True
		else:
			return False

class LineSegment():
	def __init__(self, start_point, end_point):
		self.start_point = start_point
		self.end_point = end_point

	def get_direction(self):
		delta_x = self.end_point.x - self.start_point.x
		delta_y = self.end_point.y - self.start_point.y
		mod = sqrt(delta_x**2 + delta_y**2)
		return delta_x/mod, delta_y/mod

	def get_mod(self):
		delta_x = self.end_point.x - self.start_point.x
		delta_y = self.end_point.y - self.start_point.y
		mod = sqrt(delta_x**2 + delta_y**2)
		return mod

	def if_rect_cross(self, other_line):
		q1 = self.start_point
		q2 = self.end_point
		p1 = other_line.start_point
		p2 = other_line.end_point

		if min(p1.x,p2.x) <= max(q1.x,q2.x) and\
		    min(q1.x,q2.x) <= max(p1.x,p2.x) and\
		    min(p1.y,p2.y) <= max(q1.y,q2.y) and\
		    min(q1.y,q2.y) <= max(p1.y,p2.y):
		    return True
		else:
			return False

	def if_inside_rect(self, diagonal_line):
		q1 = self.start_point
		q2 = self.end_point
		p1 = diagonal_line.start_point
		p2 = diagonal_line.end_point

		if min(p1.x, p2.x) <= min(q1.x, q2.x) and\
			min(p1.y, p2.y) <= min(q1.y, q2.y) and\
			max(p1.x, p2.x) >= max(q1.x, q2.x) and\
			max(p1.y, p2.y) >= max(q1.y, q2.y):
			if q1.x == q2.x and (q1.x == p1.x or q1.x == p2.x):
				return False
			elif q1.y == q2.y and (q1.y == p1.y or q1.y == q2.y):
				return False
			else:
				return True
		else:
			return False


	def if_cross_line_segment(self, other_line):
  		if(self.if_rect_cross(other_line)):
  			q1 = self.start_point
  			q2 = self.end_point
  			p1 = other_line.start_point
  			p2 = other_line.end_point

  			if (((q1.x-p1.x)*(q1.y-q2.y)-(q1.y-p1.y)*(q1.x-q2.x)) * ((q1.x-p2.x)*(q1.y-q2.y)-(q1.y-p2.y)*(q1.x-q2.x))) < 0 and\
  			(((p1.x-q1.x)*(p1.y-p2.y)-(p1.y-q1.y)*(p1.x-p2.x)) * ((p1.x-q2.x)*(p1.y-p2.y)-(p1.y-q2.y)*(p1.x-p2.x))) < 0:
  				return True

  		return False

	def if_cross_block(self, block, border=False):
		half_width = block.width / 2
		point_one = Point(block.x - half_width, block.y - half_width)
		point_two = Point(block.x - half_width, block.y + half_width)
		point_three = Point(block.x + half_width, block.y + half_width)
		point_four = Point(block.x + half_width, block.y - half_width)

		line_segment_one = LineSegment(point_one, point_two)
		line_segment_two = LineSegment(point_two, point_three)
		line_segment_three = LineSegment(point_three, point_four)
		line_segment_four  = LineSegment(point_four, point_one)

		diagonal_line_segment = LineSegment(point_one, point_three)

		if self.if_cross_line_segment(line_segment_one) or\
			self.if_cross_line_segment(line_segment_two) or\
			self.if_cross_line_segment(line_segment_three) or\
			self.if_cross_line_segment(line_segment_four):
			return True
		elif not border and self.if_inside_rect(diagonal_line_segment):
			return True 
		else:
			return False

	def if_cross_any_block(self, block_list):
		for block in block_list:
			if self.if_cross_block(block):
				return True

		return False

	def if_cross_border(self, border_width=BATTLEFIELD_WIDTH):
		border_block = Block(border_width/2 - 0.5, border_width/2 - 0.5, border_width + 1 - SOLDIER_WIDTH)
		return self.if_cross_block(border_block, border=True)
	
	def rotate_clockwise(self, radian):
	    delta_x = self.end_point.x - self.start_point.x
	    delta_y = self.end_point.y - self.start_point.y
	    mod = sqrt(delta_x**2 + delta_y**2)
	    new_angle = atan2(delta_y, delta_x) - radian
	    new_delta_x = cos(new_angle) * mod
	    new_delta_y = sin(new_angle) * mod
	    return LineSegment(self.start_point, Point(self.start_point.x + new_delta_x, self.start_point.y + new_delta_y))

	def __str__(self):
		return str((self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y))