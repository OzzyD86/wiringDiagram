_int = None

class highlighting():
	def highlightSet(self, val):
		global _int
		_int = val
		#raise Exception(val)
		main.redraw()
		
	def draw(self, *args, **kwargs):
		global _int
		if (_int is not None):
			#raise Exception("run")
			for i in kwargs["canvas"].find_all():
				p = kwargs["canvas"].gettags(i)
				if ("_wire" in p):
					if (("wid:" + str(_int)) in p):
						kwargs["canvas"].itemconfig(i, fill="white")
						#raise Exception(p)
					else:
						kwargs["canvas"].itemconfig(i, fill="purple")
		pass
		
	def owc(self, menu, **kwargs):
		if (kwargs["wid"] is not None):
			menu.add_command(label="Highlight", command= lambda hl=kwargs["wid"]: self.highlightSet(hl))
		return menu
		
hl = highlighting()

MANIFEST = {
	"order":1,
	"events": {
		"onWireClick": [hl.owc],
		"onCanvasRedraw" : [hl.draw]
	}
}