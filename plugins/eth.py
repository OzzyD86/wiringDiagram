class eth():
	def init(self, **kwargs):
		kwargs['win'].op_config.register("proto", "eth")
		pass
	
	def mns(self, *args, **kwargs):
		print(args)
		mn = (main.core.dia.getDeviceID(kwargs['args'][0]))
		dv = main.core.dia.getDevice(mn)
		
		global internal
		for i in internal:
			kwargs['w'].deleteItem(i)
		internal = []
		
		for i in dv.connectors:
			print(dv.connectors[i])
			if (dv.connectors[i]['proto'] == 'eth'):
				port = ".".join(("conn." + i).split(".")[1:])
				p = main.core.struct.cur.execute("SELECT `data` from `eth_data` where `device` = ? and `conn` = ?", (mn, port))
				p_data = p.fetchone()
				print(p_data)
				if (p_data is not None):
					value = p_data['data']
				else:
					value = ""
				print("Collect " + port + " on object " + mn)
				kwargs['w'].addItem(kwargs['w'].frames["Eth"], "conn." + i, {
					"type": "Entry",
					"name": i,
					"value" : value
				})
				internal.append("conn." + i)
		return {}
	
	def devComplete(**kwargs):
		global internal
		for i in internal:
			port = ".".join(i.split(".")[1:])
			
			print("Add " + kwargs[i] + " to " + port + " on object " + kwargs['mName'])
			p = main.core.struct.cur.execute("REPLACE INTO `eth_data` (`device`, `conn`, `data`) VALUES (?, ?, ?)", (kwargs['mName'], port, kwargs[i]))
			
			pass
		print(kwargs)
		
	def edit(self, **kwargs):
		
		return {
			"Name": "Eth",
			"Widgets" : {
			
			}
		}
		
	def checkFileLoad(self, **kwargs):
		main.core.struct.cur.execute("create table if not exists `eth_data` (`device`	TEXT NOT NULL, 	`conn`	TEXT NOT NULL, `data`	TEXT, PRIMARY KEY(`device`,`conn`))")
			

internal = []
		
MANIFEST = {
	"order": 0,
	"events": {
		"onFileLoad": [ eth.checkFileLoad ],
		"onInitialise": [eth.init],
		"onDeviceEditComplete": [eth.devComplete],
		"onDeviceEditDialog" : [eth.edit],
		"onMachineNameSet" : [eth.mns]
	}
	
}