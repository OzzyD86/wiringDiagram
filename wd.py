from copy import copy
from PIL import Image, ImageDraw, ImageFont
#forom incs.diagram import diagram
#forom dev import device
	
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
from widgets.inputDialog import inputDialog
import sys
from incs.config import config

def report_callback_exception(self, exc, val, tb):
	d = Tk.Toplevel()
	text_box = Tk.Text(d, wrap=Tk.WORD, width=80, height=10)
	text_box.insert("0.0", str(traceback.extract_stack()) + "\n" + str(val))
	text_box.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
	d.rowconfigure(0, weight=1)
	d.columnconfigure(0, weight=1)
	#d.go()

tkinter.Tk.report_callback_exception = report_callback_exception

class version(Tk.Toplevel):
	def __init__(self, master, a = [], *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		d = Tk.Label(self, text="WiringDiagram v0.0.1", font=("Arial 15"))
		d.grid(sticky="snew", padx=5)
		for i in a:
			Tk.Label(self, text="* " + i, font="Arial 6").grid(sticky="w", padx=5)
		Tk.Button(self, text="Ok", command = self.destroy).grid(pady=5)

import incs.wdTk
import os, importlib

class loader():
	def __init__(self):
		self.loaders = {}
	
	def is_loaded(self, mod):
		return (mod in list(self.loaders.keys()))
		
class wdTk(incs.wdTk.wdTk):

	def cueEvts(self, event = "", exec=True, **kwargs):
		out = []
		#print("Run events for " + event)
		if (event in self.events):
			for i in self.events[event]:
				if (exec):
					out.append(i(self, **kwargs))
				else:
					out.append(i)
					
		return out
		
	def pluginLoad(self):
		self.events = {}
		mods = {}
		loaders = {}
		setattr(self, "loaders", loader())

		for i in os.scandir("plugins"):
			if (os.path.isfile("plugins/" + i.name)):
				mods[i.name.split(".")[0]] = importlib.import_module("plugins." + i.name.split(".")[0])
				nm= i.name.split(".")[0]
				a = mods[nm]
				
				d = getattr(a, i.name.split(".")[0])
				setattr(a, "main", self) # Does this work?
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
		for i in sorted(loaders.keys()):
			for k in loaders[i]:
				for l,m in k["events"].items():
					if (not l in self.events):
						self.events[l] = []
					for n in m:
						self.events[l].append(n)
					pass
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
		for i in self.cueEvts("onMachineNameSet", w=w, val=val, args=args):
			for j,k in i.items():
				w.set(j,k)
		
	def setM2(self, *args):
		#showerror(args, args)
		pass
		
app = "wiringDiagram"
try:
	t = wdTk( c=config)
	s = ttk.Style()

	if hasattr(sys, 'getandroidapilevel'):
		s.configure('Treeview', rowheight=48+8)

	#setattr(t, "config", config())
	#t.config.open()
	t.menu["root"].add_command(label="Configure", command= t.conf.open)
	
	#p = pjaDialog().go()
	t.cueEvts("onInitialise", win=t) # good to go!
	ch = [
		#"Prevent canvas menu spawn crash when no file loaded",
		"New file enables menu items",
		"New file replaces existing file, but backs it up",
		"Canvas prevents drag crashes and errors when empty",
		"Updates to highlighting plugin",
		"Config now in its own file",
		"Scale is radio button not check box"
	]
	#version(t, ch)
	#t.open_file("f.db")
	#t.redraw()
	t.window.mainloop()
	
except Exception as e:
	#t.destroy()
	d = Tk.Tk()
	font = ("Arial", 6)
	
	d.title("Error")
	Tk.Label(d, text=app + " ran into an error", font="Arial 8 bold").grid(sticky="w")
	
	Tk.Label(d, text=str(type(e).__name__) + ": " +str(e), font= [*font, "bold"]).grid()
	d.rowconfigure(0, weight=1)
	d.columnconfigure(0, weight=1)
	d.mainloop()

