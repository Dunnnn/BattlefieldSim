import numpy as np
import functools
import random
import threading
import copy

from math import sin, cos, atan2, sqrt, pi, exp

from util_lib import *
from constants import * 
import itertools

# Classes below are business logic classes
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
		self.army_a.cast_move(self.battlefield_map)
		self.army_b.cast_move(self.battlefield_map)

	def attack_round(self):
		self.army_a.attack(self.army_b)
		self.army_b.attack(self.army_a)

	def cast_damage_round(self):
		self.army_a.cast_damage()
		self.army_b.cast_damage()

	def remove_death(self):
		self.army_a.remove_death(self.battlefield_map)
		self.army_b.remove_death(self.battlefield_map)

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
    def __init__(self, army_item_color, army_id):
    	self.soldier_list = []
    	self.soldier_factory = SoldierFactory()
    	self.army_item_color = army_item_color
    	self.army_id = army_id

    def add_soldiers(self, num_soldiers, center_x, center_y, damage, weapon_type, attack_target_mode, march_target_mode, escape_behavior_mode, escape_fixed_rate=None, escape_threshold=None):
    	relative_pos_indices = np.random.choice(DEPLOY_ARMY_RECT_WIDTH**2, size=num_soldiers, replace=False)
    	x_pos = np.floor((relative_pos_indices/DEPLOY_ARMY_RECT_WIDTH))
    	y_pos = (relative_pos_indices%DEPLOY_ARMY_RECT_WIDTH)

    	start_x = center_x - (DEPLOY_ARMY_RECT_WIDTH - 1) / 2
    	start_y = center_y - (DEPLOY_ARMY_RECT_WIDTH - 1) / 2
    	
    	abs_x_array = start_x + x_pos
    	abs_y_array = start_y + y_pos

    	new_soldier_list = []

    	for i in range(len(abs_x_array)):
    		x = (int)(abs_x_array[i])
    		y = (int)(abs_y_array[i])
    		soldier = self.soldier_factory.generate_soldier(x=x, y=y,\
    			damage=damage, weapon_type=weapon_type, attack_target_mode=attack_target_mode,\
    			march_target_mode=march_target_mode, escape_behavior_mode=escape_behavior_mode,\
    			escape_fixed_rate=escape_fixed_rate, escape_threshold=escape_threshold)
    		
    		self.soldier_list.append(soldier)
    		new_soldier_list.append(soldier)

    	return new_soldier_list

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
    		t=threading.Thread(target=soldier.move, args=(self, friend_center, enemy_army, enemy_center, battlefield_map, sema))
    		threads.append(t)

    	for thread in threads:
    		thread.start()

    	for thread in threads:
    		thread.join()

    def cast_move(self, battlefield_map):
    	for soldier in self.soldier_list:
    		to_x = soldier.x + soldier.to_move_x
    		to_y = soldier.y + soldier.to_move_y
    		if battlefield_map.not_occupied((to_x, to_y)):
    			del battlefield_map.soldiers[(soldier.x, soldier.y)]
    			soldier.x = to_x
    			soldier.y = to_y
    			battlefield_map.add_soldier((to_x, to_y))

    		soldier.to_move_x = 0
    		soldier.to_move_y = 0
    		
    def attack(self, enemy_army):
    	"""
    	This function only stores the total damage in the enemy Soldier Object. Attack will be
		executed in cast_attack()
    	"""
    	for soldier in self.soldier_list:
    		soldier.attack(enemy_army)

    def cast_damage(self):
    	for soldier in self.soldier_list:
    		soldier.health_point = soldier.health_point - soldier.damage_to_bear
    		soldier.damage_to_bear = 0

    def remove_death(self, battlefield_map):
    	for soldier in self.soldier_list:
    		if soldier.is_dead():
    			del battlefield_map.soldiers[(soldier.x, soldier.y)]
    			self.soldier_list.remove(soldier)

    def center(self):
    	total_x = 0
    	total_y = 0
    	for soldier in self.soldier_list:
    		total_x += soldier.x
    		total_y += soldier.y
    	return (int)(total_x/self.size()), (int)(total_y/self.size())

    def get_soldiers(self):
    	return self.soldier_list
    			
    def size(self):
    	return len(self.soldier_list)

    def clear(self):
    	self.soldier_list.clear()

class SoldierFactory():
	def generate_soldier(self, x, y, damage, weapon_type, attack_target_mode, march_target_mode, escape_behavior_mode, escape_fixed_rate=None, escape_threshold=None):
		if attack_target_mode == WEAKEST_TARGET_OPTION:
			attack_target_mode = WeakestAttackTargetMode()
		elif attack_target_mode == VULNERABLE_TARGET_OPTION:
			attack_target_mode = VulnerableAttackTargetMode()
		elif attack_target_mode == RANDOM_TARGET_OPTION:
			attack_target_mode = RandomAttackTargetMode()

		if march_target_mode == WEAKEST_TARGET_OPTION:
			march_target_mode = WeakestMarchTargetMode()
		elif march_target_mode == VULNERABLE_TARGET_OPTION:
			march_target_mode = VulnerableMarchTargetMode()
		elif march_target_mode == RANDOM_TARGET_OPTION:
			march_target_mode = RandomMarchTargetMode()

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
		sema.acquire()
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
		intersection_point = caculate_intersection_with_border((self.x, self.y), (target_x, target_y), BATTLEFIELD_WIDTH, CELL_WIDTH)
		target_x, target_y = find_closest_passable_cell(intersection_point, battlefield_map)
		self.to_move_x, self.to_move_y = self.caculate_movement(self.x, self.y, target_x, target_y, friend_army, enemy_army, battlefield_map)

	def get_enemies_in_attack_range(self, enemy_army):
		results = {}
		for enemy in enemy_army.get_soldiers():
			euclidean_distance = euclidean_dist((self.x, self.y), (enemy.x, enemy.y))
			if euclidean_distance <= self.attack_range:
				results[enemy] = euclidean_distance

		return results

	def caculate_movement(self, start_x, start_y, target_x, target_y, friend_army, enemy_army, battlefield_map):
		start = (start_x, start_y)
		target = (target_x, target_y)
		frontier = PriorityQueue()
		frontier.put(start, 0)
		came_from = {}
		cost_so_far = {}
		came_from[start] = None
		cost_so_far[start] = 0

		while not frontier.empty():
			current = frontier.get()

			if current == target:
				break
        
			for next in battlefield_map.passable_neighbors(current):
				new_cost = cost_so_far[current] + battlefield_map.cost(current, next)
				if next not in cost_so_far or new_cost < cost_so_far[next]:
					cost_so_far[next] = new_cost
					priority = new_cost + heuristic(target, next)
					frontier.put(next, priority)
					came_from[next] = current

		current = target
		previous = None

		try:
			came_from[current]
		except KeyError:
			if DEBUG_MODE:
				print('No Path Between')
				print(start)
				print(target)
			return 0, 0

		while current != start:
			previous = current
			current = came_from[current]

		if previous:
			return previous[0] - start_x, previous[1] - start_y
		else:
			return 0, 0

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
		self.attack_range = 1000

	def hit_rate(self, enemy):
		"""Sigmoid function"""
		dist = euclidean_dist((self.x, self.y), (enemy.x, enemy.y)) * CELL_WIDTH
		return 1 / (1 + exp(0.01 * dist-5))

	def march(self, friend_army, enemy_army, battlefield_map):
		target = self.march_target_mode.choose_target(self, enemy_army)
		target_x = target.x
		target_y = target.y
		self.to_move_x, self.to_move_y = self.caculate_movement(self.x, self.y, target_x, target_y, friend_army, enemy_army, battlefield_map)

class Saber(Soldier):
	def __init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode):
		Soldier.__init__(self, x, y, damage, attack_target_mode, march_target_mode, escape_behavior_mode)
		self.attack_range = SABER_ATTACK_RANGE

	def hit_rate(self, enemy):
		point_self = (self.x, self.y)
		point_enemy = (enemy.x ,enemy.y)
		dist = heuristic(point_self, point_enemy)
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
		self.attack_range = 1000
	
	def hit_rate(self, enemy):
		"""An inverse version of sigmoid function"""
		dist = euclidean_dist((self.x, self.y), (enemy.x, enemy.y)) * CELL_WIDTH
		return -1 / (1 + exp(0.03 * dist-4) ) + 1

	def march(self, friend_army, enemy_army, battlefield_map):
		target = self.march_target_mode.choose_target(self, enemy_army)
		target_x = 2 * self.x - target.x
		target_y = 2 * self.y - target.y
		intersection_point = caculate_intersection_with_border((self.x, self.y), (target_x, target_y), BATTLEFIELD_WIDTH, CELL_WIDTH)
		target_x, target_y = find_closest_passable_cell(intersection_point, battlefield_map)
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
	def choose_target(self, decider, enemy_army):
		pass

class WeakestAttackTargetMode(TargetMode):
	def choose_target(self, decider, enemy_army):
		weakest = random.choice(enemy_army.get_soldiers())
		enemies_in_range = decider.get_enemies_in_attack_range(enemy_army)
		for enemy in enemies_in_range:
			if enemy.health_point <= weakest.health_point:
				weakest = enemy

		return weakest

class WeakestMarchTargetMode(TargetMode):
	def choose_target(self, decider, enemy_army):
		weakest = random.choice(enemy_army.get_soldiers())
		for enemy in enemy_army.get_soldiers():
			if enemy.health_point <= weakest.health_point:
				weakest = enemy

		return weakest

class VulnerableAttackTargetMode(TargetMode):
	def choose_target(self, decider, enemy_army):
		"""Hacky way to decide the most vulnerable enemy"""
		vulnerable = random.choice(enemy_army.get_soldiers())
		enemies_in_range = decider.get_enemies_in_attack_range(enemy_army)
		if isinstance(decider, Sniper):
			for enemy in enemies_in_range:
				decider_pos = (decider.x, decider.y)
				vulnerable_pos = (vulnerable.x, vulnerable.y)
				if enemies_in_range[enemy] > euclidean_dist(vulnerable_pos, decider_pos) :
					vulnerable = enemy
		else:
			for enemy in enemies_in_range:
				decider_pos = (decider.x, decider.y)
				vulnerable_pos = (vulnerable.x, vulnerable.y)
				if enemies_in_range[enemy] < euclidean_dist(vulnerable_pos, decider_pos):
					vulnerable = enemy

		return vulnerable

class VulnerableMarchTargetMode(TargetMode):
	def choose_target(self, decider, enemy_army):
		"""Hacky way to decide the most vulnerable enemy"""
		vulnerable = random.choice(enemy_army.get_soldiers())
		if isinstance(decider, Sniper):
			for enemy in enemy_army.get_soldiers():
				enemy_pos = (enemy.x, enemy.y)
				decider_pos = (decider.x, decider.y)
				vulnerable_pos = (vulnerable.x, vulnerable.y)
				if euclidean_dist(enemy_pos, decider_pos) > euclidean_dist(vulnerable_pos, decider_pos) :
					vulnerable = enemy
		else:
			for enemy in enemy_army.get_soldiers():
				enemy_pos = (enemy.x, enemy.y)
				decider_pos = (decider.x, decider.y)
				vulnerable_pos = (vulnerable.x, vulnerable.y)
				if euclidean_dist(enemy_pos, decider_pos) < euclidean_dist(vulnerable_pos, decider_pos):
					vulnerable = enemy

		return vulnerable


class RandomAttackTargetMode(TargetMode):
	def choose_target(self, decider, enemy_army):
		random_enemy = random.choice(enemy_army.get_soldiers())
		enemies_in_range = decider.get_enemies_in_attack_range(enemy_army)
		if enemies_in_range:
			random_enemy = random.choice(list(enemies_in_range.keys()))

		return random_enemy

class RandomMarchTargetMode(TargetMode):
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

class BattlefieldMap():
	"""A battlefield map is a grid list"""
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.blocks = {}
		self.soldiers = {}
		self.weights = {}

	def cost(self, from_node, to_node):
		return self.weights.get(to_node, 1)

	def in_bounds(self, id):
		(x, y) = id
		return 0 <= x < self.width and 0 <= y < self.height

	def passable(self, id):
		try:
			self.blocks[id]
			return False
		except KeyError:
			return True

	def not_occupied(self, id):
		try:
			self.soldiers[id]
			return False
		except KeyError:
			return True

	def add_soldier(self, id):
		self.soldiers[id] = True

	def add_soldiers(self, soldiers):
		for soldier in soldiers:
			self.add_soldier((soldier.x, soldier.y))

	def add_block(self, id):
		self.blocks[id] = True

	def add_blocks(self, center_id, width):
		(center_x, center_y) = center_id

		start_x = (int) (center_x - (width - 1) / 2)
		end_x = (int) (center_x + (width - 1) / 2)
		start_y = (int) (center_y - (width - 1) / 2)
		end_y = (int) (center_y + (width - 1) / 2)
		x_list = list(range(start_x, end_x + 1))
		y_list = list(range(start_y, end_y + 1))
		blocks_to_add = list(itertools.product(x_list, y_list))
		blocks_to_add = filter(self.in_bounds, blocks_to_add)
		blocks_to_add = list(filter(self.passable, blocks_to_add))

		for block in blocks_to_add:
			self.add_block(block)

		return blocks_to_add

	def passable_neighbors(self, id):
		unfiltered_result = self.neighbors(id)
		results = filter(self.passable, unfiltered_result)
		return results

	def neighbors(self, id):
		(x, y) = id
		results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
		if (x + y) % 2 == 0: results.reverse() # aesthetics
		results = filter(self.in_bounds, results)
	
		return list(results)

	def convert_coord_to_cell(self, coords):
		(coord_x, coord_y) = coords
		return (int) (coord_x / CELL_WIDTH), (int) (coord_y / CELL_WIDTH)

	def convert_cell_to_coord(self, id):
		(x, y) = id
		return CELL_WIDTH / 2 + x * CELL_WIDTH, CELL_WIDTH / 2 + y * CELL_WIDTH

	def clear(self):
		self.blocks.clear()
		self.soldiers.clear()