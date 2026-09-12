from copy import copy
from PIL import Image, ImageDraw, ImageFont
from incs.diagram import diagram
from dev import device

def drag_start(event):
	widget = event.widget
	widget._drag_start_x = event.x
	widget._drag_start_y = event.y
	print("Yes?")

def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
		
def check_current_version():
	return t.core.check_current_version()

import tkinter as Tk
import tkinter.ttk as ttk
import tkinter.filedialog

from tkinter.messagebox import showerror

def report_callback_exception(self, exc, val, tb):
	showerror("Error", message=str(val))

#Tk.Tk.report_callback_exception = report_callback_exception

#from incs.wdCore omport wdCore

class pjaDialog():
	def __init__(self):
		self.top = Tk.Toplevel()
		#self.master = master
		self.top.protocol('WM_DELETE_WINDOW', self.cancel_command)

		self.tree = ttk.Treeview(self.top)
		self.tree.grid(column=0, row=0, sticky='news')	
		bt = Tk.Button(self.top, text='Select', command=self.ok)
		bt.grid(column=0, row=1)

	def ok(self):
		self.quit(self.tree.selection())

	def quit(self, answer=None):
		self.how = answer
		self.top.destroy()

	def cancel_command(self):
		print("Cancel?")
		self.quit(None)		

	def go(self):
		self.top.wait_visibility() # window needs to be visible for the grab
		self.how = None
		self.top.wait_window(self.top)
		return self.how

import incs.wdTk
	
class wdTk(incs.wdTk.wdTk):
	def click_call(self, event):
		#print(self.canvas.find_closest(event.x,event.y))
		#print(event)
		d = Tk.Menu()
		d.add_command(label="Create Device here", command= lambda event=event: self.devAddWin(event))
		d.add_command(label="Waypoint Device here", command= lambda event=event: self.waypointAddWin(event))
	
		d.add_separator()
		d.add_command(label="Hello", state="disabled")
		d.add_command(label=str(self.canvas.find_closest(event.x,event.y)))
		d.add_separator()
		tags = []
		for i in self.canvas.gettags(self.canvas.find_closest(event.x,event.y)):
			tags.append(i)
			d.add_command(label=i)

		if ("_dev" in tags):
			d.add_command(label="Edit device " + str(self.canvas.find_closest(event.x,event.y)[0]))
			pass
		d.tk_popup(self.canvas.winfo_rootx()+event.x, self.canvas.winfo_rooty()+event.y)
		pass
	
	def setmName(self, *nope):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.mName.get())]
		left, top, width, height = self.core.dia.locs[obj]
		self.top.set(top)
		self.left.set(left)
		self.width.set(width)
		self.height.set(height)

	def setmName2(self, w, val, *args):
		p = w.data['mName']["obj"].get_key_of_value(args[0])
		#KEYS, VALUES = self.getKeys()
		#obj = KEYS[VALUES.index(self.mName.get())]
		#raise Exception(self.core.dia.locs[p])
		left, top, width, height = self.core.dia.locs[p]
		w.set("top", top)
		w.set("left", left)
		w.set("width", width)
		w.set("height", height)
		
	def setM2(self, *args):
		pass
		
t = wdTk()

#p = pjaDialog().go()

t.open_file("f.db")
t.redraw()

#t.core.dia.exportPng().save("mx2.png")
t.window.mainloop()
