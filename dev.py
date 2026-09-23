class device():
	def __init__(self, machName, name):
		self.machName = machName
		self.name = name
		self.connectors = {}
		
	def addConnector(self, key, proto = None, direction = None):
		self.connectors[key] = {
			"proto": proto,
			"direction": direction,
			"connected": None
		}
		
	def delConnector(self, key):
		if (key in self.connectors):
			del self.connectors[key]
			return True
		return False
		
		pass