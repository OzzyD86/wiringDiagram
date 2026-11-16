import tkinter as Tk
from copy import copy

class configCore():
	#def __init__(self, master=None):
	#	super().__init__()
		
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
