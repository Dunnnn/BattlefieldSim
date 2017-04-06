from math import sqrt
import collections
import heapq

from constants import *

"""
This library provides functions that are necessary
but do not fit in the MVC framework.
"""

# Classes below are helper classes
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

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_dist(a, b):
	(x1, y1) = a
	(x2, y2) = b
	return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def caculate_intersection_with_border(start, end, battlefield_width, cell_width):
	start_x, start_y = start
	end_x, end_y = end

	start_x = (start_x + 0.5) * cell_width
	start_y = (start_y + 0.5) * cell_width
	end_x = (end_x + 0.5) * cell_width
	end_y = (end_y + 0.5) * cell_width

	assert (0 <= start_x < battlefield_width)
	assert (0 <= start_y < battlefield_width)

	min_x = min(start_x, end_x)
	min_y = min(start_y, end_y)
	max_x = max(start_x, end_x)
	max_y = max(start_y, end_y)

	result_x = end_x
	result_y = end_y

	slope = None

	try:
		slope = (end_y - start_y) / (end_x - start_x)
	except ZeroDivisionError:
		if min_y <= 0 <= max_y:
			result_y = 0
		elif min_y <= battlefield_width <= max_y:
			result_y = battlefield_width

	
	if slope is not None:
		if slope == 0:
			if min_x <= 0 <= max_x:
				result_x = 0
			elif min_x <= battlefield_width <= max_x:
				result_x = battlefield_width
		else:
			x_to_examine = (0 - start_y) / slope + start_x
			if min_x <= x_to_examine <= max_x and 0 <= x_to_examine <= battlefield_width:
				result_x = x_to_examine
				result_y = 0
      
			x_to_examine = (battlefield_width - start_y) / slope + start_x
			if min_x <= x_to_examine <= max_x and 0 <= x_to_examine <= battlefield_width:
				result_x = x_to_examine
				result_y = battlefield_width

			y_to_examine = (0 - start_x) * slope + start_y
			if min_y <= y_to_examine <= max_y and 0 <= y_to_examine <= battlefield_width:
				result_x = 0
				result_y = y_to_examine

			y_to_examine = (battlefield_width - start_x) * slope + start_y
			if min_y <= y_to_examine <= max_y and 0 <= y_to_examine <= battlefield_width:
				result_x = battlefield_width
				result_y = y_to_examine


	if result_x == battlefield_width:
		result_x -= 1
	
	if result_y == battlefield_width:
		result_y -= 1

	if result_x < 0 or result_y < 0 and DEBUG_MODE:
		print("---Error---")
		print(start)
		print(end)
		print(result_x)
		print(result_y)
		print("-----------")

	return (int) (result_x / cell_width), (int) (result_y / cell_width)

def find_closest_passable_cell(cell, map):
	frontier = Queue()
	frontier.put(cell)
	came_from = {}
	came_from[cell] = None

	while not frontier.empty():
		current = frontier.get()

		if map.passable(current):
			return current     

		for next in map.neighbors(current):
			if next not in came_from:
				frontier.put(next)
				came_from[next] = current
