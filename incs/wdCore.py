from incs.diagram import diagram
from dev import device

class wdCore():
	def __init__(self, x = None):
		self.dia = diagram()
		self.struct = None #diagramStructure()

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
		
	def addDevice(self, hName, mName, coords = (400,300,50,50)):
		self.struct.cur.execute("insert into units (iName, proName, left, top, width, height) values(?, ?,?,?,?,?)", 
			(mName, hName, *coords))
		self.dia.addDevice(hName, device(mName))
		#if (i["left"] is not None):
		self.dia.locateDevice(mName, (coords[0],coords[1]),(coords[2], coords[3]))

	def updateDevice(self, mName, coords):
		self.struct.cur.execute("update units set left = ?, top = ?, width = ?, height = ? WHERE `iName` = ?",
			(*coords, mName))
		self.dia.locateDevice(mName, (
			coords[0], coords[1]), 
			(coords[2], coords[3]))
		pass
	
	def deleteDevice(self, obj):
		if (self.struct is not None):
			# Delete the object
			self.struct.cur.execute("delete from units where iName = ?", (obj,))
	
			# Delete its connectors
			# Delete any wires relating to it

		del self.dia.dev[obj]