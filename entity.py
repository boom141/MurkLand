import pygame, random, math
from pygame.locals import*

from caching.animation import*
from light_mask import*

class Player:
	def __init__(self,location):
		self.animation = Animation('./assets/animation')
		self.image = pygame.image.load('assets/animation/player_idle/0.png')
		self.rect = self.image.get_rect(x=location[0],y=location[1])
		self.wall_jump = False
		self.free_fall = 0
		self.vertical_momentum = 0
		self.horizontal_momentum = 0
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
				collision_types['right'] = True
			elif player_move[0] < 0:
				self.rect.left = tile.right 
				collision_types['left'] = True
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

		if self.vertical_momentum < 0:
			self.frame_count = 0
		elif self.vertical_momentum > 0 and self.state == 'jump':
			self.frame_count = 1

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
			if self.free_fall < 6:
				self.vertical_momentum = -3
			elif self.free_fall > 6 and self.wall_jump:
				self.vertical_momentum = -4 
				self.horizontal_momentum = 5 if self.flip else -6

# player state -------------------------------------------------------#			
		self.state = 'idle'
		if self.free_fall > 7:
			self.state = 'jump'
		elif player_move[0] > 0 or player_move[0] < 0:
			self.state = 'run'
	
	
# player gravity -------------------------------------------------------#
		
		player_move[1] += self.vertical_momentum * delta_time
		player_move[0] += self.horizontal_momentum 
		self.vertical_momentum += 0.2
		self.horizontal_momentum -= 0.2
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3
		if self.horizontal_momentum < 0:
			self.horizontal_momentum = 0

		
		collisions = self.move(player_move,game_data.tile_rects)

		if collisions['bottom']:
			self.free_fall = 0
			self.vertical_momentum = 0
			self.horizontal_momentum = 0
		else:
			self.free_fall += 1

		if collisions['left'] or collisions['right']:
			self.wall_jump = True
		else:
			self.wall_jump = False

		self.image = self.change_state(delta_time)
		self.image2 = pygame.transform.flip(self.image,self.flip,False)
		self.image2_rect = self.image2.get_rect(center=(self.rect.centerx,self.rect.centery))

	def draw(self,surface,scroll):
		# image_scale = pygame.transform.scale(self.image,(17,33)).convert()
		surface.blit(self.image2,(self.image2_rect.x - scroll[0], self.image2_rect.y - scroll[1]))


class Light_Orb(pygame.sprite.Sprite):
	def __init__(self,location):
		self.location = location
		self.particles = []
		self.particles_glow = []
		self.hit_box = pygame.Rect(location[0],location[1],50,50)

	def orb_glow(self,radius,color):
		surf = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surf, color, (radius, radius), radius)
		surf.set_colorkey((0, 0, 0))
		return surf
	def update(self):
		self.particles.append([[self.location[0], self.location[1]], [0,0], 4])

		r = 10 * math.sqrt(random.randint(1,2))
		theta = random.random() * 2 * math.pi
		x = self.location[0] + r * math.cos(theta)
		y = self.location[1] + r * math.sin(theta)
		distance_x = self.location[0] - int(x) 
		distance_y = self.location[1]- int(y)
		direction_x = math.cos(math.atan2(distance_y,distance_x)) 
		direction_y = math.sin(math.atan2(distance_y,distance_x))

		self.particles_glow.append([[x, y], [direction_x,direction_y], 5])
	
	def render(self,surface,scroll,delta_time):

		for particle in self.particles:
			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1]
			particle[2] -= 0.3
			particle[1][1] += 0
			pygame.draw.circle(surface, (255, 255, 255), [int(particle[0][0]) - scroll[0], int(particle[0][1]) - scroll[1]], int(particle[2]))

			radius = particle[2] * 2
			
			surface.blit(self.orb_glow(radius, (20, 20, 50)), (int(particle[0][0] - radius) - scroll[0], int(particle[0][1] - radius) - scroll[1]), special_flags=BLEND_RGB_ADD)
			if particle[2] <= 0:
				self.particles.remove(particle)


		for glow in self.particles_glow:
			glow[0][0] += glow[1][0] * delta_time
			glow[0][1] += glow[1][1] * delta_time
			glow[2] -= 0.3
			glow[1][1] += 0
			pygame.draw.circle(surface, (255, 255, 255), [int(glow[0][0]) - scroll[0], int(glow[0][1]) - scroll[1]], int(particle[2]))

			radius = particle[2] * 2
			
			surface.blit(self.orb_glow(radius, (20, 20, 50)), (int(glow[0][0] - radius) - scroll[0], int(glow[0][1] - radius) - scroll[1]), special_flags=BLEND_RGB_ADD)
			if glow[2] <= 0:
				self.particles_glow.remove(glow)

		#pygame.draw.rect(surface, 'green',  (self.hit_box.x - 10 - scroll[0], self.hit_box.y - 10 - scroll[1],20,20), 1)