from dev import device
from copy import deepcopy

def devAddCheck(self, *args, **kwargs):
	#print(args, kwargs, self.vars[kwargs['a']].get())

	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	y = device(self.vars['mName'].get(), self.vars['hName'].get())


	aa = p.objMk(self.c, y, (250, 150, 50, 50), connector_names = True)

def devDupCheck(self, *args, **kwargs):
	print(args, kwargs, self.vars[kwargs['a']].get())
	#v = int(self.vars['val'].get())
	#print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	mm = self.data['dName']["obj"].get_key_of_value(self.vars['dName'].get())
	x = (p.locs[mm])

	y = deepcopy(p.getDevice(mm))
	y.machName = self.vars['mName'].get()
	y.name = self.vars['hName'].get()

	aa = p.objMk(self.c, y, (250, 150, x[2], x[3]), connector_names = True)

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
