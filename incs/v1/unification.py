import incs.wdTk
from incs.v1.loader import loader
import os, importlib
import tkinter as Tk

class wdTkUnification(incs.wdTk.wdTk):
	
	## == Plugin and event calling ===
	
	def registerEvt(self, event, call):
		if (not hasattr(self, "events")):
			self.events = {}
			
		if (event not in self.events):
			self.events[event] = []
			
		self.events[event].append(call)
	
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
		if (not hasattr(self, "events")):
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

	# == Window-y shenanigans
	
	def updateWindowTitle(self):
		title = self.app_name
		title += " v" + ".".join(self.version)
		if (self._open_file is not None):
			title += " [" + self._open_file 
			if (self.core.struct.is_changed()):
				title += "*"
			title += "]"
		self.window.title(title)

	def resize_canvas(self, event):
		new_width = event.width
		new_height = event.height

		# Update the canvas size
		self.canvas.config(width=new_width, height=new_height)
	
	def quit(self):
		if (self._open_file is not None):
			if (self.core.struct.is_changed()):
				a = Tk.messagebox.askyesnocancel(title="Unsaved Changes", message="There are unsaved changes. Save before closing?")
				if (a is None):
					return None
				elif (a is True):
					self.file_save()
			else:
				if not (Tk.messagebox.askquestion(title="Exit WiringDiagram", message="Are you sure") == "yes"):
					return None
		self.cueEvts("onUninitialise", win=self)
		exit(0)