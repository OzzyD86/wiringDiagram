import json

class dataWrapper():
	def __init__(self, data = {}):
		self.data = data
	
	def __copy__(self):
		return dataWrapper(copy(self.data))
		
	def get(self):
		return self.data
		
	def set(self, data):
		self.data = data
		
	def load(self, data):
		self.data = json.loads(data)
	
	def save(self):
		return json.dumps(self.data)
