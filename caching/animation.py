import pygame,os

class Animation:
	def __init__(self,path):
		self.animation_database = {}

		for folder in os.listdir(path):
			image_con = []
			for image in os.listdir(f'{path}/{folder}'):
				img = pygame.image.load(f'{path}/{folder}/{image}').convert()
				img.set_colorkey((0,0,0))
				image_con.append(img)	
		
			self.animation_database[f'{folder}'] = image_con


