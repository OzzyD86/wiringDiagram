class loader():
	def __init__(self):
		self.loaders = {}
	
	def is_loaded(self, mod):
		return (mod in list(self.loaders.keys()))
