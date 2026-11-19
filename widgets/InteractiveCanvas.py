import tkinter as Tk

class InteractiveCanvas(Tk.Frame):
	def __init__(self, master, **kwargs):
		super().__init__(master)
		print(kwargs)
		self.canvas = Tk.Canvas(self, **kwargs)
		self.canvas.grid(sticky='news', column=0, row=0)
		self.canvas.config(scrollregion = (0,-0,800,600))

		self.canvas.grid_propagate (False)

		self.vscroll = Tk.Scrollbar(self)
		self.vscroll.grid(column=1, row=0,sticky="news")
		self.hscroll = Tk.Scrollbar(self,orient=Tk.HORIZONTAL)
		self.hscroll.grid(column=0, row=1,sticky="news")
		self.canvas.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)
		self.vscroll.config( command = self.canvas.yview )
		self.hscroll.config( command = self.canvas.xview )
		