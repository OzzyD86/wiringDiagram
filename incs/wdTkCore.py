#import tkinter as Tk
#import tkinter.ttk as ttk
#from incs.wdCore import wdCore
#from widgets.connector_points import connector_points
#from widgets.EntryWidget import EntryWidget, ComboEntryWidget, SpinEntryWidget
import tkinter.messagebox

from widgets.inputDialog import inputDialog, inputDialog2, inputDialog3

class wdTkCore():
	
	# === Device Adding
	
	def devAddWin(self, event = None):
		d = getattr(event, "x", 0)

		self.aw = inputDialog(self.window, data={
			"mName": {
				"type" : "Entry",
				"name" : "New Machine Name",
			},
			"hName": {
				"type" : "Entry",
				"name" : "Human Name",
			},
			"x": {
				"type" : "Entry",
				"name" : "X Position",
				"value": getattr(event, "x", 300)
			},
			"y": {
				"type" : "Entry",
				"name" : "Y Position",
				"value": getattr(event, "y", 300)
			},
		})
		self.aw.addButton("Add", "add")
		self.aw.passFunc("add", self.devAddComplete)

	def devAddComplete(self, **kwargs):
		if (kwargs['mName'] in self.core.dia.listDevices()):
			tkinter.messagebox.showerror(title="Cannot add device", message="The name of the device is already in use.")
			return False
		
		self.core.addDevice(
			kwargs['mName'], kwargs['hName'],
			(int(kwargs['x']),int(kwargs['y']),50,50))
		
		self.updateWindowTitle()		
		self.redraw()
		return True
		
	# == Device Editing
	
	def devEditWin(self):
		if (len(self.core.dia.listDevices())== 0):
			Tk.messagebox.showerror(title="No devices", message="There are no devices to edit.")
			return False
		
		self.aw = inputDialog2(self.window, data={
			"mName":{
				"type" : "Combo",
				"name": "Edit Machine",
				"values": self.core.dia.listDevices(True),
				"onUpdate": self.setmName2,
			},
			"top": {
				"type": "Entry", "name": "Top"
			},
			"left": {
				"type": "Entry", "name": "Left"
			},
			"width": {
				"type": "Entry", "name": "Width"
			},
			"height": {
				"type": "Entry", "name": "Height"
			}
		})
		self.aw.addButton("Edit", "edit")
		self.aw.passFunc("edit", self.devEditComplete)

	def devEditComplete(self, **kwargs):
		p = self.core.dia.listDevices(True)
	
		if (kwargs['mName'] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to edit.")
			return False
		
		obj = list(p.keys())[list(p.values()).index(kwargs["mName"])]
		
		self.core.updateDevice(obj,
			(int(kwargs['left']),
			int(kwargs['top']), 
			int(kwargs['width']), 
			int(kwargs['height']))
		)
		self.canvas.config(scrollregion=(self.core.dia.bounds))
		self.updateWindowTitle()

		self.redraw()
		return True
		
	# == Device Deleting
	
	def devDelWin(self):
		if (len(self.core.dia.listDevices())== 0):
			tkinter.messagebox.showerror(title="No devices", message="There are no devices to delete.")
			return False
			
		self.aw = inputDialog2(self.window, data={
			"dhName":{
				"type" : "Combo",
				"name": "Edit Machine",
				"values": self.core.dia.listDevices(True),
				#"onUpdate": self.setmName2,
			},
			"lb": {
				"type": "Label",
				"text": "Deleting a device will not remove its plugs or any connected wires from the database. They will simply not be shown",
			}
		})
		self.aw.addButton("Delete", "delete")
		self.aw.passFunc("delete", self.devDelComplete)

	def devDelComplete(self, **kwargs):
		p = self.core.dia.listDevices(True)
	
		if (kwargs['dhName'] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to delete.")
			return False
		
		obj = list(p.keys())[list(p.values()).index(kwargs["dhName"])]
	
		self.core.deleteDevice(obj)
		self.updateWindowTitle()

		self.redraw()
		self.aw.destroy()
		return True

	## === Plug Management
	
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

	def connAddComplete(self, **kwargs):
		p = self.core.dia.listDevices(True)
	
		if (kwargs['mhName'] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to edit.")
			return False
		
		obj = list(p.keys())[list(p.values()).index(kwargs["mhName"])]

		if (kwargs['cName'] in self.core.dia.getDevice(obj).connectors.keys()):
			Tk.messagebox.showerror(title="Cannot add plug", message="The name of the plug is already in use for this device.")
			return False
		
		if (int(kwargs['val']) == 1):
			self.core.addConnector(obj, kwargs['cName'], dir= kwargs['ddName'])
		elif (int(kwargs['val']) > 1):
			for i in range(int(kwargs['val'])):
				self.core.addConnector(obj, kwargs['cName']+"_"+str(i+1), dir= kwargs['ddName'])
		else:
			Tk.messagebox.showerror(title="Cannot add plug", message="Invalid value.")
			return False
		
		self.updateWindowTitle()

		self.redraw()
		return True

	# == Plug Deleting
	
	def getPlugs(self, *args, **kwargs):
	
		p = self.core.dia.listDevices(True)
	
		if (args[2] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to delete.")
			return False
		
		obj = list(p.keys())[list(p.values()).index(args[2])]

		ii = self.core.dia.getDevice(obj).connectors.keys()

		args[0].data['outcName']['obj'].setValues(list(ii)) # Could be prettier?
		args[0].data['outcName']['values'] = list(ii)
		
	def connDelWin(self):
		self.aw = inputDialog2(self.window, data= {
			"outdName": {
				"type" : "Combo",
				"name": "Machine Name",
				"values": self.core.dia.listDevices(True),
				"onUpdate": self.getPlugs
			},

			"outcName": {
				"type" : "Combo",
				"name": "Connection Name",
				"values": {},
			},
		})
		self.aw.addButton("Delete", "delete")
		self.aw.passFunc("delete", self.connDelComplete)		
	
	def connDelComplete(self, **kwargs):
		p = self.core.dia.listDevices(True)
	
		if (kwargs['outdName'] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to delete.")
			return False
		
		objIn= list(p.keys())[list(p.values()).index(kwargs['outdName'])]
		
		self.core.deleteConnector(objIn, kwargs['outcName'])
		
		self.updateWindowTitle()		
		self.redraw()
		return True

	## === Wire Management
	
	# == Add a wire
	
	def getPlugsForDev(self, win, val, *args, **kwargs):
		print(win, val, args, kwargs)
		rep = val[0]["target"]
		if (rep == "outcName"):
			d = win.data["outdName"]["obj"].get_key_of_value(args[0])
			#win.data["outcName"]["obj"]., 
			win.data['outcName']['obj'].setValues(list(self.core.dia.getDevice(d).connectors.keys())) # Could be prettier?
			win.data['outcName']['values'] = list(self.core.dia.getDevice(d).connectors.keys())
			#Tk.messagebox.showerror(args, d)
		elif (rep == "incName"):
			d = win.data["indName"]["obj"].get_key_of_value(args[0])
			#win.data["outcName"]["obj"]., 
			win.data['incName']['obj'].setValues(list(self.core.dia.getDevice(d).connectors.keys())) # Could be prettier?
			win.data['incName']['values'] = list(self.core.dia.getDevice(d).connectors.keys())
			#Tk.messagebox.showerror(args, d)
	
			pass
		else:
			Tk.messagebox.showerror(val[0]["target"], args)

	def wireAddWin(self):
		self.aw = inputDialog3(self.window, data={
			"outdName" : {
				"type":"Combo",
				"name":"Output Device Name",
				"values": self.core.dia.listDevices(True),
				"onUpdate": self.getPlugsForDev,
				"updateVars": [{"target" : "outcName"}]
			},
			"outcName" : {
				"type":"Combo",
				"name":"Output Connector Name",
				"values": {},
			},
			"indName" : {
				"type":"Combo",
				"name":"Output Device Name",
				"values": self.core.dia.listDevices(True),
				"onUpdate": self.getPlugsForDev,
				"updateVars": [{"target" : "incName"}]
			},
			"incName" : {
				"type":"Combo",
				"name":"Output Connector Name",
				"values": {},
			}
		})
		self.aw.addButton("Add", "add")
		self.aw.passFunc("add", self.wireAddComplete)

	def wireAddComplete(self, **kwargs):
		KEYS, VALUES = self.getKeys()
		
		#print(self.indName.get(), self.incName.get(),
		#	self.outdName.get(), self.outcName.get())
		if (kwargs["indName"] not in KEYS):
			tkinter.messagebox.showwarning(title="Cannot select device", message="Please select a valid output device.")
			return

		if (kwargs["outdName"] not in KEYS):
			tkinter.messagebox.showwarning(title="Cannot select device", message="Please select a valid input device.")
			return
		
		objIn = kwargs["indName"]
		objOut = kwargs["outdName"]
		#return False
		
		self.core.addWire(objOut, kwargs["outcName"], objIn, kwargs["incName"])
		self.updateWindowTitle()

		self.redraw()
		return True

	## === Waypointing

	# == Adding
	
	def waypointAddWin(self):
		self.aw = inputDialog3(self.window, data={
			"wName": {
				"type": "Entry",
				"name": "Waypoint name"
			},
			"top": {
				"type": "Entry",
				"name": "Waypoint top position"
			},
			"left": {
				"type": "Entry",
				"name": "Waypoint left position"
			},
		})
		self.aw.addButton("Add", "add")
		self.aw.passFunc("add", self.waypointAddComplete)

	def waypointAddComplete(self, **kwargs):
		for i in self.core.dia.wp.values():
			if (kwargs['wName'] == i["name"]):
				tkinter.messagebox.showerror(title="Cannot add waypoint", message="The name of the waypoint is already in use.")
				return False
		
		self.core.addWaypoint(
			kwargs['wName'],
			(int(kwargs['left']),int(kwargs['top'])))
		
		self.updateWindowTitle()		
		self.redraw()
		return True

	# == Editing
	
	def setwName(self, win, val, *nope):
		
		obj = win.data['wName']['obj'].get_key_of_value(nope[0])
		
		d = self.core.dia.wp[obj]

		win.set("top", int(d['loc'][1]))
		win.set("left", int(d['loc'][0]))
		
	def waypointEditWin(self):
		#if (len(self.core.dia.listDevices())== 0):
		#	tkinter.messagebox.showerror(title="No devices", message="There are no devices to edit.")
		#	return False
		
		VALUES = {}
		for i,j in self.core.dia.wp.items():
			VALUES[i] = j["name"]

		self.aw = inputDialog3(self.window, data={
			"wName": {
				"type": "Combo",
				"name": "Edit Waypoint",
				"values" : VALUES,
				"onUpdate": self.setwName
			},
			"top": {
				"type": "Entry",
				"name" : "Top position",
			},
			"left": {
				"type": "Entry",
				"name" : "Left position",
			}

		})
		self.aw.addButton("Edit", "edit")
		self.aw.passFunc("edit", self.waypointEditComplete)
		
	def waypointEditComplete(self, **kwargs):
		obj = kwargs['wName']

		print(self.core.updateWaypoint(obj, (int(kwargs['left']), int(kwargs['top']))))
		
		self.canvas.config(scrollregion=(self.core.dia.bounds))
		self.updateWindowTitle()

		self.aw.destroy()
		self.redraw()

	# == Delete Waypoint 
	
	def waypointDelWin(self):
		#if (len(self.core.dia.listDevices())== 0):
		#	tkinter.messagebox.showerror(title="No devices", message="There are no devices to delete.")
		#	return False
		VALUES = {}
		for i,j in self.core.dia.wp.items():
			VALUES[i] = j["name"]
			
		self.aw = inputDialog3(self.window, data={
			"wpName": {
				"type":"Combo",
				"name":"Waypoint Name",
				"values": VALUES
			},
			"delRel": {
				"type":"Checkbox",
				"name":"Delete associated paths"
			}
		})
		self.aw.addButton("Delete", "del")
		self.aw.passFunc("del", self.waypointDelComplete)

	def waypointDelComplete(self, **kwargs):
		
		obj = kwargs["wpName"]
		#Tk.messagebox.showerror(obj, obj)
		
		self.core.deleteWaypoint(obj)
		self.updateWindowTitle()

		self.redraw()
		return True
		
	# == Add wire to waypoint
	
	def help(self, *args, **kwargs): #Not a helpful name!!
		st = "START"
		en = "END"
		stpos = 1
		out = {}
		p = args[0].data["wire"]["obj"].get_key_of_value(args[2]) # That's prettier
		if (p in self.core.dia.cwps):
			for i in self.core.dia.cwps[p]:
				out[stpos] = "(" + str(stpos) + ") " + str(st) + " -> " + str(i)
				st = i
				stpos += 1

		out[stpos] = "(" + str(stpos) + ") " + str(st) + " -> " + str(en)
		print(list(out.values()))
		args[0].data["pos"]["obj"].setValues(out)
		args[0].data["pos"]["values"] = out
		#print("I run here?")
		#self.cb_pos.setState("readonly")
		
	def routeAddWin(self):
		VALUES = {}
		for i,j in self.core.dia.conns.items():
			VALUES[i] = "(" + str(i) + "), Connecting " + j[0][0] + " via " + j[0][1] + " to " + j[1][0] + " via " + j[1][1]
	
		#Tk.messagebox.showerror("", self.core.dia.wp)
		self.aw = inputDialog3(self.window, data={
			"wire": {
				"type": "Combo",
				"name": "Select Wire",
				"values": VALUES,
				"onUpdate": self.help
			},
			"wpn": {
				"type":"Combo",
				"name":"Select Waypoint",
				"values": self.core.dia.wp
			},
			"pos" : {
				"type":"Combo",
				"name":"Position",
				"values": []
			},
		})
		self.aw.addButton("Add", "add")
		self.aw.passFunc("add", self.routeAddComplete)

	# == Delete waypoint wire mapping
	
	def routeAddComplete(self, **kwargs):
		
		wire = int(kwargs["wire"]) # So much prettier!
		wpn = str(kwargs["wpn"])
		ord = int(kwargs["pos"]) # Update with prettier way>

		self.core.dia.addConnectionWaypoint(
			int(wire),
			int(wpn),
			int(ord)
		)
		self.core.struct.cur.execute("update wp_ls set ord = ord + 1 where wire_id = ? and ord >= ?",
			(wire, ord)
		)

		self.core.struct.cur.execute("insert into wp_ls (wire_id, wp_id, ord) values (?,?,?)",
			(wire, wpn, ord)
		)
		
		self.updateWindowTitle()
		self.core.struct.set_changed()
		self.redraw()
		return True

	def getWps(self, win, val, *args, **kwargs):
		print(win, val, args, kwargs)
		o = None
		for i,j in self.core.dia.conns.items():
			if (args[0] == ("(" + str(i) + "), Connecting " + j[0][0] + " via " + j[0][1] + " to " + j[1][0] + " via " + j[1][1])):
				o = i
		
		if (o is not None):
			win.data['wp']['obj'].setValues(self.core.dia.cwps[o]) # Could be prettier?
			win.data['wp']['values'] = self.core.dia.cwps[o]

		print(o)
			
	def routeDelWin(self):
		VALUES = {}
		for i,j in self.core.dia.conns.items():
			VALUES[i] = "(" + str(i) + "), Connecting " + j[0][0] + " via " + j[0][1] + " to " + j[1][0] + " via " + j[1][1]

		self.aw = inputDialog3(self.window, data={
			"wire": {
				"type": "Combo",
				"name": "Wire",
				"values": VALUES,
				"onUpdate" : self.getWps
			},
			"wp" : {
				"type": "Combo",
				"name": "Waypoint",
				"values" : {}
			}
		})
		self.aw.addButton("Delete", "del")
		self.aw.passFunc("del", self.routeDelComplete)
			
	def routeDelComplete(self, **kwargs):
		print(kwargs)

		r = []
		rem = None
		
		for i in self.core.dia.cwps[kwargs['wire']]:
			if (str(i) == kwargs['wp']):
				print("added",i)
				r.append(i)
			else:
				rem = i['wpid']
				print("skipped",i)

		print(r)

		if (rem is not None):
			self.core.dia.cwps[kwargs['wire']] = r
				
			self.core.struct.cur.execute("delete from wp_ls where wire_id = ? and wp_id =?",
				(kwargs['wire'],rem)
			)

		self.core.struct.set_changed()
		self.updateWindowTitle()
		self.redraw()
		return True
