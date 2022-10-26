import pygame,noise,random

class Bubble_Bg(pygame.sprite.Sprite):
	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.radius = 3
		self.timer = 100
		self.alive = True

	def circle_surf(self, radius, color):
		surf = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surf, color, (radius, radius), radius)
		surf.set_colorkey((0, 0, 0))
		return surf

	def render(self,surface,dt,direction):
		# if self.alive:
		# 	self.timer -= 0.5
		# 	if self.timer <= 0:
		# 		self.kill()
				
		path = noise.pnoise2(self.position[0] / 3,self.position[1] /3, octaves=2) * 3

		if path < 0:
			direction[0] *= random.randint(-2,2)
		self.position[0] += direction[0] * dt
		if path > 0:
			direction[1] *= random.randint(-2,2)
		self.position[1] += direction[1] * dt