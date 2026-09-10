import tkinter as Tk
import tkinter.ttk as ttk
from incs.wdCore import wdCore
from widgets.connector_points import connector_points
from widgets.EntryWidget import EntryWidget, ComboEntryWidget, SpinEntryWidget
import tkinter.messagebox

from widgets.inputDialog import inputDialog, inputDialog2

from incs.wdTkCore import wdTkCore

class wdTk(wdTkCore):
	def resize_canvas(self, event):
   
		new_width = event.width
		new_height = event.height

		# Update the canvas size
		self.canvas.config(width=new_width, height=new_height)

	def click_call(self, event):
		pass
		
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
		self.canvas.bind("<Button-3>", self.click_call)
		#self.window.bind('<Configure>', self.resize_canvas)
	
		self.menu = {
			"root" : Tk.Menu(),
			"file": Tk.Menu(),
			"add": Tk.Menu(),
			"edit": Tk.Menu(),
			"delete": Tk.Menu(),
			"export": Tk.Menu()
		}
		self.sc = Tk.IntVar()
		self.sc.set(1)
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
		add.add_command(label="Waypoint", command = self.waypointAddWin)
		add.add_command(label="Waypoint Connector", command=self.routeAddWin)
	
		edit = self.menu["edit"]
		edit.add_command(label="Device", command=self.devEditWin)
		edit.add_command(label="Plug", state=Tk.DISABLED)
		edit.add_command(label="Connection", state=Tk.DISABLED)
		edit.add_command(label="Waypoint", command=self.waypointEditWin)
		edit.add_command(label="Waypoint Connector", state=Tk.DISABLED)
	
		delete = self.menu["delete"]
		delete.add_command(label="Device", command=self.devDelWin)
		delete.add_command(label="Plug", command=self.connDelWin)
		delete.add_command(label="Connection", command=self.wireDelWin)
		delete.add_command(label="Waypoint", command= self.waypointDelWin)
		delete.add_command(label="Waypoint Connector", command=self.routeDelWin)
	
		self.waypointing = Tk.BooleanVar()
		self.waypointing.set(True)
		self.waypointing.trace('w', self.set_export_vars)
		self.wp_labels = Tk.BooleanVar()
		self.wp_labels.set(False)
		self.wp_labels.trace('w', self.set_export_vars)
		self.conn_labelling = Tk.BooleanVar()
		self.conn_labelling.set(False)
		self.conn_labelling.trace('w', self.set_export_vars)
		self.core.dia.conn_labelling.trace('w', self.set_export_vars)
		
		self.scale = Tk.Menu()
		self.scale.add_checkbutton(label="1x", onvalue=1,variable=self.sc)
		self.scale.add_checkbutton(label="2x", onvalue=2,variable=self.sc)
		self.sc.trace('w', self.set_export_vars)
		
		#self.wp_labelling = False
		self.menu["export"].add_checkbutton(label="Honour waypoints", onvalue=True, offvalue=False, variable=self.waypointing)
		self.menu["export"].add_checkbutton(label="Show waypoint labels", onvalue=True, offvalue=False, variable=self.wp_labels)
		self.menu["export"].add_checkbutton(label="Show connector labels", onvalue=True, offvalue=False, variable=self.conn_labelling)
		self.menu["export"].add_cascade(label="Scale...", menu= self.scale)
		self.menu["export"].add_separator()
		self.menu["export"].add_command(label="PNG", command=self.export_png)

		y = self.menu["root"]
		y.add_cascade(label="File", menu=self.menu["file"])
		y.add_cascade(label="Add", menu=self.menu["add"])
		y.add_cascade(label="Edit", menu=self.menu["edit"])
		y.add_cascade(label="Delete", menu=self.menu["delete"])
		y.add_cascade(label="Export", menu=self.menu["export"])

		self.window.config(menu=self.menu["root"])
	
	def set_export_vars(self, *args, **kwargs):
		self.core.dia.waypointing = self.waypointing
		self.core.dia.wp_labelling = self.wp_labels
		self.core.dia.conn_labelling = self.conn_labelling
		self.redraw()
		
	def open_file(self, file):
		self.core.open_file(file)
		self._open_file = file
		self.canvas.config(scrollregion=(self.core.dia.bounds))
		self.set_export_vars()
		self.updateWindowTitle()
		
	def quit(self):
		if (self.core.struct.is_changed()):
			a = Tk.messagebox.askyesnocancel(title="Unsaved Changes", message="There are unsaved changes. Save before closing?")
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
			q = self.core.dia.dev[i].name
			KEYS.append(i)
			VALUES.append(q + " (" + i + ")")
		return (KEYS, VALUES)
	
	## === Do Device Management
	
	# == Device Adding

	def dupDevAddWin(self):
		self.aw = Tk.Toplevel()

		KEYS, VALUES = self.getKeys()

		self.dName = Tk.StringVar(self.aw)
		self.mName = Tk.StringVar(self.aw)
		self.hName = Tk.StringVar(self.aw)
	
		ComboEntryWidget(self.aw, text="Existing machine to duplicate", variable=self.dName, values=VALUES).grid()
		#Tk.Label(self.aw, text="Existing machine to duplicate").grid()
		#a = ttk.Combobox(self.aw, state='readonly', textvariable= self.dName, values=VALUES).grid()

		EntryWidget(self.aw, text="New Machine Name", variable=self.mName).grid()
		EntryWidget(self.aw, text="Human Name", variable=self.hName).grid()

		Tk.Button(self.aw, text="Add", command=self.dupDevAddComplete).grid()

	def dupDevAddComplete(self):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.dName.get())]
		
		if (self.mName.get() in self.core.dia.listDevices()):
			Tk.messagebox.showerror(title="Cannot add device", message="The name of the device is already in use.")
			return False
		
		d = self.core.dia.getDevice(obj)
		s = self.core.dia.locs[obj]
		
		self.core.addDevice(
			self.mName.get(), self.hName.get(),
			(400,300,s[2],s[3]))
		
		for i, j in d.connectors.items():
			self.core.addConnector(self.mName.get(), i, dir=  j['direction'])

		self.updateWindowTitle()		
		self.aw.destroy()
		self.redraw()

	def alert(self, *args, **kwargs): # For inputDialog testing purposes only. Please don't use for else (oh unless you want to print kwargs and print a warning) and remove after
		Tk.messagebox.showwarning("Button pressed", "Yes. This is triggered")
		print(args, kwargs)
	
	def example(self, win, val, *args, **kwargs):
		print(win, val, args, kwargs)
		Tk.messagebox.showerror(args, kwargs)

	def file_save(self):
		self.core.struct.store.commit() # That needs moving
		self.core.struct.clear_changed()
		self.updateWindowTitle()
		pass
		
	## === Do Plug Management
	
	# == Plug Adding
	
	def connAddWin(self):
		self.aw = inputDialog2(self.window, data={
			"mhName": {
				"type" : "Combo",
				"name": "Machine Name",
				"values": self.core.dia.listDevices(True),
			},
			"cName": {
				"type": "Entry",
				"name": "Connection Name"
			},
			"ddName": {
				"type": "Combo",
				"name": "Data Direction",
				"values": {"None" : "None", "In": "In", "Out":"Out","Both":"Both" },
			},
			"val" :{
				"type":"Spin",
				"name":"Quantity"
			}
		})
		self.aw.addButton("Add", "add")
		self.aw.passFunc("add", self.connAddComplete)

		#KEYS, VALUES = self.getKeys()
		self.val = Tk.IntVar(self.aw)
		#self.cName = Tk.StringVar(self.aw)
		#self.mhName = Tk.StringVar(self.aw)
		#self.ddName = Tk.StringVar(self.aw)
		#self.ddName.set("None")
		
		#ComboEntryWidget(self.aw, text="Machine Name", variable=self.mhName, values=VALUES).grid()		

		#EntryWidget(self.aw, text="Connection Name", variable=self.cName).grid()

		#ComboEntryWidget(self.aw, text="Data Direction", variable=self.ddName, values=["In", "Out", "Both", "None"]).grid()		
		
		#SpinEntryWidget(self.aw, text="Quantity", min=1, max=32, variable=self.val).grid()
		
		#Tk.Button(self.aw, text="Add", command=self.connAddComplete).grid()

	def connAddComplete(self):
		KEYS, VALUES = self.getKeys()
		if not self.mhName.get() in VALUES:
			Tk.messagebox.showerror(title="No device", message="No.")
			return False
			
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
		
	# == Connection Deleting
	
	def connDelWin(self):
		self.aw = Tk.Tk()
		KEYS, VALUES = self.getKeys()
	
		self.outdName = Tk.StringVar(self.aw)
		self.outcName = Tk.StringVar(self.aw)

		self.b = ComboEntryWidget(self.aw, text="Connection Name", variable=self.outcName)#.grid()	# I have to set it up first because it's called, but drawn later!

		ComboEntryWidget(self.aw, text="Machine Name", variable=self.outdName, values=VALUES, command= lambda *a, b = self.b.box: self.setM(i = self.outdName.get(), o = b)).grid()
		
		#Tk.Label(self.aw, text="Machine Name").grid()
		#a = ttk.Combobox(self.aw, state='readonly', textvariable= self.outdName, values=VALUES).grid()
		
		#Tk.Label(self.aw, text="Connection Name").grid()
		#self.b = ttk.Combobox(self.aw, state='disabled', textvariable= self.outcName)
		self.b.grid()
		
		Tk.Button(self.aw, text="Delete", command=self.connDelComplete).grid()
		#self.outdName.trace('w', lambda *a, b = self.b: self.setM(i = self.outdName.get(), o = b)) #self.setOutC)
		#self.indName.trace('w', lambda *a, b = self.e: self.setM(i = self.indName.get(), o = b))#self.setInC)
	
	def connDelComplete(self):
		KEYS, VALUES = self.getKeys()
			
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		objIn = KEYS[VALUES.index(self.outdName.get())]

		self.core.deleteConnector(objIn, self.outcName.get())
		
		#self.core.addWire(objOut, self.outcName.get(), objIn, self.incName.get())
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

		aa = ComboEntryWidget(self.aw, text="Output Connection Name", state='disabled', variable=self.outcName)

		ComboEntryWidget(self.aw, text="Output Machine Name", variable=self.outdName, values=VALUES, 
			command = lambda *a, b = aa.box: self.setM(i = self.outdName.get(), o = b)).grid()
		aa.grid()

		bb = ComboEntryWidget(self.aw, text="Output Machine Name", state='disabled', variable=self.incName)

		ComboEntryWidget(self.aw, text="Input Machine Name", variable=self.indName, values=VALUES, 
			command = lambda *a, b = bb.box: self.setM(i = self.indName.get(), o = b)).grid()			
		bb.grid()
				
		Tk.Button(self.aw, text="Add", command=self.wireAddComplete).grid()
	
	def wireAddComplete(self):
		KEYS, VALUES = self.getKeys()
			
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		if (self.indName.get() not in VALUES):
			tkinter.messagebox.showwarning(title="Cannot select device", message="Please select a valid output device.")
			return
			
		if (self.outdName.get() not in VALUES):
			tkinter.messagebox.showwarning(title="Cannot select device", message="Please select a valid input device.")
			return
			
		objIn = KEYS[VALUES.index(self.indName.get())]
		objOut = KEYS[VALUES.index(self.outdName.get())]

		self.core.addWire(objOut, self.outcName.get(), objIn, self.incName.get())
		self.updateWindowTitle()

		self.redraw()
		self.aw.destroy()

	# = Wire Deleting
	
	def wireDelWin(self):
		self.aw = Tk.Toplevel()
		KEYS, VALUES = self.getKeys()
		
		self.a = connector_points(self.aw, self.core.dia)
		self.a.pass_machines(self.getKeys()).go().grid(sticky="news")
		Tk.Button(self.aw, text="Delete", command=self.wireDelComplete).grid(sticky='swen')
		self.aw.columnconfigure(0, weight=1)
		#self.mName.trace('w', self.setM2)

	def wireDelComplete(self):
		KEYS, VALUES = self.getKeys()
		
		o = self.a.get()
		#Tk.messagebox.showerror("", o[2]["values"][0])

		obj = KEYS[VALUES.index(o[0])]
		#Tk.messagebox.showerror("Yes", o)

		#self.core.deleteWire(obj, o[1])
		self.core.deleteWireByID(int(o[2]["values"][0]))
		self.updateWindowTitle()
		self.redraw()
		self.aw.destroy()
		pass
	
	## === Waypoint management
	
	# == Adding
	
	def waypointAddWin(self):
		self.aw = Tk.Tk()
		self.wName = Tk.StringVar(self.aw)
		self.top = Tk.IntVar(self.aw)
		self.left = Tk.IntVar(self.aw)
		
		EntryWidget(self.aw, text="Waypoint Name", variable=self.wName).grid()
		EntryWidget(self.aw, text="Top position", variable=self.top).grid()
		EntryWidget(self.aw, text="Left position", variable=self.left).grid()
		Tk.Button(self.aw, text="Add", command=self.waypointAddComplete).grid()

	def waypointAddComplete(self):
		for i in self.core.dia.wp.values():
			if (self.wName.get() == i["name"]):
				tkinter.messagebox.showerror(title="Cannot add waypoint", message="The name of the waypoint is already in use.")
				return False
		
		self.core.addWaypoint(
			self.wName.get(),
			(self.left.get(),self.top.get()))
		
		self.updateWindowTitle()		
		self.aw.destroy()
		self.redraw()
	
	# == Editing
	
	def setwName(self, *nope):
		
		obj = self.wName.get()
		#print(obj)
		for i,j in self.core.dia.wp.items():
			if (j["name"] == obj):
				#print(obj, j["name"], i)
				o = i
		d = self.core.dia.wp[o]
		#print(d)
		self.top.set(d["loc"][1])
		self.left.set(d["loc"][0])
		
	def waypointEditWin(self):
		#if (len(self.core.dia.listDevices())== 0):
		#	tkinter.messagebox.showerror(title="No devices", message="There are no devices to edit.")
		#	return False
		VALUES = []
		self.aw = Tk.Tk()
		for i,j in self.core.dia.wp.items():
			VALUES.append(j["name"])
	
		self.top = Tk.StringVar(self.aw)
		self.left = Tk.StringVar(self.aw)
		self.wName = Tk.StringVar(self.aw)
		
		ComboEntryWidget(self.aw, text="Edit Waypoint", variable=self.wName, values=VALUES, 
			command = self.setwName).grid()

		#Tk.Label(self.aw, text="Edit Waypoint").grid()
		#a = ttk.Combobox(self.aw, state='readonly', textvariable= self.wName, values=VALUES).grid()
		
		EntryWidget(self.aw, text="Top position", variable=self.top).grid()
		EntryWidget(self.aw, text="Left position", variable=self.left).grid()

		#self.wName.trace('w',self.setwName)
		Tk.Button(self.aw, text="Edit", command=self.waypointEditComplete).grid()

	def waypointEditComplete(self):
		obj = self.wName.get()

		print(self.core.updateWaypoint(obj, (int(self.left.get()), int(self.top.get()))))
		
		self.canvas.config(scrollregion=(self.core.dia.bounds))
		self.updateWindowTitle()

		self.aw.destroy()
		self.redraw()
	# == Deleting
	
	def waypointDelWin(self):
		#if (len(self.core.dia.listDevices())== 0):
		#	tkinter.messagebox.showerror(title="No devices", message="There are no devices to delete.")
		#	return False
		VALUES = []
		self.aw = Tk.Tk()
		for i,j in self.core.dia.wp.items():
			VALUES.append(j["name"])
			#print(i)

		#self.mName = Tk.StringVar(self.aw)
		self.wpName = Tk.StringVar(self.aw)

		ComboEntryWidget(self.aw, text="Waypoint Name", variable=self.wpName, values=VALUES).grid()

		#Tk.Label(self.aw, text="Waypoint Name").grid()
		#a = ttk.Combobox(self.aw, state='readonly', textvariable= self.wpName, values=VALUES)
		#a.grid()
		
		var = Tk.IntVar()
		Tk.Checkbutton(self.aw, text="Delete associated paths", variable=var, 
			onvalue=1, offvalue=0, state=Tk.DISABLED).grid()
		#Tk.Label(self.aw, text="Human Name").grid()
		#Tk.Entry(self.aw, textvariable= self.hName).grid()
		Tk.Button(self.aw, text="Delete", command=self.waypointDelComplete).grid()

	def waypointDelComplete(self):
		
		# Load the objects
		#KEYS, VALUES = self.getKeys()
		
		# Find the object
		#if not self.dhName.get() in VALUES:
		#	tkinter.messagebox.showerror(title="No device", message="No.")
		#	return False
			
		obj = self.wpName.get()
		
		self.core.deleteWaypoint(obj)
		self.updateWindowTitle()

		self.redraw()
		self.aw.destroy()
		pass
	
	## === Routing management
	
	# == Add Route
	def setRoute(self, *args, **kwargs):
		#print(self.core.dia.cwps)
		p = {0: "Insert at beginning" }
		if (int(self.wire.get()) in self.core.dia.cwps):
			for i in self.core.dia.cwps[int(self.wire.get())]:
				p[i["order"]] = "Insert after " + str(i["wpid"])
		else:
			print("Blank")
		self.b['state']='readonly'
		self.b["values"] = list(p.values())
	
	def help(self, *args, **kwargs):
		st = "START"
		en = "END"
		stpos = 1
		out = {}
		
		p = self.w.get_key_of_value(args[1].get()) # That's prettier
		if (p in self.core.dia.cwps):
			for i in self.core.dia.cwps[p]:
				out[stpos] = "(" + str(stpos) + ") " + str(st) + " -> " + str(i)
				st = i
				stpos += 1

		out[stpos] = "(" + str(stpos) + ") " + str(st) + " -> " + str(en)
		print(list(out.values()))
		self.cb_pos.setValues(list(out.values()))
		#print("I run here?")
		self.cb_pos.setState("readonly")
		
	def routeAddWin(self):
		self.aw = Tk.Toplevel(self.window)
		VALUES = {}
		
		for i,j in self.core.dia.conns.items():
			print(i,j)
			VALUES[i] = "(" + str(i) + "), Connecting " + j[0][0] + " via " + j[0][1] + " to " + j[1][0] + " via " + j[1][1]
		#KEYS, VALUES = self.getKeys()
	
		self.wire = Tk.StringVar(self.aw)
		self.pos = Tk.StringVar(self.aw)
		self.wpn = Tk.StringVar(self.aw)

		self.cb_pos = ComboEntryWidget(self.aw, text="Position", state='disabled', variable=self.pos)

		self.w = ComboEntryWidget(self.aw, text="Select Wire Id", variable=self.wire, values=VALUES,
			command = lambda *a : self.help("update", self.wire))
		self.w.grid(sticky='news', padx =5)
		self.aw.columnconfigure(0, weight = 1)

		p = []
		for i,j in self.core.dia.wp.items():
			p.append(j)

		ComboEntryWidget(self.aw, text="Select Waypoint", variable=self.wpn, values=p).grid(sticky='news', padx=5)
		
		self.cb_pos.grid(sticky='swen')
		
		Tk.Button(self.aw, text="Add", command=self.routeAddComplete).grid()
		
	def routeAddComplete(self):
		print(self.wpn.get())
		
		wire = int(self.wire.get().strip("(").split(")")[0]) # We NEED a prettier way of doing this!
#		print("wp:",wp)
		for i,j in self.core.dia.wp.items():
			if (self.wpn.get() == str(j)):
				wpn = i
				print("i:",i)
			else:
				print(i,j)
		q = self.core.struct.cur.execute(
			"select max(ord) as o from wp_ls where wire_id = ?",
			(wire,)
		)
		r = q.fetchone()
		s = dict(r)
		
		ord = int(self.pos.get().strip("(").split(")")[0]) # Update with prettier way>

		self.core.dia.addConnectionWaypoint(
			wire,
			wpn,
			ord
		)
		self.core.struct.cur.execute("update wp_ls set ord = ord + 1 where wire_id = ? and ord >= ?",
			(wire, ord)
		)

		self.core.struct.cur.execute("insert into wp_ls (wire_id, wp_id, ord) values (?,?,?)",
			(wire, wpn, ord)
		)
		pass
		
		'''KEYS, VALUES = self.getKeys()
			
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		objIn = KEYS[VALUES.index(self.indName.get())]
		objOut = KEYS[VALUES.index(self.outdName.get())]

		self.core.addWire(objIn, self.incName.get(), objOut, self.outcName.get())'''
		self.updateWindowTitle()
		self.core.struct.set_changed()
		self.redraw()
		self.aw.destroy()
	
	def getRoutes(self):
		p = {}
		for i,j in self.core.dia.cwps.items():
			for k in j:
				p[i,k["wpid"], k["order"]] = str((i,k["wpid"]))
		return p
	
	def routeDelWin(self):
		self.aw = Tk.Tk()
		
		VALUES = list(self.getRoutes().values())
		print(self.getRoutes().values())
		#KEYS, VALUES = self.getKeys()
	
		self.rName = Tk.StringVar(self.aw)

		ComboEntryWidget(self.aw, text="Select Wire Id", variable=self.rName, values=VALUES).grid()
		
		#Tk.Label(self.aw, text="select wire id").grid()
		#a = ttk.Combobox(self.aw, state='readonly', textvariable= self.rName, values=VALUES).grid()

		Tk.Button(self.aw, text="Delete", command=self.routeDelComplete).grid()
	
	def routeDelComplete(self):
		q = self.getRoutes()
		KEYS = list(q.keys())
		VALUES = list(q.values())
		#print(list(q.values()))
		p = KEYS[VALUES.index(self.rName.get())]
		print(p)
		
		if (int(p[0]) in self.core.dia.cwps.keys()):
			q = self.core.dia.cwps[int(p[0])]
			r = []
			for i in q:
				#print(i)
				if (i["wpid"] != int(p[1])):
					print("added",i)
					r.append(i)
				else:
					print("skipped",i)
			self.core.dia.cwps[int(p[0])] = r
		else:
			print("no",self.core.dia.cwps)
			
		self.core.struct.cur.execute("delete from wp_ls where wire_id = ? and wp_id =?",
			(p[0],p[1])
		)

		#self.core.addWire(objIn, self.incName.get(), objOut, self.outcName.get())''#'
		self.core.struct.set_changed()
		self.updateWindowTitle()
		self.redraw()
		self.aw.destroy()
	# == Drawing management ==

	def setM(self, *what, **kwargs):
		#print(what)
		#print(kwargs)
		
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(kwargs['i'])]
		ii = self.core.dia.getDevice(obj).connectors.keys()

		print(kwargs['o'])
		if (kwargs['o']["state"] is None):
			# Oh! Then try this:
			kwargs['o'].setState("readonly")
			kwargs['o'].setValues(list(ii))
			print(kwargs['o'])
		else:
			kwargs['o']["state"]='readonly'
			kwargs['o']["values"]=list(ii)
				
	def redraw(self):
		d = self.core.dia
		q = d.bbox()
		q2 = []
		t= 0
		for i in q:
			if (t in [0, 1]):
				a = -10
			else:
				a = 10
			q2.append((i * self.sc.get()) + a)
		
		#q2 = [q2[1], q2[0], q2[3], q2[2]]
		a = d.buildWaypointLists()
		#print(a)
		olines = {}
		self.canvas.delete("all")
		for i in d.listDevices():
			if (i in d.locs):
				aa = d.objMk(self.canvas, d.getDevice(i), d.locs[i])
				d.getDevice(i).drwConnPos = aa

		for k,i in d.conns.items():
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
				n = []
				cs = []
				st = d.getDevice(i[0][0]).drwConnPos[i[0][1]]
				fn =  d.getDevice(i[1][0]).drwConnPos[i[1][1]]
				if (k in d.cwps):
					for l in d.cwps[k]:
						#print(l)
						if (l["wpid"] in d.wp):
							n += d.wp[l["wpid"]]["loc"]
							cs.append(l["wpid"])
							#print(d.wp[l["wpid"]]["loc"])
				#print(n)
			
				if (self.waypointing.get()):
					if (len(cs) > 1):
						#print(cs)
						r = self.canvas.create_line(st,n[0:2], fill="black")
						r = self.canvas.create_line(n[-2:] ,fn, fill="black")
	
						for m in range(len(cs)-1):
							q = (cs[m], cs[m+1])
							#print(q)
							if ((cs[m], cs[m+1]) in olines):
								olines[cs[m], cs[m+1]] += 1
							else:
								olines[cs[m], cs[m+1]] = 1
					else:
						r = self.canvas.create_line(st,n,fn, fill="black")
				else:
					r = self.canvas.create_line(st,fn, fill="black")


		if (self.waypointing.get()):
			for m,n in olines.items():
				self.canvas.create_line(d.wp[m[0]]["loc"], d.wp[m[1]]["loc"], width=n, fill="black")
			#print(m,n)
			
		if (self.wp_labels.get()):
			for i,j in d.wp.items():
				self.canvas.create_text(j["loc"][0],j["loc"][1],text=j["name"],font=('Arial',4))

		#	print(i,j)
		self.canvas.scale("all", 0,0, self.sc.get(), self.sc.get())
		self.canvas.config(scrollregion=(q2))
		
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
			a = Tk.messagebox.askyesnocancel(title="Unsaved Changes", message="There are unsaved changes. Save before clearing?")
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
