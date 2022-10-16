# Setup pygame ---------------------------------------------------#
import pygame,os,time,sys,random
from pygame.locals import *
pygame.init()

# imported python files ------------------------------------------#
from map_loader import*
from caching.tile_set import*
from caching.grass import*
from entity import*

# global variables ------------------------------------------------#
FPS = 60
SCREEN_SIZE = (500,500)
TILE_SIZE = 16
last_time = time.time()

# Setup window ---------------------------------------------------#
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
display = pygame.Surface((150,150))
pygame.display.set_caption('MurkLand')


class Game_Data:
	def __init__(self):
		self.map_data = Map_Loader()
		self.grass = Grass('./assets/grass')
		self.tile_set = Tile_Set('./assets/tile_set')
		self.map_data.Load('map/map0.json')		
		self.true_scroll = [0,0]
		self.scroll = [0,0]
		self.tile_rects = []
		self.tile_map = {}
		self.grass_map = {}
	
	def render_map(self,surface):
		self.tile_rects = []
		for data in sorted(self.map_data.tile_map):
			image_id = data[2].split('.')
			surface.blit(self.tile_set.tile_asset[data[1]][int(image_id[0])],(data[3] - self.scroll[0],data[4] - self.scroll[1]))
			pygame.draw.rect(surface, 'green', (data[3]-self.scroll[0],data[4]-self.scroll[1],TILE_SIZE,TILE_SIZE), 1)
			if data[0] != 0 and data[1] != 'third-tile-set':
				self.tile_rects.append(pygame.Rect(data[3],data[4],TILE_SIZE,TILE_SIZE))

game_data = Game_Data()
player = Player([game_data.map_data.spawn_point[0][0],game_data.map_data.spawn_point[0][1]-30])


# game loop --------------------------------------------------------------#
while 1:
# framerate independence -------------------------------------------------#
	delta_time = time.time() - last_time
	delta_time *= 60
	last_time = time.time()

# fill the screen --------------------------------------------------------#  
	display.fill((25,25,25))

# camera -----------------------------------------------------------------#
	game_data.true_scroll[0] += (player.rect.centerx - display.get_width() // 2 - game_data.true_scroll[0]) / 5
	game_data.true_scroll[1] += (player.rect.centery - display.get_height() // 2 - game_data.true_scroll[1]) / 5
	game_data.scroll = game_data.true_scroll.copy()
	game_data.scroll[0] = int(game_data.true_scroll[0])
	game_data.scroll[1] = int(game_data.true_scroll[1])

# rendering ---------------------------------------------------------------#
	game_data.render_map(display)

	player.update(delta_time,game_data)
	player.draw(display,game_data.scroll)

	# for data in game_data.map_data.grass_loc:
	# 	for grass in range(len(game_data.grass.blades)):
	# 		game_data.grass.render_grass(display,[data[0] + (grass*3) - game_data.scroll[0],data[1] - game_data.scroll[1]],grass,0)

	for event in pygame.event.get(): # event loop
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
	screen.blit(pygame.transform.scale(display,SCREEN_SIZE),(0,0))
	pygame.display.update()
	clock.tick(FPS)
