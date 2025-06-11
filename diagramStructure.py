import sqlite3

class diagramStructure():
	
	def __init__(self, f):
		self.store = sqlite3.connect(f)
		self.store.row_factory = sqlite3.Row
		self.cur = self.store.cursor()
		
	def build(self):
		self.cur.execute('''
			CREate table if not exists `units`
				(iName TEXT NOT NULL UNIQUE,
				proName TEXT NOT NULL, 
				top INTEGER DEFAULT 0,
				left INTEGER DEFAULT 0,
				width INTEGER DEFAULT 50,
				height INTEGER DEFAULT 50
				)
		
		''')
		
		self.cur.execute('''
			CREate table if not exists `conns`
				(dName TEXT NOT NULL,
				cName TEXT NOT NULL,
				proto TEXT NULL,
				direction TEXT NULL)
		''')
		
		self.cur.execute('''
			CREate table if not exists `wire`
				(devOut TEXT NOT NULL,
				connOut TEXT NOT NULL,
				devIn TEXT NULL,
				connIn TEXT NULL)
		''')
		self.store.commit()
		pass
