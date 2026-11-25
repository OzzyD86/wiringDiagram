from incs.conf.configCore import configCore
from widgets.inputDialog import inputDialog

class configBase(configCore):
	def __init__(self):
		configCore.__init__(self)
		self.outerPolicies = {}
		self.innerPolicies = {}
		pass
	
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
