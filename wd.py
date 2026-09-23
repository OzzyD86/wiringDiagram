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
import traceback
from tkinter.messagebox import showerror

class config():
	def __init__(self):
		self.dev = Tk.BooleanVar(value=True)
		
def report_callback_exception(self, exc, val, tb):
	d = pjaDialog()
	text_box = Tk.Text(d.top, wrap=Tk.WORD, width=80, height=10)
	text_box.insert("0.0", str(traceback.extract_stack()) + "\n" + str(val))
	text_box.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
	d.top.rowconfigure(0, weight=1)
	d.top.columnconfigure(0, weight=1)
	
	d.go()
	#showerror("Error", message=str(traceback.extract_stack()) + "\n" + str(val))

Tk.Tk.report_callback_exception = report_callback_exception

#from incs.wdCore omport wdCore

class pjaDialog():
	def __init__(self):
		self.top = Tk.Toplevel()
		#self.master = master
		self.top.protocol('WM_DELETE_WINDOW', self.cancel_command)

		#self.tree = ttk.Treeview(self.top)
		#self.tree.grid(column=0, row=0, sticky='news')	
		#bt = Tk.Button(self.top, text='Select', command=self.ok)
		#bt.grid(column=0, row=1)

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
import os, importlib

class loader():
	def __init__(self):
		self.loaders = {}
	
	def is_loaded(self, mod):
		return (mod in list(self.loaders.keys()))
		
class wdTk(incs.wdTk.wdTk):
	def pluginLoad(self):
		mods = {}
		loaders = {}
		setattr(self, "loaders", loader())

		for i in os.scandir("plugins"):
			if (os.path.isfile("plugins/" + i.name)):
				mods[i.name.split(".")[0]] = importlib.import_module("plugins." + i.name.split(".")[0])
				nm= i.name.split(".")[0]
				a = mods[nm]
				
				d = getattr(a, i.name.split(".")[0])
				if (hasattr(a, "MANIFEST")):
					if (a.MANIFEST["order"] in loaders):
						loaders[a.MANIFEST["order"]].append(a.MANIFEST)
					else:
						loaders[a.MANIFEST["order"]] = [a.MANIFEST]
					self.loaders.loaders[nm] = True
		#			#displayText.insert(tkinter.END, str(d) + "\n")
		#		else:
		#			notebook.add( d(notebook), text=i.name.split(".")[0])

		#displayText.insert(tkinter.END, win.core.loaders.loaders)
		#for i in sorted(loaders.keys()):
		#	for k in loaders[i]:
		#		notebook.add(k["call"](notebook), text=k["name"])

	def click_call(self, event):
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		#print(self.canvas.find_closest(event.x,event.y))
		#print(event)
		p = copy(event)
		p.x = x
		p.y = y
		d = Tk.Menu()
		d.add_command(label="Create Device here", command= lambda event=event: self.devAddWin(p))
		d.add_command(label="Create Waypoint here", command= lambda event=event: self.waypointAddWin(p))
	
		d.add_separator()
		d.add_command(label="Hello", state="disabled")
		d.add_command(label=str(self.canvas.find_closest(x,y)))
		d.add_separator()
		tags = []

		for i in self.canvas.gettags(self.canvas.find_closest(x,y)):
			tags.append(i)
			d.add_command(label=i)

		if ("_dev" in tags):
			d.add_command(label="Edit device " + str(self.canvas.find_closest(x,y)[0]))
			pass
		d.tk_popup(self.canvas.winfo_rootx()+event.x, self.canvas.winfo_rooty()+event.y)
		pass
	
	'''def setmName(self, *nope):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.mName.get())]
		left, top, width, height = self.core.dia.locs[obj]
		self.top.set(top)
		self.left.set(left)
		self.width.set(width)
		self.height.set(height)'''
		
	def contextDevMove(self, obj, x,y):
		p = self.core.dia.locs[obj]
		_,_,w,h = p

		self.devEditComplete(**{
			"mName": obj,
			"left": x,
			"top": y,
			"width": w,
			"height": h
		})
		
	def setmName2(self, w, val, *args):
		p = w.data['mName']["obj"].get_key_of_value(args[0])
		left, top, width, height = self.core.dia.locs[p]
		w.set("top", top)
		w.set("left", left)
		w.set("width", width)
		w.set("height", height)
		
	def setM2(self, *args):
		#showerror(args, args)
		pass
		
t = wdTk()
setattr(t, "config", config())
#p = pjaDialog().go()

t.open_file("f.db")
t.redraw()

#t.core.dia.exportPng().save("mx2.png")
t.window.mainloop()
