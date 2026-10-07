_int = []

class highlighting():
	def highlightSet(self, val):
		global _int
		if (type(val) is list):
			_int = val
		else:
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
			
			a = kwargs["canvas"].create_line(st, drw[i], fn, fill="chocolate1",width=10)
			kwargs["canvas"].addtag_withtag("_highlight", a)
		
		'''if (_int is not None):
			#raise Exception("run")
			for i in kwargs["canvas"].find_all():
				p = kwargs["canvas"].gettags(i)
				if ("_wire" in p):
					if (("wid:" + str(_int[0])) in p):
						kwargs["canvas"].itemconfig(i, fill="deep pink")
						#raise Exception(p)
					else:
						kwargs["canvas"].itemconfig(i, fill="black")
		pass'''
		
	def owc(self, menu, **kwargs):
		if (kwargs["wid"] is not None):
			menu.add_command("Highlighting", label="Highlight", command= lambda hl=kwargs["wid"]: self.highlightSet(hl))
		return menu

	def obc(self, menu, **kwargs):
		if ("wire_list" in kwargs):
			print(kwargs["wire_list"])
			if (len(kwargs["wire_list"]) == 1):
				menu.add_command("Highlighting", label="Highlight", command= lambda hl=kwargs["wire_list"]: self.highlightSet(hl))
			elif (len(kwargs["wire_list"]) > 1):
				menu.add_command("Highlighting", label="Highlight " + str(len(kwargs['wire_list'])), command= lambda hl=kwargs["wire_list"]: self.highlightSet(hl))
		return menu
		
hl = highlighting()

MANIFEST = {
	"order":1,
	"events": {
		"onWireClick": [hl.owc],
		"onBridgeClick" : [hl.obc],
		"onCanvasRedraw" : [hl.draw]
	}
}