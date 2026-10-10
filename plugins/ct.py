import tkinter as tk
import tkinter.ttk as ttk
import os

class ct():
	def init(self, **kwargs):
		if (os.path.exists("store.d")):
			f = open("store.d", "r")
			d = int(f.read())
			f.close()
		else:
			d = 0
	
		nn = None
		p = kwargs['win']
		for i in  p.winfo_children():
			if (type(i) == ttk.Notebook):
				nn = i
		ct=0

		fr = tk.Frame(nn)
		self.ic_max = max(1,ct)
		self.c_max = max(1, 0, d)
		tk.Label(fr, text="Canvas ID").grid()
		self.cid = tk.Label(fr, text="00")
		self.cid.grid(row=0,column=1)
		self.p = ttk.Progressbar(fr, orient="horizontal")
		self.p.grid(column=2, row=0, columnspan=1, sticky='news')
		self.p.configure(maximum = self.c_max)
		self.qq = ttk.Progressbar(fr, orient="horizontal")
		self.qq.grid(column=2, row=1, columnspan=1, sticky='news')

		tk.Label(fr, text="Item count").grid(row=1,column=0)
		self.ic = tk.Label(fr, text=str(ct))
		self.ic.grid(row=1,column=1)
	
		fr.columnconfigure(2, weight=1)
		nn.add(fr, text="Stats")
		self.val = 0
		self.p.configure(value = self.val)
		self.cid.configure(text = str(self.val) + "/" + str(self.c_max))
		pass
		
	def redraw(self, **kwargs):
		tmp = 0
		ct = 0

		for i in kwargs['canvas'].find_all():
			#print(i)
			if (i > tmp):
				tmp = i
			ct+= 1
		pass
		self.val = max(self.val, tmp)
		self.ic_max = max(self.ic_max,ct)
		self.c_max = max(self.c_max, self.val)
		self.p.configure(maximum = self.c_max)
		self.ic.configure(text=str(ct))
		self.p.configure(value = self.val)
		self.qq.configure(value = ct)
		self.cid.configure(text = str(self.val) + "/" + str(self.c_max))
		
	def uninit(self, **kwargs):
		p = open("store.d", "w")
		p.write(str(self.c_max))
		p.close()
		print("Done! Bye!")
		pass
		
MANIFEST = {
	"order": 0,
	"events": {
		"onInitialise": [ct.init],
		"onCanvasRedraw": [ct.redraw],
		"onUninitialise": [ct.uninit]
	}
}