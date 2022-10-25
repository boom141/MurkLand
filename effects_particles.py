import pygame
from pygame.locals import*

class Pulse_Ease_Out(pygame.sprite.Sprite):
	def __init__(self,position,option,color,value):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.radius = 0
		self.radius_value = option[0]
		self.width = option[1]
		self.duration = option[2]
		self.color = color
		self.play_animation = value

	def render(self,surface,scroll,dt):
		if self.play_animation:
			if self.radius > self.duration - 20:
				self.radius_value = 0.7

		self.radius += self.radius_value * dt
		if self.radius >= self.duration:
			self.kill()

		pygame.draw.circle(surface, self.color,(self.position[0] - scroll[0],self.position[1] - scroll[1]),int(self.radius),self.width)

class Static_Particle(pygame.sprite.Sprite):
	def __init__(self,position,direction,options,physics,glow): # options are [duration,gravity,seconds,width,color], physics are [bounce,tile_map,tile_size]
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.options = options
		self.physics = physics
		self.glow = glow
		self.gravity = 0
	
	def orb_glow(self,radius,color):
		surf = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surf, color, (radius, radius), radius)
		surf.set_colorkey((0, 0, 0))
		return surf

	def render(self,surface,scroll,dt): 
		self.position[0] += self.direction[0] * dt
		loc_str = f'{int(self.position[0] / self.physics[2])}:{int(self.position[1] / self.physics[2])}'
		if self.physics[0] > 0:
			if loc_str in self.physics[1]:
				self.direction[0] = -self.physics[0] * self.direction[0]
				self.direction[1] *= 0.95 # modifying velocity for each axis
				self.position[0] += self.direction[0] * 2
		self.position[1] += self.direction[1] * dt
		loc_str = f'{int(self.position[0] / self.physics[2])}:{int(self.position[1] / self.physics[2])}'
		if self.physics[0] > 0:
			if loc_str in self.physics[1]:
				self.direction[1] = -self.physics[0] * self.direction[1]
				self.direction[0] *= 0.95
				self.position[1] += self.direction[1] * 2
		self.options[0] -= self.options[2]
		self.direction[1] += self.gravity
		self.gravity += self.options[1]
		
		pygame.draw.circle(surface, self.options[4], [self.position[0] - scroll[0], self.position[1] - scroll[1]], self.options[0], self.options[3])
		
		radius = self.options[0] * 2

		if self.glow:
			surface.blit(self.orb_glow(radius, (20, 20, 60)), (int(self.position[0] - radius) - scroll[0], int(self.position[1] - radius) - scroll[1]), special_flags=BLEND_RGB_ADD)
		
		if self.options[0] <= 0:
			self.kill()
		
		