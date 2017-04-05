import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sidepanel import SidePanel

from constants import *

class BattlefieldView():
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sidepanel = SidePanel(master)
        self.canvas = tk.Canvas(self.frame, width=BATTLEFIELD_WIDTH, height=BATTLEFIELD_WIDTH, bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.chosen_area = None

    def create_chosen_area(self, center_x, center_y, outline_color, area_width):
    	self.clear_chosen_area()
    	half_width = area_width / 2
    	self.chosen_area = self.canvas.create_rectangle((center_x - half_width, center_y - half_width, center_x + half_width, center_y + half_width), outline=outline_color, tags="chosen_area")

    def create_block(self, center_x, center_y, block_width):
    	half_width = block_width / 2
    	self.canvas.create_rectangle((center_x - half_width, center_y - half_width, center_x + half_width, center_y + half_width), fill="grey", outline="grey", tags=BLOCK_ITEM_TAG)

    def create_soldier_item(self, center_x, center_y, army_item_color, soldier_width):
    	half_width = soldier_width / 2
    	return self.canvas.create_oval((center_x - half_width, center_y - half_width, center_x + half_width, center_y + half_width), fill=army_item_color, outline=army_item_color, tags=SOLDIER_ITEM_TAG)

    def if_chosen_area_overlap_with_item(self, tags):
        # If statement prevent some weird cases when chosen area are empty
        if not self.canvas.bbox(self.chosen_area):
            return True

        if set(self.canvas.find_overlapping(*self.canvas.bbox(self.chosen_area))).intersection(set(self.canvas.find_withtag(tags))):
            return True
        else:
            return False

    def if_chosen_area_cross_border(self):
        chosen_area_bbox = self.canvas.bbox(self.chosen_area)
        ul_x = chosen_area_bbox[0]
        ul_y = chosen_area_bbox[1]
        br_x = chosen_area_bbox[2]
        br_y = chosen_area_bbox[3]
        if ul_x < -1 or ul_y < -1 or br_x > BATTLEFIELD_WIDTH or br_y > BATTLEFIELD_WIDTH:
            return True
        else:
            return False

    def mark_chosen_area_red(self):
        # If statement to prevent some weird cases when chosen area are empty
        if self.canvas.bbox(self.chosen_area):
            self.canvas.itemconfig(self.chosen_area, fill="red", outline="red")

    def clear_chosen_area(self):
    	if self.chosen_area:
    		self.canvas.delete(self.chosen_area)

    def clear_items_withtag(self, tag):
        self.canvas.delete(tag)

    def clear_canvas(self):
    	self.canvas.delete("all")

    def move_item(self, item, dx, dy):
        self.canvas.move(item, dx, dy)

    def update(self, func):
        self.canvas.update()
        if func:
            self.canvas.after(20, func)
