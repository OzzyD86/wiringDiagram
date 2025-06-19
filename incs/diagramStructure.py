import sqlite3

class diagramStructure():
	
	def __init__(self, f):
		self._changed = False
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
		
		self.store.execute('''
			create table if not exists config
				(key text unique not null,
				value text)
		''')
		try:
			self.store.execute('''insert into config
					(key, value) VALUES (?,?)
				''', ("version", 1))
		except:
			pass
		self.store.commit()
		
	def check_version(self):
		try:
			p = self.store.execute("Select * from config where key = ?", ("version",))

			pass
		except sqlite3.OperationalError as e:
			self.store.execute('''
				create table if not exists config
				(key text unique not null,
				value text)
			''')
			try:
				self.store.execute('''insert into config
					(key, value) VALUES (?,?)
				''', ("version", 0))
			except:
				pass
			return 0
		
		q = p.fetchone()
		#print(q)
		if (q is None):
			self.store.execute('''insert into config
				(key, value) VALUES (?,?)
			''', ("version", 1))
			return 0

		return int(q["value"])
		
	def update_version(self, _from, _to):
		if (_from < 1 and _to > 0):
			self.store.execute("alter table conns add column draw_position text not null default 'auto'")
			print("Draw position for connectors")
		
			self.store.execute("alter table units add column draw_style text not null default 'auto'")
			print("Draw position for units")
		
			self.store.execute("update config set value = 1 where key = 'version'")
		
		if (_from < 2):
			self.store.execute('''create table if not exists waypoints
				(id integer primary key autoincrement,
				`name` text not null,
				x integer not null,
				y integer not null
				)
			''')
			self.store.execute('''create table if not exists wp_ls
				(wire_id integer not null,
				wp_id integer not null,
				`ord` integer not null,
				primary key (wire_id,ord))
			''')
			self.store.execute("CREATE TABLE tmp AS SELECT * FROM wire")
			self.store.execute("drop TABLE wire")
			self.cur.execute('''
				CREate table if not exists `wire`
					(id integer primary key autoincrement,
					devOut TEXT NOT NULL,
					connOut TEXT NOT NULL,
					devIn TEXT NULL,
					connIn TEXT NULL)
				''')
			self.store.execute('''insert into wire
				(devOut, connOut, devIn, connIn)
				select devOut, connOut, devIn, connIn from tmp''')
		
			self.store.execute("drop TABLE tmp")
		
			self.store.execute("update config set value = 2 where key = 'version'")
		
			print("Draw position for connectors")

		pass

	def is_changed(self):
		return self._changed
		
	def set_changed(self):
		self._changed = True
		
	def clear_changed(self):
		self._changed = False