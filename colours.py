def colourDirection(d, hx=False):
	if (d is None):
		c = (0,0,0)
	elif (d in ["In", "in"]):
			c=(255,0,0)
	elif (d in ["Out", "out"]):
			c=(0,0,255)
	elif (d in ["Bi", "Both", "bi", "both"]):
			c=(255,0,255)
	else:
			#raise exception("No")
		c=(196,196,196)
	if (hx):
		return "#" + hex(c[0])[2:].zfill(2) + hex(c[1])[2:].zfill(2) + hex(c[2])[2:].zfill(2)
	return c