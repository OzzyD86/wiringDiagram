from copy import copy
from PIL import Image, ImageDraw
import math as maths

def drag_start(event):
	widget = event.widget
	widget._drag_start_x = event.x
	widget._drag_start_y = event.y
	print("Yes?")

def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

from diagramStructure import diagramStructure

class diagram():
	
	def __init__(self):
		self.dev = {}
		self.conns = []
		self.locs = {}
		
	def addDevice(self, key, dev):
		self.dev[key] = dev
		pass
		
	def listDevices(self):
		return list(self.dev.keys())
	
	def locateDevice(self, dName, pos = (0,0), sz = (50,50)):
		self.locs[dName] = (*pos, *sz)
		#print(self.locs)
		
	def getDevice(self, key):
		try:
			return self.dev[key]
		except:
			return None
			
	def addConnection(self, a, b):
		if (a[0] not in self.dev):
			return False
		
		if (b[0] not in self.dev):
			return False
			
		_out = self.dev[a[0]]
		_in = self.dev[b[0]]
		
		if (not a[1] in _out.connectors ):
			return False

		if (not b[1] in _in.connectors):
			return False
		
		_out.connectors[a[1]]["connected"] = b
		_in.connectors[b[1]]["connected"] = a
		
		self.conns.append((a,b))
		
	def load(self, resource):
		for i in resource.cur.execute("select * from units"):
		#print(dict(i))
			self.addDevice(i['iName'], device(i['proName']))
			if (i["left"] is not None):
				self.locateDevice(i["iName"], (i["left"],i["top"]),(i["width"],i["height"]))

		for i in resource.cur.execute("select * from conns order by `dName` ASC, direction DESC"):#, cName asc"):
			#print(dict(i))
			dv = self.getDevice(i["dName"])
			if (dv is not None):
				dv.addConnector(i["cName"], proto="XLR", direction=i["direction"])
			else:
				print("Connection called for", i["cName"],"on",i["dName"],"which does not exist.")
				pass
				
		for i in resource.cur.execute("select * from wire"):
			self.addConnection(
				(i["devOut"], i["ConnOut"]),
				(i["devIn"], i["ConnIn"])
			)
		pass
		
def check_current_version():
	return 1
	
class device():
	def __init__(self, name):
		self.name = name
		self.connectors = {}
		
	def addConnector(self, key, proto = None, direction = None):
		self.connectors[key] = {
			"proto": proto,
			"direction": direction,
			"connected": None
		}
		pass

f = diagramStructure("f.db")
print(f.check_version())
if (f.check_version() < check_current_version()):
	print("Update needed")
	f.update_version(f.check_version(), check_current_version())
#exit(1)
#f.build()
d = diagram()
d.load(f)

from colours import colourDirection
	
im = Image.new("RGB", (800,600), (255,255,255))
dr = ImageDraw.Draw(im)

def objMk(dr, p, dms = (0,0,1,1), _type = 1):
	poss = { "left": [], "right": [], "top": [], "bottom" : [] }

	if (type(dr) is ImageDraw.ImageDraw):
		a = 1
	elif (type(dr) is Tk.Canvas):
		a = 2
	else:
		#print(type(dr))
		raise Exception("Unplacable")
	
	if (_type in [0, 1]):
		if (_type == 0):
			ct = 0
			nat = ["left", "right"]
			for i in p.connectors.keys():
				poss[nat[ct%2]].append(i)
				ct+=1
			#print(poss)

		if (_type == 1):
			ct = 0
			nat = ["left", "right"]
			for i in p.connectors.keys():
				if (p.connectors[i]['direction'] in ["In", "in"]):
					poss["left"].append(i)
				elif (p.connectors[i]['direction'] in ["Out", "out"]):
					poss["right"].append(i)
				else:
					poss[nat[ct%2]].append(i)
					ct+=1
			#print(poss)
		
	else:
		pass

	outmap = {}
	
	for fa, fb in poss.items():
		tt = (0,0)
		#print(fa)
		ln = len(fb)
		#print(ln)
		ct = 0
		if (fa in ["left", "top"]):
			os = (- (dms[2]/2)-2.5, - (dms[3]/2)-2.5)
		elif (fa in ["right"]):
			os = ((dms[2]/2)+2.5, - (dms[3]/2))
		elif (fa in ["bottom"]):
			os = (-(dms[2]/2), (dms[3]/2)+2.5)
		else:
			os = (0,0)
			
		for fc in fb:
			if (fa in ["left", "right"]):
				os = (os[0], (-dms[3] /2) + ((ct+1) / (ln+1) * dms[3]))
			if (fa in ["top", "bottom"]):
				os = ((-dms[2] /2) + ((ct+1) / (ln+1) * dms[2]), os[1])
			lf = dms[0] + os[0]
			tp = dms[1] + os[1]

			c = colourDirection(p.connectors[fc]["direction"], a==2)

			if (a==1):
				dr.rectangle((lf-2.5, tp-2.5, lf + 2.5, tp+2.5), outline=c)
			elif (a==2):
				dr.create_rectangle(lf-2.5, tp-2.5, lf + 2.5, tp+2.5, outline=c)
			
			print(p)
			ct += 1
			outmap[fc] = (lf,tp)

	if (a==1):
		dr.rectangle(
			(dms[0]-(dms[2]/2), dms[1] - (dms[3]/2),
			dms[0]+(dms[2]/2), dms[1] + (dms[3]/2)),
			outline=(0,0,0)
		)
	elif (a == 2):
		rct = dr.create_rectangle(
			dms[0]-(dms[2]/2), dms[1] - (dms[3]/2),
			dms[0]+(dms[2]/2), dms[1] + (dms[3]/2),
			outline="black"
		)
		dr.create_text(dms[0],dms[1],text=p.name,font=('Arial',4))
		#dr.tag_bind(rct, "<Button-1>", drag_start)
		#dr.tag_bind(rct, "<B1-Motion>", drag_motion)

	return outmap

# Any reason why I'm doing this here?
#for i in d.listDevices():
#	if (i in d.locs):
#		aa = objMk(dr, d.getDevice(i), d.locs[i])
#	d.getDevice(i).drwConnPos = aa

import tkinter as Tk
import tkinter.ttk as ttk

class wdCore():
	def __init__(self, x):
		self.dia = diagram()
		self.struct = None #diagramStructure()
		
		# Right-o! Let's set up a canvas ... but here?!
		self.canvas = Tk.Canvas(x, width=800, height=600)
		self.canvas.grid()

	def importStruct(self, struct):
		self.struct = struct

class wdTk():
	def __init__(self):
		self.window = Tk.Tk()
		self.window.title("WiringDiagram")
		self.core = wdCore(self.window)
		
		self.menu = {
			"root" : Tk.Menu(),
			"file": Tk.Menu(),
			"add": Tk.Menu()
		}
	
		add = self.menu["add"]
		add.add_command(label="Device", command=self.devAddWin)
		add.add_command(label="Plug", command=self.connAddWin)
		add.add_command(label="Connection", command=self.wireAddWin)

	def file_save(self):
		f.store.commit() # That needs moving
	
	def devAddComplete(self):
		if (self.mName.get() in d.listDevices()):
			tkinter.messagebox.showerror(title="Cannot add device", message="The name of the device is already in use.")
			return False
			
		self.core.struct.cur.execute("insert into units (iName, proName, left, top, width, height) values(?, ?,?,?,?,?)", 
			(self.mName.get(), self.hName.get(),
			400,300,50,50))
		d.addDevice(self.mName.get(), device(self.hName.get()))
		#if (i["left"] is not None):
		d.locateDevice(self.mName.get(), (400,300),(50, 50))

		self.aw.destroy()
		redraw()
		pass
	
	def getKeys(self):
		KEYS = []
		VALUES = []
		for i in d.listDevices():
			KEYS.append(i)
			VALUES.append(i + " (" + i + ")")
		return (KEYS, VALUES)
		
	def devDelComplete(self):
		
		# Load the objects
		KEYS, VALUES = self.getKeys()
			
		# Find the object
		if not self.dhName.get() in VALUES:
			tkinter.messagebox.showerror(title="No device", message="No.")
			return False
			
		obj = KEYS[VALUES.index(self.dhName.get())]
		print(obj)
		
		if (self.core.struct is not None):
			# Delete the object
			self.core.struct.cur.execute("delete from units where iName = ?", (obj,))
			#self.core.struct.store.commit() # Don't do that here
	
			# Delete its connectors
			# Delete any wires relating to it
		
		#print("m:",self.mName.get())
		#print("dh:", self.dhName.get())
		del d.dev[obj]
		redraw()
		self.aw.destroy()
		pass
		
	def devAddWin(self):
		self.aw = Tk.Tk()
		self.mName = Tk.StringVar(self.aw)
		self.hName = Tk.StringVar(self.aw)
		Tk.Label(self.aw, text="Machine Name").grid()
		Tk.Entry(self.aw, textvariable= self.mName).grid()
		Tk.Label(self.aw, text="Human Name").grid()
		Tk.Entry(self.aw, textvariable= self.hName).grid()
		Tk.Button(self.aw, text="Add", command=self.devAddComplete).grid()

	def devEditComplete(self):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.mName.get())]
		d.locateDevice(obj, (int(self.left.get(), 10),
			int(self.top.get())), 
			(int(self.width.get()), 
			int(self.height.get())))
		self.core.struct.cur.execute("update units set top = ?, left = ?, width = ?, height = ? WHERE `iName` = ?",
			(self.top.get(), self.left.get(), self.width.get(), self.height.get(), obj))

		self.aw.destroy()

		redraw()
	
	def devEditWin(self):
		if (len(d.listDevices())== 0):
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

	def setmName(self, *nope):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.mName.get())]
		left, top, width, height = d.locs[obj]
		self.top.set(top)
		self.left.set(left)
		self.width.set(width)
		self.height.set(height)
		#print(d.locs)
		
	def devDelWin(self):
		if (len(d.listDevices())== 0):
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

	def connAddComplete(self):
		KEYS, VALUES = self.getKeys()
	
		obj = KEYS[VALUES.index(self.mhName.get())]
		if (self.cName.get() in d.getDevice(obj).connectors.keys()):
			tkinter.messagebox.showerror(title="Cannot add plug", message="The name of the plug is already in use for this device.")
			return False
		self.core.struct.cur.execute("insert into conns (dName, cName) values(?, ?)", (obj, self.cName.get()))
		d.getDevice(obj).addConnector(self.cName.get(), proto="XLR")
		redraw()
		self.aw.destroy()
		
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

	def setInC(self, *what):
		self.e["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		
		obj = KEYS[VALUES.index(self.indName.get())]
		ii = d.getDevice(obj).connectors.keys()
		#print(ii)
		
		self.e["values"]=list(ii)

	def setM(self, *what, **kwargs):
		#print(what)
		print(kwargs)
		self.b["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		
		obj = KEYS[VALUES.index(kwargs['i'])]
		ii = d.getDevice(obj).connectors.keys()
		
		kwargs['o']["values"]=list(ii)
		
	def setOutC(self, *kwargs):

		#print(what)
		self.b["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		
		obj = KEYS[VALUES.index(self.outdName.get())]
		ii = d.getDevice(obj).connectors.keys()
		
		self.b["values"]=list(ii)
		
	def wireAddComplete(self):
		KEYS, VALUES = self.getKeys()
			
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		objIn = KEYS[VALUES.index(self.indName.get())]
		objOut = KEYS[VALUES.index(self.outdName.get())]

		self.core.struct.cur.execute("insert into wire (devIn,connIn,devOut,connOut) values (?,?,?,?)",
			(objIn, self.incName.get(),
			objOut, self.outcName.get()))
			
		d.addConnection(
				(objIn, self.incName.get()),
				(objOut, self.outcName.get())
			)
		redraw()
		self.aw.destroy()
	
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

	def wireDelComplete(self):
		KEYS, VALUES = self.getKeys()
			
		obj = KEYS[VALUES.index(self.cName.get())]
	
		print(obj, self.mName.get())
		self.core.struct.cur.execute("delete from wire where DevOut = ? and ConnOut = ?",
			(obj, self.mName.get()))
		self.core.struct.cur.execute("delete from wire where DevIn = ? and ConnIn = ?",
			(obj, self.mName.get()))
		redraw()
		self.aw.destroy()
		pass
		
	def setM2(self, *args):
		pass
		
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

	def file_new(self):
		a = tkinter.filedialog.asksaveasfilename()
		if (len(a) == 0):
			print("Cancelled?")
		else:
			global f,t,d
			f = diagramStructure(a)
			f.build()
			self.dia = d = diagram()
			d.load(f)
			self.core.importStruct(f)
			redraw()
			print("Yes")
		#print(type(a), a)
		
def redraw():
	wdc.canvas.delete("all")
	for i in d.listDevices():
	#print(i)
		if (i in d.locs):
			aa = objMk(wdc.canvas, d.getDevice(i), d.locs[i])
			d.getDevice(i).drwConnPos = aa

	for i in d.conns:
		p =0
		pin = None
		pout = None
		if (d.getDevice(i[0][0]) is not None):
			pin = d.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
		else:
			p+=1
			print("oops")
			
		if (d.getDevice(i[1][0]) is not None):
			pout = d.getDevice(i[1][0]).connectors[i[1][1]]["direction"]
		else:
			p+=1
			print("oops")
			
		if (pin == pout):
			if (pin is not None):
				print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
		
		if (p ==0):
			st = d.getDevice(i[0][0]).drwConnPos[i[0][1]]
			fn =  d.getDevice(i[1][0]).drwConnPos[i[1][1]]
			#dr.line((st,fn), fill=(0,0,0))
			r = wdc.canvas.create_line(st,fn, fill="black")
		#else:
		print(pin, pout)
		
t = wdTk()

t.core.importStruct(f)

x = t.window
y = t.menu["root"]
x.config(menu=y)
wdc = t.core

redraw()

for i in d.conns:
	pin = d.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
	pout = d.getDevice(i[1][0]).connectors[i[1][1]]["direction"]

	if (pin == pout):
		if (pin is not None):
			print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
			
	st = d.getDevice(i[0][0]).drwConnPos[i[0][1]]
	fn =  d.getDevice(i[1][0]).drwConnPos[i[1][1]]
	dr.line((st,fn), fill=(0,0,0))
	#wdc.canvas.create_line(st,fn, fill="black")

import tkinter.filedialog
	
mf = t.menu["file"]
mf.add_command(label="New", command= t.file_new)
mf.add_separator()
mf.add_command(label="Save", command= t.file_save)

edit = Tk.Menu()
edit.add_command(label="Device", command=t.devEditWin)
edit.add_command(label="Plug", state=Tk.DISABLED)
edit.add_command(label="Connection", state=Tk.DISABLED)

delete = Tk.Menu()
delete.add_command(label="Device", command=t.devDelWin)
delete.add_command(label="Plug", state=Tk.DISABLED)
delete.add_command(label="Connection", command=t.wireDelWin)

y.add_cascade(label="File", menu=mf)
y.add_cascade(label="Add", menu=t.menu["add"])
y.add_cascade(label="Edit", menu=edit)
y.add_cascade(label="Delete", menu=delete)
x.mainloop()
im.save("mx.png")