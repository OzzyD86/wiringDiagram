from copy import copy
from PIL import Image, ImageDraw, ImageFont
import math as maths
from diagramStructure import diagramStructure
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
	return 1

import tkinter as Tk
import tkinter.ttk as ttk

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
		d.add_command(label="Hello")
		d.add_command(label=str(self.canvas.find_closest(event.x,event.y)))
		d.add_separator()
		for i in self.canvas.gettags(self.canvas.find_closest(event.x,event.y)):
			d.add_command(label=i)
		d.tk_popup(self.canvas.winfo_rootx()+event.x, self.canvas.winfo_rooty()+event.y)
		pass
			
	def file_save(self):
		f.store.commit() # That needs moving
		pass
	
	def setmName(self, *nope):
		KEYS, VALUES = self.getKeys()
		obj = KEYS[VALUES.index(self.mName.get())]
		left, top, width, height = self.core.dia.locs[obj]
		self.top.set(top)
		self.left.set(left)
		self.width.set(width)
		self.height.set(height)
		#print(d.locs)
		
	def setInC(self, *what):
		self.e["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		
		obj = KEYS[VALUES.index(self.indName.get())]
		ii = self.core.dia.getDevice(obj).connectors.keys()
		#print(ii)
		
		self.e["values"]=list(ii)

	def setM(self, *what, **kwargs):
		#print(what)
		#print(kwargs)
		self.b["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		
		obj = KEYS[VALUES.index(kwargs['i'])]
		ii = self.core.dia.getDevice(obj).connectors.keys()
		
		kwargs['o']["values"]=list(ii)
		
	def setOutC(self, *kwargs):

		#print(what)
		self.b["state"]='readonly'
		
		KEYS, VALUES = self.getKeys()
		
		obj = KEYS[VALUES.index(self.outdName.get())]
		ii = self.core.dia.getDevice(obj).connectors.keys()
		
		self.b["values"]=list(ii)
				
	def setM2(self, *args):
		pass
		
	def file_load(self):
		a = tkinter.filedialog.askopenfile()
		
		#print(a.name,a)
		# This is literally the new code
		if (a is None):
			print("Cancelled?")
		else:
			a = a.name
			global f,t,d
			f = diagramStructure(a)
			f.build()
			if (f.check_version() < check_current_version()):
				print("Update needed")
				f.update_version(f.check_version(), check_current_version())

			self.core.dia = diagram() #WTF!!!
			#d.load(f)
			self.core.load(f)
		#	d = self.core.dia #diagram()
			self.core.importStruct(f)
			self.redraw()
		pass
		
	def file_new(self):
		a = tkinter.filedialog.asksaveasfilename()
		if (len(a) == 0):
			print("Cancelled?")
		else:
			global f,t,d
			f = diagramStructure(a)
			f.build()
			if (f.check_version() < check_current_version()):
				print("Update needed")
				f.update_version(f.check_version(), check_current_version())

			self.core.dia = diagram() #WTF!!!
			#d.load(f)
			self.core.load(f)
			#d = self.core.dia #diagram()
			self.core.importStruct(f)
			self.redraw()
			
			#print("Yes")
		#print(type(a), a)
		
	def redraw(self):
		d = self.core.dia
		
		self.canvas.delete("all")
		for i in d.listDevices():
			if (i in d.locs):
				aa = d.objMk(self.canvas, d.getDevice(i), d.locs[i])
				d.getDevice(i).drwConnPos = aa

		for i in d.conns:
			p =0
			pin = None
			pout = None
			if (d.getDevice(i[0][0]) is not None):
				pin = d.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
			else:
				p+=1
			
			if (d.getDevice(i[1][0]) is not None):
				pout = d.getDevice(i[1][0]).connectors[i[1][1]]["direction"]
			else:
				p+=1
			
			if (pin == pout):
				if (pin is not None):
					print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
		
			if (p == 0):
				st = d.getDevice(i[0][0]).drwConnPos[i[0][1]]
				fn =  d.getDevice(i[1][0]).drwConnPos[i[1][1]]
				#dr.line((st,fn), fill=(0,0,0))
				r = self.canvas.create_line(st,fn, fill="black")
			#else:
			#print(pin, pout)
		
t = wdTk()

#p = pjaDialog().go()

import tkinter.filedialog

f = t.core.struct = diagramStructure("f.db")
t.core.importStruct(t.core.struct)

x = t.window
wdc = t.core

print(wdc.struct.check_version())
if (wdc.struct.check_version() < check_current_version()):
	print("Update needed")
	wdc.struct.update_version(wdc.struct.check_version(), check_current_version())

wdc.struct.build()
#d = wdc.dia = diagram()
wdc.load(f)
	
#wdc.dia = d # this is a placeholder!
t.redraw()

#t.core.dia.exportPng().save("mx2.png")
x.mainloop()
