import pygame,os


class Tile_Set:
    def __init__(self,path):
        self.tile_asset = {}

        for folder in sorted(os.listdir(path)):
            file_list = []
            for files in sorted(os.listdir(f'{path}/{folder}')):
                image = pygame.image.load(f'{path}/{folder}/{files}').convert()
                image.set_colorkey((0,0,0))
                file_list.append(image)
            self.tile_asset[f'{folder}'] = file_list       
        
        

# tile_set = Tile_Set('../assets/tile_set')