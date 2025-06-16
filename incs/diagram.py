from colours import colourDirection
from PIL import Image, ImageDraw, ImageFont
import tkinter as Tk

class diagram():
	def __init__(self):
		self.bounds = [0,0,0,0]
		self.dev = {}
		self.conns = []
		self.locs = {}
		
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
		_tmp = []
		for i in self.conns:
			if not (a == i[0] or a == i[1]):
				_tmp.append(i)
			else:
				print("Deleted", i)
		self.conns = _tmp
	
	def addConnection(self, a, b):
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
		
		self.conns.append((a,b))
	
	def bbox(self, p):
		pass
		
	def objMk(self, dr, p, dms = (0,0,1,1), _type = 1, honour_db = False):
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
			tt = (0,0)
			ln = len(fb)
			ct = 0
			if (fa in ["left", "top"]):
				os = (- (dms[2]/2)-2.5, - (dms[3]/2)-2.5)
			elif (fa in ["right"]):
				os = ((dms[2]/2)+2.5, - (dms[3]/2))
			elif (fa in ["bottom"]):
				os = (-(dms[2]/2), (dms[3]/2)+2.5)
			else:
				os = (0,0)
			
			for fc in fb:
				if (fa in ["left", "right"]):
					os = (os[0], (-dms[3] /2) + ((ct+1) / (ln+1) * dms[3]))
				if (fa in ["top", "bottom"]):
					os = ((-dms[2] /2) + ((ct+1) / (ln+1) * dms[2]), os[1])
				lf = dms[0] + os[0]
				tp = dms[1] + os[1]

				c = colourDirection(p.connectors[fc]["direction"], a==2)

				if (a==1):
					dr.rectangle((lf-2.5, tp-2.5, lf + 2.5, tp+2.5), outline=c)
				elif (a==2):
					op = dr.create_rectangle(lf-2.5, tp-2.5, lf + 2.5, tp+2.5, outline=c)
					dr.addtag_withtag("_conn", op)
					dr.addtag_withtag(fc, op)
				#print(p)
				ct += 1
				outmap[fc] = (lf,tp)

		if (a==1):
			dr.rectangle(
				(dms[0]-(dms[2]/2), dms[1] - (dms[3]/2),
				dms[0]+(dms[2]/2), dms[1] + (dms[3]/2)),
				outline=(0,0,0)
			)
			dr.text((dms[0],dms[1]), p.name,font=f,fill=(0,0,0))
	
		elif (a == 2):
			rct = dr.create_rectangle(
				dms[0]-(dms[2]/2), dms[1] - (dms[3]/2),
				dms[0]+(dms[2]/2), dms[1] + (dms[3]/2),
				outline="black"
			)
			dr.addtag_withtag(p.name, rct)
			dr.addtag_withtag("_dev", rct)
			dr.create_text(dms[0],dms[1],text=p.name,font=('Arial',4))
		#dr.tag_bind(rct, "<Button-1>", drag_start)
		#dr.tag_bind(rct, "<B1-Motion>", drag_motion)

		return outmap
		
	def exportPng(self):
		im = Image.new("RGB", (800,600), (255,255,255))
		#f = ImageFont.load_default_imagefont()
		dr = ImageDraw.Draw(im)
		for i in self.listDevices():
			if (i in self.locs):
				aa = self.objMk(dr, self.getDevice(i), self.locs[i])
			self.getDevice(i).drwConnPos = aa
	
		for i in self.conns:
			pin = self.getDevice(i[0][0]).connectors[i[0][1]]["direction"]
			pout = self.getDevice(i[1][0]).connectors[i[1][1]]["direction"]

			if (pin == pout):
				if (pin is not None):
					print("Plugged " + str(pin) + " into " + str(pout) + " with", i)
			
			st = self.getDevice(i[0][0]).drwConnPos[i[0][1]]
			fn =  self.getDevice(i[1][0]).drwConnPos[i[1][1]]
			dr.line((st,fn), fill=(0,0,0))
		return im