from widgets.inputDialog import inputDialog
import tkinter as Tk
from copy import copy
import sys
import json
import sqlite3

class config2():
	def __init__(self):
		self.outerPolicies = {}
		self.innerPolicies = {}
		pass
		
	def addOption(self, placement, key, data = {}, **kwargs):
		if (not placement in self.outerPolicies):
			self.outerPolicies[placement] = []
		
		self.outerPolicies[placement].append(key)
		if (not key in self.policy):
			if ("store" in data):
				self.policy[key] = data["store"]
			else:
				self.policy[key] = Tk.StringVar()
		
		self.innerPolicies[key] = data
		
		if ("value" in data):
			self.policy[key].set(data["value"])
	
	def portData(self, policy, data):
		if (policy in self.policy):
			print("CHANGE POLICY")
			if (hasattr(data, "save")):
				data = data.save()
			if (hasattr(self.policy[policy], "load")):
				self.policy[policy].load(copy(data))
			else:
				self.policy[policy].set(copy(data))
				#tkinter.messagebox.showerror("load", type(self.conf.policy[i[0]].get()))
			
			if (policy in self.innerPolicies):
				self.innerPolicies[policy]["value"] = self.policy[policy].get()
		else:
			print("NO POLICY FOR " + policy + "!")

	def open(self):
		pages = {}
		for i,j in self.outerPolicies.items():
			pages[i] = {}
			for k in j:
				pages[i][k] = self.innerPolicies[k]
				
		p = pages
		if ("General" in p):
			d = p["General"]
			del p["General"]
		else:
			d={}

		v = inputDialog(data=d)
		
		for i,j in p.items():
			v.addNb(i,j)
		for i,j in self.policy.items():
			v.set(i,j.get())
		v.vars["connector_context"] = self.policy["connector_context"]
		
		v.addButton("OK", "ok")
		v.passFunc("ok", self.ok)
			
def addOk(s, *args, **kwargs):
	
	x = kwargs["i"].nametowidget(".").conf # Aha! That's how to do it!
	y = []

	for i in ["left", "top", "bottom", "right"]:
		if (kwargs["pos_" + i] == "1"):
			y.append(i)
	kwargs["i"].add([kwargs["name"],{"name": kwargs["name"],"colour":kwargs["colour"], "pos":y}])
	#s.data
	x.innerPolicies["connector_context"]["value"][kwargs["name"]] = {
		"name": kwargs["name"],
		"colour": kwargs["colour"],
		"pos": y
	} 
	return True
	
def addPoodOk(s, *args, **kwargs):
	x = kwargs["i"].nametowidget(".").conf # Aha! That's how to do it!
	y = []

	for i in ["r", "g", "b"]:
		y.append(int(kwargs[i]))
	kwargs["i"].add([kwargs["name"],{ "hex":kwargs["hex"], "rgb":y}])
	#s.data
	x.innerPolicies["colours"]["value"][kwargs["name"]] = {
		"hex": kwargs["hex"],
		"rgb": y
	} # This shouldnt be done here!!
	return True
	
def doop(*args, **kwargs):
	dd = args[0].master.master.data
	if ("colours" in dd):
		vars = {}
		#Tk.messagebox.showerror("",dd["colours"]["obj"].exter_storage)
		for i,j in dd["colours"]["obj"].exter_storage.items():
			vars[i] = i
	else:
		vars ={
			"black":"Black"
		}
	x = inputDialog(args[0], data={
		"name": {
			"name":"Name",
			"type": "Entry",
		},
		"colour": {
			"name":"Colour",
			"type": "Combo",
			"values": vars
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
	x.passFunc("ok", lambda i=args[0], s=x, **kwargs: addOk(**kwargs, i =i,s=s))
	#Tk.messagebox.showerror("add",args)

def pood(*args, **kwargs):
	x = inputDialog(args[0], data={
		"name": {
			"name":"Name",
			"type": "Entry",
		},
		"hex": {
			"name":"Hexadecimal Value",
			"type": "Entry",
		},
		"r":{
			"name":"Red",
			"type": "Entry",
		},
		"g":{
			"name":"Green",
			"type": "Entry",
		},
		"b":{
			"name":"Blue",
			"type": "Entry",
		}
	})
	x.addButton("OK", "ok")
	x.passFunc("ok", lambda i=args[0], s=x, **kwargs: addPoodOk(**kwargs, i =i,s=s))

class dataWrapper():
	def __init__(self, data = {}):
		self.data = data
	
	def __copy__(self):
		return dataWrapper(copy(self.data))
		
	def get(self):
		return self.data
		
	def set(self, data):
		self.data = data
		
	def load(self, data):
		self.data = json.loads(data)
	
	def save(self):
		return json.dumps(self.data)
		
class config(config2):
	def save(self):
		self.db.commit()
		
	def __init__(self, master=None):
		super().__init__()
		self.db = sqlite3.connect("incs/core.db")
		self.cur = self.db.cursor()
		self.cur.execute("create table if not exists `config` (`key` text not null primary key, `value` text)")
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
			"colours" : dataWrapper({
				"Black": {"hex":"#000000","rgb":[0,0,0]},
				"Red": {"hex":"#FF0000","rgb":[255,0,0]},
				"Blue": {"hex":"#0000FF","rgb":[0,0,255]},
				"Purple": {"hex":"#FF00FF","rgb":[255,0,255]},
			})
		}
		self.roPols = {
			"mode" : Tk.BooleanVar(value = (hasattr(sys, "getandroidapilevel")))	
		}
		
		for i in self.cur.execute("SELECT * FROM `config`"):
			print(type(self.policy[i[0]]))
			if (hasattr(self.policy[i[0]], "load")):
				self.policy[i[0]].load(i[1])
			else:
				self.policy[i[0]].set(i[1])
			#print(i[0], i[1])
			
		self.addOption("Working General", "dev",{
			"name":"Developer mode",
			"type": "Checkbox",
			"value": self.policy["dev"].get()
		})
		self.addOption("Working General", "contextCollapse",{
			"name":"Collapse context menu",
			"type": "Checkbox",
			"value": self.policy["contextCollapse"].get()
		})
		
		self.addOption("General", "connector_context", {
			"name": "Connector Contexts",
			"type": "TreeView",
			"headings": { "name":"Name","colour":"Colour", "pos": "Sides"},
			"onAdd" : [doop],
			"varStore": self.policy["connector_context"],
			"value": self.policy["connector_context"].get()
		})
		self.addOption("Test", "colours", {
			"name": "Colours",
			"type": "TreeView",
			"headings": { "hex":"Hex","rgb":"RGB"},
			"onAdd" : [pood],
			"varStore": self.policy["colours"],
			"value": self.policy["colours"].get()
		})
		self.dev = self.policy["dev"]
		self.contextCollapse = self.policy["contextCollapse"]
		
	def ok(self, **kwargs):
		d = dataWrapper()
		for i,j in kwargs["connector_context"].items():
			#Tk.messagebox.showerror(i, j)
			d.data[i] = j#{"name": j["name"], "colour": j["colour"], "pos": j["pos"] }
		kwargs["connector_context"] = d.get()
		#Tk.messagebox.showerror("", kwargs["connector_context"])
		for i,j in kwargs.items():
			self.policy[i].set(j)
			self.innerPolicies[i]["value"] = j#self.policy[i]
			y=j
			t=False
			for k in self.outerPolicies.values():
				if (i in k):
					t = True
			
			if (t):
				if (type(y) is dict):
					y = json.dumps(y)
					
				self.cur.execute("replace into config (`key`, `value`) values (?,?)", (i, y))
		#Tk.messagebox.showerror("co", self.policy["connector_context"].get())
		
		self.policy["connector_context"] = d
		self.innerPolicies["connector_context"]["value"] = d.get()
		self.dev.set(self.policy["dev"].get())
		self.contextCollapse.set(self.policy["contextCollapse"].get())
		self.db.commit()
		#self.save()
		return True