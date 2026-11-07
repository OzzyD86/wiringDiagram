import tkinter as Tk
import tkinter.ttk as ttk
	
class connector_points(Tk.Frame):

	def setM(self, *what, **kwargs): # This is used a lot, can it be stored elsewhere and imported(?)
		kwargs['o']["state"]='readonly'
		
		KEYS, VALUES = self.machs
		obj = KEYS[VALUES.index(kwargs['i'])]
		ii = self.diagram.getDevice(obj).connectors.keys()
		
		kwargs['o']["values"]=list(ii)
		
	def pass_machines(self, machs):
		self.machs = machs
		#print(machs)
		return self
		
	def connector_selector(self, *args, **kwargs):
	
		KEYS, VALUES = self.machs
		obj = KEYS[VALUES.index(self.mName.get())]
		
		for i in self.c.get_children():
			self.c.delete(i)
			
		for i in self.diagram.conns.items():
			#print(i[1])
			if (i[1][0][0] == obj) or (i[1][1][0] == obj):
				if (i[1][0][1] == self.cName.get()) or (i[1][1][1] == self.cName.get()):
					if (i[1][0][1] == self.cName.get()):
						self.c.insert("", "end", values=(i[0], i[1][1][0], i[1][1][1]))
					else:
						self.c.insert("", "end", values=(i[0], i[1][0][0], i[1][0][1]))
					
					#print(i)
		pass
		
	def __init__(self, master, diagram, variable=None, **kwargs):
		super().__init__(master, **kwargs)
		s = ttk.Style(self)
		s.configure('Treeview', rowheight=56)

		self.cName = Tk.StringVar(self)
		self.mName = Tk.StringVar(self)
		self.diagram = diagram

	def go(self):
		VALUES = self.machs[1]

		Tk.Label(self, text="Machine Name").grid()
		a = ttk.Combobox(self, state='readonly', textvariable= self.mName, values=VALUES).grid()

		Tk.Label(self, text="Connection Point").grid()
		self.b = ttk.Combobox(self, state='disabled', textvariable= self.cName, values=VALUES)
		self.b.grid()
		self.mName.trace('w', lambda *a, b = self.b: self.setM(i = self.mName.get(), o = b))
		self.cName.trace('w', self.connector_selector)
		
		Tk.Label(self, text="Connection").grid()
		self.c = ttk.Treeview(self, columns=("Id", "DevIn", "ConnIn"), show="headings")
		self.c.heading("Id", text="Connection Id")
		self.c.heading("DevIn", text="Input Device")
		self.c.heading("ConnIn", text="Input Connector")
		#tree.pack(fill=tk.BOTH, expand=True)
		self.c.grid()
		#self.c.bind('<Button-1>', self.get)
		return self
		
	def get(self, *args):
		print (self.mName.get(), self.cName.get(), self.c.item(self.c.focus()))
		return  (self.mName.get(), self.cName.get(), self.c.item(self.c.selection()[0]))
	pass
