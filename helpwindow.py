import tkinter as tk
from constants import *

class HelpWindow():
	def __init__(self, master):
		master.title("Help")
		master.protocol('WM_DELETE_WINDOW', self.hide_window)
		self.opened = False
		self.master = master
		self.frame = tk.Frame(master)
		self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		self.text = tk.Text(self.frame, width=75, height=40)
		self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		with open(HELP_FILE) as f:
			data = f.readlines()

		line_index = 1
		for line in data:
			is_heading = False
			if line[0] == '#':
				is_heading = True
				line = line[1:]

			self.text.insert(tk.END, line)
			
			if is_heading:
				self.text.tag_add('underline', "{}.0".format(line_index), "{}.{}".format(line_index, len(line)))
			
			line_index += 1

		self.text.tag_config("underline", underline=True)
		self.text.config(state=tk.DISABLED)

	def hide_window(self):
		self.master.withdraw()
		self.opened = False
