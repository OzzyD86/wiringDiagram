#import tkinter as Tk
#import tkinter.ttk as ttk
#from incs.wdCore import wdCore
#from widgets.connector_points import connector_points
#from widgets.EntryWidget import EntryWidget, ComboEntryWidget, SpinEntryWidget
import tkinter.messagebox

from widgets.inputDialog import inputDialog, inputDialog2

class wdTkCore():
	
	# === Device Adding
	
	def devAddWin(self, event = None):
		d = getattr(event, "x", 0)

		self.aw = inputDialog(self.window, data={
			"mName": {
				"type" : "Entry",
				"name" : "New Machine Name",
			},
			"hName": {
				"type" : "Entry",
				"name" : "Human Name",
			},
			"x": {
				"type" : "Entry",
				"name" : "X Position",
				"value": getattr(event, "x", 300)
			},
			"y": {
				"type" : "Entry",
				"name" : "Y Position",
				"value": getattr(event, "y", 300)
			},
		})
		self.aw.addButton("Add", "add")
		self.aw.passFunc("add", self.devAddComplete)

	def devAddComplete(self, **kwargs):
		if (kwargs['mName'] in self.core.dia.listDevices()):
			tkinter.messagebox.showerror(title="Cannot add device", message="The name of the device is already in use.")
			return False
		
		self.core.addDevice(
			kwargs['mName'], kwargs['hName'],
			(int(kwargs['x']),int(kwargs['y']),50,50))
		
		self.updateWindowTitle()		
		self.redraw()
		return True
		
	# == Device Editing
	
	def devEditWin(self):
		if (len(self.core.dia.listDevices())== 0):
			Tk.messagebox.showerror(title="No devices", message="There are no devices to edit.")
			return False
		
		self.aw = inputDialog2(self.window, data={
			"mName":{
				"type" : "Combo",
				"name": "Edit Machine",
				"values": self.core.dia.listDevices(True),
				"onUpdate": self.setmName2,
			},
			"top": {
				"type": "Entry", "name": "Top"
			},
			"left": {
				"type": "Entry", "name": "Left"
			},
			"width": {
				"type": "Entry", "name": "Width"
			},
			"height": {
				"type": "Entry", "name": "Height"
			}
		})
		self.aw.addButton("Edit", "edit")
		self.aw.passFunc("edit", self.devEditComplete)

	def devEditComplete(self, **kwargs):
		p = self.core.dia.listDevices(True)
	
		if (kwargs['mName'] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to edit.")
			return False
		
		obj = list(p.keys())[list(p.values()).index(kwargs["mName"])]
		
		self.core.updateDevice(obj,
			(int(kwargs['left']),
			int(kwargs['top']), 
			int(kwargs['width']), 
			int(kwargs['height']))
		)
		self.canvas.config(scrollregion=(self.core.dia.bounds))
		self.updateWindowTitle()

		self.redraw()
		return True
		
	# == Device Deleting
	
	def devDelWin(self):
		if (len(self.core.dia.listDevices())== 0):
			tkinter.messagebox.showerror(title="No devices", message="There are no devices to delete.")
			return False
			
		self.aw = inputDialog2(self.window, data={
			"dhName":{
				"type" : "Combo",
				"name": "Edit Machine",
				"values": self.core.dia.listDevices(True),
				#"onUpdate": self.setmName2,
			},
			"lb": {
				"type": "Label",
				"text": "Deleting a device will not remove its plugs or any connected wires from the database. They will simply not be shown",
			}
		})
		self.aw.addButton("Delete", "delete")
		self.aw.passFunc("delete", self.devDelComplete)

	def devDelComplete(self, **kwargs):
		p = self.core.dia.listDevices(True)
	
		if (kwargs['dhName'] not in list(p.values())):
			Tk.messagebox.showerror(title="Device not found", message="There is no device to delete.")
			return False
		
		obj = list(p.keys())[list(p.values()).index(kwargs["dhName"])]
	
		self.core.deleteDevice(obj)
		self.updateWindowTitle()

		self.redraw()
		self.aw.destroy()
		return True
