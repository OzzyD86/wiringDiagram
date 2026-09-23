print("HELLO!")

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

def a(self, w, val, *args):
	return { "Test" : "Get data here" }
	
MANIFEST = {
	"order": 0,
	"events": {
		"onDeviceAddDialog" : [devAddWin],
		"onDeviceEditDialog" : [devAddWin],
		#"onMachineNameSet" : [a]
	}
}