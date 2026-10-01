_int = []

class highlighting():
	def highlightSet(self, val):
		global _int
		_int = [val]
		#raise Exception(val)
		main.redraw()
		
	def draw(self, *args, **kwargs):
		global _int
		kwargs["canvas"].delete("_highlight")
		drw = {}
		for i in _int:
			drw[i] = []
			if (i in main.core.dia.cwps.keys()):
				for j in main.core.dia.cwps[i]:
					drw[i].append(main.core.dia.wp[j["wpid"]]["loc"])
		
		for i in _int:
			d = main.core.dia
			q = d.conns[i]
			st = d.getDevice(q[0][0]).drwConnPos[q[0][1]]
			fn =  d.getDevice(q[1][0]).drwConnPos[q[1][1]]
			
			a = kwargs["canvas"].create_line(st, drw[i], fn, fill="white",width=10)
			kwargs["canvas"].addtag_withtag("_highlight", a)

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