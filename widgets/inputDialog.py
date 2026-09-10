import tkinter as Tk
import tkinter.ttk as ttk
#from incs.wdCore import wdCore
#from widgets.connector_points import connector_points
from widgets.EntryWidget import EntryWidget, ComboEntryWidget, SpinEntryWidget
#import tkinter.messagebox

class inputDialog(Tk.Toplevel):
	def __init__(self, master, data={}, **kwargs):
		self.data = data # This will be useful later!
		self.vars = {}
		self.funcs = {}
		super().__init__(master, **kwargs)
		for i, j in data.items():
			self.vars[i] = Tk.StringVar(self)
			if ("value" in j):
				self.vars[i].set(j["value"])
			if (j["type"] in ["Entry"]):
				EntryWidget(self, text=j["name"], variable=self.vars[i]).grid(padx=5, pady=(5,0), sticky='nsew')
			elif (j["type"] in ["Combo"]):
				ComboEntryWidget(self, text=j["name"], variable=self.vars[i], values=j['values'], command= j["onUpdate"]).grid(sticky='nsew')		
		self.columnconfigure(0, weight=1)
		
	def addButton(self, title, local_action = "add"):
		self.funcs[local_action] = []
		Tk.Button(self, text=title, command=lambda: self.button_press(local_action)).grid(padx=5, pady=(5, 0), sticky='swen')
	
	def set(self, op, val):
		self.vars[op] = val
		
	def passFunc(self, loc, func):
		self.funcs[loc].append(func)
		
	def button_press(self, mode):
		snd={}
		#print("Do stuff here") 
		for i,j in self.vars.items():
			if (type(j) is Tk.StringVar):
				#print(self.data[i])
				snd[i] = j.get()
			else:
				print("Slight panic:", i, j)
					
		for i in self.funcs[mode]:
			t = i(**snd)
		
		if (t):
			self.destroy()

class inputDialog2(inputDialog):
	def __init__(self, master, data={}, **kwargs):
		super().__init__(master, **kwargs)
		self.data = data # This will be useful later!
		self.vars = {}
		self.funcs = {}
		for i, j in data.items():
			self.vars[i] = Tk.StringVar(self)
			print(j)
			if ("onUpdate" in j.keys()):
				
				c = j['onUpdate']
			else:
				c = None
			if ("value" in j):
				self.vars[i].set(j["value"])
			if (j["type"] in ["Entry"]):
				EntryWidget(self, text=j["name"], variable=self.vars[i]).grid(padx=5, pady=(5,0), sticky='nsew')
			elif (j["type"] in ["Combo"]):
				ComboEntryWidget(self, text=j["name"], variable=self.vars[i], values=j['values'], command= c, cArgs=j['updateVars']).grid(sticky='nsew')		
		self.columnconfigure(0, weight=1)