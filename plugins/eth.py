class eth():
	def init(self, **kwargs):
		kwargs['win'].op_config.register("proto", "eth")
		pass
	
	def mns(self, *args, **kwargs):
		print(args)
		print(kwargs)
		#print(main.core.dia.getDevice(mName))
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