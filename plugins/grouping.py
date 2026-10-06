from widgets.inputDialog import inputDialog
from PIL import ImageDraw, ImageFont
class grouping():
	def checkInit(self, erm, **kwargs):
		try:
			p = main.core.struct.cur.execute("select * from `group`")
		except:
			main.core.struct.cur.execute("create table `group` (id integer primary key autoincrement, `name` text not null)")
			main.core.struct.cur.execute("create table `group_residents` (id integer primary key autoincrement, `group_id` integer not null, `name` text not null, `type` text not null)")
		
g = grouping()

def model_data_loader():
	s = []
	for i in main.core.struct.cur.execute("select `name` from `group`"):
		s.append(i[0])
	return {
		"group" : {
			"type" : "Combo",
			"name" : "Group",
			"values" : s,
			"editable" : True,
		}
	}
	
### == This does all the device stuff
			
def odc(menu, **kwargs):
	menu.add_separator()
	menu.add_command(label="Add to group", command = lambda dev=kwargs["dev"].machName: groupAddWin(device=dev))
	menu.add_command(label="Remove from group", command = lambda dev=kwargs["dev"].machName: groupRemComplete(device=dev))
	return menu

def groupRemComplete(**kwargs):
	#raise Exception(kwargs)
	e = main.core.struct.cur.execute("delete from group_residents where `name` = ? and `type` = 'device'", (kwargs["device"],))
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
		main.core.updateDevice(i[0],
			(p[0] - alter[0], p[1] - alter[1], p[2], p[3])
		)
		#main.core.dia.locateDevice(i[0],
		#	(p[0] - alter[0], p[1] - alter[1]),
		#	(p[2], p[3]))
		#raise Exception(
	
	for i in main.core.struct.cur.execute("select `name` from `group_residents` where `type` = 'waypoint' and group_id = ?", (gid,)).fetchall():
		p = main.core.dia.wp[int(i[0])]["loc"]
		main.waypointEditComplete(wName=int(i[0]),
			left=int(p[0]-(alter[0]/main.sc.get())),
			top=int(p[1] -(alter[1]/main.sc.get())))
		pass
		
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

def redrawPNG(img, offset=(0,0)):
	l = ImageDraw.Draw(img)
	gps = {}
	gpNames = {}
	for i in main.core.struct.cur.execute("select * from `group`").fetchall():
		gpNames[i[0]] = i[1]
	for i in main.core.struct.cur.execute("select * from group_residents").fetchall():
		if (i[1] not in gps):
			gps[i[1]] = [None, None, None, None]
		if (i[3] == "device"):
			e = main.core.dia.locs[i[2]]
			if (gps[i[1]][0] is None or e[0] - (e[2]/2) < gps[i[1]][0]):
				gps[i[1]][0] = e[0]-1 -(e[2]/2)
			if (gps[i[1]][1] is None or e[1] - (e[3]/2)  < gps[i[1]][1]):
				gps[i[1]][1] = e[1] - (e[3]/2)-1
			if (gps[i[1]][2] is None or e[0] + (e[2]/2) > gps[i[1]][2]):
				gps[i[1]][2] = e[0]+1 +(e[2]/2)
			if (gps[i[1]][3] is None or e[1] + (e[3]/2)> gps[i[1]][3]):
				gps[i[1]][3] = e[1] + (e[3]/2)+1
				
		elif (i[3] == "waypoint"):
			e = main.core.dia.wp[int(i[2])]["loc"]
			if (gps[i[1]][0] is None or e[0] < gps[i[1]][0]):
				gps[i[1]][0] = e[0]-1
			if (gps[i[1]][1] is None or e[1] < gps[i[1]][1]):
				gps[i[1]][1] = e[1] -1
			if (gps[i[1]][2] is None or e[0] > gps[i[1]][2]):
				gps[i[1]][2] = e[0]+1
			if (gps[i[1]][3] is None or e[1] > gps[i[1]][3]):
				gps[i[1]][3] = e[1] +1
			pass
	f = ImageFont.load_default_imagefont()
	for i,j in gps.items():
		x = (j[0]+j[2]-(offset[0]*2)) / 2
		y = (j[1]+j[3]-(offset[1]*2)) / 2
		l.text(
			(x,y), text=gpNames[i], fill=(192,192,0), font = f)
		l.rectangle((j[0]-offset[0],j[1]-offset[1],j[2]-offset[0],j[3]-offset[1]), outline=(192,192,0))
		#op = kwargs["canvas"].create_rectangle(j[0], j[1], j[2], j[3], width=5, outline="yellow")
		#kwargs["canvas"].addtag_withtag("_group", op)
		#kwargs["canvas"].addtag_withtag("gid:"+str(i), op)
		#kwargs["canvas"].lower(op)
	return img
	
def redrawCanvas(self, **kwargs):
	self.canvas.delete("_group")
	gps = {}
	for i in main.core.struct.cur.execute("select * from group_residents").fetchall():
		if (i[1] not in gps):
			gps[i[1]] = [None, None, None, None]
		if (i[3] == "device"):
			e = main.core.dia.locs[i[2]]
			if (gps[i[1]][0] is None or e[0] - (e[2]/2) < gps[i[1]][0]):
				gps[i[1]][0] = e[0]-1 -(e[2]/2)
			if (gps[i[1]][1] is None or e[1] - (e[3]/2)  < gps[i[1]][1]):
				gps[i[1]][1] = e[1] - (e[3]/2)-1
			if (gps[i[1]][2] is None or e[0] + (e[2]/2) > gps[i[1]][2]):
				gps[i[1]][2] = e[0]+1 +(e[2]/2)
			if (gps[i[1]][3] is None or e[1] + (e[3]/2)> gps[i[1]][3]):
				gps[i[1]][3] = e[1] + (e[3]/2)+1
				
		elif (i[3] == "waypoint"):
			e = main.core.dia.wp[int(i[2])]["loc"]
			if (gps[i[1]][0] is None or e[0] < gps[i[1]][0]):
				gps[i[1]][0] = e[0]-1
			if (gps[i[1]][1] is None or e[1] < gps[i[1]][1]):
				gps[i[1]][1] = e[1] -1
			if (gps[i[1]][2] is None or e[0] > gps[i[1]][2]):
				gps[i[1]][2] = e[0]+1
			if (gps[i[1]][3] is None or e[1] > gps[i[1]][3]):
				gps[i[1]][3] = e[1] +1
			pass
		#for j in (0,1,2,3):
			
	for i,j in gps.items():
		op = kwargs["canvas"].create_rectangle(j[0], j[1], j[2], j[3], width=5, outline="yellow")
		kwargs["canvas"].addtag_withtag("_group", op)
		kwargs["canvas"].addtag_withtag("gid:"+str(i), op)
		kwargs["canvas"].lower(op)
	pass
	
def devAddWin(s, **kwargs):
	return { "Name" : "Group",
		"Widgets" : model_data_loader()
	}
	
def groupAddWin(**kwargs):
	#raise Exception(kwargs)
	d = inputDialog(main, data = model_data_loader())
	d.addButton("Add", "add")
	d.passFunc("add", devGroupComplete, device= kwargs["device"])

def devAddComplete(**kwargs):
	if (kwargs["group"] != ""):
		devGroupComplete(group = kwargs["group"], device=kwargs["mName"])
	else:
		groupRemComplete(device=kwargs["mName"])
	return True
	
def devEditVarsPopulate(self, w, val, args):
	p = w.data['mName']["obj"].get_key_of_value(args[0])
	aa = main.core.struct.cur.execute("select a.`name` from `group` a join `group_residents` b on a.id = b.group_id where b.`name` = ? and b.`type` = 'device'", (p,)).fetchone()
	if (aa is not None):
		return {"group":  aa[0]}
	return {"group":""}
	return kwargs

### == This does all the waypoint stuff

def wpEditVarsPopulate(self, w, val, args):
	#raise Exception(self,w,val,args)
	for i,j in self.core.dia.wp.items():
			if j["name"] == args[0]:
				wp = i
	#p = w.data['mName']["obj"].get_key_of_value(args[0])
	aa = main.core.struct.cur.execute("select a.`name` from `group` a join `group_residents` b on a.id = b.group_id where b.`name` = ? and b.`type` = 'waypoint'", (wp,)).fetchone()
	if (aa is not None):
		return {"group":  aa[0]}
	return {"group":""}
	
def waypointAddComplete(**kwargs):
	for j,i in main.core.dia.wp.items():
		if (kwargs['wName'] == i["name"]):
			kwargs["wp"] = j
			break
	#raise Exception(kwargs)
	if (kwargs["group"] != ""):
		wpGroupComplete(group = kwargs["group"], wp=kwargs["wp"])
	else:
		wpGroupRemComplete(wp=kwargs["wp"])
	return True
	
def waypointEditComplete(**kwargs):
	if (kwargs["group"] != ""):
		wpGroupComplete(group = kwargs["group"], wp=kwargs["wName"])
	else:
		wpGroupRemComplete(wp=kwargs["wName"])
	return True
	
def wpGroupRemComplete(**kwargs):
	#raise Exception(kwargs)
	e = main.core.struct.cur.execute("delete from group_residents where `name` = ? and `type` = 'waypoint'", (kwargs["wp"],))
	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True
	
def wpGroupComplete(**kwargs):
	p = main.core.struct.cur.execute("select count(*) from `group` where `name` = ?", (kwargs["group"],))
	if (p.fetchone()[0] == 0):
		e = main.core.struct.cur.execute("insert into `group` (`name`) values (?)", (kwargs["group"],))
	
	e = main.core.struct.cur.execute("insert into `group_residents` (`group_id`, `name`, `type`) select `id`, ?, 'waypoint' from `group` where `name` = ?", (kwargs["wp"],kwargs["group"]))

	#raise Exception(kwargs)
	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True
	
def wpAddComplete(**kwargs):
	if (kwargs["group"] != ""):
		wpGroupComplete(group = kwargs["group"], wp=kwargs["wp"])
	else:
		wpGroupRemComplete(wp=kwargs["wp"])
	return True
	
def wpGroupAddWin(**kwargs):
	#raise Exception(kwargs)
	d = inputDialog(main, data = model_data_loader())
	d.addButton("Add", "add")
	d.passFunc("add", wpAddComplete, wp= kwargs["wp"])

def multiAddWin(**kwargs):
	#raise Exception(kwargs)
	d = inputDialog(main, data = model_data_loader())
	d.addButton("Add", "add")
	d.passFunc("add", multiAddComplete, wp= kwargs["sel"])

def multiAddComplete(wp, **kwargs):
	for i in wp["machs"]:
		devAddComplete(mName=i, **kwargs)
	for i in wp["wps"]:
		waypointEditComplete(wp=i, **kwargs) # That SHOULD work!
		pass
	return True
	
def osmm(menu, **kwargs):
	a = "Group " + str(len(kwargs["sel"]["machs"])) + " devices and "+ str(len(kwargs["sel"]["wps"])) + " waypoints"
	menu.add_command(label=a, command=lambda sel=kwargs["sel"]: multiAddWin(sel = sel))
	return menu
	
def owc(menu, **kwargs):
	menu.add_separator()
	menu.add_command(label="Add to group", command = lambda wp=kwargs["wp"]: wpGroupAddWin(wp=wp))
	menu.add_command(label="Remove from group", command = lambda wp=kwargs["wp"]: wpGroupRemComplete(wp=wp))
	return menu
	
MANIFEST = {
	"order": 0,
	"events": {
		"onFileLoad": [ g.checkInit ],
		#"onMenuSpawn" : [menu],
		#"onDevEditWinPreDef": [devEditVarsPopulate],
		"onMachineNameSet": [devEditVarsPopulate],
		"onDeviceAddDialog" : [devAddWin],
		"onDeviceAddComplete" : [devAddComplete],
		"onDeviceEditDialog" : [devAddWin],
		"onDeviceEditComplete" : [devAddComplete],
		"onDeviceClick": [odc],
		"onWaypointClick": [owc],
		"onUnknownDrag": [checkGroupDrag],
		"onCanvasRedraw": [redrawCanvas],
		
		"onWaypointAddDialog" : [devAddWin],
		"onWaypointAddComplete" : [waypointAddComplete],
		"onWaypointEditDialog" : [devAddWin],
		"onWaypointNameSet": [wpEditVarsPopulate],
		"onWaypointEditComplete" : [waypointEditComplete],
		"onExportPNG": [redrawPNG],
		
		"onSelectionMakeMenu" : [osmm]
		#"onAnyClick": [oac],
		#"onDeviceAddDialog" : [devAddWin],
		#"onDeviceEditDialog" : [devAddWin],
		#"onMachineNameSet" : [a]
		
		#"onDeviceAddComplete" : [devAddComplete],
		#"onDeviceEditComplete" : [devAddWin],
	}
}