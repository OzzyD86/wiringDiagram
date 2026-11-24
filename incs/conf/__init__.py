import tkinter as Tk
from copy import copy
import incs.config
import json

class configCore():
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

class GLOBAL(configCore):
	pass

class LOCAL(configCore):
	
	def __init__(self):
		pass
		
	def ok(self, **kwargs):
		ww = self.master.nametowidget(".")
		cur = ww.core.struct.cur # Aha! That's how to do it!
		d = incs.config.dataWrapper()
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
					
				cur.execute("replace into config (`key`, `value`) values (?,?)", (i, y))
		
		o = {}
		o[None] = ["left", "right", "top", "bottom"]
		for i,j in d.get().items():
			o[i] = j["pos"]
		ww.core.dia.connector_context = o
		#raise Exception(o)
		self.policy["connector_context"] = d
		self.innerPolicies["connector_context"]["value"] = d.get()
		ww.redraw()
		return True