import tkinter as Tk
import tkinter.ttk as ttk
#from incs.wdCore import wdCore
#from widgets.connector_points import connector_points
from widgets.EntryWidget import EntryWidget, ComboEntryWidget, SpinEntryWidget
#import tkinter.messagebox

class inputDialog3(Tk.Toplevel):
	def __init__(self, master, data={}, **kwargs):
		super().__init__(master, **kwargs)
		self.data = data # This will be useful later!
		self.vars = {}
		self.funcs = {}
		for i, j in data.items():
			self.vars[i] = Tk.StringVar(self)
			#print(j)
			if ("onUpdate" in j.keys()):
				c = j['onUpdate']
			else:
				c = None
			if ("updateVars" in j.keys()):
				cc = j["updateVars"]
			else:
				cc = []
			if ("value" in j):
				self.vars[i].set(j["value"])
				
			if (j["type"] in ["Entry"]):
				j["obj"] = EntryWidget(self, text=j["name"], variable=self.vars[i])#.grid(padx=5, pady=(5,0), sticky='nsew')
			elif (j["type"] in ["Combo"]):
				j["obj"] = ComboEntryWidget(self, text=j["name"], variable=self.vars[i], values=j['values'], command= c, cArgs=(self, cc))#.grid(sticky='nsew')		
			elif (j["type"] in ["Label", "Text"]):
				j["obj"] = Tk.Label(self, text= j["text"], wraplength=800) #.grid(padx=5,pady=(5,0), sticky='sewn')
			elif (j["type"] in ["Spin"]):
				j["obj"] = SpinEntryWidget(self, text=j["name"], min=1, max=32, variable=self.vars[i])
			elif(j["type"] in ["Checkbox"]):
				j["obj"] = Tk.Checkbutton(self, text=j["name"], variable=self.vars[i], 
					onvalue=1, offvalue=0, state=Tk.DISABLED)
	
			j["obj"].grid(padx=5, pady=(5,0), sticky='nsew')
		self.columnconfigure(0, weight=1)

		
	def addButton(self, title, local_action = "add"):
		self.funcs[local_action] = []
		Tk.Button(self, text=title, command=lambda: self.button_press(local_action)).grid(padx=5, pady=(5, 0), sticky='swen')
	
	def set(self, op, val):
		self.vars[op].set(val)

	def passFunc(self, loc, func):
		self.funcs[loc].append(func)
		
	def button_press(self, mode):
		snd={}
		#print("Do stuff here") 
		for i,j in self.vars.items():
			if (type(j) is Tk.StringVar):
				if (self.data[i]["type"] in ["Combo"] and type(self.data[i]["values"]) is dict):
					snd[i] = self.data[i]["obj"].get_key_of_value(j.get())
				else:
					snd[i] = j.get()
			else:
				print("Slight panic:", i, j)
					
		for i in self.funcs[mode]:
			t = i(**snd)
		
		if (t):
			self.destroy()

