import pygame
from pygame.locals import*

from caching.animation import*

class Player:
	def __init__(self,location):
		self.animation = Animation('./assets/animation')
		self.image = pygame.image.load('assets/animation/player_idle/0.png')
		self.rect = self.image.get_rect(x=location[0],y=location[1])
		self.double_jump = -1
		self.free_fall = 0
		self.vertical_momentum = 0
		self.momentum_value = 0.3
		self.frame_count = 0
		self.state = 'idle'
		self.flip = False

	def collision(self,tile_rects):
		hit_list = []
		for tile in tile_rects:
			if self.rect.colliderect(tile):
				hit_list.append(tile)

		return hit_list
	
	def move(self,player_move,tile_rects):
		collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
		self.rect.x += player_move[0]
		hit_list = self.collision(tile_rects)
		for tile in hit_list:
			if player_move[0] > 0:
				self.rect.right = tile.left
			elif player_move[0] < 0:
				self.rect.left = tile.right
		self.rect.y += player_move[1]
		hit_list = self.collision(tile_rects)
		for tile in hit_list:
			if player_move[1] > 0:
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif player_move[1]  < 0:
				self.rect.top = tile.bottom
		
		return collision_types

	def change_state(self,delta_time):
		frame = self.animation.animation_database[f'player_{self.state}']

		self.frame_count += 0.1 * delta_time
		if self.frame_count >= (len(frame) - 1):
			self.frame_count = 0

		return frame[int(self.frame_count)]

	def update(self,delta_time,game_data):
		player_move = [0,0]
		if pygame.key.get_pressed()[K_d]:
			player_move[0] += 2.5 * delta_time
			self.flip = False
		if pygame.key.get_pressed()[K_a]:
			player_move[0] -= 2.5 * delta_time
			self.flip = True
		if pygame.key.get_pressed()[K_SPACE]:
			if self.free_fall < 6 and self.double_jump == -1:
				self.vertical_momentum = -10
				self.double_jump = 0 
			elif self.free_fall > 6 and self.double_jump == 0:
				self.vertical_momentum = -4
				self.double_jump = 1

# player state -------------------------------------------------------#			
		self.state = 'idle'
		if player_move[0] > 0 or player_move[0] < 0:
				self.state = 'run'
	
# player gravity -------------------------------------------------------#
		player_move[1] += self.vertical_momentum * delta_time
		self.vertical_momentum += self.momentum_value
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3

		collisions = self.move(player_move,game_data.tile_rects)

		if collisions['bottom']:
			self.free_fall = 0
			self.vertical_momentum = 0
			self.double_jump = -1
		else:
			self.free_fall += 1

		self.image = self.change_state(delta_time)
		self.image = pygame.transform.flip(self.image,self.flip,False)

	def draw(self,surface,scroll):
		# image_scale = pygame.transform.scale(self.image,(17,33)).convert()
		surface.blit(self.image,(self.rect.x - scroll[0], self.rect.y - scroll[1]))
