from incs.diagram import diagram
from dev import device
from incs.diagramStructure import diagramStructure

from incs.wire import wire

class wdCore():
	
	def __init__(self, x = None):
		self.dia = diagram()
		self.struct = None #diagramStructure()

		self.waypointing = True
		self.wp_labelling = False
		
	def check_current_version(self):
		return 2
		
	def open_file(self, file):
		
		f = diagramStructure(file)
		f.build()
		if (f.check_version() < self.check_current_version()):
			print("Update needed")
			f.update_version(f.check_version(), self.check_current_version())

		self.dia.clear()
		self.load(f)

		self.importStruct(f)
		f.clear_changed()
		
		pass
		
	def load(self, resource):
		for i in resource.cur.execute("select * from units"):
		#print(dict(i))
			self.dia.addDevice(i['iName'], device(i['proName']))
			if (i["left"] is not None):
				self.dia.locateDevice(i["iName"], (i["left"],i["top"]),(i["width"],i["height"]))

		for i in resource.cur.execute("select * from conns order by `dName` ASC, direction DESC"):#, cName asc"):
			#print(dict(i))
			dv = self.dia.getDevice(i["dName"])
			if (dv is not None):
				dv.addConnector(i["cName"], proto="XLR", direction=i["direction"])
			else:
				print("Connection called for", i["cName"],"on",i["dName"],"which does not exist.")
				pass
				
		for i in resource.cur.execute("select * from wire"):
			print(list(i))
			self.dia.addConnection(i["id"],
				(i["devIn"], i["ConnIn"]),
				(i["devOut"], i["ConnOut"])
			)
			
		for i in resource.cur.execute("select * from waypoints"):
			self.dia.addWaypoint(i["id"], i["name"],
				(i["x"], i["y"])
				#(i["devIn"], i["ConnIn"])
			)
		for i in resource.cur.execute("select * from wp_ls order by wire_id asc, `ord` asc"):
			self.dia.addConnectionWaypoint(
				i["wire_id"], i["wp_id"], i["ord"]
			)
		pass
		
	def importStruct(self, struct):
		self.struct = struct
		
	def addDevice(self, mName, hName, coords = (400,300,50,50)):
		self.struct.cur.execute("insert into units (iName, proName, left, top, width, height) values(?, ?,?,?,?,?)", 
			(mName, hName, *coords))
		self.struct.set_changed()
		self.dia.addDevice(mName, device(hName))
		#if (i["left"] is not None):
		self.dia.locateDevice(mName, (coords[0],coords[1]),(coords[2], coords[3]))

	def updateDevice(self, mName, coords):
		self.struct.cur.execute("update units set left = ?, top = ?, width = ?, height = ? WHERE `iName` = ?",
			(*coords, mName))
		self.dia.locateDevice(mName, (
			coords[0], coords[1]), 
			(coords[2], coords[3]))
		self.struct.set_changed()

		pass
	
	def deleteDevice(self, obj):
		if (self.struct is not None):
			# Delete the object
			self.struct.cur.execute("delete from units where iName = ?", (obj,))
	
			# Delete its connectors
			# Delete any wires relating to it

		del self.dia.dev[obj]
		self.struct.set_changed()
	
	def addConnector(self, obj, cName, proto = "XLR", dir = "auto"):
		self.struct.cur.execute("insert into conns (dName, cName, direction) values(?, ?, ?)", (obj, cName, dir))
		self.dia.getDevice(obj).addConnector(cName, proto, dir)
		self.struct.set_changed()

	def deleteConnector(self, dev, conn):
		self.dia.getDevice(dev).delConnector(conn)
		self.struct.cur.execute("delete from conns where dName = ? and cName = ?", 
			(dev, conn))
			
	def addWire(self, devIn, conIn, devOut, conOut):
		self.struct.cur.execute("insert into wire (devIn,connIn,devOut,connOut) values (?,?,?,?)",
			(devIn, conIn, devOut, conOut))
		#print(self.struct.cur.lastrowid)
		self.dia.addConnection(self.struct.cur.lastrowid, 
			(devIn, conIn),
			(devOut, conOut)
		)
		self.struct.set_changed()

	def deleteWireByID(self, id):
		#raise Exception("Not working yet")
		print(id)
		self.struct.cur.execute("delete from wire where id = ?",
			(id,))
			
		#self.struct.cur.execute("delete from wire where DevIn = ? and ConnIn = ?",
		#	(obj, conn))
			
		self.dia.deleteConnectionByID(int(id))
		self.struct.set_changed()
		
	def deleteWire(self, obj, conn):
		self.struct.cur.execute("delete from wire where DevOut = ? and ConnOut = ?",
			(obj, conn))
		self.struct.cur.execute("delete from wire where DevIn = ? and ConnIn = ?",
			(obj, conn))
			
		self.dia.deleteConnection((obj, conn))
		self.struct.set_changed()
		
	def addWaypoint(self, hName, coords = (50,50)):
		self.struct.cur.execute("insert into waypoints (name, x, y) values(?,?,?)", 
			(hName, *coords))
		self.struct.set_changed()
		k = self.struct.cur.lastrowid
		self.dia.addWaypoint(k, hName, coords)
		return True
		
	def updateWaypoint(self,wid,loc):
		
		for i,j in self.dia.wp.items():
			if (i == wid):
				#print(obj, j["name"], i)
				o = i
				
		if (o not in self.dia.wp):
			return False
			
		d = self.dia.wp[o]
		d['loc'] = (loc)
	
		self.struct.cur.execute("update waypoints set x = ?, y = ? where id = ?",
			(loc[0], loc[1], o)
		)
		return True
		
	def deleteWaypoint(self,wid):
		#for i,j in self.dia.wp.items():
		#	if (j['name'] == wid):
		#		a = i
				
		del self.dia.wp[wid]
		self.struct.cur.execute("delete from waypoints where id = ?", (wid,))
		self.struct.set_changed()
		return True
