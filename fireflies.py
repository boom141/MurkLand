import pygame, random
from pygame.locals import*


class Fireflies(pygame.sprite.Sprite):
	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.radius = 1

	def circle_surf(self, radius, color):
		surf = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surf, color, (radius, radius), radius)
		surf.set_colorkey((0, 0, 0))
		return surf

	def render(self,surface,dt,direction,scroll):
		# direction = [random.randint(0, 20) / 10 - 1, random.randrange(-1,1)]
		
		if random.randint(0,1) == 0:
			direction[0] *= random.randint(-2,2)
		self.position[0] += direction[0] * dt
		if random.randint(0,1) == 0:
			direction[1] *= random.randint(-2,2)
		self.position[1] += direction[1] * dt

		glow_radius = self.radius * 2
		pygame.draw.circle(surface, 'yellow', [self.position[0] - scroll[0], self.position[1] - scroll[1]], self.radius)
		surface.blit(self.circle_surf(glow_radius, (70, 70, 17)), (int(self.position[0] - glow_radius) - scroll[0],
		int(self.position[1] - glow_radius) - scroll[1]), special_flags=BLEND_RGBA_ADD)