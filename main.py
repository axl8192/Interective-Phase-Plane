from Definitions import *
from math import *

#--Main Inits--#
ventx, venty = init_graf(1000, 1000, ifullscreen=False, iunit=103, icx = 50, icy = 930)
caption = "ODE System"
fnt = pygame.font.Font(None, 70)

#--- Phase Diagram ---#
class Slope_Field_Slope:
	def __init__(self, x1, x2, x1_new, x2_new, color, triangle_vert):
		self.color = color
		self.x1 = x1
		self.x2 = x2
		self.x1_new = x1_new
		self.x2_new = x2_new
		self.triangle_vert = triangle_vert

def draw_slope_field(slopes):
	for sl in slopes:
		pygame.draw.aaline(vent, sl.color, xytc(sl.x1,sl.x2), xytc(sl.x1_new,sl.x2_new))

		if len(sl.triangle_vert) != 0:
			v0 = xytc(sl.triangle_vert[0][0], sl.triangle_vert[0][1])
			v1 = xytc(sl.triangle_vert[1][0], sl.triangle_vert[1][1])
			v2 = xytc(sl.triangle_vert[2][0], sl.triangle_vert[2][1])
			vert = (v0, v1, v2)
			gfxdraw.filled_polygon(vent, vert, sl.color)
			gfxdraw.aapolygon(vent, vert, sl.color)

def compute_slope_field(f1, f2, xi, xf, count, strange_color=True, fixed_length = True, triangle = True, max_color_mod = 0.7):
	dt = abs(xf-xi)/count
	slopes = []
	
	for i in range(0, count+1):
		for j in range(0, count+1):
			try:
				x1 = xi*(count-i)/count + xf*i/count
				x2 = xi*(count-j)/count + xf*j/count

				dx1 = f1(x1, x2)*dt
				dx2 = f2(x1, x2)*dt
				
				original_mod = sqrt(dx1**2+dx2**2)
				mod_multiplier = 1
				if fixed_length: mod_multiplier = dt/original_mod

				x1_new = x1 + dx1*mod_multiplier/2
				x2_new = x2 + dx2*mod_multiplier/2

				color = (200,200,200)
				if strange_color:
					intensity = clamp(original_mod*255/max_color_mod, 0, 255)
					color = (intensity, 255-intensity, 255-intensity)

				triangle_vert = []
				if triangle:
					size_x1 = x1_new-x1
					size_x2 = x2_new-x2

					r = math.sqrt(size_x1**2+size_x2**2)
					dc = 3/5 * r 
					ang_r = math.atan2(size_x2, size_x1)
					ang_psc = math.pi/2 - ang_r
					psc = math.sqrt(r**2-dc**2)/3 #Porción de semicuerda
					dx, dy = psc*math.cos(ang_psc), psc*math.sin(ang_psc)
					dcx, dcy = dc*math.cos(ang_r), dc*math.sin(ang_r)
					p_cx,p_cy = x1+dcx,x2+dcy

					triangle_vert = [(x1+size_x1, x2+size_x2), (p_cx-dx, p_cy+dy),  (p_cx+dx, p_cy-dy)]
				
				slopes.append(Slope_Field_Slope(x1, x2, x1_new, x2_new, color, triangle_vert))
				
			except: pass
	
	return slopes

def solve_2x2_system_euler(f1, f2, p, dt = 0.05, iters=30, color = (255,255,255)):
	x1 = p.x
	x2 = p.y

	for i in range(iters):
		x1_new = x1+f1(x1, x2)*dt
		x2_new = x2+f2(x1, x2)*dt
		pygame.draw.line(vent, color, xytc(x1,x2), xytc(x1_new, x2_new))
		x1 = x1_new
		x2 = x2_new

def solve_2x2_system_euler_improved(f1, f2, p, dt = 0.05, iters=30, color = (255,255,255)):
	x1 = p.x
	x2 = p.y

	for i in range(iters):

		m1_x1 = f1(x1, x2)
		x1_new_first = x1 + m1_x1*dt
		m1_x2 = f2(x1, x2)
		x2_new_first = x2 + m1_x2*dt

		m2_x1 = f1(x1_new_first, x2_new_first)
		x1_new = x1 + (m1_x1+m2_x1)/2*dt
		m2_x2 = f2(x1_new_first, x2_new_first)
		x2_new = x2 + (m1_x2+m2_x2)/2*dt

		pygame.draw.line(vent, color, xytc(x1,x2), xytc(x1_new, x2_new))
		x1 = x1_new
		x2 = x2_new

def solve_2x2_system_RK4(f1, f2, p, dt = 0.05, iters=30, color = (255,255,255)):
	x1 = p.x
	x2 = p.y

	for i in range(iters):

		x1_k1 = f1(x1,x2)
		x2_k1 = f2(x1,x2)

		x1_k2 = f1(x1+0.5*dt*x1_k1, x2+0.5*dt*x2_k1)
		x2_k2 = f2(x1+0.5*dt*x1_k1, x2+0.5*dt*x2_k1)

		x1_k3 = f1(x1+0.5*dt*x1_k2, x2+0.5*dt*x2_k2)
		x2_k3 = f2(x1+0.5*dt*x1_k2, x2+0.5*dt*x2_k2)

		x1_k4 = f1(x1+dt*x1_k3, x2+dt*x2_k3)
		x2_k4 = f2(x1+dt*x1_k3, x2+dt*x2_k3)

		x1_new = x1 + dt/6*(x1_k1+2*x1_k2+2*x1_k3+x1_k4)
		x2_new = x2 + dt/6*(x2_k1+2*x2_k2+2*x2_k3+x2_k4)

		pygame.draw.line(vent, color, xytc(x1,x2), xytc(x1_new, x2_new))
		x1 = x1_new
		x2 = x2_new

#--- Separated Functions ---#
def solve_2x2_system_euler_separ(f1, f2, p, dt = 0.05, iters=30):
	x1 = p.x
	x2 = p.y

	t = 0
	for i in range(iters):
		x1_new = x1+f1(x1, x2)*dt
		x2_new = x2+f2(x1, x2)*dt
		pygame.draw.line(vent, (255,0,0), xytc(t,x1), xytc(t+dt, x1_new))
		pygame.draw.line(vent, (0,255,0), xytc(t,x2), xytc(t+dt, x2_new))
		x1 = x1_new
		x2 = x2_new
		t += dt

def solve_2x2_system_euler_improved_separ(f1, f2, p, dt = 0.05, iters=30):
	x1 = p.x
	x2 = p.y
	
	t = 0
	for i in range(iters):

		m1_x1 = f1(x1, x2)
		x1_new_first = x1 + m1_x1*dt
		m1_x2 = f2(x1, x2)
		x2_new_first = x2 + m1_x2*dt

		m2_x1 = f1(x1_new_first, x2_new_first)
		x1_new = x1 + (m1_x1+m2_x1)/2*dt
		m2_x2 = f2(x1_new_first, x2_new_first)
		x2_new = x2 + (m1_x2+m2_x2)/2*dt

		pygame.draw.line(vent, (255,0,0), xytc(t,x1), xytc(t+dt, x1_new))
		pygame.draw.line(vent, (0,255,0), xytc(t,x2), xytc(t+dt, x2_new))
		x1 = x1_new
		x2 = x2_new
		t += dt

def solve_2x2_system_RK4_separ(f1, f2, p, dt = 0.05, iters=30):
	x1 = p.x
	x2 = p.y
	
	t = 0
	for i in range(iters):

		x1_k1 = f1(x1,x2)
		x2_k1 = f2(x1,x2)

		x1_k2 = f1(x1+0.5*dt*x1_k1, x2+0.5*dt*x2_k1)
		x2_k2 = f2(x1+0.5*dt*x1_k1, x2+0.5*dt*x2_k1)

		x1_k3 = f1(x1+0.5*dt*x1_k2, x2+0.5*dt*x2_k2)
		x2_k3 = f2(x1+0.5*dt*x1_k2, x2+0.5*dt*x2_k2)

		x1_k4 = f1(x1+dt*x1_k3, x2+dt*x2_k3)
		x2_k4 = f2(x1+dt*x1_k3, x2+dt*x2_k3)

		x1_new = x1 + dt/6*(x1_k1+2*x1_k2+2*x1_k3+x1_k4)
		x2_new = x2 + dt/6*(x2_k1+2*x2_k2+2*x2_k3+x2_k4)

		pygame.draw.line(vent, (255,0,0), xytc(t,x1), xytc(t+dt, x1_new))
		pygame.draw.line(vent, (0,255,0), xytc(t,x2), xytc(t+dt, x2_new))
		x1 = x1_new
		x2 = x2_new
		t += dt

#--- Init System ---#
def calculate_parameters(lmbda):
	a = 4*sqrt(3)*lmbda**2
	b = 4*lmbda
	c = sqrt(3)*lmbda
	d = 2*lmbda

	critical_points = [(0,0),                    (0, 2*sqrt(3)*lmbda),  (4*lmbda, 0), 
					   (4*lmbda, 2*sqrt(3)*lmbda), (lmbda, sqrt(3)*lmbda), (3*lmbda, sqrt(3)*lmbda)]

	slopes_xi, slopes_xf = 0, 4*lmbda + 0.3

	return a, b, c, d, critical_points, slopes_xi, slopes_xf

initial_p = Point((0.6,2.7), 10, (255,0,0), False, [])

lmbda = 2
a, b, c, d, critical_points, slopes_xi, slopes_xf = calculate_parameters(lmbda)

#Las funciones miembro derecho del sistema. Nota: estos clamp están ahí para evitar overflows.
f1 = lambda x1, x2: clamp(a*x1+x1*x2*(x1-b)-c*x1**2, -2**30, 2**30)
f2 = lambda x1, x2: clamp(0.5*x1**2*x2-d*x1*x2+x2**2*(c-0.5*x2), -2**30, 2**30)

slopes_count = 20
show_triangles = True

slopes = compute_slope_field(f1, f2, slopes_xi, slopes_xf, slopes_count, triangle = show_triangles, max_color_mod = lmbda**4)

#--Bucle principal--#
while True:
	#--Background--#
	vent.fill((0,0,0))
	draw_grid(True)

	#--Numerical Methods--#
	#solve_2x2_system_euler(f1, f2, initial_p, dt = 0.01, iters = 1000, color = (0,255,0))
	#solve_2x2_system_euler_improved(f1, f2, initial_p, dt = 0.01, iters = 1000, color = (0,100,255))
	solve_2x2_system_RK4(f1, f2, initial_p, dt = 0.01, iters = 1000, color = (239, 127, 26))
	draw_slope_field(slopes)

	#solve_2x2_system_euler_separ(f1, f2, initial_p, dt = 0.01, iters = 1000)
	#solve_2x2_system_euler_improved_separ(f1, f2, initial_p, dt = 0.01, iters = 1000)
	#solve_2x2_system_RK4_separ(f1, f2, initial_p, dt = 0.01, iters = 1000)

	#--Critical Points--#
	for p in critical_points:
		pygame.gfxdraw.filled_circle(vent, xtc(p[0]), ytc(p[1]), 10, (0,255,0))
		pygame.gfxdraw.aacircle(vent, xtc(p[0]), ytc(p[1]), 10, (0,255,0))
		pass

	#--Intial value--#
	initial_p.update([])
	
	#--UI--#
	pygame.draw.rect(vent, (0,0,0), (0,0,130,50))
	show_text(fnt,"λ="+str(round(lmbda, 1)), (255,255,255), (5,5))

	#--Events--#
	
	# Basic controls
	for event in pygame.event.get():
		basic_controls(event)

	# Change parameter
	if pygame.key.get_pressed()[pygame.K_UP]:
		lmbda += clock.get_time()/1000
		a, b, c, d, critical_points, slopes_xi, slopes_xf = calculate_parameters(lmbda)
		slopes = compute_slope_field(f1, f2, slopes_xi, slopes_xf, slopes_count, triangle = show_triangles, max_color_mod = lmbda**4)
	elif pygame.key.get_pressed()[pygame.K_DOWN]:
		lmbda -= clock.get_time()/1000
		if lmbda < 0: lmbda = 0
		a, b, c, d, critical_points, slopes_xi, slopes_xf = calculate_parameters(lmbda)
		slopes = compute_slope_field(f1, f2, slopes_xi, slopes_xf, slopes_count, triangle = show_triangles, max_color_mod = lmbda**4)

	#--Display update--#
	clock.tick(0)
	pygame.display.set_caption(caption + f" - {int(clock.get_fps())} fps")
	pygame.display.update()
