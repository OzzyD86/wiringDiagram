import tkinter as Tk

class scrollableFrame(Tk.Frame):
	def __init__(self, master = None, contents = None, **kwargs):
		super().__init__(master, **kwargs)
		self.ca = Tk.Canvas(self)
		
		if (contents is not None):
			self.fr = contents
		else:
			self.fr = Tk.Frame()

		self.fr.bind("<Configure>", lambda e: self.ca.configure(scrollregion=self.ca.bbox("all")))
		self.ca.create_window((4, 4), window=self.fr, anchor='nw')
		#self.ca.config(scrollregion=(self.ca.bbox("all")))

		self.ca.grid(column=0, row=0, sticky="news")
		self.scr = Tk.Scrollbar(self)
		self.scr.grid(column=1, row=0,sticky="news")

		self.ca.configure(yscrollcommand=self.scr.set)#, xscrollcommand=self.hscroll.set)
		self.scr.configure( command = self.ca.yview )

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
	