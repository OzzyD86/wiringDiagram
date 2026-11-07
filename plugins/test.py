from PIL import ImageFont, ImageDraw
import tkinter as Tk
from incs.diagram import i18n # move this some time?

class test():
	def init(self, **kwargs):
		main.op_config.register("objMk", "test", { "func": test.objMk} )
		#raise Exception(main.op_config)
	pass

	def objMk(dr, p, dms = (0,0,1,1), _type = 1, honour_db = False, offset = (0,0), connector_names = False, highlight_connected = False):
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
			raise Exception("Unplacable", type(dr))
	
		if (_type in [0, 1]):
			if (_type == 0):
				ct = 0
				nat = ["left", "right"]
				for i in p.connectors.keys():
					poss[nat[ct%len(nat)]].append(i)
					ct+=1
			#print(poss)

			if (_type == 1):
				ct = 0
				#nat = ["left", "right"]
				for i in p.connectors.keys():
					if (p.connectors[i]['direction'] in self.connector_context):
						x = self.connector_context[p.connectors[i]['direction']]
						
					else:
						x = self.connector_context[None]
						
					poss[x[ct%len(x)]].append(i)
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
				an = Tk.N
				os = (-(dms[2]/2), (dms[3]/2)+2.5)
			else:
				os = (0,0)
			
			for fc in fb:
				#print(fc)
				if (fa in ["left", "right"]):
					ro = 0
					os = (os[0], (-dms[3] /2) + ((ct+1) / (ln+1) * dms[3]))
				if (fa in ["top", "bottom"]):
					ro=90
					os = ((-dms[2] /2) + ((ct+1) / (ln+1) * dms[2]), os[1])
				lf = dms[0] + os[0]
				tp = dms[1] + os[1]

				c = colourDirection(p.connectors[fc]["direction"], a==2)
				
				if (highlight_connected):
					if (fc in p.connectors and p.connectors[fc]["connected"] is not None):
						tc = "#FF0000"
					else:
						tc = "#000000"
				else:
					tc = "#000000"
				if (a==1):
					dr.rectangle((lf-2.5+offset[0], tp-2.5+offset[1], lf + 2.5+offset[0], tp+2.5+offset[1]), outline=c)
				elif (a==2):
					op = dr.create_rectangle(lf-2.5, tp-2.5, lf + 2.5, tp+2.5, outline=c)
					dr.addtag_withtag("_conn", op)
					dr.addtag_withtag("c:"+p.machName+"."+fc, op)
					if (connector_names):
						otx = dr.create_text(lf+to[0],tp+to[1],text=fc,font=i18n["font_small"],angle=ro,anchor=an, fill=tc)
						dr.addtag_withtag("_conn", otx)
						dr.addtag_withtag("c:"+p.machName+"."+fc, otx)
					#print(fc)
				ct += 1
				outmap[fc] = (lf,tp)

		if (a==1):
			dr.rectangle(
				(dms[0]-(dms[2]/2)+offset[0], dms[1] - (dms[3]/2)+offset[1],
				dms[0]+(dms[2]/2)+offset[0], dms[1] + (dms[3]/2)+offset[1]),
				outline=(0,0,0)
			)
			dr.text((dms[0]+offset[0],dms[1]+offset[1]), p.name,font=f,fill=(0,0,0), anchor="mm")
	
		elif (a == 2):
			rct = dr.create_rectangle(
				dms[0]-(dms[2]/2), dms[1] - (dms[3]/2),
				dms[0]+(dms[2]/2), dms[1] + (dms[3]/2),
				outline="black"
			)
			dr.addtag_withtag("mn:"+p.machName, rct)
			dr.addtag_withtag("_dev", rct)
			tx = dr.create_text(dms[0],dms[1],text=p.name,font=i18n["font_large"])
			dr.addtag_withtag("mn:"+p.machName, tx)
			dr.addtag_withtag("_dev", tx)
		#dr.bind("<Button-1>", self.down)
		#dr.bind("<ButtonRelease-1>", self.test)

		#dr.tag_bind(rct, "<Button-1>", drag_start)
		#dr.tag_bind(rct, "<B1-Motion>", drag_motion)

		return outmap
		
	def plugAddWin(self, **kwargs):
		
		return {
			"Name": "IC Force Position",
			"Widgets" : {
				"force_side": {
					"type": "Combo",
					"name": "Side",
					"values": {
						"none" : "None", 
						#"In": "In", "Out":"Out","Both":"Both" },
					},
					"value": "None"
				},
				"force_pos" :{
					"type":"Spin",
					"name":"Position"
				}
			}
		}
		
MANIFEST = {
	"order": 0,
	"events": {
		#"onFileLoad": [ eth.checkFileLoad ],
		"onPluginInitialise": [test.init],
		"onPlugAddDialog": [test.plugAddWin],
		#"onDeviceEditDialog" : [eth.edit],
		#"onMachineNameSet" : [eth.mns]
	}
	
}