import tkinter as Tk
import tkinter.ttk as ttk
from incs.wdCore import wdCore

class wdTk():
	def resize_canvas(self, event):
   
		new_width = event.width
		new_height = event.height

		# Update the canvas size
		self.canvas.config(width=new_width, height=new_height)

	def __init__(self):
		self.app_name = "WiringDiagram"
		self._open_file = None
		
		self.window = Tk.Tk()
		self.window.title(self.app_name)
		self.core = wdCore(self.window)
		self.window.protocol('WM_DELETE_WINDOW', self.quit)
		self.window.geometry("860x660")
		#frame = Tk.Frame(self.window, height=900,width=700)
		#frame.grid(column=0,row=0)
		self.canvas = Tk.Canvas(self.window, width=800, height=600)
		self.canvas.grid(sticky="news")
		self.vscroll = Tk.Scrollbar(self.window)
		self.vscroll.grid(column=1, row=0,sticky="news")
		self.hscroll = Tk.Scrollbar(self.window,orient=Tk.HORIZONTAL)
		self.hscroll.grid(column=0, row=1,sticky="news")
		self.canvas.config(scrollregion = (0,-0,800,600))
		self.canvas.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)
		self.vscroll.config( command = self.canvas.yview )
		self.hscroll.config( command = self.canvas.xview )
		self.window.rowconfigure(0, weight=1)
		self.window.columnconfigure(0, weight=1)
		#self.canvas.bind("<Button-1>", self.click_call)
		#self.window.bind('<Configure>', self.resize_canvas)
	
		self.menu = {
			"root" : Tk.Menu(),
			"file": Tk.Menu(),
			"add": Tk.Menu(),
			"edit": Tk.Menu(),
			"delete": Tk.Menu(),
			"export": Tk.Menu()
		}
	
		mf = self.menu["file"]
		mf.add_command(label="New", command= self.file_new)
		mf.add_separator()
		mf.add_command(label="Load", command=self.file_load)
		mf.add_command(label="Save", command= self.file_save)
		mf.add_command(label="Save As...", state=Tk.DISABLED)
		mf.add_separator()
		mf.add_command(label="Properties...", state=Tk.DISABLED)
		mf.add_separator()
		mf.add_command(label="Quit", command=self.quit)
			
		add = self.menu["add"]
		add.add_command(label="Device", command=self.devAddWin)
		add.add_command(label="Duplicate Device", command=self.dupDevAddWin)
		add.add_separator()
		add.add_command(label="Plug", command=self.connAddWin)
		add.add_command(label="Connection", command=self.wireAddWin)

		edit = self.menu["edit"]
		edit.add_command(label="Device", command=self.devEditWin)
		edit.add_command(label="Plug", state=Tk.DISABLED)
		edit.add_command(label="Connection", state=Tk.DISABLED)

		delete = self.menu["delete"]
		delete.add_command(label="Device", command=self.devDelWin)
		delete.add_command(label="Plug", state=Tk.DISABLED)
		delete.add_command(label="Connection", command=self.wireDelWin)

		self.menu["export"].add_command(label="PNG", command=self.export_png)

		y = self.menu["root"]
		y.add_cascade(label="File", menu=self.menu["file"])
		y.add_cascade(label="Add", menu=self.menu["add"])
		y.add_cascade(label="Edit", menu=self.menu["edit"])
		y.add_cascade(label="Delete", menu=self.menu["delete"])
		y.add_cascade(label="Export", menu=self.menu["export"])

		self.window.config(menu=self.menu["root"])
		
	def open_file(self, file):
		self.core.open_file(file)
		self._open_file = file
		self.canvas.config(scrollregion=(self.core.dia.bounds))

		self.updateWindowTitle()
		
	def quit(self):
		#print("Closing:", self.core.struct.is_changed())
		if (self.core.struct.is_changed()):
			a = Tk.messagebox.askyesnocancel(title="Unsaved Changed", message="There are unsaved changes. Save before closing?")
			#print(a)
			if (a is None):
				return None
			elif (a is False):
				exit(0)
			elif (a is True):
				self.file_save()

				exit(0)
		else:
			if (Tk.messagebox.askquestion(title=None, message="Are you sure") == "yes"):
				exit(0)
			
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

	def dupDevAddWin(self):
		self.aw = Tk.Tk()

		KEYS, VALUES = self.getKeys()

		self.dName = Tk.StringVar(self.aw)
		self.mName = Tk.StringVar(self.aw)
		self.hName = Tk.StringVar(self.aw)
	
		Tk.Label(self.aw, text="Existing machine to duplicate").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.dName, values=VALUES).grid()

		Tk.Label(self.aw, text="New Machine Name").grid()
		Tk.Entry(self.aw, textvariable= self.mName).grid()
		Tk.Label(self.aw, text="Human Name").grid()
		Tk.Entry(self.aw, textvariable= self.hName).grid()
		Tk.Button(self.aw, text="Add", command=self.dupDevAddComplete).grid()

	def dupDevAddComplete(self):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.dName.get())]
		
		
		if (self.mName.get() in self.core.dia.listDevices()):
			tkinter.messagebox.showerror(title="Cannot add device", message="The name of the device is already in use.")
			return False
		
		d = self.core.dia.getDevice(obj)
		s = self.core.dia.locs[obj]
		print(s)
		
		self.core.addDevice(
			self.mName.get(), self.hName.get(),
			(400,300,s[2],s[3]))
		
		for i, j in d.connectors.items():
			self.core.addConnector(self.mName.get(), i, dir=  j['direction'])

		self.updateWindowTitle()		
		self.aw.destroy()
		self.redraw()

		
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
		
		self.updateWindowTitle()		
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
		self.canvas.config(scrollregion=(self.core.dia.bounds))
		self.updateWindowTitle()

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
		self.updateWindowTitle()

		self.redraw()
		self.aw.destroy()
		pass
		
	## === Do Connector Management
	
	# == Connector Adding
	
	def connAddWin(self):
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()
		self.val = Tk.IntVar(self.aw)
		self.cName = Tk.StringVar(self.aw)
		self.mhName = Tk.StringVar(self.aw)
		self.ddName = Tk.StringVar(self.aw)
		self.ddName.set("None")
		Tk.Label(self.aw, text="Machine Name").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.mhName, values=VALUES)
		a.grid()
		Tk.Label(self.aw, text="Connection Name").grid()
		Tk.Entry(self.aw, textvariable= self.cName).grid()
		Tk.Label(self.aw, text="Data Direction").grid()
		a = ttk.Combobox(self.aw, state='readonly', textvariable= self.ddName, values=["In", "Out", "Both", "None"]).grid()

		Tk.Label(self.aw, text="Quantity").grid()
		Tk.Spinbox(self.aw, from_=1, to=32, textvariable=self.val).grid()
		
		Tk.Button(self.aw, text="Add", command=self.connAddComplete).grid()

	def connAddComplete(self):
		KEYS, VALUES = self.getKeys()
	
		obj = KEYS[VALUES.index(self.mhName.get())]
		if (self.cName.get() in self.core.dia.getDevice(obj).connectors.keys()):
			Tk.messagebox.showerror(title="Cannot add plug", message="The name of the plug is already in use for this device.")
			return False
		
		if (self.val.get() == 1):
			self.core.addConnector(obj, self.cName.get(), dir= self.ddName.get())
		elif (self.val.get() > 1):
			for i in range(self.val.get()):
				self.core.addConnector(obj, self.cName.get()+"_"+str(i+1), dir= self.ddName.get())
			pass
		else:
			Tk.messagebox.showerror(title="Cannot add plug", message="Invalid value.")
			return False
		
		self.updateWindowTitle()

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
		
		Tk.Label(self.aw, text="Output Connection Name").grid()
		self.b = ttk.Combobox(self.aw, state='disabled', textvariable= self.outcName)
		self.b.grid()
			
		Tk.Label(self.aw, text="Input Machine Name").grid()
		c = ttk.Combobox(self.aw, state='readonly', textvariable= self.indName, values=VALUES).grid()
		Tk.Label(self.aw, text="Input Connection Name").grid()
		self.e = ttk.Combobox(self.aw, state='disabled', textvariable= self.incName)
		self.e.grid()
		Tk.Button(self.aw, text="Add", command=self.wireAddComplete).grid()
		self.outdName.trace('w', lambda *a, b = self.b: self.setM(i = self.outdName.get(), o = b)) #self.setOutC)
		self.indName.trace('w', lambda *a, b = self.e: self.setM(i = self.indName.get(), o = b))#self.setInC)
	
	def wireAddComplete(self):
		KEYS, VALUES = self.getKeys()
			
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		objIn = KEYS[VALUES.index(self.indName.get())]
		objOut = KEYS[VALUES.index(self.outdName.get())]

		self.core.addWire(objIn, self.incName.get(), objOut, self.outcName.get())
		self.updateWindowTitle()

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
		#self.mName.trace('w', self.setM2)
		Tk.Button(self.aw, text="Delete", command=self.wireDelComplete).grid()

	def wireDelComplete(self):
		KEYS, VALUES = self.getKeys()
			
		obj = KEYS[VALUES.index(self.cName.get())]

		self.core.deleteWire(obj, self.mName.get())
		self.updateWindowTitle()
		self.redraw()
		self.aw.destroy()
		pass
		
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

	def setM(self, *what, **kwargs):
		#print(what)
		#print(kwargs)
		kwargs['o']["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(kwargs['i'])]
		ii = self.core.dia.getDevice(obj).connectors.keys()
		
		kwargs['o']["values"]=list(ii)
				
	def redraw(self):
		d = self.core.dia
		
		self.canvas.delete("all")
		for i in d.listDevices():
			if (i in d.locs):
				aa = d.objMk(self.canvas, d.getDevice(i), d.locs[i])
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
				r = self.canvas.create_line(st,fn, fill="black")
		
	def export_png(self):
		files = [#('All Files', '*.*'), 
			 ('Portable Network Graphics', '*.png')]
		file = Tk.filedialog.asksaveasfile(filetypes = files, defaultextension = files)
		
		if (file is not None):
			self.core.dia.exportPng().save(file.name)
		#print(file)
		
	def file_load(self):
		if (self.core.struct.is_changed()):
			a = Tk.messagebox.askyesnocancel(title="Unsaved Changed", message="There are unsaved changes. Save before load?")
			#print(a)
			if (a is None):
				return None
			elif (a is True):
				self.file_save()


		files = [#('All Files', '*.*'), 
			 ('Databases', '*.db')]
		a = Tk.filedialog.askopenfile(filetypes = files, defaultextension = files)
	
		# This is literally the new code
		if (a is None):
			print("Cancelled?")
		else:
			a = a.name
			self.core.open_file(a)
			self.redraw()
			self._open_file = a
			self.core.struct.clear_changed()
			self.canvas.config(scrollregion=(self.core.dia.bounds))
			self.updateWindowTitle()
			
		pass
	
	def updateWindowTitle(self):
		title = self.app_name
		if (self._open_file is not None):
			title += " [" + self._open_file 
			if (self.core.struct.is_changed()):
				title += "*"
			title += "]"
		self.window.title(title)
		
	def file_new(self):
		if (self.core.struct.is_changed()):
			a = Tk.messagebox.askyesnocancel(title="Unsaved Changed", message="There are unsaved changes. Save before clearing?")
			#print(a)
			if (a is None):
				return None
			elif (a is True):
				self.file_save()


		files = [#('All Files', '*.*'), 
			 ('Databases', '*.db')]
	
		a = Tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files)
		if (len(a) == 0):
			print("Cancelled?")
		else:
			self._open_file = a
			self.core.open_file(a)
			self.redraw()
			self.updateWindowTitle()
			self.core.struct.clear_changed()
			
			#print("Yes")
		#print(type(a), a)
