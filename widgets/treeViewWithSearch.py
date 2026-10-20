import tkinter
from tkinter import ttk
from tkinter.messagebox import showerror

class treeViewWithSearch(tkinter.Frame):
	
	def checkForSearch(self, item):
		n = self.tt.get()
		if not item in self.storage:
			return False
			
		for i in self.storage[item][1]:
			if (i.upper().find(n.upper()) >= 0):
				# Maybe add it if it doesn't exist
				return True
		
		# Maybe remove it if it shouldn't exist
		return False

	def clear(self):
		self.tv.delete(*self.tv.get_children())
		self.storage = {}
		
	def search(self, a,b,c):
		n = self.tt.get()
		disp = []

		self.tv.delete(*self.tv.get_children())
		for i,j in self.storage.items():
			t=0
			for k in j[1]:
				if (str(k).upper().find(n.upper()) >= 0):
					t+= 1
			if (t >0):
				add = []
				if (j not in disp):
					k = j.copy()
					
					while (k[0] != ""):
						l = k[0]
						k = self.storage[k[0]]
						if (l not in disp):
							if (l not in add and l not in disp):
								disp.insert(0, l)
						else:
							break
					if (i not in add and i not in disp):
						add.append(i)
				disp += add
							
		#print(disp)
		while (len(disp) > 0):
			for i,j in self.storage.items():
				if (i in disp):
					if (not self.tv.exists(j[0]) and not j[0] == ""):
						a = self.forcedisp(j[0])
						print(a)
						for k in a:
							disp.remove(k)
					disp.remove(i)
					self.tv.insert(j[0], "end", i, text=j[1][0], values= j[1][1:])
					#self.tv.insert(j[0], "end", i, values= j[1])
					if (i in self.opens):
						self.tv.item(i, open=True)

	def forcedisp(self, obj):
		item = self.storage[obj]
		subobj = []
		if (not self.tv.exists(item[0]) and not item[0] == ""):
			subobj = self.forcedisp(item[0])
#		print(item)
#		exit()
		self.tv.insert(item[0], "end", obj, text=item[1][0], values = item[1][1:])
		return [obj] + subobj
		
	def exists(self, item):
		return self.tv.exists(item)
	
	def get_children(self, item = None, di = False):
		if (di):
			o=[]
			for i in self.tv.get_children(item):
				o.append(self.storage[i])
			return o
		else:
			return self.tv.get_children(item)
			
	def selected(self):
		return self.tv.selection()
	
	def move(self, what, where, loc = 0):
		self.tv.move(what, where , loc)
		self.storage[what][0] = where 

	def delete(self, id):
		
		if (type(id) in [list, tuple]):
			for i in id:
				if (i in self.storage):
					del self.storage[i]
					del self.exter_storage[i]
				elif(int(i) in self.storage):
					del self.storage[int(i)]
					del self.exter_storage[int(i)]
				else:
					del self.exter_storage[str(i)]
					del self.storage[str(i)] # Is this not good enough for you?!
		else:
			del self.exter_storage[id]
			del self.storage[id]
		self.tv.delete(id)
		# We need to solve recursive deletes here?
		pass
	
	def item(self, item):
		return self.tv.item(item)
	
	def update(self, item, data):
		d = self.storage[item]
		self.storage[item] = [d[0], data]
		self.tv.item(item, text=data[0], values= data[1:])

	def add(self, data, parent = ""):
		self.storage[data[0]] = [parent, data[1].values()]
		self.exter_storage[data[0]] = data[1]
		self.tv.insert(parent, "end", data[0], text=list(data[1].values())[0], values= list(data[1].values())[1:])

	def update_closed_items(self, event):
		tree = event.widget
		item_id = tree.focus()
		self.opens.discard(item_id)
		#showerror(event.type, self.opens)
		
	def update_open_items(self, event):
		tree = event.widget
		item_id = tree.focus()
    
		if event.type == "35" or "Open" in str(event):  # <<TreeviewOpen>>
			self.opens.add(item_id)
		#elif event.type == "36" or "Close" in str(event):  # <<TreeviewClose>>
		#	self.opens.discard(item_id)
		#showerror(event.type, self.opens)
      
	def doAdd(self):
		o = []
		for i in self.adds:
			o.append(i(self))
		return o

	def delSel(self):
		if (self.selected() is not None):
			self.delete(self.selected())
	
	def __init__(self, master, storeSize = 2, compile_keys = None, **kw):
		self.storage = {}
		self.exter_storage = {}
		self.opens = set()
		self.master = master
		self.adds = []
		
		self.compileKeys = compile_keys
			
		if ("adds" in kw):
			self.adds = kw["adds"]
			del kw["adds"]
		super().__init__(master, **kw)
		p = tkinter.Frame(self)
		tkinter.Button(p, text="Add", command=self.doAdd).grid(row=0, column=0)
		
		self.tt = tkinter.StringVar()

		self.search_label = tkinter.Label(self, text="search")
		self.search_label.grid(padx=5, pady=5)
		self.search_box = tkinter.Entry(self, textvariable=self.tt)
		self.tt.trace_add('write', self.search)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(1, weight=1)
	
		self.search_box.grid(column=1, columnspan=2, row=0,sticky="ew")
		
		self.tv = ttk.Treeview(self,columns=list(range(1,storeSize+1)),show="tree headings")
		self.tv.bind("<<TreeviewOpen>>", self.update_open_items)
		self.tv.bind("<<TreeviewClose>>", self.update_closed_items)

		self.tv.grid(columnspan=2, row=1, sticky="news")
		self.sb = tkinter.Scrollbar(self)
		self.sb.grid(column=2,row=1,sticky="ns")
		self.sb.config(command=self.tv.yview)
		self.tv.config(yscrollcommand=self.sb.set)
		
		p.grid(row=2, columnspan=3)
		#tkinter.Button(p, text="Edit", state="disabled").grid(row=0, column=1)
		tkinter.Button(p, text="Remove", command=self.delSel).grid(row=0, column=2)
	
	def get(self):
		
		return self.exter_storage
		if (self.compileKeys is not None):
			return self.get_compile()
			
		o = {}
		for i,j in self.storage.items():
			o[i] = j[1]
		return o
		
	def get_compile(self):
		o = {}
		#raise Exception(self.storage.items())
		for i,j in self.storage.items():
			
			if (len(list(self.compileKeys)) != len(j[1])):
				pass#raise Exception(j[1], self.compileKeys)
			else:
				t = {}
				for k in self.compileKeys:
					t[k] = j[1].pop(0)
				#o[i] = j[1]
				o[i] = t
		#raise Exception(o)
		return o