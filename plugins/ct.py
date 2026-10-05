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
		
		print(d)
		p = kwargs['win']
		self.max = max(1, 0, d)
		self.p = ttk.Progressbar(p, orient="horizontal")
		self.p.grid(row=2, columnspan=2, sticky='news')
		self.p.configure(maximum = self.max)
		self.val = 0
		self.p.configure(value = self.val)
		pass
		
	def redraw(self, **kwargs):
		tmp = 0
		print(kwargs['canvas'])
		for i in kwargs['canvas'].find_all():
			#print(i)
			if (i > tmp):
				tmp = i
		pass
		self.val = max(self.val, tmp)
		self.max = max(self.max, self.val)
		self.p.configure(maximum = self.max)
		self.p.configure(value = self.val)
	
	def uninit(self, **kwargs):
		p = open("store.d", "w")
		p.write(str(self.max))
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