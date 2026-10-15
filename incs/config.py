from widgets.inputDialog import inputDialog
import tkinter as Tk
from copy import copy
import sys

class config():
	def __init__(self):
		self.policy = {
			"dev" : Tk.BooleanVar(value=False),
			"contextCollapse": Tk.BooleanVar(value=False),
			#"mode" : Tk.BooleanVar(value = (hasattr(sys, "getandroidapilevel")))
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
			"type": "Entry",
			"value": {
				"None": {
					"name" : "None",
					"colour" : "black",
					"pos" : ["left", "right"]
				},
				"In": {
					"name" : "In",
					"colour" : "red",
					"pos" : ["left"]
				},
				"Out": { "name" : "Out", "colour" : "red", "pos" : ["right"] },
				"Both": {
					"name" : "Both",
					"colour" : "purple",
					"pos" : ["left", "right"]
				}
			}
		})
		self.innerPolicies = {}
		self.dev = self.policy["dev"]
		self.contextCollapse = self.policy["contextCollapse"]
	
	def addOption(self, placement, key, data = {}, **kwargs):
		if (not placement in self.outerPolicies):
			self.outerPolicies[placement] = {}
		
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
		v.addButton("OK", "ok")
		v.passFunc("ok", self.ok)
		pass
		
	def ok(self, **kwargs):
		for i,j in kwargs.items():
			self.policy[i].set(j)
			
		#raise Exception(kwargs)
		self.dev.set(self.policy["dev"].get())
		#raise Exception(self.policy["dev"].get() == 1)
		self.contextCollapse.set(self.policy["contextCollapse"].get())
		return True