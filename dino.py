import pygame
#from pygame.locals import *
import sys
from sys import exit
import os
from random import randrange, choice
# import pygame_menu


pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640
ALTURA = 480

BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)


tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dino')


icones = pygame.image.load('imagens/tile.png').convert_alpha()
pygame.display.set_icon(icones)

sprite_sheet = pygame.image.load(os.path.join(
    diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(
    os.path.join(diretorio_sons, 'death_sound.wav'))
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(
    os.path.join(diretorio_sons, 'score_sound.wav'))
som_pontuacao.set_volume(1)

colidiu = False

escolha_obstaculo = choice([0, 1])

pontos = 0

velocidade_jogo = 10


def exibir_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)

    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

    
def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = ALTURA - 64 - 96//2
    dino.pulo = False
    dino_voador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obstaculo = choice([0, 1])
    
'''
def main_menu():
    while True:
        tela.fill((0, 0, 0))
        exibir_mensagem('Menu Do Dino', fonte, (255, 255, 255), tela, 20, 20)
        
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                config()
        
        pygame.draw.rect(tela, (255, 0, 0), button_1)
        pygame.draw.rect(tela, (255, 0, 0), button_2)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
    relogio.tick(60)
    pygame.display.update()

def game():
    run = True
    while run:
        tela.fill(255, 2, 50)

        exibir_mensagem('Dino', fonte, (255, 255, 255), tela, 20, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    relogio.tick(60)
    pygame.display.update() 

def config():
    run = True
    while run:
        tela.fill(255, 2, 50)

        exibir_mensagem('Configura????o', fonte, (255, 255, 255), tela, 20, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    relogio.tick(60)
    pygame.display.update()
'''




class Dino(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(
            os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)

        self.imagens_dinossauro = []

        for i in range(3):

            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos_y_inicial = ALTURA - 64 - 96 // 2
        self.rect.center = (100, ALTURA - 64)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        elif self.rect.y < self.pos_y_inicial:
            self.rect.y += 20
        else:
            self.rect.y = self.pos_y_inicial

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50, 200, 50)

        self.rect.x -= velocidade_jogo


class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.escolha = escolha_obstaculo

        self.rect.center = (LARGURA, ALTURA - 64)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo


class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagens_dinossauro = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)

        self.escolha = escolha_obstaculo

        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinossauro[int(self.index_lista)]


todos_as_sprites = pygame.sprite.Group()
dino = Dino()
todos_as_sprites.add(dino)


for i in range(4):
    nuvem = Nuvens()
    todos_as_sprites.add(nuvem)


for i in range(LARGURA * 2 // 64):
    chao = Chao(i)
    todos_as_sprites.add(chao)

cacto = Cacto()
todos_as_sprites.add(cacto)

dino_voador = DinoVoador()
todos_as_sprites.add(dino_voador)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cacto)
grupo_obstaculos.add(dino_voador)

relogio = pygame.time.Clock()

while True:

    relogio.tick(30)
    tela.fill(BRANCO)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(
        dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todos_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo == choice([0, 1])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1

        game_over = exibir_mensagem('GAME OVER - SEU RUIM', 50, (255, 6, 6))
        tela.blit(game_over, (LARGURA//2, ALTURA//2))
        restart = exibir_mensagem('Aperte (R) para Reiniciar', 20, (0, 0, 0))
        tela.blit(restart, (LARGURA//2, (ALTURA//2) + 60))

    else:
        pontos += 1
        todos_as_sprites.update()
        texto_pontos = exibir_mensagem(pontos, 40, (0, 0, 0))
        
    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade_jogo >= 23:
            velocidade_jogo += 0

        else:
            velocidade_jogo += 1
    if pontos + 100 and colidiu == True:
        score = exibir_mensagem(f'SCORE: {pontos}', 40, (0, 0, 128))
        tela.blit(score, (20, 20))
        if score == pontos:
            sco = exibir_mensagem(f'SCORE: {score}', 20, (0, 255, 0))

        todos_as_sprites.update()

    tela.blit(texto_pontos, (520, 30))

    pygame.display.flip()
