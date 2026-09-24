import tkinter as Tk
import tkinter.ttk as ttk
from incs.wdCore import wdCore
from widgets.connector_points import connector_points
from widgets.EntryWidget import EntryWidget, ComboEntryWidget, SpinEntryWidget
import tkinter.messagebox
import math as maths
from widgets.inputDialog import inputDialog
from incs.wdTkCore import wdTkCore

class wdTk(wdTkCore):
	def resize_canvas(self, event):
   
		new_width = event.width
		new_height = event.height

		# Update the canvas size
		self.canvas.config(width=new_width, height=new_height)

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

	def click_call(self, event):
		pass
	
	def gpw(self, wp1, wp2):
		cd = {}
		for i,j in self.core.dia.cwps.items():
			for k in j:
				if (int(k["wpid"]) == int(wp1)):
					cd[i] = k
		o = {}
		for i in list(cd.keys()):
			for k in self.core.dia.cwps[i]:
				if (int(k["wpid"]) == int(wp2)) and (abs(cd[i]["order"] - k["order"]) == 1):
					o[i] = (min(k["order"], cd[i]["order"]))
					pass
		return o
		pass
		
	def b1_down(self, event):
		self.b1_pressed = event
		
	def b1_up(self, event):
		d = Tk.Menu()
		down = self.b1_pressed
		up = event
		
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		
		up.x = int(self.canvas.canvasx(up.x) / 1)
		up.y = int(self.canvas.canvasy(up.y) / 1)
		down.x = int(self.canvas.canvasx(down.x) / 1)
		down.y = int(self.canvas.canvasy(down.y) / 1)
		
		if (maths.sqrt(pow(down.x-x,2) + pow(down.y-y,2)) < 5):
			click = True
		else:
			click=False
		#print(self.canvas.find_closest(event.x,event.y))
		#print(event)
		#p = copy(event)
		#p.x = x
		#p.y = y
#		d.add_command(label="Create Device here", command= lambda event=event: self.devAddWin(p))
#		d.add_command(label="Create Waypoint here", command= lambda event=event: self.waypointAddWin(p))
	
#		d.add_separator()
		if (self.config.dev.get()):
			d.add_command(label="Start: " + str((down.x, down.y)), state="disabled")
			d.add_command(label="Finish: " + str((up.x, up.y)), state="disabled")
			d.add_separator()
			d.add_command(label="Canvas Start: " + str((self.canvas.canvasx(down.x), self.canvas.canvasy(down.y))), state="disabled")
			d.add_command(label="Canvas Finish: " + str((self.canvas.canvasx(up.x), self.canvas.canvasy(up.y))), state="disabled")
			d.add_separator()
		
#	d.add_command(label=str(self.canvas.find_closest(x,y)))
	
		tags = []
		name = None
		wid = None
		wwis = None
		for i in self.canvas.gettags(self.canvas.find_closest(down.x,down.y)):
			tags.append(i)
			if (self.config.dev.get()):
				d.add_command(label=i)
			if (i.split(":")[0] == "mn"):
				name = i.split(":")[1]
			if (i.split(":")[0] == "wn"):
				name = i.split(":")[1]
			if (i.split(":")[0] == "wid"):
				wid = int(i.split(":")[1])
			if (i.split(":")[0] == "br"):
				wwid = (i.split(":")[1:3])
			if (i.split(":")[0] == "c"):
				conn = i.split(":")[1].split(".")
				
		d.add_separator()
		
		if ("_conn" in tags):
			if ("_conn" in self.canvas.gettags(self.canvas.find_closest(up.x, up.y))):
				if (not click):
					for i in self.canvas.gettags(self.canvas.find_closest(up.x, up.y)):
						if (i.split(":")[0] == "c"):
							conn2 = i.split(":")[1].split(".")
				
					d.add_command(label="Create connection", command= lambda : self.wireAddComplete(indName=conn2[0], incName = conn2[1], outdName = conn[0], outcName = conn[1]))
		
		if ("_dev" in tags):
			if (not click):
				d.add_command(label="Move device here", command= lambda : self.contextDevMove(name,int(up.x/self.sc.get()),int(up.y/self.sc.get())))
				d.add_command(label="Duplicate device here...", command= lambda : self.dupDevAddWin(dName=name, top=int(up.y/self.sc.get()), left=int(up.x/self.sc.get())))
				p = self.canvas.gettags(self.canvas.find_closest(up.x, up.y))
				if ("_dev" in p):
					iName = None
					for i in p:
						if (i.split(":")[0] == "mn"):
							iName = i.split(":")[1]
					d.add_command(label="Make connection between devices", command= lambda : self.wireAddWin(outdName=name, indName=iName))
				elif ("_conn" in p):
					iName, con = None, None
					for i in p:
						if (i.split(":")[0] == "c"):
							iName, con = i.split(":")[1].split(".")
					d.add_command(label="Connect here from this device", command= lambda : self.wireAddWin(outdName=name, indName=iName, incName = con))
	
			else:
				d.add_command(label="Edit device...", command = lambda dName=name: self.devEditWin(mName=dName))
				d.add_command(label="Delete device", command= lambda : self.devDelComplete(dhName=name))
		
				pass
		if ("_wp" in tags):
			if (not click):
				d.add_command(label="Move waypoint", command= lambda : self.waypointEditComplete(wName=int(name),left=int(up.x/self.sc.get()),top=int(up.y/self.sc.get())))
			else:
				det = Tk.Menu()
				#det.lift()
				d.add_command(label="Delete waypoint", command= lambda : self.waypointDelComplete(wpName=int(name), delRel = True))
				for k,i in self.core.dia.cwps.items():
					for j in i:
						if (int(j["wpid"]) == int(name)):
							d.add_command(label="Wire " + str(k), command= lambda k=int(k),j=j : self.routeDelComplete(wire=k, wp = j))
				#d.add_cascade(label = "Detach...", menu=det)
		if ("_wire" in tags):
			if (wid is not None):
				d.add_command(label="Delete wire " + str(wid), command= lambda event=event: self.wireDelComplete(wid))
	
			p = self.canvas.gettags(self.canvas.find_closest(up.x, up.y))
			if ("_wp" in p):
				pt = None
				br = None
				for i in p:
					if (i.split(":")[0] == "wn"):
						pt = i.split(":")[1]
					
				if ("wp_bridge" in tags):
					if (wwid is not None):
						e = self.gpw(wwid[0], wwid[1])
						for i,j in e.items():
							d.add_command(label="Connect wire " + str(i) + " to waypoint " + str(pt) +" at order "+str(j+1), command= lambda pt=pt,wid=i,o=j+1 : self.routeAddComplete(wire=wid, wpn=pt, pos=o))
		
				if ("BEGIN" in tags):
					if (pt is not None):
						d.add_command(label="Connect wire " + str(wid) + " to waypoint " + str(pt), command= lambda event=event: self.routeAddComplete(wire=wid, wpn=pt, pos=1))
				elif ("END" in tags):
					ord = 0
					for i in self.core.dia.cwps[wid]:
						if (i["order"] > ord):
							ord = i["order"]
							
					d.add_command(label="Connect wire " + str(wid) + " to waypoint " + str(pt), command= lambda event=event: self.routeAddComplete(wire=wid, wpn=pt, pos=ord+1))

				elif ("straight_line" in tags):
					if (pt is not None):
						d.add_command(label="Connect wire " + str(wid) + " to waypoint " + str(pt), command= lambda event=event: self.routeAddComplete(wire=wid, wpn=pt, pos=1))
		if (click):
			d.add_command(label="Create Device here", command= lambda event=event: self.devAddWin(up))
			d.add_command(label="Create Waypoint here", command= lambda event=event: self.waypointAddWin(up))
		
		#d.add_command(label= d.keys())
		d.tk_popup(self.canvas.winfo_rootx()+int(event.x/self.sc.get()), self.canvas.winfo_rooty()+int(event.y/self.sc.get()))
		self.b1_pressed = None

	def motion(self, event):
		self.canvas.itemconfig(self.canvas.find_withtag("current"), fill="yellow")
		
	def __init__(self):
		self.app_name = "WiringDiagram"
		self._open_file = None
		
		self.window = Tk.Tk()
		self.pluginLoad()
		
		self.window.title(self.app_name)
		self.core = wdCore(self.window)
		self.window.protocol('WM_DELETE_WINDOW', self.quit)
		self.window.geometry("860x660")
		#frame = Tk.Frame(self.window, height=900,width=700)
		#frame.grid(column=0,row=0)
		self.canvas = Tk.Canvas(self.window, width=800, height=600)
		self.canvas.grid(sticky="news")
		self.canvas.grid_propagate (False)
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
		self.canvas.bind("<Button-1>", self.b1_down)
		self.canvas.bind("<ButtonRelease-1>", self.b1_up)
		#self.canvas.bind("<Motion>", self.motion)
		#self.window.bind('<Configure>', self.resize_canvas)
	
		self.menu = {
			"root" : Tk.Menu(),
			"file": Tk.Menu(),
			"add": Tk.Menu(),
			"edit": Tk.Menu(),
			"delete": Tk.Menu(),
			"export": Tk.Menu(),
			"plugins": Tk.Menu()
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
		
		self.scale = Tk.Menu(self.menu["export"])
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

		for i in self.cueEvts("onMenuSpawn"):
			pass
			self.menu["plugins"].add_cascade(label=i["name"], menu=i["menu"])
			
		y = self.menu["root"]
		y.add_cascade(label="File", menu=self.menu["file"])
		y.add_cascade(label="Add", menu=self.menu["add"])
		y.add_cascade(label="Edit", menu=self.menu["edit"])
		y.add_cascade(label="Delete", menu=self.menu["delete"])
		y.add_cascade(label="Plugins", menu=self.menu["plugins"])
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

	def file_save(self):
		self.core.struct.store.commit() # That needs moving
		self.core.struct.clear_changed()
		self.updateWindowTitle()
		pass
		
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

	def alert(self, *args, **kwargs): # For inputDialog testing purposes only. Please don't use for else (oh unless you want to print kwargs and print a warning) and remove after
		Tk.messagebox.showwarning("Button pressed", "Yes. This is triggered")
		print(args, kwargs)

	'''def example(self, win, val, *args, **kwargs):
		print(win, val, args, kwargs)
		
		Tk.messagebox.showerror(val, args)'''
		
	## === Do Wire Management
	
	# = Wire Deleting
	
	def wireDelWin(self):	# I'm not updating this just yet
		self.aw = inputDialog(self.window, data={
		
		})

		KEYS, VALUES = self.getKeys()
		
		self.a = connector_points(self.aw, self.core.dia)
		self.a.pass_machines(self.getKeys()).go().grid(sticky="news")
		Tk.Button(self.aw, text="Delete", command=self.wireDelComplete).grid(sticky='swen')
		self.aw.columnconfigure(0, weight=1)

	def wireDelComplete(self, id= None):
		KEYS, VALUES = self.getKeys()
		no_draw = False
		if (id is None):
			o = self.a.get()
			#Tk.messagebox.showerror("", o[2]["values"][0])

			#obj = KEYS[VALUES.index(o[0])]
			id = int(o[2]["values"][0])
		else:
			no_draw = True
		#Tk.messagebox.showerror("Yes", o)

		#self.core.deleteWire(obj, o[1])
		self.core.deleteWireByID(int(id))
		self.updateWindowTitle()
		self.redraw()
		if (not no_draw):
			self.aw.destroy()
		pass
	
	## === Waypoint management
			
	## === Routing management
	
	# == Add Route
	def setRoute(self, *args, **kwargs):	## Is this function used?
		#print(self.core.dia.cwps)
		p = {0: "Insert at beginning" }
		if (int(self.wire.get()) in self.core.dia.cwps):
			for i in self.core.dia.cwps[int(self.wire.get())]:
				p[i["order"]] = "Insert after " + str(i["wpid"])
		else:
			print("Blank")
		self.b['state']='readonly'
		self.b["values"] = list(p.values())
	
	def getRoutes(self):
		p = {}
		for i,j in self.core.dia.cwps.items():
			for k in j:
				p[i,k["wpid"], k["order"]] = str((i,k["wpid"]))
		return p
			
	# == Drawing management ==

	def setM(self, *what, **kwargs):
		
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(kwargs['i'])]
		ii = self.core.dia.getDevice(obj).connectors.keys()

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
		self.canvas.delete("_dev")
		self.canvas.delete("_conn")
		for i in d.listDevices():
			if (i in d.locs):
				aa = d.objMk(self.canvas, d.getDevice(i), d.locs[i])
				d.getDevice(i).drwConnPos = aa

		self.canvas.delete("_wire")
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
			
				if (self.waypointing.get()):
					if (len(cs) > 1):
						#print(cs)
						r = self.canvas.create_line(st,n[0:2], fill="green")
						self.canvas.addtag_withtag("_wire", r)
						self.canvas.addtag_withtag("BEGIN", r)
						self.canvas.addtag_withtag("wid:" + str(k), r)
						self.canvas.addtag_withtag(st,r)
						r = self.canvas.create_line(n[-2:] ,fn, fill="green")
						self.canvas.addtag_withtag("_wire", r)
						self.canvas.addtag_withtag("END", r)
						self.canvas.addtag_withtag("wid:" + str(k), r)
						self.canvas.addtag_withtag(st,r)
						for m in range(len(cs)-1):
							q = (cs[m], cs[m+1])
							#print(q)
							if ((cs[m], cs[m+1]) in olines):
								olines[cs[m], cs[m+1]] += 1
							else:
								olines[cs[m], cs[m+1]] = 1
					else:
						
						if (len(n) == 0):
							r = self.canvas.create_line(st,n,fn, fill="black")
							self.canvas.addtag_withtag("_wire", r)
							self.canvas.addtag_withtag("wid:" + str(k), r)
							self.canvas.addtag_withtag("straight_line", r)
						else:
							o = 0
							nn = []
							t = []
							n.append(fn)
							for i in n:
								t.append(i)
								o+=1
								if ((o%2)==0):
									nn.append(tuple(t))
									t= []
							if (len(t) > 0):
								nn.append(t)
							o=0
							for i in nn:
								#s = self.canvas.create_text(250,150,text=n)
								#return
								r = self.canvas.create_line(st,i, fill="black")
								if (o == 0):
									self.canvas.addtag_withtag("BEGIN", r)
								o+= 1
								st = i
								self.canvas.addtag_withtag("_wire", r)
								self.canvas.addtag_withtag("bendy_line", r)
								self.canvas.addtag_withtag(cs, r)
								self.canvas.addtag_withtag("wid:" + str(k), r)
								#self.canvas.addtag_withtag(st, r)
							self.canvas.addtag_withtag("END", r)
				else:
					r = self.canvas.create_line(st,fn, fill="black")
					self.canvas.addtag_withtag("_wire", r)
					#self.canvas.addtag_withtag(m, r)
					#self.canvas.addtag_withtag(st, r)

		if (self.waypointing.get()):
			for m,n in olines.items():
				pass
				r = self.canvas.create_line(d.wp[m[0]]["loc"], d.wp[m[1]]["loc"], width=n, fill="black")
				
				self.canvas.addtag_withtag("_wire", r)
				self.canvas.addtag_withtag("wp_bridge", r)
				self.canvas.addtag_withtag("br:"+str(m[0])+":"+str(m[1]), r)
				self.canvas.addtag_withtag(st, r)
		
		self.canvas.delete("_wp")
		if (self.wp_labels.get()):
			for i,j in d.wp.items():
				r = self.canvas.create_text(j["loc"][0],j["loc"][1],text=j["name"],font=('Arial',4))
				self.canvas.addtag_withtag("_wp", r)
				self.canvas.addtag_withtag("wn:" + str(i), r)
				self.canvas.addtag_withtag(j, r)

		self.canvas.scale("all", 0,0, self.sc.get(), self.sc.get())
		self.canvas.config(scrollregion=(q2))
		
	def export_png(self):
		files = [#('All Files', '*.*'), 
			 ('Portable Network Graphics', '*.png')]
		file = Tk.filedialog.asksaveasfile(filetypes = files, defaultextension = files)
		
		if (file is not None):
			self.core.dia.exportPng().save(file.name)
		
	def updateWindowTitle(self):
		title = self.app_name
		if (self._open_file is not None):
			title += " [" + self._open_file 
			if (self.core.struct.is_changed()):
				title += "*"
			title += "]"
		self.window.title(title)
		
