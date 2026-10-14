class wire():
	def __init__(self, start_point = None, end_point = None):
		self.start_point = start_point
		self.end_point = end_point
		self.routes = []
		
	def addRoute(self, wp, order = None):
		if (order is None):
			self.routes.append(wp)
		else:
			self.routes.insert(order, wp)
	
	def removeRoute(self, order):
		self.routes.pop(order)
