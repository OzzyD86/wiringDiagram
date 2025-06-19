from incs.diagram import diagram
from dev import device
from incs.diagramStructure import diagramStructure

class wdCore():
	
	def __init__(self, x = None):
		self.dia = diagram()
		self.struct = None #diagramStructure()

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
			self.dia.addConnection(
				(i["devOut"], i["ConnOut"]),
				(i["devIn"], i["ConnIn"])
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

	def addWire(self, devIn, conIn, devOut, conOut):
		self.struct.cur.execute("insert into wire (devIn,connIn,devOut,connOut) values (?,?,?,?)",
			(devIn, conIn, devOut, conOut))
			
		self.dia.addConnection(
			(devIn, conIn),
			(devOut, conOut)
		)
		self.struct.set_changed()

	def deleteWire(self, obj, conn):
		self.struct.cur.execute("delete from wire where DevOut = ? and ConnOut = ?",
			(obj, conn))
		self.struct.cur.execute("delete from wire where DevIn = ? and ConnIn = ?",
			(obj, conn))
			
		self.dia.deleteConnection((obj, conn))
		self.struct.set_changed()
