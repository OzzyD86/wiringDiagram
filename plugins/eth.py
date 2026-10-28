class eth():
	def init(self, **kwargs):
		kwargs['win'].op_config.register("proto", "eth")
		pass
	
	def mns(self, *args, **kwargs):
		print(args)
		mn = (main.core.dia.getDeviceID(kwargs['args'][0]))
		print(main.core.dia.getDevice(mn))
		return {}
		
		
	def edit(self, **kwargs):
		
		return {
			"Name": "Eth",
			"Widgets" : {
			
			}
		}
		
MANIFEST = {
	"order": 0,
	"events": {
		"onInitialise": [eth.init],
		"onDeviceEditDialog" : [eth.edit],
		"onMachineNameSet" : [eth.mns]
	}
	
}