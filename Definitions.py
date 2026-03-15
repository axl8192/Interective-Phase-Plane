import pygame, sys, math
from pygame import freetype, gfxdraw
pygame.init()

ventx, venty = 800, 800
fullscreen = False
vent = pygame.display.set_mode((ventx, venty), pygame.FULLSCREEN*fullscreen)

cx = ventx//2
cy = venty//2
unit = 20
zoom_step = 5
dragging = False

clock = pygame.time.Clock()
caption = "Graficator"

n_fnt = freetype.Font("Files/Helvetica Compressed/HVUK____.PFB")

def init_graf(iventx, iventy, ifullscreen=fullscreen, iunit=unit, icx=None, icy=None):
	global ventx, venty, fullscreen, vent, cx, cy, unit
	ventx, venty = iventx, iventy
	fullscreen = ifullscreen
	
	vent = pygame.display.set_mode((iventx, iventy), pygame.FULLSCREEN*ifullscreen)
	if icx == None: 
		cx = ventx//2
	else:
		cx = icx
	if icy == None:
		cy = venty//2
	else:
		cy = icy
	unit = iunit
	return ventx, venty

xtm = lambda x: (x-cx)/unit
ytm = lambda y: -(y-cy)/unit
def xytm(x, y): return (xtm(x), ytm(y))

xtc = lambda x: int(clamp(x*unit+cx, -2**30, 2**30))
ytc = lambda y: int(clamp(-y*unit+cy, -2**30, 2**30))
def xytc(x, y): return (xtc(x), ytc(y))

def draw_grid(numeros=False):
	sm = 25
	s = min(sm, get_unit())
	lm = 3
	l = min(lm, get_unit()/lm)

	for i in range(0, ventx//unit+1):
		px = i*unit+cx%unit

		pygame.draw.line(vent, (20,20,20), (px, 0), (px, venty-1))

		if numeros and xtm(px)!=0:
			pygame.draw.line(vent, (255,255,255), (px, cy-l), (px,cy+l))

			n = f"{int(xtm(px))}"
			nr = n_fnt.render(n, size=s, fgcolor=(200,200,200))
			vent.blit(nr[0], (px-nr[1].width/2, cy+s*8/sm))

	for i in range(0, venty//unit+1):
		py =  i*unit+cy%unit
		
		pygame.draw.line(vent, (20,20,20), (0,py), (ventx-1,py))

		if numeros and ytm(py)!=0:
			pygame.draw.line(vent, (255,255,255), (cx-l,py), (cx+l,py))

			n = f"{int(ytm(py))}"
			nr = n_fnt.render(n, size=s, fgcolor=(200,200,200))
			vent.blit(nr[0], (cx-nr[1].width-s*10/sm, py-s*8/sm))
	
	pygame.draw.line(vent, (255,255,255), (0,cy), (ventx-1,cy))
	pygame.draw.line(vent, (255,255,255), (cx,0), (cx,venty-1))

	#pygame.draw.polygon(vent, (255,255,255), ((cx,0),(cx-5,10), (cx+5,10)))
	#pygame.draw.polygon(vent, (255,255,255), ((ventx-1, cy),(ventx-11, cy+5), (ventx-11, cy-5)))

def clamp(x,a,b):
	return max(a, min(x, b))

def basic_controls(event):
	global dragging, zoom_step, cx, cy
	def zoom(step):
		global cx, cy, unit
		opx, opy = xytm(ventx//2, venty//2)
		unit += step
		opx, opy = xytc(opx, opy)
		dx, dy = ventx//2-opx, venty//2-opy
		cx, cy = cx+dx, cy+dy

	#Quit
	if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
		pygame.quit()
		sys.exit()

	#Mouse
	if event.type == pygame.MOUSEBUTTONDOWN:
		if event.button == 2:
			dragging = True
		if event.button == 4:
			zoom(zoom_step)
		if event.button == 5 and unit-zoom_step>1:
			zoom(-zoom_step)
	if event.type == pygame.MOUSEBUTTONUP:
		if event.button == 2:
			dragging = False

	rel = pygame.mouse.get_rel()
	if dragging:
		cx += rel[0]
		cy += rel[1]

def get_unit():
	return unit
def set_zoom_step(n_zoom_step):
	global zoom_step
	zoom_step = n_zoom_step

def show_text(fuente, texto, color, posicion):
	render = fuente.render(texto, 1, color)
	vent.blit(render, posicion)
def hText(x,y,l,font):
	offset = 0
	for element in l:
		render = font.render(element[0], 1, element[1])
		vent.blit(render, (x+offset,y))
		offset += render.get_size()[0]+element[2]

class Point:
	def __init__(self, posi, r, color, isrim, pointlist):
		self.x, self.y = posi[0], posi[1]
		self.xc, self.yc = xytc(posi[0], posi[1])
		self.r = r
		self.color = color
		self.isrim = isrim
		self.dragging = True

		pointlist.append(self)

	def update(self, pointlist):
		self.xc, self.yc = xytc(self.x, self.y)
		if not self.isrim: gfxdraw.filled_circle(vent, self.xc, self.yc, self.r, self.color)
		gfxdraw.aacircle(vent, self.xc, self.yc, self.r, self.color)

		mx, my = pygame.mouse.get_pos()

		if self.dragging == False and (mx-self.xc)**2+(my-self.yc)**2 <= self.r**2 and pygame.mouse.get_pressed()[0]:
			
			dragging_another = False
			for p in pointlist:
				if p.dragging:
					dragging_another = True

			if not dragging_another:
				self.dragging = True

		elif self.dragging == True and not pygame.mouse.get_pressed()[0]:
			self.dragging = False

		if self.dragging == True:
			for p in pointlist:
				pxc, pyc = xytc(p.x, p.y)
				if p!=self and (mx-pxc)**2+(my-pyc)**2 < (p.r+self.r)**2:
					return

			self.x, self.y = xytm(mx,my)

	def set_pos(self, x, y):
		self.x, self.y = x,y
		self.xc, self.yc = xytc(x,y)
