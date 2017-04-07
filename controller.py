import tkinter as tk
import itertools
import numpy as np

from constants import *
from validate_lib import *
from model import *
from view import BattlefieldView
from helpwindow import HelpWindow
from plotwindow import PlotWindow


class SimulatorController():
    def __init__(self):
        # Main Window
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.view = BattlefieldView(self.root)

        # Help Doc
        self.helpwindow = tk.Toplevel(self.root)
        self.helpwindow.resizable(width=False, height=False)
        self.helpwindow_view = HelpWindow(self.helpwindow)
        self.helpwindow.withdraw()
        self.helpwindow_view.opened = False

        # Plot Display
        self.plotwindow = tk.Toplevel(self.root)
        self.plotwindow.resizable(width=False, height=False)
        self.plotwindow_view = PlotWindow(self.plotwindow)
        self.plotwindow.withdraw()
        self.plotwindow_view.opened = False


        self.battlefield_map = BattlefieldMap(BATTLEFIELD_MAP_WIDTH, BATTLEFIELD_MAP_WIDTH)
        self.blue_army = Army(BLUE_ARMY_ITEM_COLOR, BLUE_ARMY) 
        self.red_army = Army(RED_ARMY_ITEM_COLOR, RED_ARMY)
        self.battle = Battle(self.blue_army, self.red_army, self.battlefield_map)

        self.view.sidepanel.start_button.bind("<Button>", self.start_sim)
        self.view.sidepanel.clear_button.bind("<Button>", self.clear_sim)
        self.view.sidepanel.help_button.bind("<Button>", self.open_help)
        self.view.sidepanel.plot_button.bind("<Button>", self.display_result)

        self.view.sidepanel.blue_deploy_button.bind("<Button>", lambda event, army=BLUE_ARMY: self.enter_deploy_army_mode(event, army))
        self.view.sidepanel.red_deploy_button.bind("<Button>", lambda event, army=RED_ARMY: self.enter_deploy_army_mode(event, army))
        self.view.sidepanel.add_block_button.bind("<Button>", self.enter_add_block_mode)
  
    def run(self):
        self.root.title("Battlefield Simulator")
        self.root.deiconify()
        self.root.mainloop()

    def open_help(self, event):
        if self.helpwindow_view.opened:
            self.helpwindow.withdraw()
            self.helpwindow_view.opened = False
        else:
            self.helpwindow.deiconify()
            self.helpwindow_view.opened = True

    def display_result(self, event):
        if self.plotwindow_view.opened:
            self.plotwindow.withdraw()
            self.plotwindow_view.opened = False
        else:
            self.plotwindow.deiconify()
            self.plotwindow_view.opened = True

    def plot_result(self):
        record = self.battle.get_battle_record()
        time = record.shape[1]
        T = np.arange(time)
        self.plotwindow_view.plot(T, record[0, :], 'b', T, record[1, :], 'r')
        self.plotwindow_view.title(PLOT_TITLE)
        self.plotwindow_view.xlabel(X_LABEL)
        self.plotwindow_view.legend(LEGEND, loc=LEGEND_LOC)

    def start_sim(self, event):
        if self.blue_army.size() <= 0 or self.red_army.size() <= 0:
            self.set_warning_message(NOT_ENOUGH_SOLDIER_TEXT)
            return 

        self.set_info_message("Simulating...")
        self.__disable_side_panel()
        self.battle.start()

        self.sim_next_round()

    def sim_next_round(self):
        if self.battle.is_battle_over():
            self.__enable_side_panel()
            self.view.sidepanel.normal_plot_button()
            self.view.sidepanel.disable_start_button()
            self.set_info_message(SIMULATION_END_TEXT)
            self.plot_result()
            return
        
        self.battle.next_round()

        if DEBUG_MODE:
            print("ROUND COMPLETED")

        self.redraw_armies(self.sim_next_round)
        self.view.sidepanel.set_total_num_soldier(self.blue_army, self.blue_army.size())
        self.view.sidepanel.set_total_num_soldier(self.red_army, self.red_army.size())

    def enter_deploy_army_mode(self, event, army):
        if army == BLUE_ARMY:
            self.enter_place_mode(DEPLOY_BLUE_ARMY_MODE)
        elif army == RED_ARMY:
            self.enter_place_mode(DEPLOY_RED_ARMY_MODE)

    def enter_add_block_mode(self, event):
        self.enter_place_mode(ADD_BLOCK_MODE)

    def enter_place_mode(self, mode):
        if mode == ADD_BLOCK_MODE:
            try:
                self.block_width = self.view.sidepanel.get_block_width()
            except ValueError as e:
                self.set_warning_message(e)
                return

            self.view.canvas.bind("<Motion>", lambda event, outline_color=ADD_BLOCK_OUTLINE, area_width=self.block_width: self.choose_area(event, outline_color, area_width))
            self.view.canvas.bind("<Button>", lambda event, area_width=self.block_width: self.add_block(event, area_width))

        else:
            chosen_army = None
            outline_color = None

            if mode == DEPLOY_BLUE_ARMY_MODE:
                chosen_army = self.blue_army
                outline_color = DEPLOY_BLUE_ARMY_OUTLINE
            elif mode == DEPLOY_RED_ARMY_MODE:
                chosen_army = self.red_army
                outline_color = DEPLOY_RED_ARMY_OUTLINE

            try:
                self.num_soldier = self.view.sidepanel.get_num_soldier()
                self.damage = self.view.sidepanel.get_damage(chosen_army)
                self.weapon_type = self.view.sidepanel.get_weapon_type()
                self.attack_target_mode = self.view.sidepanel.get_attack_target_mode()
                self.march_target_mode = self.view.sidepanel.get_march_target_mode()
                self.escape_behavior_mode = self.view.sidepanel.get_escape_behavior_mode()
                self.escape_fixed_rate = self.view.sidepanel.get_escape_fixed_rate()
                self.escape_threshold = self.view.sidepanel.get_escape_threshold()
            except ValueError as e:
                self.set_warning_message(e)
                return

            total_num_soldier = chosen_army.size() + self.num_soldier

            if not is_valid_total_num_soldier(total_num_soldier):
                self.set_warning_message(OVER_MAX_NUM_SOLDIER_TEXT)
                return

            self.view.canvas.bind("<Motion>", lambda event, outline_color=outline_color, area_width=DEPLOY_ARMY_RECT_WIDTH: self.choose_area(event, outline_color, area_width))
            self.view.canvas.bind("<Button>", lambda event, army=chosen_army: self.add_soldiers(event, army))

        # Disable All Side Buttons
        self.set_warning_message(PLACE_TEXT)
        self.__disable_side_panel()

        # Bind Function to return escape the mode
        self.root.bind("<Escape>", lambda event, msg=WELCOME_TEXT, msg_type=INFO_MESSAGE_TYPE: self.quit_place_mode(event, msg, msg_type))

        # Bind Function To Canvas
        self.view.canvas.bind("<Leave>", self.leave_canvas)

    def __disable_side_panel(self):
        self.view.sidepanel.disable_add_block()
        self.view.sidepanel.disable_start_button()
        self.view.sidepanel.disable_clear_button()
        self.view.sidepanel.disable_weapon_sel()
        self.view.sidepanel.disable_damage_set()
        self.view.sidepanel.disable_attack_target()
        self.view.sidepanel.disable_march_target()
        self.view.sidepanel.disable_escape_behav()
        self.view.sidepanel.disable_army_deploy()

    def __enable_side_panel(self):
        self.view.sidepanel.normal_add_block()
        self.view.sidepanel.normal_start_button()
        self.view.sidepanel.normal_clear_button()
        self.view.sidepanel.normal_weapon_sel()
        self.view.sidepanel.normal_damage_set()
        self.view.sidepanel.normal_attack_target()
        self.view.sidepanel.normal_march_target()
        self.view.sidepanel.normal_escape_behav()
        self.view.sidepanel.normal_army_deploy()

    def quit_place_mode(self, event, msg, msg_type):
        self.__quit_place_mode(msg, msg_type)

    def __quit_place_mode(self, msg, msg_type):
        # Enable all available side buttons
        self.set_message(msg, msg_type)

        self.__enable_side_panel()

        # Clear canvas
        self.__leave_canvas()

        # Unbind events
        self.root.unbind("<Escape>")
        self.view.canvas.unbind("<Motion>")
        self.view.canvas.unbind("<Button>")
        self.view.canvas.unbind("<Leave>")

    def choose_area(self, event, outline_color, area_width):
        center_cell = self.battlefield_map.convert_coord_to_cell((event.x, event.y))
        center_x, center_y = self.battlefield_map.convert_cell_to_coord(center_cell)
        area_width = area_width * CELL_WIDTH
        self.view.create_chosen_area(center_x, center_y, outline_color, area_width)

    def leave_canvas(self, event):
        self.__leave_canvas()

    def add_block(self, event, block_width):
        if self.view.if_chosen_area_overlap_with_item(SOLDIER_ITEM_TAG):
            self.view.mark_chosen_area_red()
        else:
            center_cell = self.battlefield_map.convert_coord_to_cell((event.x, event.y))
            center_x, center_y = self.battlefield_map.convert_cell_to_coord(center_cell)
            block_list = self.battlefield_map.add_blocks(center_cell, block_width)
            for block_x, block_y in block_list:
                self.view.create_block((block_x+0.5)*CELL_WIDTH, (block_y+0.5)*CELL_WIDTH, CELL_WIDTH)


    def add_soldiers(self, event, army):
        center_x, center_y = self.battlefield_map.convert_coord_to_cell((event.x, event.y))

        if self.view.if_chosen_area_overlap_with_item(SOLDIER_ITEM_TAG) or\
            self.view.if_chosen_area_overlap_with_item(BLOCK_ITEM_TAG) or\
            self.view.if_chosen_area_cross_border():
            self.view.mark_chosen_area_red()
        else:
            total_num_soldier = army.size() + self.num_soldier

            if not is_valid_total_num_soldier(total_num_soldier):
                self.__quit_place_mode(OVER_MAX_NUM_SOLDIER_TEXT, WARNING_MESSAGE_TYPE)
                return

            new_soldiers = army.add_soldiers(num_soldiers=self.num_soldier, center_x=center_x, center_y=center_y, damage=self.damage, weapon_type=self.weapon_type,\
                    attack_target_mode=self.attack_target_mode, march_target_mode=self.march_target_mode, escape_behavior_mode=self.escape_behavior_mode,\
                    escape_fixed_rate=self.escape_fixed_rate, escape_threshold=self.escape_threshold)
            self.battlefield_map.add_soldiers(new_soldiers)
            self.view.sidepanel.set_total_num_soldier(army, total_num_soldier)
            self.redraw_armies()

    def clear_sim(self, event):
        # Model Clear
        self.battlefield_map.clear()
        self.battle.clear()

        # Main Window Clear
        self.view.clear_canvas()

        # Plot Clear
        self.plotwindow_view.clear()

        # Side Panel Adjustment
        self.view.sidepanel.set_total_num_soldier(self.blue_army, self.blue_army.size())
        self.view.sidepanel.set_total_num_soldier(self.red_army, self.red_army.size())
        self.view.sidepanel.normal_start_button()
        self.view.sidepanel.disable_plot_button()
        self.view.sidepanel.set_info_message(WELCOME_TEXT)

    def __leave_canvas(self):
        self.view.clear_chosen_area()

    def set_message(self, msg, msg_type):
        if msg_type == INFO_MESSAGE_TYPE:
            self.set_info_message(msg)
        elif msg_type == WARNING_MESSAGE_TYPE:
            self.set_warning_message(msg)

    def set_info_message(self, text):
        self.view.sidepanel.set_info_message(text)

    def set_warning_message(self, text):
        self.view.sidepanel.set_warning_message(text)

    def redraw_armies(self, func=None):
        self.clear_items_withtag(SOLDIER_ITEM_TAG)
        self.draw_soldiers(self.blue_army.get_soldiers(), self.blue_army.army_item_color)
        self.draw_soldiers(self.red_army.get_soldiers(), self.red_army.army_item_color)
        self.view.update(func)

    def draw_soldiers(self, soldier_list, army_item_color):
        for soldier in soldier_list:
            self.draw_soldier(soldier, army_item_color)

    def draw_soldier(self, soldier, army_item_color):
        coord_x, coord_y = self.battlefield_map.convert_cell_to_coord((soldier.x, soldier.y))
        self.view.create_soldier_item(coord_x, coord_y, army_item_color, SOLDIER_WIDTH)

    def clear_items_withtag(self, tag):
        self.view.clear_items_withtag(tag)