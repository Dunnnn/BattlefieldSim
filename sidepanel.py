import tkinter as tk
from tkinter import font
from constants import *
from validate_lib import *

class SidePanel():
    def __init__(self, root):
        self.frame = tk.Frame(root, bd=2, relief="raised")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Message Section
        self.msg_sec = tk.Frame(self.frame, bd=2, relief="groove", bg=MESSAGE_BG_COLOR, height=1)
        self.msg_sec.pack(fill=tk.X, expand=1)

        self.message = tk.StringVar()
        self.message.set(WELCOME_TEXT)

        self.msg_label = tk.Label(self.msg_sec, textvariable=self.message, font=font.Font(size=MESSAGE_FONT_SIZE,weight="bold"), bg=MESSAGE_BG_COLOR, wraplength=MESSAGE_WRAP_LENGTH)
        self.msg_label.pack(side=tk.LEFT)

        # Add Block Section
        self.add_block = tk.Frame(self.frame)
        self.add_block.pack(pady=5, fill=tk.BOTH, expand=1)

        self.block_width_var = tk.IntVar()
        self.block_width_var.set(MIN_BLOCK_WIDTH)

        self.add_block_label = tk.Label(self.add_block, text="Add Blocks To Map", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.add_block_label.grid(row=0, columnspan=3, sticky='WE')
        self.block_width_label = tk.Label(self.add_block, text="Block Width")
        self.block_width_label.grid(row=1, column=0, sticky='WE')
        self.block_width_entry = tk.Entry(self.add_block, textvariable=self.block_width_var, width=10)
        self.block_width_entry.grid(row=1, column=1, sticky='WE')
        self.add_block_button = tk.Button(self.add_block, text="Click To Add")
        self.add_block_button.grid(row=1, column=2, sticky='WE')

        # Weapon Selection Section
        self.weapon_sel = tk.Frame(self.frame)
        self.weapon_sel.pack(pady=5, fill=tk.BOTH, expand=1)

        self.weapon_sel_label = tk.Label(self.weapon_sel, text="Weapon Selection", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.weapon_sel_label.grid(row=0, columnspan=3, sticky='WENS')

        self.weapon_var = tk.IntVar()

        self.machine_gun_button = tk.Radiobutton(self.weapon_sel, text="Machine Gun", variable=self.weapon_var, value=MACHINE_GUN_OPTION)
        self.sword_button = tk.Radiobutton(self.weapon_sel, text="Sword", variable=self.weapon_var, value=SWORD_OPTION)
        self.sniper_gun_button = tk.Radiobutton(self.weapon_sel, text="Sniper Rifle", variable=self.weapon_var, value=SNIPER_GUN_OPTION)

        self.machine_gun_button.grid(row=1, column=0)
        self.sword_button.grid(row=1, column=1)
        self.sniper_gun_button.grid(row=1, column=2)

        # Damage Setting
        self.damage_set = tk.Frame(self.frame)
        self.damage_set.pack(pady=5, fill=tk.BOTH, expand=1)

        self.damage_set_label = tk.Label(self.damage_set, text="Damage Setting", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.damage_set_label.grid(row=0, columnspan=4, sticky='WENS')

        self.blue_damage_var = tk.DoubleVar()
        self.blue_damage_var.set(MIN_DAMAGE)
        self.red_damage_var = tk.DoubleVar()
        self.red_damage_var.set(MIN_DAMAGE)

        self.blue_damage_set_label = tk.Label(self.damage_set, text="Blue:", fg="blue")
        self.blue_damage_entry = tk.Entry(self.damage_set, textvariable=self.blue_damage_var, width=10)
        self.red_damage_set_label = tk.Label(self.damage_set, text="Red:", fg="red")
        self.red_damage_entry = tk.Entry(self.damage_set, textvariable=self.red_damage_var, width=10)

        self.blue_damage_set_label.grid(row=1, column=0)
        self.blue_damage_entry.grid(row=1, column=1)
        self.red_damage_set_label.grid(row=1, column=2)
        self.red_damage_entry.grid(row=1, column=3)

        # Target Mode Selction Section
        self.attack_target = tk.Frame(self.frame)
        self.attack_target.pack(pady=5, fill=tk.BOTH, expand=1)

        self.attack_target_label = tk.Label(self.attack_target, text="Attck Target", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.attack_target_label.grid(row=0, columnspan=3, sticky='WENS')

        self.attack_target_var = tk.IntVar()

        self.attack_target_weakest_button = tk.Radiobutton(self.attack_target, text="Weakest", variable=self.attack_target_var, value=WEAKEST_TARGET_OPTION)
        self.attack_target_vulnerable_button = tk.Radiobutton(self.attack_target, text="Vulnerable", variable=self.attack_target_var, value=VULNERABLE_TARGET_OPTION)
        self.attack_target_random_button = tk.Radiobutton(self.attack_target, text="Random", variable=self.attack_target_var, value=RANDOM_TARGET_OPTION)

        self.attack_target_weakest_button.grid(row=1, column=0)
        self.attack_target_vulnerable_button.grid(row=1, column=1)
        self.attack_target_random_button.grid(row=1, column=2)

        # March Mode Selection Section
        self.march_target = tk.Frame(self.frame)
        self.march_target.pack(pady=5, fill=tk.BOTH, expand=1)

        self.march_target_label = tk.Label(self.march_target, text="March Target", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.march_target_label.grid(row=0, columnspan=3, sticky='WENS')

        self.march_target_var = tk.IntVar()

        self.march_target_weakest_button = tk.Radiobutton(self.march_target, text="Weakest", variable=self.march_target_var, value=WEAKEST_TARGET_OPTION)
        self.march_target_vulnerable_button = tk.Radiobutton(self.march_target, text="Vulnerable", variable=self.march_target_var, value=VULNERABLE_TARGET_OPTION)
        self.march_target_random_button = tk.Radiobutton(self.march_target, text="Random", variable=self.march_target_var, value=RANDOM_TARGET_OPTION)

        self.march_target_weakest_button.grid(row=1, column=0)
        self.march_target_vulnerable_button.grid(row=1, column=1)
        self.march_target_random_button.grid(row=1, column=2)

        # Escape Behavior Selection Section
        self.escape_behav = tk.Frame(self.frame)
        self.escape_behav.pack(pady=5, fill=tk.BOTH, expand=1)

        self.escape_behav_label = tk.Label(self.escape_behav, text="Escape Behavior", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.escape_behav_label.grid(row=0, columnspan=3, sticky='WENS')

        self.escape_behav_var = tk.IntVar()

        self.fixed_rate_escape_button = tk.Radiobutton(self.escape_behav, text="Fixed Rate", variable=self.escape_behav_var, value=FIXED_RATE_OPTION, command=self.show_fixed_rate_sub)
        self.health_threshold_escape_button = tk.Radiobutton(self.escape_behav, text="Threshold", variable=self.escape_behav_var, value=THRESHOLD_OPTION, command=self.show_threshold_sub)
        self.health_linear_escape_button = tk.Radiobutton(self.escape_behav, text="Linear", variable=self.escape_behav_var, value=LINEAR_OPTION, command=self.show_linear_sub)

        self.fixed_rate_escape_button.grid(row=1, column=0)
        self.health_threshold_escape_button.grid(row=1, column=1)
        self.health_linear_escape_button.grid(row=1, column=2)

        self.fixed_rate_escape_val_var = tk.IntVar()

        self.fixed_rate_escape_val_label = tk.Label(self.escape_behav, text="Chance To Escape:")
        self.fixed_rate_escape_val_entry = tk.Entry(self.escape_behav, textvariable=self.fixed_rate_escape_val_var, width=10)
        self.fixed_rate_escape_val_mark_label = tk.Label(self.escape_behav, text="%")

        self.fixed_rate_escape_val_label.grid(row=2, column=0)
        self.fixed_rate_escape_val_entry.grid(row=2, column=1)
        self.fixed_rate_escape_val_mark_label.grid(row=2, column=2)

        self.health_threshold_escape_val_var = tk.IntVar()

        self.health_threshold_escape_val_label = tk.Label(self.escape_behav, text="Escape When Health Under:")
        self.health_threshold_escape_val_entry = tk.Entry(self.escape_behav, textvariable=self.health_threshold_escape_val_var, width=10)

        # Army Deployment Section
        self.army_deploy = tk.Frame(self.frame)
        self.army_deploy.pack(pady=5, fill=tk.BOTH, expand=1)

        self.army_deploy_label = tk.Label(self.army_deploy, text="Army Deploy", width=MENU_WIDTH, bg=SECTION_TITLE_BG)
        self.army_deploy_label.grid(row=0, columnspan = 4, sticky='WENS')

        self.num_soldier_var = tk.IntVar()
        self.num_soldier_var.set(MIN_NUM_SOLDIER)

        self.num_soldier_entry = tk.Entry(self.army_deploy, textvariable=self.num_soldier_var, width=10)
        self.blue_deploy_button = tk.Button(self.army_deploy, text="Deploy Blue")
        self.red_deploy_button = tk.Button(self.army_deploy, text="Deploy Red")
        self.num_soldier_entry.grid(row=1, column=0, columnspan=2)
        self.blue_deploy_button.grid(row=1, column=2)
        self.red_deploy_button.grid(row=1, column=3)

        self.num_blue_soldier_size_text = tk.StringVar()
        self.num_blue_soldier_size_text.set("Blue Army Size: {0:03d}".format(0))
        self.num_red_soldier_size_text = tk.StringVar()
        self.num_red_soldier_size_text.set("Red Army Size: {0:03d}".format(0))

        self.num_blue_soldier_label = tk.Label(self.army_deploy, textvariable=self.num_blue_soldier_size_text, fg="blue")
        self.num_red_soldier_label = tk.Label(self.army_deploy, textvariable=self.num_red_soldier_size_text, fg="red")
        self.num_blue_soldier_label.grid(row=2, column=0, columnspan=2)
        self.num_red_soldier_label.grid(row=2, column=2, columnspan=2)

        # Action Section
        self.action_sel = tk.Frame(self.frame)
        self.action_sel.pack(pady=5, fill=tk.BOTH, expand=1)

        self.start_button = tk.Button(self.action_sel, text="Start")
        self.start_button.pack(side=tk.LEFT,fill=tk.BOTH)

        self.clear_button = tk.Button(self.action_sel, text="Clear")
        self.clear_button.pack(side=tk.LEFT,fill=tk.BOTH)

        self.help_button = tk.Button(self.action_sel, text="Help")
        self.help_button.pack(side=tk.LEFT,fill=tk.BOTH)

        self.plot_button = tk.Button(self.action_sel, text="Plot Result", state=tk.DISABLED)
        self.plot_button.pack(side=tk.LEFT,fill=tk.BOTH)

    def show_fixed_rate_sub(self):
        self.health_threshold_escape_val_var.set(0)
        self.fixed_rate_escape_val_var.set(0)

        self.health_threshold_escape_val_label.grid_forget()
        self.health_threshold_escape_val_entry.grid_forget()        

        self.fixed_rate_escape_val_label.grid(row=2, column=0)
        self.fixed_rate_escape_val_entry.grid(row=2, column=1)
        self.fixed_rate_escape_val_mark_label.grid(row=2, column=2)

    def show_threshold_sub(self):
        self.health_threshold_escape_val_var.set(0)
        self.fixed_rate_escape_val_var.set(0)

        self.fixed_rate_escape_val_label.grid_forget()
        self.fixed_rate_escape_val_entry.grid_forget()
        self.fixed_rate_escape_val_mark_label.grid_forget()

        self.health_threshold_escape_val_label.grid(row=2, column=0, columnspan=2)
        self.health_threshold_escape_val_entry.grid(row=2, column=2)

    def show_linear_sub(self):
        self.health_threshold_escape_val_var.set(0)
        self.fixed_rate_escape_val_var.set(0)

        self.fixed_rate_escape_val_label.grid_forget()
        self.fixed_rate_escape_val_entry.grid_forget()
        self.fixed_rate_escape_val_mark_label.grid_forget()

        self.health_threshold_escape_val_label.grid_forget()
        self.health_threshold_escape_val_entry.grid_forget()

    def set_warning_message(self, msg):
        self.message.set(msg)
        self.msg_sec['bg'] = WARNING_BG_COLOR
        self.msg_label['bg'] = WARNING_BG_COLOR
        self.msg_label['fg'] = 'white'

    def set_info_message(self, msg):
        self.message.set(msg)
        self.msg_sec['bg'] = MESSAGE_BG_COLOR
        self.msg_label['bg'] = MESSAGE_BG_COLOR
        self.msg_label['fg'] = 'black'

    # Functions to disable different sections of side panel
    def disable_start_button(self):
        self.start_button['state'] = 'disabled'

    def disable_clear_button(self):
        self.clear_button['state'] = 'disabled'

    def disable_plot_button(self):
        self.plot_button['state'] = 'disabled'

    def disable_blue_deploy_button(self):
        self.blue_deploy_button['state'] = 'disabled'

    def disable_red_deploy_button(self):
        self.red_deploy_button['state'] = 'disabled'

    def disable_weapon_sel(self):
        self.machine_gun_button['state'] = 'disabled'
        self.sword_button['state'] = 'disabled'
        self.sniper_gun_button['state'] = 'disabled'

    def disable_attack_target(self):
        self.attack_target_weakest_button['state'] = 'disabled'
        self.attack_target_vulnerable_button['state'] = 'disabled'
        self.attack_target_random_button['state'] = 'disabled'

    def disable_march_target(self):
        self.march_target_weakest_button['state'] = 'disabled'
        self.march_target_vulnerable_button['state'] = 'disabled'
        self.march_target_random_button['state'] = 'disabled'

    def disable_escape_behav(self):
        self.fixed_rate_escape_button['state'] = 'disabled'
        self.health_threshold_escape_button['state'] = 'disabled'
        self.health_linear_escape_button['state'] = 'disabled'
        self.fixed_rate_escape_val_entry['state'] = 'disabled'
        self.health_threshold_escape_val_entry['state'] = 'disabled'

    def disable_army_deploy(self):
        self.disable_blue_deploy_button()
        self.disable_red_deploy_button()
        self.num_soldier_entry['state'] = 'disabled'

    def disable_add_block(self):
        self.block_width_entry['state'] = 'disabled'
        self.add_block_button['state'] = 'disabled'
    
    def disable_damage_set(self):
        self.blue_damage_entry['state'] = 'disabled'
        self.red_damage_entry['state'] = 'disabled'

    # Functions to enable different sections of side panel
    def normal_start_button(self):
        self.start_button['state'] = 'normal'

    def normal_clear_button(self):
        self.clear_button['state'] = 'normal'

    def normal_plot_button(self):
        self.plot_button['state'] = 'normal'

    def normal_blue_deploy_button(self):
        self.blue_deploy_button['state'] = 'normal'

    def normal_red_deploy_button(self):
        self.red_deploy_button['state'] = 'normal'

    def normal_weapon_sel(self):
        self.machine_gun_button['state'] = 'normal'
        self.sword_button['state'] = 'normal'
        self.sniper_gun_button['state'] = 'normal'

    def normal_attack_target(self):
        self.attack_target_weakest_button['state'] = 'normal'
        self.attack_target_vulnerable_button['state'] = 'normal'
        self.attack_target_random_button['state'] = 'normal'

    def normal_march_target(self):
        self.march_target_weakest_button['state'] = 'normal'
        self.march_target_vulnerable_button['state'] = 'normal'
        self.march_target_random_button['state'] = 'normal'

    def normal_escape_behav(self):
        self.fixed_rate_escape_button['state'] = 'normal'
        self.health_threshold_escape_button['state'] = 'normal'
        self.health_linear_escape_button['state'] = 'normal'
        self.fixed_rate_escape_val_entry['state'] = 'normal'
        self.health_threshold_escape_val_entry['state'] = 'normal'

    def normal_army_deploy(self):
        self.normal_blue_deploy_button()
        self.normal_red_deploy_button()
        self.num_soldier_entry['state'] = 'normal'
    
    def normal_damage_set(self):
        self.blue_damage_entry['state'] = 'normal'
        self.red_damage_entry['state'] = 'normal'

    def normal_add_block(self):
        self.block_width_entry['state'] = 'normal'
        self.add_block_button['state'] = 'normal'

    # Getter
    def get_block_width(self):
        block_width = None

        try:
            block_width = self.block_width_var.get()
        except tk.TclError:
            raise ValueError(INCORRECT_BLOCK_WIDTH_TEXT)

        if not is_valid_block_width(block_width):
            raise ValueError(INCORRECT_BLOCK_WIDTH_TEXT)
        else:
            return block_width

    def get_damage(self, army):
        damage = None

        try:
            if army.army_id == BLUE_ARMY:
                damage = self.blue_damage_var.get()
            elif army.army_id == RED_ARMY:
                damage =  self.red_damage_var.get()
        except tk.TclError:
            raise ValueError(INCORRECT_DAMAGE_TEXT)

        if not is_valid_damage(damage):
            raise ValueError(INCORRECT_DAMAGE_TEXT)
        else:
            return damage

    def get_num_soldier(self):
        num_soldier = None

        try:
            num_soldier =  self.num_soldier_var.get()
        except tk.TclError:
            raise ValueError(INCORRECT_NUM_SOLDIER_TEXT)

        if not is_valid_num_soldier(num_soldier):
            raise ValueError(INCORRECT_NUM_SOLDIER_TEXT)
        else:
            return num_soldier

    def get_weapon_type(self):
        return self.weapon_var.get()

    def get_attack_target_mode(self):
        return self.attack_target_var.get()

    def get_march_target_mode(self):
        return self.march_target_var.get()

    def get_escape_behavior_mode(self):
        return self.escape_behav_var.get()

    def get_escape_fixed_rate(self):
        escape_fixed_rate = None

        try:
            escape_fixed_rate = self.fixed_rate_escape_val_var.get()
        except tk.TclError:
            raise ValueError(INCORRECT_ESCAPE_FIXED_RATE_TEXT)

        if not is_valid_escape_fixed_rate(escape_fixed_rate):
            raise ValueError(INCORRECT_ESCAPE_FIXED_RATE_TEXT)
        else:
            return escape_fixed_rate

    def get_escape_threshold(self):
        escape_threshold = None
        try:
            escape_threshold =  self.health_threshold_escape_val_var.get()
        except tk.TclError:
            raise ValueError(INCORRECT_ESCAPE_THRESHOLD_TEXT)

        if not is_valid_threshold(escape_threshold):
            raise ValueError(INCORRECT_ESCAPE_THRESHOLD_TEXT)
        else:
            return escape_threshold



    # Setter
    def set_total_num_soldier(self, army, num):
        if army.army_id == BLUE_ARMY:
            self.num_blue_soldier_size_text.set("Blue Army Size: {0:03d}".format(num))
        elif army.army_id == RED_ARMY:
            self.num_red_soldier_size_text.set("Red Army Size: {0:03d}".format(num))

