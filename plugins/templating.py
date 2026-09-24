from tkinter import Menu
import json
import tkinter as Tk
from widgets.inputDialog import inputDialog

class templating():
	pass

def devAddWin(s, **kwargs):
	return { "Name": "Sample",
		"Widgets" : {
			"Test": {
				"type" : "Entry",
				"name": "Test"
			}
		}
	}

def devAddComplete(**kwargs):
	pass#raise Exception(kwargs)
	
def a(self, w, val, *args):
	return { "Test" : "Get data here" }

def menu(self):
	x = Menu()
	x.add_command(label= "Load from file", state="disabled")
	x.add_command(label= "Save to file", state="disabled")
	
	return {
		"name" : "Templating",
		"menu" : x
	}
	
def tmpSaveWin(template):
	files = [#('All Files', '*.*'), 
			 ("wiringDiagram Template", '*.wdt')]
	a = Tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files)
	if (len(a) == 0):
		print("Cancelled?")
	else:
		json.dump(template, open(a, "w"))
		pass

def tmpLoadComplete(**kwargs):
	self = kwargs["core"]
	d = json.load(kwargs["file"])
	
	self.core.addDevice(
			kwargs["mName"], kwargs["hName"],
			(int(kwargs["left"]),int(kwargs["top"]),d["sz"][0],d["sz"][1]))
	
	for i, j in d["connectors"].items():
			self.core.addConnector(kwargs["mName"], i, dir=  j['direction'])

	self.redraw()
	#raise Exception(kwargs)
	self.updateWindowTitle()
	return True
	
def tmpLoadWin(core, event):
	files = [#('All Files', '*.*'), 
			 ("wiringDiagram Template", '*.wdt')]
	
	a = Tk.filedialog.askopenfile(filetypes = files, defaultextension = files)

	if (a is None):
		print("Cancelled?")
	else:
		#d = json.load(a)
		d = inputDialog(None, data={
		"mName":{
				"type": "Entry", "name": "New Machine Name"
			},
			"hName": {
				"type": "Entry", "name": "New Human Name"
			},
			"top": {
				"type": "Entry", "name": "Top", "value":event.y
			},
			"left": {
				"type": "Entry", "name": "Left","value":event.x
			}
		})
		#for i,j in preDefs.items():
		#	self.aw.set(i, j)
		d.addButton("Add", "add")
		d.passFunc("add", tmpLoadComplete, file=a, core=core)
		pass
	
def odc(menu, **kwargs):
	menu.add_separator()
	tmp = {
		"name": kwargs["dev"].name,
		"connectors": kwargs["dev"].connectors,
		"sz": kwargs["loc"][2:4]
	}
	menu.add_command(label="Save as template...", command = lambda : tmpSaveWin(tmp))
	return menu

def oac(menu, **kwargs):
	menu.add_command(label="Load device from template...", command = lambda: tmpLoadWin(kwargs["core"], kwargs["event"]))
	return menu
MANIFEST = {
	"order": 0,
	"events": {
		"onMenuSpawn" : [menu],
		"onDeviceClick": [odc],
		"onAnyClick": [oac],
		#"onDeviceAddDialog" : [devAddWin],
		#"onDeviceEditDialog" : [devAddWin],
		#"onMachineNameSet" : [a]
		
		#"onDeviceAddComplete" : [devAddComplete],
		#"onDeviceEditComplete" : [devAddWin],
	}
}