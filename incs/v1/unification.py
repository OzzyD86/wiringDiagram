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

	# Final move from wd.py
	
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
				
	def getConfVar(self, key, otherwise = None):
		var = otherwise
		
		# Check global config
		b = self.conf
		if (hasattr(b, "policy")):
			if (key in b.policy):
				if (b.policy[key].get() is not None):
					var = b.policy[key].get()
		
		c = self.core.dia.conf
		if (hasattr(c, "policy")):
			if (key in c.policy):
				if (c.policy[key].get() is not None):
					var = c.policy[key].get()
		# Check local config
		
		return var
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
		
	## === File Shenanigans

	def file_new(self):
		if (self._open_file is not None):
			if (self.core.struct.is_changed()):
				a = Tk.messagebox.askyesnocancel(title="Unsaved Changes", message="There are unsaved changes. Save before clearing?")
				#print(a)
				if (a is None):
					return None
				elif (a is True):
					self.file_save()
		files = [#('All Files', '*.*'), 
			 ('Databases', '*.db')]
	
		a = Tk.filedialog.asksaveasfilename(title="Save new file", filetypes = files, defaultextension = files)
		if (len(a) == 0):
			pass#print("Cancelled?")
		else:
			if (os.path.exists(a)):
				os.rename(a, a + ".bak")
				
			self._open_file = a
			self.core.open_file(a)
			self.cueEvts("onFileLoad")
			for i in self.loaded:
				i[0].entryconfig(i[1], state="normal")
			for i,j in self.conf.policy.items():
				self.core.dia.conf.portData(i,j)
				
			o = {}
			o[None] = ["left", "right", "top", "bottom"]
			for i,j in self.core.dia.conf.policy["connector_context"].get().items():
				o[i] = j["pos"]
				
			self.core.dia.connector_context = o
			self.redraw()
			self.updateWindowTitle()
			self.core.struct.clear_changed()
	
	def file_save(self):
		if (self._open_file is not None):
			self.core.struct.store.commit() # That needs moving
			self.core.struct.clear_changed()
			self.updateWindowTitle()
