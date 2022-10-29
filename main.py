# Setup pygame ---------------------------------------------------#
import pygame,os,time,sys,random,math
from pygame.locals import *
pygame.init()

# imported python files ------------------------------------------#
from map_loader import*
from main_menu import*
from effects_particles import*
from backdrop import*
from misc import*
from caching.tile_set import*
from caching.animation import*
from entity import*
from fireflies import*
from sound_music import*
from grass_module import grass


# global variables ------------------------------------------------#
FPS = 60
SCREEN_SIZE = (500,500)
TILE_SIZE = 16
last_time = time.time()

# Setup window ---------------------------------------------------#
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
display = pygame.Surface((170,170))
light_surf = display.copy()
bg_light_surf = screen.copy()
main_menu = screen.copy()
menu_surf = screen.copy()
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
		self.foliage = []
		self.grass_loc = []
		self.grass_tiles = ['0.png','1.png','2.png']
		self.avoid = [[0,1],['third-tile-set','decoration']]
		self.master_time = 0
		self.light_images = []
		self.firefly_light = []
		self.bg_images = []
		self.frame_count = 0
		self.shrink = True
		self.light_orbs = pygame.sprite.Group()
		self.fireflies = pygame.sprite.Group()
		self.particles = pygame.sprite.Group()
		self.effects = pygame.sprite.Group()
		self.backdrop = pygame.sprite.Group()

	def render_map(self,surface):
		self.tile_rects = []
		self.grass_loc = []
		for data in sorted(self.map_data.tile_map):
			image_id = data[2].split('.')
			surface.blit(self.tile_set.tile_asset[data[1]][int(image_id[0])],(data[3] - self.scroll[0],data[4] - self.scroll[1]))
			if data[0] not in self.avoid[0] and data[1] not in self.avoid[1]:
				self.tile_rects.append(pygame.Rect(data[3],data[4],TILE_SIZE,TILE_SIZE))
			if data[1] == 'first-tile-set' and data[2] in self.grass_tiles:
				self.grass_loc.append(pygame.Rect(data[3] - self.scroll[0], data[4] - self.scroll[1], TILE_SIZE,TILE_SIZE))

pygame.mixer.music.load('./sfx/bgm.wav')
pygame.mixer.music.play(-1)

game_data = Game_Data()

gm = grass.GrassManager('./assets/grass', tile_size=TILE_SIZE, stiffness=600, max_unique=5, place_range=[1, 1])
gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))

player = Player([game_data.map_data.spawn_point[0][0],game_data.map_data.spawn_point[0][1] - 10])
player_status = Player_Status()

for data in game_data.map_data.foliage:
	flip_id = data[2].split('.')
	if int(flip_id[0]) > 2:
		flip = True
	else:
		flip = False
	game_data.foliage.append(Foliage_Animation('./assets/crown',[data[3],data[4]],flip))

for data in game_data.map_data.light_orb:
	game_data.light_orbs.add(Light_Orb([data[0],data[1]]))

light_mask = Light_Mask()

light_mask_image = pygame.image.load('./assets/light_mask/light.png')
for i in range(50,80):
	game_data.firefly_light.append(pygame.transform.scale(light_mask_image,(i,i)))

menu = Main_Menu()
home, switch_range = True, True

def glow(surface,radius,delta_time,entity):
	if game_data.shrink:
		game_data.frame_count += 0.0111 * delta_time
	else:
		game_data.frame_count -= 0.0111 * delta_time

	if entity == 0:		
		if game_data.frame_count >= (len(game_data.light_images)): 
			game_data.frame_count = len(game_data.light_images) - 1
			game_data.shrink = False
		if game_data.frame_count <= 1:
			game_data.frame_count = 1
			game_data.shrink = True
		
		image = game_data.light_images[int(game_data.frame_count)]

	else:
		if game_data.frame_count >= (len(game_data.firefly_light)): 
			game_data.frame_count = len(game_data.firefly_light) - 1
			game_data.shrink = False
		if game_data.frame_count <= 1:
			game_data.frame_count = 1
			game_data.shrink = True
		
		image = game_data.firefly_light[int(game_data.frame_count)]

	surface.blit(image,(radius[0]-int(image.get_width()/2),
	radius[1]-int(image.get_height()/2)),special_flags=BLEND_RGBA_ADD) 


# game loop --------------------------------------------------------------#
	

while 1:	
# framerate independence -------------------------------------------------#
	delta_time = time.time() - last_time
	delta_time *= 60
	last_time = time.time()

# fill the screen --------------------------------------------------------# 
	screen.fill((25,25,25))
	display.fill((25,25,25))
	light_surf.fill((0,0,0))
	main_menu.fill((25,25,25))
	main_menu.set_colorkey((25,25,25))

# camera -----------------------------------------------------------------#
	game_data.true_scroll[0] += (player.rect.centerx - display.get_width() // 2 - game_data.true_scroll[0]) / 5
	game_data.true_scroll[1] += (player.rect.centery - display.get_height() // 2 - game_data.true_scroll[1]) / 5
	game_data.scroll = game_data.true_scroll.copy()
	game_data.scroll[0] = int(game_data.true_scroll[0])
	game_data.scroll[1] = int(game_data.true_scroll[1])

# map edges --------------------------------------------------------------#
	if game_data.scroll[0] < 855:
		game_data.scroll[0] = 855
	if game_data.scroll[0] > 1543:
		game_data.scroll[0] = 1543
	if game_data.scroll[1] < 676:
		game_data.scroll[1] = 676

# rendering ---------------------------------------------------------------#

	for tile in game_data.map_data.outer_tiles:
		image_id = tile[2].split('.')
		display.blit(game_data.tile_set.tile_asset[tile[1]][int(image_id[0])],(tile[3] - game_data.scroll[0], tile[4] - game_data.scroll[1]))

	for tree in game_data.foliage:
		tree.render(display,game_data.scroll,delta_time)
	
	game_data.render_map(display)

	
	player.update(delta_time,game_data)
	if home == False:	
		player.draw(display,game_data.scroll)

	game_data.light_images = []
	for i in range(player.player_light - 50,player.player_light):
		game_data.light_images.append(pygame.transform.scale(light_mask_image,(i,i)))

	gm.apply_force((player.rect.centerx , player.rect.centery ), 8 , 10)
	rot_function = lambda x, y: int(math.sin(game_data.master_time / 60 + x / 80) * 10)
	gm.update_render(display, delta_time, offset=game_data.scroll, rot_function=rot_function)
	for data in game_data.grass_loc:	
		gm.place_tile((int((data.x + game_data.scroll[0])) // TILE_SIZE, int((data.y - 1 + game_data.scroll[1])) // TILE_SIZE), 3, [0, 1, 2, 3, 5])

	game_data.master_time += delta_time
	
	for orb in game_data.light_orbs:
		orb.collision(player,player_status,game_data)
		orb.render(display,game_data.scroll,delta_time)
		glow(light_surf,[orb.location[0] - game_data.scroll[0],orb.location[1] - game_data.scroll[1]],delta_time,0)
	
	
	glow(light_surf,[player.rect.centerx - game_data.scroll[0],player.rect.centery - game_data.scroll[1]],delta_time,0)

	if home:
		range_value = 100
	else:
		if switch_range:
			game_data.fireflies.empty()
		range_value = 170
		switch_range = False

	r = range_value * math.sqrt(random.randint(1,2))
	theta = random.random() * 2 * math.pi
	x = player.rect.centerx + r * math.cos(theta)
	y = player.rect.centery + r * math.sin(theta)
	distance_x = player.rect.centerx - int(x) 
	distance_y = player.rect.centery - int(y)
	direction_x = math.cos(math.atan2(distance_y,distance_x)) 
	direction_y = math.sin(math.atan2(distance_y,distance_x))


	if len(game_data.fireflies) <= 30:
		game_data.fireflies.add(Fireflies([x,y]))



	for firefly in game_data.fireflies:
		firefly.render(display,delta_time,[direction_x,direction_y],game_data.scroll)
		glow(light_surf,[firefly.position[0] - game_data.scroll[0],firefly.position[1] - game_data.scroll[1]],delta_time,1)


	for particle in game_data.particles:
		particle.render(display,game_data.scroll,delta_time)
	
	for effect in game_data.effects:
		effect.render(display,game_data.scroll,delta_time)

	display.blit(light_surf,(0,0),special_flags=BLEND_RGB_MULT)


	screen.blit(pygame.transform.scale(display,SCREEN_SIZE),(0,0))

	if home == False:
		player_status.render(screen)
	
	if pygame.mouse.get_pressed()[0]:
		home = False
		pygame.mouse.set_visible(False)

	if home == True:
		menu.render_text(main_menu,"Caryl's",'Minecraft.ttf',60,'white',[80,120])
		menu.render_text(main_menu,"MurkLand",'Minecraft.ttf',60,'white',[80,190])
		menu.render_text(main_menu,"'Click' To Start",'Minecraft.ttf',20,'white',[170,400])

	for event in pygame.event.get(): # event loop
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		
	screen.blit(main_menu,(0,0))
	pygame.display.update()
	clock.tick(FPS)
