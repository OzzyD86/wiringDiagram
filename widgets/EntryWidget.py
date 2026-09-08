import tkinter as Tk
import tkinter.ttk as ttk

class EntryWidget(Tk.Frame):
	def __init__(self, master=None, text="", variable=None, command=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		
		Tk.Label(self, text=text).grid(sticky='nesw')
		Tk.Entry(self, textvariable= variable).grid(sticky='nesw')
		self.columnconfigure(0, weight=1)
	pass
	
class ComboEntryWidget(Tk.Frame):
	def __init__(self, master=None, text="", variable=None, command=None, values = {}, state='readonly', *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.inter_values = values
		if (variable is None):
			self.choice = Tk.StringVar(self)
		else:
			self.choice = variable
		if (type(values) == dict):
			ls = list(values.values())
		else:
			ls = values
			
		Tk.Label(self, text=text).grid(sticky='nesw')
		self.box = ttk.Combobox(self, state=state, textvariable= self.choice, values= ls)
		self.box.grid(sticky='nesw')
		if (command is not None):
			variable.trace('w', command)
		self.columnconfigure(0, weight=1)

	def setState(self, state='readonly'):
		self.box['state'] = state
	
	def setValues(self, values = {}):
		self.inter_values = values
		if (type(values) == dict):
			ls = list(values.values())
		else:
			ls = values
		self.box['values'] = ls

	def get(self):
		return self.choice
		
	def get_key_of_value(self, value):
		for key, val in self.inter_values.items():
			if val == value:
				return key
		return None
		
class SpinEntryWidget(Tk.Frame):
	def __init__(self, master = None, text="", variable=None, min=0, max=100, command=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		Tk.Label(self, text=text).grid(sticky='nesw')
		Tk.Spinbox(self, from_=min, to=max, textvariable=variable).grid(sticky='nesw')
		self.columnconfigure(0, weight=1)
