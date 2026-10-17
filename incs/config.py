from widgets.inputDialog import inputDialog
import tkinter as Tk
from copy import copy
import sys
import json

def addOk(*args, **kwargs):
	x = kwargs["i"].nametowidget(".").conf # Aha! That's how to do it!
	y = []
	#Tk.messagebox.showerror("", kwargs)
	for i in ["left", "top", "bottom", "right"]:
		if (kwargs["pos_" + i] == "1"):
			y.append(i)
	kwargs["i"].add([kwargs["name"],kwargs["name"],kwargs["colour"],y])
	return True
	
def doop(*args, **kwargs):
	x = inputDialog(args[0], data={
		"name": {
			"name":"Name",
			"type": "Entry",
		},
		"colour": {
			"name":"Colour",
			"type": "Combo",
			"values": {
				"black":"Black",
			},
		},
		"pos_left":{
			"name":"Left",
			"type": "Checkbox",
			"value": 1
		},
		"pos_top":{
			"name":"Top",
			"type": "Checkbox",
			"value": 1#.policy["contextCollapse"].get()
		},
		"pos_right":{
			"name":"Right",
			"type": "Checkbox",
			"value": 1#.policy["contextCollapse"].get()
		},
		"pos_bottom":{
			"name":"Bottom",
			"type": "Checkbox",
			"value": 1#.policy["contextCollapse"].get()
		}
	})
	x.addButton("OK", "ok")
	x.passFunc("ok", lambda i=args[0], **kwargs: addOk(**kwargs, i =i))
	#Tk.messagebox.showerror("add",args)

class dataWrapper():
	def __init__(self, data = {}):
		self.data = data
		
	def get(self):
		return self.data
		
	def set(self, data):
		self.data = data
		
	def load(self, data):
		self.data = json.loads(data)
	
	def save(self):
		return json.dumps(self.data)
		
class config():
	def __init__(self, master=None):
		self.master = master
		self.policy = {
			"dev" : Tk.BooleanVar(value=False),
			"contextCollapse": Tk.BooleanVar(value=False),
			"mode" : Tk.BooleanVar(value = (hasattr(sys, "getandroidapilevel"))),
			"connector_context" : dataWrapper({
				"None": { "name" : "None", "colour" : "black", "pos" : ["left", "right"] },
				"In": { "name" : "In", "colour" : "red", "pos" : ["left"] },
				"Out": { "name" : "Out", "colour" : "blue", "pos" : ["right"] },
				"Both": { "name" : "Both", "colour" : "purple", "pos" : ["left", "right"] }
			}),
		}
		self.outerPolicies = {}
		self.roPols = {
			"mode" : Tk.BooleanVar(value = (hasattr(sys, "getandroidapilevel")))	
		}
		self.addOption("General", "dev",{
			"name":"Developer mode",
			"type": "Checkbox",
			"value": self.policy["dev"].get()
		})
		self.addOption("General", "contextCollapse",{
			"name":"Collapse context menu",
			"type": "Checkbox",
			"value": self.policy["contextCollapse"].get()
		})
		self.addOption("General", "mode",{
			"name":"Android mode",
			"type": "Checkbox",
			"value": (hasattr(sys, "getandroidapilevel"))
		})
		self.addOption("General", "connector_context", {
			"name": "Connector Contexts",
			"type": "TreeView",
			"onAdd" : [doop],
			
			"value": self.policy["connector_context"].get()
		})
		self.innerPolicies = {}
		self.dev = self.policy["dev"]
		self.contextCollapse = self.policy["contextCollapse"]
	
	def addOption(self, placement, key, data = {}, **kwargs):
		if (not placement in self.outerPolicies):
			self.outerPolicies[placement] = {}
		
		if (not key in self.policy):
			self.policy[key] = Tk.StringVar()
		
		self.outerPolicies[placement][key] = data
		if ("value" in data):
			self.policy[key].set(data["value"])
		
	def open(self):
		p = self.outerPolicies.copy()
		if ("General" in p):
			d = p["General"]
			del p["General"]
		else:
			d={}
		v = inputDialog(data=d)
		#if ("" in self.outerPolicies):
		#	del self.outerPolicies[""]
		for i,j in p.items():
			v.addNb(i,j)
		for i,j in self.policy.items():
			v.set(i,j.get())
		v.vars["connector_context"] = self.policy["connector_context"]
		
		v.addButton("OK", "ok")
		v.passFunc("ok", self.ok)
		pass
		
	def ok(self, **kwargs):
		cur = self.master.nametowidget(".").core.struct.cur # Aha! That's how to do it!
	
		#Tk.messagebox.showerror("", kwargs["connector_context"])
		for i,j in kwargs.items():
			self.policy[i].set(j)
			y = self.policy[i].get()
			if (type(y) is dict):
				y = json.dumps(y)
			cur.execute("replace into config (`key`, `value`) values (?,?)", (i, y))
		#Tk.messagebox.showerror("co", self.policy["connector_context"].get())
		
		d = dataWrapper()
		for i,j in kwargs["connector_context"].items():
			#Tk.messagebox.showerror(i, j)
			d.data[i] = {"name": j[0], "colour": j[1], "pos": j[2] }
		self.policy["connector_context"] = d
		self.outerPolicies["General"]["connector_context"]["value"] = d.get()
		self.dev.set(self.policy["dev"].get())
		self.contextCollapse.set(self.policy["contextCollapse"].get())

		return True