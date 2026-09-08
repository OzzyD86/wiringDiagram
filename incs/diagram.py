from colours import colourDirection
from PIL import Image, ImageDraw, ImageFont
import tkinter as Tk

i18n = {
	"font_small" : ('Arial', 6),
	"font_large" : ('Arial', 8)
}
class diagram():
	def __init__(self):
		self.bounds = [0,0,0,0]
		self.dev = {}
		self.conns = {}
		self.locs = {}
		self.wp = {}
		self.cwps = {}
		self.wp_labelling = Tk.BooleanVar()
		self.wp_labelling.set(False)
		
		self.conn_labelling = Tk.BooleanVar()
		self.conn_labelling.set(True)
		
	def addWaypoint(self, key, name, loc):
		self.wp[key] = { "name" : name, "loc" : loc }
		pass
	
	def addConnectionWaypoint(self, conn, wpid, order):
		# THIS WILL NOT WORK! If any values have an order >= order above, then they'll need shifting!
		if (conn in self.cwps):
			self.cwps[conn].append({ "wpid" : wpid, "order": order})
		else:
			self.cwps[conn] = [{ "wpid" : wpid, "order": order}]
		pass
		
	def buildWaypointLists(self):
		p = {}
		for i, j in self.conns.items():
			p[i] = { "out": j[0], "in": j[1], "proc" : [] }
			if (i in self.cwps):
				for k in sorted(self.cwps[i], key=lambda kk: kk['order']):
					p[i]["proc"].append(k["wpid"])
					#print(k)
		return p
		
	def clear(self):
		self.__init__() # Just makes sense
		
	def addDevice(self, key, dev):
		self.dev[key] = dev
		
	def listDevices(self):
		return list(self.dev.keys())
	
	def locateDevice(self, dName, pos = (0,0), sz = (50,50)):
		self.locs[dName] = (*pos, *sz)
		
		if ((pos[0] - (sz[0] / 2) - 10) < self.bounds[0]):
			self.bounds[0] = (pos[0] - (sz[0] / 2) - 10)
			
		if ((pos[0] + (sz[0] / 2) + 10) > self.bounds[2]):
			self.bounds[2] = (pos[0] + (sz[0] / 2) + 10) 
			
		if ((pos[1] - (sz[1] / 2) - 10) < self.bounds[1]):
			self.bounds[1] = (pos[1] - (sz[1] / 2) - 10)
			
		if ((pos[1] + (sz[1] / 2) + 10) > self.bounds[3]):
			self.bounds[3] = (pos[1] + (sz[1] / 2) + 10) 
			
	def getDevice(self, key):
		try:
			return self.dev[key]
		except:
			return None
	
	def deleteConnection(self, a):
		_tmp = {}
		for j,i in self.conns.items():
			if not (a == i[0] or a == i[1]):
				_tmp[j] = i
			else:
				print("Deleted", i)
		self.conns = _tmp
	
	def deleteConnectionByID(self, a):
		del self.conns[a]
		
	def addConnection(self, id, a, b):
		if (a[0] not in self.dev):
			return False
		
		if (b[0] not in self.dev):
			return False
			
		_out = self.dev[a[0]]
		_in = self.dev[b[0]]
		
		if (not a[1] in _out.connectors ):
			return False

		if (not b[1] in _in.connectors):
			return False
		
		_out.connectors[a[1]]["connected"] = b
		_in.connectors[b[1]]["connected"] = a
		
		self.conns[id] = ((a,b))
	
	def bbox(self):
		bbox = [0,0,0,0]
		for i in self.locs.items():
			#print(i[1])
			e = i[1]
			if (e[0] < bbox[0]):
				bbox[0] = e[0]
				
			if (e[2] > bbox[2]):
				bbox[2] = e[2]
				
			if (e[1] < bbox[1]):
				bbox[1] = e[1]
				
			if (e[3] > bbox[3]):
				bbox[3] = e[3]
			#pass
		
		for i in self.wp.items():
			e =(i[1]["loc"])
			#e = i[1]
			if (e[0] < bbox[0]):
				bbox[0] = e[0]
				
			if (e[0] > bbox[2]):
				bbox[2] = e[0]
				
			if (e[1] < bbox[1]):
				bbox[1] = e[1]
				
			if (e[1] > bbox[3]):
				bbox[3] = e[1]
			#pass
			
		#for i in bbox:
		#	i = i * 
		return bbox
		
	def objMk(self, dr, p, dms = (0,0,1,1), _type = 1, honour_db = False, offset = (0,0)):
		try:
			f = ImageFont.load_default_imagefont()
		except:
			f = ImageFont.load_default() #_imagefont()
		poss = { "left": [], "right": [], "top": [], "bottom" : [] }

		if (type(dr) is ImageDraw.ImageDraw):
			a = 1
		elif (type(dr) is Tk.Canvas):
			a = 2
		else:
			a = 0
			#print(type(dr))
		# Maybe in the future, a diagramless version will be needed?
		#print(type(dr))
			raise Exception("Unplacable")
	
		if (_type in [0, 1]):
			if (_type == 0):
				ct = 0
				nat = ["left", "right"]
				for i in p.connectors.keys():
					poss[nat[ct%2]].append(i)
					ct+=1
			#print(poss)

			if (_type == 1):
				ct = 0
				nat = ["left", "right"]
				for i in p.connectors.keys():
					if (p.connectors[i]['direction'] in ["In", "in"]):
						poss["left"].append(i)
					elif (p.connectors[i]['direction'] in ["Out", "out"]):
						poss["right"].append(i)
					else:
						poss[nat[ct%2]].append(i)
						ct+=1
			#print(poss)
		
		else:
			pass

		outmap = {}
	
		for fa, fb in poss.items():
			an = Tk.E#CENTER
			tt = (0,0)
			ln = len(fb)
			ct = 0
			if (fa in ["left", "top"]):
				if (fa in ["left"]):
					an = Tk.E
					to = (-5,0)
				else:
					an = Tk.S
				os = (- (dms[2]/2)-2.5, - (dms[3]/2)-2.5)
			elif (fa in ["right"]):
				an = Tk.W
				to = (5,0)
				os = ((dms[2]/2)+2.5, - (dms[3]/2))
			elif (fa in ["bottom"]):
				
				os = (-(dms[2]/2), (dms[3]/2)+2.5)
			else:
				os = (0,0)
			
			for fc in fb:
				if (fa in ["left", "right"]):
					ro = 0
					os = (os[0], (-dms[3] /2) + ((ct+1) / (ln+1) * dms[3]))
				if (fa in ["top", "bottom"]):
					ro=90
					os = ((-dms[2] /2) + ((ct+1) / (ln+1) * dms[2]), os[1])
				lf = dms[0] + os[0]
				tp = dms[1] + os[1]

				c = colourDirection(p.connectors[fc]["direction"], a==2)

				if (a==1):
					dr.rectangle((lf-2.5+offset[0], tp-2.5+offset[1], lf + 2.5+offset[0], tp+2.5+offset[1]), outline=c)
				elif (a==2):
					op = dr.create_rectangle(lf-2.5, tp-2.5, lf + 2.5, tp+2.5, outline=c)
					dr.addtag_withtag("_conn", op)
					dr.addtag_withtag(fc, op)
					if (self.conn_labelling.get()):
						dr.create_text(lf+to[0],tp+to[1],text=fc,font=i18n["font_small"],angle=ro,anchor=an)
				#print(fc)
				ct += 1
				outmap[fc] = (lf,tp)

		if (a==1):
			dr.rectangle(
				(dms[0]-(dms[2]/2)+offset[0], dms[1] - (dms[3]/2)+offset[1],
				dms[0]+(dms[2]/2)+offset[0], dms[1] + (dms[3]/2)+offset[1]),
				outline=(0,0,0)
			)
			dr.text((dms[0]+offset[0],dms[1]+offset[1]), p.name,font=f,fill=(0,0,0))
	
		elif (a == 2):
			rct = dr.create_rectangle(
				dms[0]-(dms[2]/2), dms[1] - (dms[3]/2),
				dms[0]+(dms[2]/2), dms[1] + (dms[3]/2),
				outline="black"
			)
			dr.addtag_withtag(p.name, rct)
			dr.addtag_withtag("_dev", rct)
			dr.create_text(dms[0],dms[1],text=p.name,font=i18n["font_large"])
		#dr.tag_bind(rct, "<Button-1>", drag_start)
		#dr.tag_bind(rct, "<B1-Motion>", drag_motion)

		return outmap
		
	def exportPng(self):
		olines = {}
		a = self.buildWaypointLists()
		#print(a)
		w = int(self.bounds[2] - self.bounds[0])
		h = int(self.bounds[3] - self.bounds[1])
		im = Image.new("RGB", (w,h), (255,255,255))
		f = ImageFont.load_default_imagefont()
		dr = ImageDraw.Draw(im)
		for i in self.listDevices():
			if (i in self.locs):
				aa = self.objMk(dr, self.getDevice(i), self.locs[i], offset = (-self.bounds[0], -self.bounds[1]))
			self.getDevice(i).drwConnPos = aa
	
		d = self
		for k,i in self.conns.items():
			p =0
			pin = None
			pout = None
			if (self.getDevice(i[0][0]) is not None):
				pin = self.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
			else:
				p+=1
			
			if (self.getDevice(i[1][0]) is not None):
				pout = self.getDevice(i[1][0]).connectors[i[1][1]]["direction"]
			else:
				p+=1
			
			if (pin == pout):
				if (pin is not None):
					print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
		
			if (p == 0):
				n = []
				cs = []
				st = self.getDevice(i[0][0]).drwConnPos[i[0][1]]
				fn =  self.getDevice(i[1][0]).drwConnPos[i[1][1]]
				if (k in self.cwps):
					#print(k)
					for l in self.cwps[k]:
						#print(l)
						if (l["wpid"] in self.wp):
							n += self.wp[l["wpid"]]["loc"]
							cs.append(l["wpid"])
							#print(d.wp[l["wpid"]]["loc"])
				#print(n)

				if (self.waypointing.get()):
					if (len(cs) > 1):
						#print(cs)
						dr.line((st[0]-self.bounds[0], st[1]-self.bounds[1],n[0]-self.bounds[0],n[1]-self.bounds[1]), fill=(0,0,0))
						dr.line((n[-2]-self.bounds[0], n[-1] ,fn[0]-self.bounds[0], fn[1]-self.bounds[1]), fill=(0,0,0))
	
						for m in range(len(cs)-1):
							q = (cs[m], cs[m+1])
							#print(q)
							if ((cs[m], cs[m+1]) in olines):
								olines[cs[m], cs[m+1]] += 1
							else:
								olines[cs[m], cs[m+1]] = 1
					else:
						#print(st,fn)
						#print("n:",n)
						if (len(n) == 0):
							dr.line((st[0]-self.bounds[0], st[1]-self.bounds[1],fn[0]-self.bounds[0], fn[1]-self.bounds[1]), fill=(0,0,0))
						else:
							dr.line((st[0]-self.bounds[0], st[1]-self.bounds[1],n[0]-self.bounds[0],n[1]-self.bounds[1]), fill="black")
							dr.line((n[0]-self.bounds[0], n[1]-self.bounds[1],fn[0]-self.bounds[0], fn[1]-self.bounds[1]), fill="black")
				else:
					dr.line((st[0]-self.bounds[0], st[1]-self.bounds[1],fn[0]-self.bounds[0], fn[1]-self.bounds[1]), fill=(0,0,0))
		
		if (self.waypointing.get()):
			for m,n in olines.items():
				dr.line((self.wp[m[0]]["loc"][0]-self.bounds[0],
					self.wp[m[0]]["loc"][1]-self.bounds[1], 
					self.wp[m[1]]["loc"][0]-self.bounds[0],
					self.wp[m[1]]["loc"][1]-self.bounds[1]), width=n, fill=(0,0,0))
		
		if (self.wp_labelling.get()):
			for i,j in self.wp.items():
				dr.text((j["loc"][0]-self.bounds[0],j["loc"][1]+self.bounds[1]), j["name"],font=f,fill=(0,0,0))

		#print(m,n)
		'''for i in self.conns.values():
			pin = self.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
			pout = self.getDevice(i[1][0]).connectors[i[1][1]]["direction"]

			if (pin == pout):
				if (pin is not None):
					print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
			
			st = self.getDevice(i[0][0]).drwConnPos[i[0][1]]
			fn =  self.getDevice(i[1][0]).drwConnPos[i[1][1]]
			dr.line((st[0] - self.bounds[0], st[1] - self.bounds[1] ,fn[0] - self.bounds[0], fn[1] - self.bounds[1]), fill=(0,0,0))'''
		return im
