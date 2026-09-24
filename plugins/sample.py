print("HELLO!")
from tkinter import Menu

class sample():
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
	return True
	
def a(self, w, val, *args):
	return { "Test" : "Get data here" }

def menu(self):
	x = Menu()
	x.add_command(label= "Hello", state="disabled")
	
	return {
		"name" : "Sample",
		"menu" : x
	}
	
MANIFEST = {
	"order": 0,
	"events": {
		"onMenuSpawn" : [menu],
		"onDeviceAddDialog" : [devAddWin],
		"onDeviceEditDialog" : [devAddWin],
		#"onMachineNameSet" : [a]
		
		"onDeviceAddComplete" : [devAddComplete],
		#"onDeviceEditComplete" : [devAddWin],
	}
}