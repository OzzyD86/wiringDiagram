class grouping():
	def checkInit(self, erm, **kwargs):
		try:
			p = main.core.struct.cur.execute("select * from `groups`")
		except:
			main.core.struct.cur.execute("create table `groups` (id integer primary key autoincrement, `name` text not null, `type` text not null)")
			pass
			
def odc(menu, **kwargs):
	menu.add_separator()
	#tmp = {
	#	"name": kwargs["dev"].name,
	#	"connectors": kwargs["dev"].connectors,
	#	"sz": kwargs["loc"][2:4]
	#}
	menu.add_command(label="Add to group", command = None, state="disabled")
	#menu.add_command(label=str(type(core)), command = None, state="disabled")

	return menu
g = grouping()

MANIFEST = {
	"order": 0,
	"events": {
		"onFileLoad": [ g.checkInit ],
		#"onMenuSpawn" : [menu],
		"onDeviceClick": [odc],
		#"onAnyClick": [oac],
		#"onDeviceAddDialog" : [devAddWin],
		#"onDeviceEditDialog" : [devAddWin],
		#"onMachineNameSet" : [a]
		
		#"onDeviceAddComplete" : [devAddComplete],
		#"onDeviceEditComplete" : [devAddWin],
	}
}