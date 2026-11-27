from widgets.inputDialog import inputDialog
from PIL import ImageDraw, ImageFont
from incs.conf.dataWrapper import dataWrapper
from tkinter.messagebox import askquestion
import tkinter.ttk as ttk
from tkinter import DISABLED
import json
import math
import tkinter as Tk
from widgets.InteractiveCanvas import InteractiveCanvas

class grouping():
	def checkInit(self, erm, **kwargs):
		
		try:
			p = main.core.struct.cur.execute("select * from `group`")
		except:
			main.core.struct.cur.execute("create table `group` (id integer primary key autoincrement, `name` text not null)")
			main.core.struct.cur.execute("create table `group_residents` (id integer primary key autoincrement, `group_id` integer not null, `name` text not null, `type` text not null)")
		
		nn = None
		p = main
		for i in  p.winfo_children():
			if (type(i) == ttk.Notebook):
				nn = i

		for i in nn.tabs():
			#nn.tab(i, additional= "none")
			print(nn.tab(i))
			print(nn.tab(i, option="text"))
		
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
	
	e = main.core.struct.cur.execute("delete from `group_residents` where `name` = ? and `type` = 'device'", (kwargs["device"],))
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
			(p[0] - (alter[0]/main.sc.get()), p[1] - (alter[1]/main.sc.get()), p[2], p[3])
		)
	
	errwp = []
	for i in main.core.struct.cur.execute("select `name` from `group_residents` where `type` = 'waypoint' and group_id = ?", (gid,)).fetchall():
		if (int(i[0]) in main.core.dia.wp):
			p = main.core.dia.wp[int(i[0])]["loc"]
			main.waypointEditComplete(wName=int(i[0]),
				left=int(p[0]-(alter[0]/main.sc.get())),
				top=int(p[1] -(alter[1]/main.sc.get())))
		else:
			errwp.append(i[0])
			print("Waypoint " + str(i[0]) + " missing from dialog")
		pass
	
	for i in errwp:
		a = askquestion("Delete waypoint", "Waypoint " + str(i[0]) + " referenced in move but does not exist. Remove from group?")
		if (a == "yes"):
			wpGroupRemComplete(wp = int(i[0]))
	
	for i in main.core.struct.cur.execute("select `name` from `group_residents` where `type` = 'group' and group_id = ?", (gid,)).fetchall():
		moveGroupId(int(i[0]), alter)# pass
		
	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True

def checkMissingWin(id):
	# Get the BBox
	gps = {}
	errwp = []
	
	b = makeBBox(id)
	
	for i in main.core.struct.cur.execute("select * from group_residents where `group_id` = ?", (id,)).fetchall():
		#print(str(i))
		if (i[1] not in gps):
			gps[i[1]] = [None, None, None, None]
		if (i[3] == "device"):
			pass
				
		elif (i[3] == "waypoint"):
			if (int(i[2]) in main.core.dia.wp):
				pass
			else:
				errwp.append(int(i[2]))
	for i in errwp:
		a = askquestion("Delete waypoint", "Waypoint " + str(i) + " referenced in check but does not exist. Remove from group?")
		if (a == "yes"):
			wpGroupRemComplete(wp = int(i))
			
	#print(id, gps[int(id)])
	m = b
	matched = { "dev": [], "wp" : []}
	for i,j in main.core.dia.locs.items():
		if (j[0] >= m[0] and j[0] <= m[2]):
			if (j[1] >= m[1] and j[1] <= m[3]):
				#print("Matched " + str(i))
				matched["dev"].append(i)
	for i,j in main.core.dia.wp.items():
		if (j['loc'][0] >= m[0] and j['loc'][0] <= m[2]):
			if (j['loc'][1] >= m[1] and j['loc'][1] <= m[3]):
				#print("Matched " + str(i))
				matched["wp"].append(i)

	for i in main.core.struct.cur.execute("select * from group_residents").fetchall():
		#print(i[3], i[2], matched)
		
		if (i[3] == "device"):
			if (i[2] in matched["dev"]):
				matched["dev"].remove(i[2])
		elif (i[3] == "waypoint"):
			if (int(i[2]) in matched["wp"]):
				print("yes")
				matched["wp"].remove(int(i[2]))
	print(matched)
	final = {}
	for i, j in matched.items():
		for k in j:
			final[str(i)+"-"+str(k)] = { "type" : i, "name" : k }
	w = dataWrapper(final)
	d = inputDialog(main, data = {
		"connector_context": {
			"name": "Add These",
			"type": "TreeView",
			"headings": { "type":"Type","name":"Name"},
			"onAdd" : [],
			"varStore": w,
			"value": w.get()
		}
	})
	d.addButton("Add", "add")
	d.passFunc("add", multiGroupComplete, group = id )

def multiGroupComplete(**kwargs):
	print(kwargs)
	d = {
		"machs": [],
		"wps" : [],
	}
	for i in kwargs['connector_context'].values():
		if (i['type'] == "wp"):
			d["wps"].append(int(i['name']))
		else:
			d["machs"].append(i['name'])
	
	gn = main.core.struct.cur.execute("select `name` from `group` where `id` = ?", (kwargs['group'],)).fetchone()
	print(gn[0])
	multiAddComplete(d, group = gn[0]) # And if this works, I'll eat my hat!
	return True
	
def checkGroupDrag(self, **kwargs):
	if ("_group" in kwargs["canTags"]):
		id = None
		for i in kwargs["canTags"]:
			if (i.split(":")[0] == "gid"):
				id = i.split(":")[1]
		down = kwargs["down"]
		up = kwargs["up"]
		self.add_command("Groups", label="Move group " + str(id) + " here", command = lambda id=id, delta=(down.x-up.x,down.y-up.y) : moveGroupId(id, delta))
	
	return self

def redrawPNG(img, offset=(0,0)):
	c = {
		0: (192,192,0),
		1: (0,192,0),
		2: (0,0,192),
		3: (192,0,0)
	}
	l = ImageDraw.Draw(img)
	gps = {}
	grp_chk=[]
	gpNames = {}
	grp_level = {}
	for i in main.core.struct.cur.execute("select * from `group`").fetchall():
		gpNames[i[0]] = i[1]
		grp_level[int(i[0])] = 0
	for i in main.core.struct.cur.execute("select * from group_residents").fetchall():
		if (i[1] not in gps):
			gps[i[1]] = [None, None, None, None]
		if (i[3] == "device"):
			if (i[2] in main.core.dia.locs):
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
			if (int(i[2]) in main.core.dia.wp):
				e = main.core.dia.wp[int(i[2])]["loc"]
				if (gps[i[1]][0] is None or e[0] < gps[i[1]][0]):
					gps[i[1]][0] = e[0]-1
				if (gps[i[1]][1] is None or e[1] < gps[i[1]][1]):
					gps[i[1]][1] = e[1] -1
				if (gps[i[1]][2] is None or e[0] > gps[i[1]][2]):
					gps[i[1]][2] = e[0]+1
				if (gps[i[1]][3] is None or e[1] > gps[i[1]][3]):
					gps[i[1]][3] = e[1] +1
		elif (i[3] == "group"):
			grp_chk.append([i[1], i[2]])
		#for j in (0,1,2,3):
	for i in grp_chk:
		#askquestion(i,i)
		p = gps[int(i[0])]
		q = gps[int(i[1])]
		if (q[0] is not None):
			if (p[0] is None or q[0] < p[0]):
				p[0] = q[0]-2
			if (p[1] is None or q[1] < p[1]):
				p[1] = q[1] -2
			if (p[2] is None or q[2] > p[2]):
				p[2] = q[2]+2
			if (p[3] is None or q[3] > p[3]):
				p[3] = q[3] +2
			
			if (grp_level[int(i[1])] >= grp_level[int(i[0])]):
				grp_level[int(i[0])] = grp_level[int(i[1])] + 1
		
	f = ImageFont.load_default_imagefont()
	for i,j in gps.items():
		x = (j[0]+j[2]-(offset[0]*2)) / 2
		y = (j[1]+j[3]-(offset[1]*2)) / 2
		l.text(
			(x,y), text=gpNames[i], fill=c[grp_level[i]], font = f)
		l.rectangle((j[0]-offset[0],j[1]-offset[1],j[2]-offset[0],j[3]-offset[1]), outline=c[grp_level[i]])
		#op = kwargs["canvas"].create_rectangle(j[0], j[1], j[2], j[3], width=5, outline="yellow")
		#kwargs["canvas"].addtag_withtag("_group", op)
		#kwargs["canvas"].addtag_withtag("gid:"+str(i), op)
		#kwargs["canvas"].lower(op)
	return img

def makeBBox(scope, old_scans = []):
	ret = [None, None, None, None]
	
	if (scope in old_scans):
		return False
		
	for i in main.core.struct.cur.execute("select a.* from group_residents a join `group` b on a.group_id = b.id where b.id = ?", (scope,)).fetchall():
		if (i[3] == "device"):
			if (i[2] in main.core.dia.dev):
				e = main.core.dia.locs[i[2]]
				if (ret[0] is None or e[0] - (e[2]/2) < ret[0]):
					ret[0] = e[0]-1 -(e[2]/2)
				if (ret[1] is None or e[1] - (e[3]/2)  < ret[1]):
					ret[1] = e[1] - (e[3]/2)-1
				if (ret[2] is None or e[0] + (e[2]/2) > ret[2]):
					ret[2] = e[0]+1 +(e[2]/2)
				if (ret[3] is None or e[1] + (e[3]/2)> ret[3]):
					ret[3] = e[1] + (e[3]/2)+1
				
		elif (i[3] == "waypoint"):
			if (int(i[2]) in main.core.dia.wp):
				e = main.core.dia.wp[int(i[2])]["loc"]
				if (ret[0] is None or e[0] < ret[0]):
					ret[0] = e[0]-1
				if (ret[1] is None or e[1] < ret[1]):
					ret[1] = e[1] -1
				if (ret[2] is None or e[0] > ret[2]):
					ret[2] = e[0]+1
				if (ret[3] is None or e[1] > ret[3]):
					ret[3] = e[1] +1
			pass
		elif (i[3] == "group"):
			e = makeBBox((i[2]), old_scans + [scope])
			if (e is False):
				return False
			if (ret[0] is None or e[0] <= ret[0]):
					ret[0] = e[0]-2
			if (ret[1] is None or e[1] <= ret[1]):
					ret[1] = e[1] -2
			if (ret[2] is None or e[0] >= ret[2]):
					ret[2] = e[0]+2
			if (ret[3] is None or e[1] >= ret[3]):
					ret[3] = e[1] +2
			
	return ret
	
def redrawCanvas(self, **kwargs):
	self.canvas.delete("_group")
	c = {
		0: "yellow",
		1: "green",
		2: "blue",
		3: "red"
	}
	gps = {}
	grp_level = {}
	grp_chk = []
	gpNames = {}
	if (main.core.struct is None):
		return
		
	for i in main.core.struct.cur.execute("select * from `group`").fetchall():
		gpNames[i[0]] = i[1]
		grp_level[int(i[0])] = 0
	for i in main.core.struct.cur.execute("select a.* from group_residents a join `group` b on a.group_id = b.id").fetchall():
		if (i[1] not in gps):
			gps[i[1]] = [None, None, None, None]
		#nams[i[1]] = i[4]
		if (i[3] == "device"):
			if (i[2] in main.core.dia.dev):
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
			if (int(i[2]) in main.core.dia.wp):
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
		elif (i[3] == "group"):
			grp_chk.append([i[1], i[2]])
		#for j in (0,1,2,3):
	for i in grp_chk:
		#askquestion(i,i)
		p = gps[int(i[0])]
		q = gps[int(i[1])]
		if (q[0] is not None):
			if (p[0] is None or q[0] < p[0]):
				p[0] = q[0]-2
			if (p[1] is None or q[1] < p[1]):
				p[1] = q[1] -2
			if (p[2] is None or q[2] > p[2]):
				p[2] = q[2]+2
			if (p[3] is None or q[3] > p[3]):
				p[3] = q[3] +2
			
			if (grp_level[int(i[1])] >= grp_level[int(i[0])]):
				grp_level[int(i[0])] = grp_level[int(i[1])] + 1
		
	for i,j in gps.items():
		if (j[0] is not None):
			op = kwargs["canvas"].create_rectangle(j[0], j[1], j[2], j[3], width=5, outline=c[grp_level[i]])
			kwargs["canvas"].addtag_withtag("_group", op)
			kwargs["canvas"].addtag_withtag("gid:"+str(i), op)
			kwargs["canvas"].lower(op)
			
			r = kwargs["canvas"].create_text(j[0],j[1],text=gpNames[i],font=('Arial',12),anchor="nw", fill=c[grp_level[i]])
			kwargs["canvas"].addtag_withtag("_group", r)
			kwargs["canvas"].addtag_withtag("gid:" + str(i), r)
			kwargs["canvas"].lower(r)
	
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
	groupRemComplete(device=kwargs["mName"])
	if (kwargs["group"] != ""):
		devGroupComplete(group = kwargs["group"], device=kwargs["mName"])
	#else:
	#	groupRemComplete(device=kwargs["mName"])
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

	wpGroupRemComplete(wp=kwargs["wp"])

	if (kwargs["group"] != ""):
		wpGroupComplete(group = kwargs["group"], wp=kwargs["wp"])
	#else:
	#	wpGroupRemComplete(wp=kwargs["wp"])
	return True
	
def waypointEditComplete(**kwargs):
	print(kwargs)
	if ("wp" in kwargs):
		use = "wp"
	elif ("wName" in kwargs):
		use = "wName"
	else:
		raise Exception("Unknown operand")
		
	wpGroupRemComplete(wp=kwargs[use])
	if (kwargs["group"] != ""):
		wpGroupComplete(group = kwargs["group"], wp=kwargs[use])
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
	wpGroupRemComplete(wp=kwargs["wp"])
	if (kwargs["group"] != ""):
		wpGroupComplete(group = kwargs["group"], wp=kwargs["wp"])
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
	
def odc(menu, **kwargs):
	#menu.add_separator()
	menu.add_command("Groups", label="Add to group", command = lambda dev=kwargs["dev"].machName: groupAddWin(device=dev))
	menu.add_command("Groups", label="Remove from group", command = lambda dev=kwargs["dev"].machName: groupRemComplete(device=dev))
	return menu
	
def osmm(menu, **kwargs):
	a = "Group " + str(len(kwargs["sel"]["machs"])) + " devices and "+ str(len(kwargs["sel"]["wps"])) + " waypoints"
	menu.add_command("Groups", label=a, command=lambda sel=kwargs["sel"]: multiAddWin(sel = sel))
	return menu
	
def owc(menu, **kwargs):
	menu.add_separator()
	menu.add_command("Groups", label="Add to group", command = lambda wp=kwargs["wp"]: wpGroupAddWin(wp=wp))
	menu.add_command("Groups", label="Remove from group", command = lambda wp=kwargs["wp"]: wpGroupRemComplete(wp=wp))
	return menu

def checkGroupClick(self, **kwargs):
	if ("_group" in kwargs["canTags"]):
		id = None
		for i in kwargs["canTags"]:
			if (i.split(":")[0] == "gid"):
				id = i.split(":")[1]
		
		self.add_command("Groups", label="Check missing group entries " + str(id), command = lambda id=id: checkMissingWin(id))
		self.add_command("Groups", label="Add this group to another", command = lambda id=id: gGroupAddWin(group=id))
		self.add_command("Groups", label="Explode group " + str(id), command = lambda id=id: explodeGroup(id))
		self.add_command("Groups", label="Close exploded tab " + str(id), command = lambda id=id: closeExplodedTab(id))
		self.add_command("Groups", label="Remove this group from its superior", state=DISABLED, command = lambda id=id: checkMissingWin(id))
	
	return self

def gGroupAddWin(**kwargs):
	#raise Exception(kwargs)
	d = inputDialog(main, data = model_data_loader())
	d.addButton("Add", "add")
	d.passFunc("add", gGroupAddComplete, chg= kwargs["group"])

def gGroupAddComplete(chg, **kwargs):
	if (kwargs["group"] != ""):
		p = main.core.struct.cur.execute("select count(*) from `group` where `name` = ?", (kwargs["group"],))
		if (p.fetchone()[0] == 0):
			e = main.core.struct.cur.execute("insert into `group` (`name`) values (?)", (kwargs["group"],))
	
		s = main.core.struct.cur.execute("select id from `group` where `name` = ?", (kwargs["group"],)).fetchone()
		m = s[0]
	
		re = makeBBox(int(chg), [int(s[0])])
		if (re is False):
			askquestion("Loop detected", "Cannot be done")
			return False
	
	e = main.core.struct.cur.execute("delete from `group_residents` where `name` = ? and `type` = 'group'", (chg,))
	if (kwargs["group"] != ""):
		e = main.core.struct.cur.execute("insert into `group_residents` (`group_id`, `name`, `type`) select `id`, ?, 'group' from `group` where `name` = ?", (int(chg),kwargs["group"]))

	main.core.struct.set_changed()
	main.updateWindowTitle()
	main.redraw()
	return True
	
### == Explode: show one group in its own tab (phase 1, read-only) ==

# Registry of open exploded tabs: group_id -> {"frame", "ic", "canvas", "tab_id", "name"}
_exploded = {}
# Key in the file's `config` table holding the ids of the open exploded tabs
_EXPLODED_CONFIG_KEY = "exploded_groups"

def _get_notebook():
	"""Find the main notebook, the way ct.py and checkInit do."""
	for i in main.winfo_children():
		if (type(i) == ttk.Notebook):
			return i
	return getattr(main, "nb", None)

def _group_name(gid):
	p = main.core.struct.cur.execute("select `name` from `group` where `id` = ?", (gid,)).fetchone()
	if (p is None):
		return None
	return p[0]

def _group_members(gid, _seen=None):
	"""Devices and waypoints in a group, expanding nested groups. Returns (set, set)."""
	if (_seen is None):
		_seen = set()
	if (gid in _seen):
		return set(), set()
	_seen.add(gid)
	devs = set()
	wps = set()
	for i in main.core.struct.cur.execute("select `name`, `type` from `group_residents` where `group_id` = ?", (gid,)).fetchall():
		if (i[1] == "device"):
			devs.add(i[0])
		elif (i[1] == "waypoint"):
			try:
				wps.add(int(i[0]))
			except (TypeError, ValueError):
				pass
		elif (i[1] == "group"):
			try:
				sd, sw = _group_members(int(i[0]), _seen)
			except (TypeError, ValueError):
				sd, sw = set(), set()
			devs |= sd
			wps |= sw
	return devs, wps

def _direct_subgroups(gid, _seen=None):
	"""Direct subgroups of a group: [(subgid, name)]. Loop-protected."""
	if (_seen is None):
		_seen = set()
	subs = []
	for i in main.core.struct.cur.execute("select `name`, `type` from `group_residents` where `group_id` = ?", (gid,)).fetchall():
		if (i[1] == "group"):
			try:
				subgid = int(i[0])
				except (TypeError, ValueError):
				continue
			if (subgid in _seen):
				continue
			_seen.add(subgid)
			name = _group_name(subgid)
			if (name is None):
				continue
			subs.append((subgid, name))
	return subs

def _draw_subgroup_boxes(cv, gid, level=1, _seen=None):
	"""Draw a box + label for each subgroup of `gid`, recursively.
	Level colours match redrawCanvas: 0 yellow, 1 green, 2 blue, 3 red.
	Drawn in increasing level order, so inner boxes sit over outer ones,
	and lowered, so devices and wires draw over them."""
	if (_seen is None):
		_seen = set()
	_seen.add(gid)
	c = {0: "yellow", 1: "green", 2: "blue", 3: "red"}
	for subgid, name in _direct_subgroups(gid, _seen):
		try:
			box = makeBBox(subgid)
		except Exception:
			continue
		if (box is False or box[0] is None or box[1] is None or box[2] is None or box[3] is None):
			continue
		colour = c.get(level, "red")
		op = cv.create_rectangle(box[0], box[1], box[2], box[3], width=5, outline=colour)
		cv.addtag_withtag("_group", op)
		cv.addtag_withtag("gid:" + str(subgid), op)
		cv.lower(op)
		r = cv.create_text(box[0], box[1], text=name, font=("Arial", 12), anchor="nw", fill=colour)
		cv.addtag_withtag("_group", r)
		cv.addtag_withtag("gid:" + str(subgid), r)
		cv.lower(r)
		_draw_subgroup_boxes(cv, subgid, level + 1, _seen)

def _bbox_exit(p0, p1, bbox):
	"""Point where the wire leaves bbox, snapped to the dominant axis,
	plus which edge it leaves through. p0 must be inside it.
	Returns (point, edge) with edge 'left'/'right'/'top'/'bottom',
	or None if p1 is inside. Ties go horizontal."""
	x0, y0 = p0
	x1, y1 = p1
	if (bbox[0] <= x1 <= bbox[2] and bbox[1] <= y1 <= bbox[3]):
		return None
	dx = x1 - x0
	dy = y1 - y0
	if (abs(dx) >= abs(dy)):
		# Horizontal exit, at the inside point's height
		if (dx > 0):
			return ((bbox[2], y0), "right")
		elif (dx < 0):
			return ((bbox[0], y0), "left")
	else:
		# Vertical exit, at the inside point's width
		if (dy > 0):
			return ((x0, bbox[3]), "bottom")
		elif (dy < 0):
			return ((x0, bbox[1]), "top")
	return None

def _marker_pos(edge, inside, dist=12):
	"""A point just inside the display from `edge`, pulled back towards `inside`."""
	dx = edge[0] - inside[0]
	dy = edge[1] - inside[1]
	l = math.sqrt(dx * dx + dy * dy)
	if (l == 0):
		return edge
	s = max(0.0, l - dist) / l
	return (inside[0] + dx * s, inside[1] + dy * s)

def _marker_angle(edge):
	"""Text rotation for a marker on an edge: read along a vertical edge."""
	if (edge == "right"):
		return 90
	if (edge == "left"):
		return 270
	return 0

def _device_display_name(d, key):
	p = d.getDevice(key)
	if (p is not None and hasattr(p, "name")):
		return p.name
	return str(key)

def _explode_label_device(d, dev, conn):
	"""Wire label: the far device's name."""
	return _device_display_name(d, dev)

def _explode_label_device_plug(d, dev, conn):
	"""Wire label: the far device and the plug it lands on."""
	return _device_display_name(d, dev) + "." + str(conn)

def _explode_label_group(d, dev, conn):
	"""Wire label: the group the far device belongs to, else its name."""
	try:
		p = main.core.struct.cur.execute("select `group_id` from `group_residents` where `type` = 'device' and `name` = ?", (dev,)).fetchone()
	except Exception:
		p = None
	if (p is not None):
		name = _group_name(p[0])
		if (name is not None):
			return name
	return _device_display_name(d, dev)

def _outside_label(d, dev, conn):
	"""The label for a wire leaving the group, per the configured style."""
	style = "device.plug"
	try:
		if ("explode_label_style" in main.conf.policy):
			style = main.getConfVar("explode_label_style", "device.plug")
	except Exception:
		pass
	try:
		v = main.op_config.fetch(style, "explodeLabelStyle", "device.plug")
		if (v is not None and "func" in v):
			return v["func"](d, dev, conn)
	except Exception:
		pass
	return _explode_label_device_plug(d, dev, conn)

def _show_through_wires():
	"""Whether wires passing through the group (neither end inside) are drawn."""
	try:
		if ("explode_show_through_wires" in main.conf.policy):
			return main.getConfVar("explode_show_through_wires", False) in ["1", True]
	except Exception:
		pass
	return False

def _outside_conn_pos(d, dev, conn):
	"""A device outside the group: its connector position from the main canvas's draw."""
	try:
		p = d.getDevice(dev).drwConnPos[conn]
	except Exception:
		return None
	return p

def _save_exploded():
	"""Store the ids of the open exploded tabs in the file's `config` table."""
	if (main.core.struct is None):
		return
	try:
		main.core.struct.cur.execute("insert or replace into `config` (`key`, `value`) values (?, ?)", (_EXPLODED_CONFIG_KEY, json.dumps(sorted(_exploded.keys()))))
	except Exception as e:
		print("explode: could not save open tabs:", e)
		return
	main.core.struct.set_changed()
	main.updateWindowTitle()

def _refit_after_resize(gid):
	"""Debounced resize handler: re-draw (and so re-fit) one exploded tab."""
	if (gid not in _exploded):
		return
	_exploded[gid]["_resize_after"] = None
	_redraw_exploded_tab(gid)

def _spawn_exploded_tab(gid):
	"""Create the tab for a group and draw it. No saving, no focus change."""
	try:
		gid = int(gid)
	except (TypeError, ValueError):
		return False
	if (gid in _exploded):
		return True
	name = _group_name(gid)
	if (name is None):
		return False
	nb = _get_notebook()
	if (nb is None):
		return False
	fr = Tk.Frame(nb)
	ic = InteractiveCanvas(fr, width=800, height=600, confine=False)
	ic.grid(sticky="news")
	fr.rowconfigure(0, weight=1)
	fr.columnconfigure(0, weight=1)
	ic.rowconfigure(0, weight=1)
	ic.columnconfigure(0, weight=1)
	nb.add(fr, text=name)
	_exploded[gid] = {"frame": fr, "ic": ic, "canvas": ic.canvas, "tab_id": nb.tabs()[-1], "name": name, "size": None, "_resize_after": None}
	cv = ic.canvas
	def _on_resize(event, _gid=gid):
		"""Re-fit on window/tab resize, only when the size really changed."""
		if (_gid not in _exploded):
			return
		ent = _exploded[_gid]
		size = (ent["canvas"].winfo_width(), ent["canvas"].winfo_height())
		if (size == ent.get("size")):
			return
		if (ent.get("_resize_after") is not None):
			try:
				ent["canvas"].after_cancel(ent["_resize_after"])
			except Exception:
				pass
		ent["_resize_after"] = ent["canvas"].after(50, lambda _g=_gid: _refit_after_resize(_g))
	cv.bind("<Configure>", _on_resize)
	_redraw_exploded_tab(gid)
	return True

def explodeGroup(gid):
	"""Open a read-only tab for a group, or focus it if it is already open."""
	try:
		gid = int(gid)
	except (TypeError, ValueError):
		return False
	if (gid in _exploded):
		nb = _get_notebook()
		if (nb is not None):
			nb.select(_exploded[gid]["tab_id"])
		return True
	if (not _spawn_exploded_tab(gid)):
		return False
	_save_exploded()
	nb = _get_notebook()
	if (nb is not None):
		nb.select(_exploded[gid]["tab_id"])
	return True

def closeExplodedTab(gid):
	"""Close the exploded tab for a group, if one is open."""
	try:
		gid = int(gid)
	except (TypeError, ValueError):
		return False
	if (gid not in _exploded):
		return False
	e = _exploded.pop(gid)
	try:
		e["frame"].destroy()
	except Exception:
		pass
	_save_exploded()
	return True

def _close_all_exploded():
	"""Destroy every exploded tab and empty the registry. Does not save (file change)."""
	for gid in list(_exploded.keys()):
		e = _exploded.pop(gid)
		try:
			e["frame"].destroy()
		except Exception:
			pass

def _draw_wire_path(cv, pts, bbox):
	"""Draw one wire path. pts is [(point, outside_label)]: a point with a label
	is an endpoint outside the group, so the wire is stubbed at the group's edge
	with a "to <label>" marker there. Unlabelled points are drawn in full.
	Stubs leave the edge at right angles (dominant axis); markers on a
	vertical edge are rotated to read along it."""
	for a in range(len(pts) - 1):
		p0, l0 = pts[a]
		p1, l1 = pts[a + 1]
		if (l0 is None and l1 is None):
			cv.create_line(p0, p1, fill="black", tags=("_wire",))
		elif (l0 is None and l1 is not None):
			# Leaving the group: stub at the edge, marker just inside it
			ex = _bbox_exit(p0, p1, bbox)
			if (ex is not None):
				pt, edge = ex
				cv.create_line(p0, pt, fill="black", tags=("_wire", "_stub"))
				m = _marker_pos(pt, p0)
				cv.create_text(m[0], m[1], text="to " + str(l1), font=("Arial", 8), anchor="center", angle=_marker_angle(edge), tags=("_stub",))
			else:
				cv.create_line(p0, p1, fill="black", tags=("_wire", "_stub"))
				cv.create_text(p1[0], p1[1], text="to " + str(l1), font=("Arial", 8), anchor="center", tags=("_stub",))
			return
		elif (l0 is not None and l1 is None):
			# Entering the group: stub from the edge, marker just inside it
			en = _bbox_exit(p1, p0, bbox)
			if (en is not None):
				pt, edge = en
				cv.create_line(pt, p1, fill="black", tags=("_wire", "_stub"))
				m = _marker_pos(pt, p1)
				cv.create_text(m[0], m[1], text="to " + str(l0), font=("Arial", 8), anchor="center", angle=_marker_angle(edge), tags=("_stub",))
			else:
				cv.create_line(p0, p1, fill="black", tags=("_wire", "_stub"))
				cv.create_text(p0[0], p0[1], text="to " + str(l0), font=("Arial", 8), anchor="center", tags=("_stub",))
		# else: both ends outside the group, nothing visible on this leg

def _draw_exploded_wires(cv, d, gid, devs, wps, connpos, bbox):
	"""Wires touching the group: whole where both ends are members, stubbed
	with a "to <label>" marker where a wire leaves the group. Wires with
	neither end in the group are only drawn when the through-wires
	setting is on: entering stub, inside segments, leaving stub."""
	for k, i in d.conns.items():
		a_dev, a_conn = i[0]
		b_dev, b_conn = i[1]
		a_in = (a_dev in devs and a_dev in connpos)
		b_in = (b_dev in devs and b_dev in connpos)
		if (not a_in and not b_in and not _show_through_wires()):
			continue
		if (a_in):
			start = connpos[a_dev].get(a_conn)
		else:
			start = _outside_conn_pos(d, a_dev, a_conn)
		if (b_in):
			end = connpos[b_dev].get(b_conn)
		else:
			end = _outside_conn_pos(d, b_dev, b_conn)
		if (start is None or end is None):
			continue
		label_a = _outside_label(d, a_dev, a_conn)
		label_b = _outside_label(d, b_dev, b_conn)
		# Raw path: (point, inside the group?). Outside points before the
		# first inside point belong to the a-side, the rest to the b-side.
		raw = [(tuple(start), a_in)]
		for w in sorted(d.cwps.get(k, []), key=lambda x: x["order"]):
			wpid = w["wpid"]
			if (wpid in d.wp):
				raw.append((tuple(d.wp[wpid]["loc"]), wpid in wps))
		raw.append((tuple(end), b_in))
		first_in = None
		for n in range(len(raw)):
			if (raw[n][1]):
				first_in = n
				break
		if (first_in is None):
			# No point inside the group at all: nothing to draw
			continue
		pts = []
		for n in range(len(raw)):
			p, inside = raw[n]
			if (inside):
				pts.append((p, None))
			elif (n < first_in):
				pts.append((p, label_a))
			else:
				pts.append((p, label_b))
		_draw_wire_path(cv, pts, bbox)

def _redraw_exploded_tab(gid):
	"""Re-draw one exploded tab from the current diagram. Read-only: no bindings."""
	if (gid not in _exploded):
		return
	if (main.core.struct is None):
		return
	e = _exploded[gid]
	cv = e["canvas"]
	d = main.core.dia
	bbox = makeBBox(gid)
	cv.delete("all")
	if (bbox is False or bbox[0] is None):
		# Empty group (or a loop): show just the name
		cv.create_text(10, 10, text=e["name"], font=("Arial", 12), anchor="nw")
		cv.config(scrollregion=(0, 0, 800, 600))
		e["size"] = (cv.winfo_width(), cv.winfo_height())
		return
	# Group box first, so devices and wires draw over it
	op = cv.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], width=5, outline="yellow")
	cv.addtag_withtag("_group", op)
	cv.addtag_withtag("gid:" + str(gid), op)
	r = cv.create_text(bbox[0], bbox[1], text=e["name"], font=("Arial", 12), anchor="nw", fill="yellow")
	cv.addtag_withtag("_group", r)
	cv.addtag_withtag("gid:" + str(gid), r)
	# Subgroup boxes, level 1 and deeper, under the devices and wires
	_draw_subgroup_boxes(cv, gid)
	# Members, skipping orphans (a deleted device leaves its group_residents row behind)
	devs, wps = _group_members(gid)
	devs = set([i for i in devs if i in d.dev and i in d.locs])
	wps = set([i for i in wps if i in d.wp])
	# Devices, via the same renderer the main canvas uses
	try:
		objMk = main.op_config.fetch(main.conf.policy["objMk"].get(), "objMk", "builtin")["func"]
	except Exception:
		objMk = d.objMk
	try:
		conn_names = main.conn_labelling.get()
	except Exception:
		conn_names = False
	connpos = {}
	for i in devs:
		try:
			aa = objMk(cv, d.getDevice(i), d.locs[i], connector_names=conn_names)
		except Exception:
			continue
		if (isinstance(aa, (list, tuple))):
			aa = aa[0]
		connpos[i] = aa
	# Waypoint labels, like the main canvas
	try:
		show_wp = main.wp_labels.get()
	except Exception:
		show_wp = False
	if (show_wp):
		for i in wps:
			r = cv.create_text(d.wp[i]["loc"][0], d.wp[i]["loc"][1], text=d.wp[i]["name"], font=("Arial", 4))
			for q in ["_wp", "wn:" + str(i), d.wp[i]]:
				cv.addtag_withtag(q, r)
	# Wires
	_draw_exploded_wires(cv, d, gid, devs, wps, connpos, bbox)
	# Fit the group to 3/4 of the canvas, centred on the canvas centre.
	# Falls back to the main redraw's 1x/2x scale when the canvas is not
	# mapped yet (spawn time) or the group has no size.
	vw = cv.winfo_width()
	vh = cv.winfo_height()
	bw = bbox[2] - bbox[0]
	bh = bbox[3] - bbox[1]
	try:
		sc = main.sc.get()
	except Exception:
		sc = 1
	if (bw > 0 and bh > 0 and vw > 1 and vh > 1):
		total = min(0.75 * vw / bw, 0.75 * vh / bh)
		cv.scale("all", 0, 0, total, total)
		cx = (bbox[0] + bbox[2]) / 2
		cy = (bbox[1] + bbox[3]) / 2
		cv.move("all", vw / 2 - cx * total, vh / 2 - cy * total)
		cv.config(scrollregion=(0, 0, vw, vh))
	else:
		cv.scale("all", 0, 0, sc, sc)
		cv.config(scrollregion=((bbox[0] * sc) - 10, (bbox[1] * sc) - 10, (bbox[2] * sc) + 10, (bbox[3] * sc) + 10))
	e["size"] = (vw, vh)

def redrawExplodedTabs(self, **kwargs):
	"""onCanvasRedraw handler: re-draw every exploded tab when the main canvas redraws."""
	for gid in list(_exploded.keys()):
		_redraw_exploded_tab(gid)

def explodeOnFileLoad(self, **kwargs):
	"""onFileLoad handler: drop the old file's exploded tabs, re-open the stored ones."""
	_close_all_exploded()
	if (main.core.struct is None):
		return
	try:
		p = main.core.struct.cur.execute("select `value` from `config` where `key` = ?", (_EXPLODED_CONFIG_KEY,)).fetchone()
	except Exception:
		return
	if (p is None):
		return
	try:
		gids = json.loads(p[0])
	except Exception:
		return
	for gid in gids:
		try:
			gid = int(gid)
		except (TypeError, ValueError):
			continue
		if (_group_name(gid) is not None):
			_spawn_exploded_tab(gid)

def explodeInit(self, **kwargs):
	"""onPluginInitialise: register the wire-label styles and the
	exploded-tab settings in the global config."""
	try:
		main.op_config.register("explodeLabelStyle", "device", {"func": _explode_label_device})
		main.op_config.register("explodeLabelStyle", "device.plug", {"func": _explode_label_device_plug})
		main.op_config.register("explodeLabelStyle", "group", {"func": _explode_label_group})
	except Exception as e:
		print("explode: could not register label styles:", e)
	try:
		styles = main.op_config._list("explodeLabelStyle")
	except Exception:
		styles = {}
	display = {"device": "Device name", "device.plug": "Device.plug", "group": "Group name"}
	values = {}
	for k in styles:
		values[k] = display.get(k, k)
	try:
		main.conf.addOption("Groups", "explode_label_style", {"name": "Exploded tab wire labels", "type": "Combo", "values": values, "value": "device.plug"})
	except Exception as e:
		print("explode: could not add label style option:", e)
	try:
		main.conf.addOption("Groups", "explode_show_through_wires", {"name": "Show wires passing through the group", "type": "Checkbox", "value": False, "store": Tk.BooleanVar(value=False)})
	except Exception as e:
		print("explode: could not add through-wires option:", e)

MANIFEST = {
	"order": 0,
	"events": {
		"onFileLoad": [ g.checkInit, explodeOnFileLoad ],
		"onPluginInitialise": [explodeInit],
		#"onMenuSpawn" : [menu],
		#"onDevEditWinPreDef": [devEditVarsPopulate],
		"onMachineNameSet": [devEditVarsPopulate],
		"onDeviceAddDialog" : [devAddWin],
		"onDeviceAddComplete" : [devAddComplete],
		"onDeviceEditDialog" : [devAddWin],
		"onDeviceEditComplete" : [devAddComplete],
		"onDeviceClick": [odc],
		"onWaypointClick": [owc],
		"onUnknownClick": [checkGroupClick],
		"onUnknownDrag": [checkGroupDrag],
		"onCanvasRedraw": [redrawCanvas, redrawExplodedTabs],
		"onGlobalConfigUpdate": [redrawExplodedTabs],
		
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