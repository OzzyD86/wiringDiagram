import tkinter as Tk

class selection():
	def check(canvas,down,up,**kwargs):
		u = up
		d = down
		#raise Exception(kwargs)
		p =canvas.find_overlapping(d.x,d.y,u.x,u.y)
		o = {
		 	"machs": [],
		 	"wps":[]
		 }
		for i in p:
			q = canvas.gettags(i)
			if ("_dev" in q):
				for i in q:
					if (i.split(":")[0] == "mn"):
						mn = i.split(":")[1]
				if (not mn in o["machs"]):
					o["machs"].append(mn)
					#Tk.messagebox.showwarning("c", mn)
			elif ("_wp" in q):
				for i in q:
					if (i.split(":")[0] == "wn"):
						mn = i.split(":")[1]
				if (not mn in o["wps"]):
					o["wps"].append(mn)
					#Tk.messagebox.showwarning("c", q)
		#Tk.messagebox.showwarning("c", o)
		return o
	
def sel(menu, **kwargs):
		menu.add_separator()
		sel = selection.check(kwargs["core"].canvas, kwargs["down"], kwargs["up"])
		core = menu.nametowidget(".") # Aha! That's how to do it!
	
		for i in core.cueEvts("onSelectionMakeMenu", False):
			menu = i(menu, sel=sel)
		#raise Exception("Boop")
		#menu.add_command(label="Add selection to group", command = lambda c=kwargs["core"].canvas: selection.check(c, kwargs["down"], kwargs["up"]))
		#menu.add_command(label="Remove from group", command = lambda wp=kwargs["wp"]: wpGroupRemComplete(wp=wp))
		return menu
	
MANIFEST = {
	"order": 0,
	"events": {
		#"onInitialise": [ct.init],
		#"onCanvasRedraw": [ct.redraw],
		"onAnyDrag": [sel]
	}
}