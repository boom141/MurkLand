# Setup pygame ---------------------------------------------------#
import pygame,os,time,sys,random,math
from pygame.locals import *
pygame.init()

# imported python files ------------------------------------------#
from map_loader import*
from caching.tile_set import*
from caching.animation import*
from entity import*
from grass_module import grass


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
		self.tile_set = Tile_Set('./assets/tile_set')
		self.map_data.Load('map/map0.json')		
		self.true_scroll = [0,0]
		self.scroll = [0,0]
		self.tile_rects = []
		self.tile_map = {}
		self.grass_loc = []
		self.grass_tiles = ['0.png','1.png','2.png']
		self.master_time = 0

	def render_map(self,surface):
		self.tile_rects = []
		self.grass_loc = []
		for data in sorted(self.map_data.tile_map):
			image_id = data[2].split('.')
			surface.blit(self.tile_set.tile_asset[data[1]][int(image_id[0])],(data[3] - self.scroll[0],data[4] - self.scroll[1]))
			if data[0] != 0 and data[1] != 'third-tile-set':
				self.tile_rects.append(pygame.Rect(data[3],data[4],TILE_SIZE,TILE_SIZE))
			if data[1] == 'first-tile-set' and data[2] in self.grass_tiles:
				self.grass_loc.append(pygame.Rect(data[3] - self.scroll[0], data[4] - self.scroll[1], TILE_SIZE,TILE_SIZE))

game_data = Game_Data()

gm = grass.GrassManager('./assets/grass', tile_size=TILE_SIZE, stiffness=600, max_unique=5, place_range=[1, 1])
gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))

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
	
	gm.apply_force((player.rect.centerx , player.rect.centery ), 8 , 10)
	rot_function = lambda x, y: int(math.sin(game_data.master_time / 60 + x / 80) * 10)
	gm.update_render(display, delta_time, offset=game_data.scroll, rot_function=rot_function)
	for data in game_data.grass_loc:	
		gm.place_tile((int((data.x + game_data.scroll[0])) // TILE_SIZE, int((data.y - 1 + game_data.scroll[1])) // TILE_SIZE), 3, [0, 1, 2, 3, 5])

	game_data.master_time += delta_time

	

	for event in pygame.event.get(): # event loop
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
	screen.blit(pygame.transform.scale(display,SCREEN_SIZE),(0,0))
	pygame.display.update()
	clock.tick(FPS)
