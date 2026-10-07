import tkinter as Tk

class megaMenu(Tk.Menu):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._collapsed = False
		self.ops = {}
		
	def collapse(self, collapse):
		self._collapsed = collapse
	
	def add_command(self, op = "default", **kwargs):
		if (op not in self.ops):
			self.ops[op] = {"opers" : {}, "menus" : [] }
			
		self.ops[op]["menus"].append(kwargs)
		
		return #super().add_command(**kwargs)
		
	def compile(self):
		for i,j in self.ops.items():
			if (self._collapsed and i not in ["default"]):
				e = Tk.Menu(self)
				for l in j["menus"]:
					e.add_command(**l)
				super().add_cascade(label=i, menu=e)
				
			else:
				super().add_command(label="section:" + str(i), state="disabled")
				for l in j["menus"]:
					super().add_command(**l)
				super().add_separator()
		return self
		
	pass