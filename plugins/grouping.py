from widgets.inputDialog import inputDialog

class grouping():
	def checkInit(self, erm, **kwargs):
		try:
			p = main.core.struct.cur.execute("select * from `group`")
		except:
			main.core.struct.cur.execute("create table `group` (id integer primary key autoincrement, `name` text not null)")
			main.core.struct.cur.execute("create table `group_residents` (id integer primary key autoincrement, `group_id` integer not null, `name` text not null, `type` text not null)")
		
			pass
			
def odc(menu, **kwargs):
	menu.add_separator()
	#tmp = {
	#	"name": kwargs["dev"].name,
	#	"connectors": kwargs["dev"].connectors,
	#	"sz": kwargs["loc"][2:4]
	#}
	menu.add_command(label="Add to group", command = lambda dev=kwargs["dev"].machName: groupAddWin(device=dev))
	menu.add_command(label="Remove from group", command = lambda dev=kwargs["dev"].machName: groupRemComplete(device=dev))
	
	#menu.add_command(label=str(type(core)), command = None, state="disabled")
	return menu

g = grouping()

def groupRemComplete(**kwargs):
	#raise Exception(kwargs)
	e = main.core.struct.cur.execute("delete from group_residents where `name` = ?", (kwargs["device"],))
	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True
	
def devGroupComplete(**kwargs):
	p = main.core.struct.cur.execute("select count(*) from `group` where `name` = ?", (kwargs["group"],))
	if (p.fetchone()[0] == 0):
		e = main.core.struct.cur.execute("insert into `group` (`name`) values (?)", (kwargs["group"],))
	
	e = main.core.struct.cur.execute("insert into `group_residents` (`group_id`, `name`, `type`) select `id`, ?, 'device' from `group` where `name` = ?", (kwargs["device"],kwargs["group"]))

	#raise Exception(kwargs)
	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True
	
def moveGroupId(gid, alter):
	#for i in main.core.dia.listDevices():
	for i in main.core.struct.cur.execute("select `name` from `group_residents` where `type` = 'device' and group_id = ?", (gid,)).fetchall():
		p = main.core.dia.locs[i[0]]
		main.core.dia.locateDevice(i[0],
			(p[0] - alter[0], p[1] - alter[1]),
			(p[2], p[3]))
		#raise Exception(
	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True
	
def checkGroupDrag(self, **kwargs):
	if ("_group" in kwargs["canTags"]):
		id = None
		for i in kwargs["canTags"]:
			if (i.split(":")[0] == "gid"):
				id = i.split(":")[1]
		down = kwargs["down"]
		up = kwargs["up"]
		self.add_command(label="Move group " + str(id) + " here", command = lambda id=id, delta=(down.x-up.x,down.y-up.y) : moveGroupId(id, delta))
	
	return self
	
def redrawCanvas(self, **kwargs):
	self.canvas.delete("_group")
	gps = {}
	for i in main.core.struct.cur.execute("select * from group_residents").fetchall():
		if (i[1] not in gps):
			gps[i[1]] = [None, None, None, None]
		e = main.core.dia.locs[i[2]]
		if (gps[i[1]][0] is None or e[0] - (e[2]/2) < gps[i[1]][0]):
			gps[i[1]][0] = e[0]-1 -(e[2]/2)
		if (gps[i[1]][1] is None or e[1] - (e[3]/2)  < gps[i[1]][1]):
			gps[i[1]][1] = e[1] - (e[3]/2)-1
		if (gps[i[1]][2] is None or e[0] + (e[2]/2) > gps[i[1]][2]):
			gps[i[1]][2] = e[0]+1 +(e[2]/2)
		if (gps[i[1]][3] is None or e[1] + (e[3]/2)> gps[i[1]][3]):
			gps[i[1]][3] = e[1] + (e[3]/2)+1
		#for j in (0,1,2,3):
			
	for i,j in gps.items():
		op = kwargs["canvas"].create_rectangle(j[0], j[1], j[2], j[3], width=5, outline="yellow")
		kwargs["canvas"].addtag_withtag("_group", op)
		kwargs["canvas"].addtag_withtag("gid:"+str(i), op)
		kwargs["canvas"].lower(op)
	pass
	
def groupAddWin(**kwargs):
	#raise Exception(kwargs)
	s = []
	for i in main.core.struct.cur.execute("select `name` from `group`"):
		s.append(i[0])
	d = inputDialog(main, data ={
		"group" : {
			"type" : "Combo",
			"name" : "Group",
			"values" : s,
			"editable" : True,
		}
	})
	d.addButton("Add", "add")
	d.passFunc("add", devGroupComplete, device= kwargs["device"])
		
MANIFEST = {
	"order": 0,
	"events": {
		"onFileLoad": [ g.checkInit ],
		#"onMenuSpawn" : [menu],
		"onDeviceClick": [odc],
		"onGroupDrag": [checkGroupDrag],
		"onCanvasRedraw": [redrawCanvas],
		#""
		#"onAnyClick": [oac],
		#"onDeviceAddDialog" : [devAddWin],
		#"onDeviceEditDialog" : [devAddWin],
		#"onMachineNameSet" : [a]
		
		#"onDeviceAddComplete" : [devAddComplete],
		#"onDeviceEditComplete" : [devAddWin],
	}
}