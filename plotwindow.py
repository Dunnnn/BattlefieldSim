import tkinter as tk
from constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotWindow():
	def __init__(self, master):
		master.title("Plot")
		master.protocol('WM_DELETE_WINDOW', self.hide_window)
		self.opened = False
		self.master = master
		self.frame = tk.Frame(master)
		self.fig = Figure( figsize=(7.5, 4), dpi=80)
		self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
		self.plt = self.fig.add_subplot(111)
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		self.canvas.show()

	def hide_window(self):
		self.master.withdraw()
		self.opened = False

	# * sign to pass variable number of parameters
	def plot(self, *args):
		self.plt.plot(*args)
		self.fig.canvas.draw()

	def title(self, *args):
		self.plt.set_title(*args)

	def xlabel(self, *args):
		self.plt.set_xlabel(*args)

	def legend(self, *args, **kw):
		self.plt.legend(*args, **kw)

	def clear(self):
		self.plt.clear()
		self.fig.canvas.draw()
