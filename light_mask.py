import pygame
from pygame.locals import *

class Light_Mask:
	def __init__(self):
		self.light_images = []
		self.frame_count = 0
		self.flip = True
		self.image = pygame.image.load('./assets/light_mask/light.png')
		for i in range(100,150):
			self.light_images.append(pygame.transform.scale(self.image,(i,i)))
	
	def glow(self,surface,radius,delta_time):

		if self.flip:
			self.frame_count += 0.3 * delta_time
		else:
			self.frame_count -= 0.3 * delta_time
				
		if self.frame_count >= (len(self.light_images)): 
			self.frame_count = len(self.light_images) - 1
			self.flip = False
		if self.frame_count <= 1:
			self.frame_count = 1
			self.flip = True
			
		image = self.light_images[int(self.frame_count)]
		surface.blit(image,(radius[0]-int(image.get_width()/2),
		radius[1]-int(image.get_height()/2)),special_flags=BLEND_RGBA_ADD)

	def render(self,surface,location,delta_time):
		light_surf = surface.copy()
		self.glow(light_surf,[location[0],location[1]],delta_time)

		surface.blit(light_surf,(0,0),special_flags=BLEND_RGB_MULT)