import tkinter as Tk

class EntryWidget(Tk.Frame):
	def __init__(self, master=None, text="", variable=None, command=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		
		Tk.Label(self, text=text).grid()
		Tk.Entry(self, textvariable= variable).grid()

		
	pass