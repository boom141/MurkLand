import pygame


class Main_Menu:
    def __init__(self):
        pass

    def render_text(self,surface,text,font,font_size,color,position):
        font_setup = pygame.font.Font(f'./fonts/{font}', font_size)
        text = font_setup.render(text,False,color)
        surface.blit(text, (position[0],position[1]))

