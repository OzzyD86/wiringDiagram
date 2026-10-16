from dev import device
from copy import deepcopy

def devAddCheck(self, *args, **kwargs):
	print(args, kwargs, self.vars[kwargs['a']].get())
	#v = int(self.vars['val'].get())
	#print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	#mm = self.data['mhName']["obj"].get_key_of_value(self.vars['mhName'].get())
	#x = (p.locs[mm])
	#y = deepcopy(p.getDevice(mm))
	y = device(self.vars['mName'].get(), self.vars['hName'].get())
	#if (v == 1):
	#	y.addConnector(self.vars['cName'].get(), direction = self.vars['ddName'].get())
	#elif (v > 1):
	#	for i in range(v):
	#		y.addConnector(self.vars['cName'].get() + "_" + str(i+1), direction = self.vars['ddName'].get())

	aa = p.objMk(self.c, y, (250, 150, 50, 50), connector_names = True)

def devEditCheck(self, *args, **kwargs):
	print(args, kwargs, self.vars[kwargs['a']].get())
	#print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	mm = self.data['mName']["obj"].get_key_of_value(self.vars['mName'].get())
	x = (p.locs[mm])
	y = deepcopy(p.getDevice(mm))
	
	try:
		aa = p.objMk(self.c, y, (250, 150, int(self.vars['width'].get()), int(self.vars['height'].get())), connector_names = True)
	except ValueError:
		pass
