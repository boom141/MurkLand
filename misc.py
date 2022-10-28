import pygame, random, math
from pygame.locals import*


class Player_Status:
	def __init__(self):
		self.health_bar = pygame.image.load('./assets/misc/health_bar3.png').convert()
		self.image_copy = self.health_bar.copy()
		self.image_scale = pygame.transform.scale(self.health_bar,(self.health_bar.get_width()*3,self.health_bar.get_height()*3))
		self.particles = []
		self.collected_orb = 0
		self.font1 = pygame.font.Font('./fonts/Minecraft.ttf',30)

	def orb_glow(self,radius,color):
		surf = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surf, color, (radius, radius), radius)
		surf.set_colorkey((0, 0, 0))
		return surf

	def render(self,surface):
		surface.blit(self.image_scale,(5,5))


		r = 30 * math.sqrt(random.randint(1,2))
		theta = random.random() * 2 * math.pi
		x = 250 + r * math.cos(theta)
		y = 250 + r * math.sin(theta)
		distance_x = 250 - int(x) 
		distance_y = 250 - int(y)
		direction_x = math.cos(math.atan2(distance_y,distance_x)) 
		direction_y = math.sin(math.atan2(distance_y,distance_x))

		orb_number = self.font1.render(f'{self.collected_orb}/4', False, ((255,255,255)))
		surface.blit(orb_number,(70,60))

		self.particles.append([[40,82], [direction_x,direction_y], 8])
		for particle in self.particles:
			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1]
			particle[2] -= 0.4
			particle[1][1] += 0
			pygame.draw.circle(surface, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

			radius = particle[2] * 2

			surface.blit(self.orb_glow(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
			
			pygame.draw.circle(surface, (225,225,225), (40,82), particle[2])
			surface.blit(self.orb_glow(radius, (20, 20, 60)), (40 - radius, 82 - radius), special_flags=BLEND_RGBA_ADD)

			if particle[2] <= 0:
				self.particles.remove(particle)

