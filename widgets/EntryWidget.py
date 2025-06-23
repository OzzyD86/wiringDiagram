import tkinter as Tk
import tkinter.ttk as ttk

class EntryWidget(Tk.Frame):
	def __init__(self, master=None, text="", variable=None, command=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		
		Tk.Label(self, text=text).grid()
		Tk.Entry(self, textvariable= variable).grid()
		
	pass
	
class ComboEntryWidget(Tk.Frame):
	def __init__(self, master=None, text="", variable=None, command=None, values = [], state='readonly', *args, **kwargs):
		super().__init__(master, *args, **kwargs)

		Tk.Label(self, text=text).grid()
		self.box = ttk.Combobox(self, state=state, textvariable= variable, values=values)
		self.box.grid()
		if (command is not None):
			variable.trace('w', command)

	def setState(self, state='readonly'):
		self.box['state'] = state
	
	def setValues(self, values = []):
		self.box['values'] = values
		
class SpinEntryWidget(Tk.Frame):
	def __init__(self, master = None, text="", variable=None, min=0, max=100, command=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		Tk.Label(self, text=text).grid()
		Tk.Spinbox(self, from_=min, to=max, textvariable=variable).grid()
		