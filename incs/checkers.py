from dev import device
from copy import deepcopy

def devAddCheck(self, *args, **kwargs):
	#print(args, kwargs, self.vars[kwargs['a']].get())

	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	y = device(self.vars['mName'].get(), self.vars['hName'].get())


	aa = p.objMk(self.c, y, (250, 150, 50, 50), connector_names = True)

def devDupCheck(self, *args, **kwargs):
	#print(args, kwargs, self.vars[kwargs['a']].get())
	#v = int(self.vars['val'].get())
	#print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	mm = self.data['dName']["obj"].get_key_of_value(self.vars['dName'].get())
	x = (p.locs[mm])

	y = deepcopy(p.getDevice(mm))
	y.machName = self.vars['mName'].get()
	y.name = self.vars['hName'].get()

	aa = p.objMk(self.c, y, (self.size[0]/2, self.size[1]/2, x[2], x[3]), connector_names = True)

def devEditCheck(self, *args, **kwargs):
	#print(args, kwargs, self.vars[kwargs['a']].get())
	#print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	mm = self.data['mName']["obj"].get_key_of_value(self.vars['mName'].get())
	if (mm is not None):
		x = (p.locs[mm])
		y = deepcopy(p.getDevice(mm))
		
		try:
			aa = p.objMk(self.c, y, (self.size[0]/2, self.size[1]/2, int(self.vars['width'].get()), int(self.vars['height'].get())), connector_names = True, highlight_connected = True)
		except ValueError:
			pass

def wireAddCheck(self, *args, **kwargs):
	#print(args, kwargs, self.vars[kwargs['a']].get())
	
	##print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	dout = self.data['outdName']["obj"].get_key_of_value(self.vars['outdName'].get())
	din = self.data['indName']["obj"].get_key_of_value(self.vars['indName'].get())
	if (dout is not None):
		loc = p.locs[dout]
		y = deepcopy(p.getDevice(dout))
		aa = p.objMk(self.c, y, (self.size[0]/3, self.size[1]/2, int(loc[2]), int(loc[3])), connector_names = True, highlight_connected = True)
		pass

	if (din is not None):
		loc = p.locs[din]
		y = deepcopy(p.getDevice(din))

		ab = p.objMk(self.c, y, (self.size[0]/3*2, self.size[1]/2, int(loc[2]), int(loc[3])), connector_names = True, highlight_connected = True)
		pass

	cout = self.data['outcName']['obj'].get().get()
	cin = self.data['incName']['obj'].get().get()
	
	if ((dout is not None) and (din is not None) and (cout in p.getDevice(dout).drwConnPos) and (cin in p.getDevice(din).drwConnPos)):
		st = p.getDevice(dout).drwConnPos[cout]
		fn = p.getDevice(din).drwConnPos[cin]
		
		r = self.c.create_line(st[0] - p.locs[dout][0] + (self.size[0]/3), 
			st[1] - p.locs[dout][1] + (self.size[1]/2),
			fn[0] - p.locs[din][0] + (self.size[0] / 3 * 2), 
			fn[1] - p.locs[din][1] + (self.size[1]/2), fill="black")

	pass

def connDelCheck(self, *args, **kwargs):
	
	#print(args, kwargs, self.vars[kwargs['a']].get())
	#v = int(self.vars['val'].get())
	#print(args[0].get())
	p = self.nametowidget(".").core.dia # Aha! That's how to do it!
	self.c.delete("all")
	
	mm = self.data['outdName']["obj"].get_key_of_value(self.vars['outdName'].get())
	print(mm)
	if (mm is not None):
		x = (p.locs[mm])
		y = deepcopy(p.getDevice(mm))
		
		y.delConnector(self.vars['outcName'].get())

		aa = p.objMk(self.c, y, (self.size[0]/2, self.size[1]/2, x[2], x[3]), connector_names = True, highlight_connected = True)
