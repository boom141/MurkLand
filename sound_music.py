import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)

class Sfx_Sound():
    def __init__(self,path):
        self.sound = pygame.mixer.Sound(path)

    def play_sound(self,loop,volume):
        self.sound.set_volume(volume)
        self.sound.play(loop)

class Sfx_Music():
    pass