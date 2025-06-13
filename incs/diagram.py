class diagram():
	def __init__(self):
		self.dev = {}
		self.conns = []
		self.locs = {}
		
	def addDevice(self, key, dev):
		self.dev[key] = dev
		
	def listDevices(self):
		return list(self.dev.keys())
	
	def locateDevice(self, dName, pos = (0,0), sz = (50,50)):
		self.locs[dName] = (*pos, *sz)

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