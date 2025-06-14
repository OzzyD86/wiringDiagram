import tkinter as Tk
import tkinter.ttk as ttk

class wdTk():

	def getKeys(self):
		KEYS = []
		VALUES = []
		#self.core.dia = d # WTF 
		for i in self.core.dia.listDevices():
			KEYS.append(i)
			VALUES.append(i + " (" + i + ")")
		return (KEYS, VALUES)
	
	## === Do Device Management
	
	# == Device Adding
	
	def devAddWin(self):
		self.aw = Tk.Tk()
		self.mName = Tk.StringVar(self.aw)
		self.hName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Machine Name").grid()
		Tk.Entry(self.aw, textvariable= self.mName).grid()
		Tk.Label(self.aw, text="Human Name").grid()
		Tk.Entry(self.aw, textvariable= self.hName).grid()
		Tk.Button(self.aw, text="Add", command=self.devAddComplete).grid()

	def devAddComplete(self):
		if (self.mName.get() in self.core.dia.listDevices()):
			tkinter.messagebox.showerror(title="Cannot add device", message="The name of the device is already in use.")
			return False
		
		self.core.addDevice(
			self.mName.get(), self.hName.get(),
			(400,300,50,50))
		
		self.aw.destroy()
		self.redraw()
		
	# == Device Editing
	
	def devEditWin(self):
		if (len(self.core.dia.listDevices())== 0):
			tkinter.messagebox.showerror(title="No devices", message="There are no devices to edit.")
			return False
			
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()
	
		self.top = Tk.StringVar(self.aw)
		self.left = Tk.StringVar(self.aw)
		self.width = Tk.StringVar(self.aw)
		self.height = Tk.StringVar(self.aw)
		self.mName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Edit Machine").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.mName, values=VALUES).grid()
		
		Tk.Label(self.aw, text="Top").grid()
		Tk.Entry(self.aw, textvariable= self.top).grid()
		Tk.Label(self.aw, text="Left").grid()
		Tk.Entry(self.aw, textvariable= self.left).grid()
		Tk.Label(self.aw, text="Width").grid()
		Tk.Entry(self.aw, textvariable= self.width).grid()
		Tk.Label(self.aw, text="Height").grid()
		Tk.Entry(self.aw, textvariable= self.height).grid()
		self.mName.trace('w',self.setmName)
		Tk.Button(self.aw, text="Add", command=self.devEditComplete).grid()

	def devEditComplete(self):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.mName.get())]
		
		self.core.updateDevice(obj,
			(int(self.left.get()),
			int(self.top.get()), 
			int(self.width.get()), 
			int(self.height.get()))
		)
		self.aw.destroy()
		self.redraw()
		
	# == Device Deleting
	
	def devDelWin(self):
		if (len(self.core.dia.listDevices())== 0):
			tkinter.messagebox.showerror(title="No devices", message="There are no devices to delete.")
			return False
			
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()

		#self.mName = Tk.StringVar(self.aw)
		self.dhName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Machine Name").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.dhName, values=VALUES)
		a.grid()
		#Tk.Label(self.aw, text="Human Name").grid()
		#Tk.Entry(self.aw, textvariable= self.hName).grid()
		Tk.Button(self.aw, text="Delete", command=self.devDelComplete).grid()

	def devDelComplete(self):
		
		# Load the objects
		KEYS, VALUES = self.getKeys()
		
		# Find the object
		if not self.dhName.get() in VALUES:
			tkinter.messagebox.showerror(title="No device", message="No.")
			return False
			
		obj = KEYS[VALUES.index(self.dhName.get())]
		
		self.core.deleteDevice(obj)
		self.redraw()
		self.aw.destroy()
		pass
		
	## === Do Connector Management
	
	# == Connector Adding
	
	def connAddWin(self):
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()
	
		self.cName = Tk.StringVar(self.aw)
		self.mhName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Machine Name").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.mhName, values=VALUES)
		a.grid()
		Tk.Label(self.aw, text="Connection Name").grid()
		Tk.Entry(self.aw, textvariable= self.cName).grid()
		Tk.Button(self.aw, text="Add", command=self.connAddComplete).grid()

	def connAddComplete(self):
		KEYS, VALUES = self.getKeys()
	
		obj = KEYS[VALUES.index(self.mhName.get())]
		if (self.cName.get() in self.core.dia.getDevice(obj).connectors.keys()):
			tkinter.messagebox.showerror(title="Cannot add plug", message="The name of the plug is already in use for this device.")
			return False
		
		self.core.addConnector(obj, self.cName.get())
			
		self.redraw()
		self.aw.destroy()
		
	## === Do Wire Management
	
	# == Wire Adding
	
	def wireAddWin(self):
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()
	
		self.indName = Tk.StringVar(self.aw)
		self.incName = Tk.StringVar(self.aw)
		self.outdName = Tk.StringVar(self.aw)
		self.outcName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Output Machine Name").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.outdName, values=VALUES).grid()
		
		self.indName.trace('w',self.setInC)
		self.outdName.trace('w',self.setOutC)
		Tk.Label(self.aw, text="Output Connection Name").grid()
		self.b = ttk.Combobox(self.aw, state='disabled', textvariable= self.outcName)
		self.b.grid()
		Tk.Label(self.aw, text="Input Machine Name").grid()
		c = ttk.Combobox(self.aw, state='readonly', textvariable= self.indName, values=VALUES).grid()
		Tk.Label(self.aw, text="Input Connection Name").grid()
		self.e = ttk.Combobox(self.aw, state='disabled', textvariable= self.incName)
		self.e.grid()
		Tk.Button(self.aw, text="Add", command=self.wireAddComplete).grid()

	def wireAddComplete(self):
		KEYS, VALUES = self.getKeys()
			
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		objIn = KEYS[VALUES.index(self.indName.get())]
		objOut = KEYS[VALUES.index(self.outdName.get())]

		self.core.addWire(objIn, self.incName.get(), objOut, self.outcName.get())
		self.redraw()
		self.aw.destroy()

	# = Wire Deleting
	
	def wireDelWin(self):
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()
		
		self.cName = Tk.StringVar(self.aw)
		self.mName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Machine Name").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.cName, values=VALUES).grid()
		
		Tk.Label(self.aw, text="Connection Point").grid()
		self.b = ttk.Combobox(self.aw, state='disabled', textvariable= self.mName, values=VALUES)
		self.b.grid()
		self.cName.trace('w', lambda *a, b = self.b: self.setM(i = self.cName.get(), o = b))
		self.mName.trace('w', self.setM2)
		Tk.Button(self.aw, text="Delete", command=self.wireDelComplete).grid()

	# == Drawing management ==
	def redraw(self):
		d = self.core.dia
		
		self.canvas.delete("all")
		for i in d.listDevices():
			if (i in d.locs):
				aa = objMk(self.canvas, d.getDevice(i), d.locs[i])
				d.getDevice(i).drwConnPos = aa

		for i in d.conns:
			p =0
			pin = None
			pout = None
			if (d.getDevice(i[0][0]) is not None):
				pin = d.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
			else:
				p+=1
			
			if (d.getDevice(i[1][0]) is not None):
				pout = d.getDevice(i[1][0]).connectors[i[1][1]]["direction"]
			else:
				p+=1
			
			if (pin == pout):
				if (pin is not None):
					print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
		
			if (p == 0):
				st = d.getDevice(i[0][0]).drwConnPos[i[0][1]]
				fn =  d.getDevice(i[1][0]).drwConnPos[i[1][1]]
				#dr.line((st,fn), fill=(0,0,0))
				r = self.canvas.create_line(st,fn, fill="black")
			#else:
			#print(pin, pout)