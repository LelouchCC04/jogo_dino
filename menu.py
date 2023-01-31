import pygame
import pygame_menu
import sys
from pygame_menu import sound
#import dino
#from dino import *


#print(pygame.font.get_fonts())

pygame.init()

surface = pygame.display.set_mode((600, 400))


def set_dificuldade(value, dificuldade):
    '''if pontos == 2000 and colidiu == False:
        velocidade_jogo + 10
    '''
    pass

def iniciando_jogo():
    runfile(r'dino.py')
    # Do the job here !
    pass

while True:
    menu = pygame_menu.Menu('DINO', 400, 300,
                        theme=pygame_menu.themes.THEME_DARK)

    menu.add.text_input('Name :', default=' ')
    menu.add.selector('Dificuldade :', [('Dificil', 1), ('Facil', 2)], onchange=set_dificuldade)
    menu.add.button('Iniciar', iniciando_jogo)
    menu.add.button('Sair', pygame_menu.events.BACK)


    menu.mainloop(surface)

