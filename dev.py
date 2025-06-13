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