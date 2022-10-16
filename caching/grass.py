import pygame,os

class Grass:
	def __init__(self,path):
		self.blades = []

		for i in sorted(os.listdir(path)):
			image = pygame.image.load(f'{path}/{i}')
			image.set_colorkey((0,0,0))
			self.blades.append(image)
		
	def render_grass(self,surf,location,blade_id,rotation):
		rotated_image = pygame.transform.rotate(self.blades[blade_id],rotation)

		surf.blit(rotated_image,(location[0] - rotated_image.get_width() // 2, location[1] - rotated_image.get_height() // 2))