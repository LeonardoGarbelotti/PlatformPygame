import pygame
import sys
import os
import math

'''
Objetos
'''
class Plataforma(pygame.sprite.Sprite):
    # Passa como argumento a localização cartesiana, tamanho e imagem
    def __init__(self,xloc,yloc,imgw,imgh,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',img)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

class Heroi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0  # variavel que anda por x
        self.movey = 0  # variavel que anda por y
        self.frame = 0
        self.noChao = False
        self.health = 1000  # vida do personagem
        self.images = []  # array das imagens

        #WALK CYCLE
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images','hero' + str(i) + '.gif')).convert_alpha()
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()


    def controlaMovimento(self, x, y):
        self.movex += x
        self.movey += y

    def update(self):
        self.rect.x = self.rect.x + self.movex
        if(self.rect.y < 350):
            self.movey += 0.5
        self.rect.y = self.rect.y + self.movey

        # andando pra esquerda
        if self.movex < 0:
            self.frame += 1
            if self.frame > ani*3:
                self.frame = 0
            self.image = self.images[self.frame//ani]

        # andando pra direita
        if self.movex > 0:
            self.frame += 1
            if self.frame > ani*3:
                self.frame = 0
            self.image = self.images[self.frame//ani]


         # colisões
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for monstro in enemy_hit_list:
            self.health -= 1
            print(self.health)

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.noChao = True

            if (self.noChao == True):
                self.rect.y = 350


class Monstro(pygame.sprite.Sprite):
    def __init__(self, x , y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',img))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def movimentaMonstro(self):
        distancia = 50
        velocidade = 5

        if self.counter >= 0 and self.counter <= distancia:
            self.rect.x += velocidade
        elif self.counter >= distancia and self.counter <= distancia*2:
            self.rect.x -= velocidade
        else:
            self.counter = 0

        self.counter += 1

class Level():
    def bad(lvl, eloc):
        if lvl == 1:
            enemy = Monstro(eloc[0],eloc[1],'yeti.png')  # cria um yeti
            enemy_list = pygame.sprite.Group()  # cria grupo de monstro
            enemy_list.add(enemy)              # adiciona o monstro ao grupo

        if lvl == 2:
            print("Level " + str(lvl) )

        return enemy_list

    def terreno(lvl, gloc, tx, ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(gloc):
                ground = Plataforma(gloc[i], alturaTela-ty, tx, ty, 'ground.png')
                ground_list.add(ground)
                i = i+1

        if lvl == 2:
            print("Level " + str(lvl))

        return ground_list

    def plataforma(lvl, tx, ty):
        plat_list = pygame.sprite.Group()
        ploc = []
        i = 0
        if lvl == 1:
            #  ploc.append((200, worldy - ty - 128, 3))
            ploc.append((300, alturaTela - ty - 256, 3))
            #ploc.append((500, alturaTela - ty - 128, 4))
            while i < len(ploc):
                j = 0
                while j <= ploc[i][2]:
                    plat = Plataforma((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, 'tile.png')
                    plat_list.add(plat)
                    j = j + 1

                i = i + 1

        if lvl == 2:
            print("Level " + str(lvl))

        return plat_list
'''
CONFIGURAÇÕES
'''
larguraTela = 960
alturaTela = 480

fps = 40  # frame rate
ani = 4  # ciclos de animação
clock = pygame.time.Clock()
pygame.init()


AZUL = (0, 0, 255)
VERMELHO = (255,0,0)
VERDE = (0, 255, 0)
PRETO = (23,23,23 )
BRANCO = (254,254,254)

tela = pygame.display.set_mode([larguraTela, alturaTela])
planoFundo = pygame.image.load(os.path.join('images','stage.png')).convert()
planoFundoBox = tela.get_rect()

heroi = Heroi()  # instancia novo heroi
heroi.rect.x = 30  # posição em X do inicio
heroi.rect.y = 350  # posição em Y do inicio
player_list = pygame.sprite.Group()
player_list.add(heroi)
passos = 10  # passos por vez

eloc = []  # cria variável
eloc = [500,335]  # localização do Monstro na tela

gloc = []  # variavel do terreno
tx = 64  # tamanho em X do bloco
ty = 64  # tammanho em Y do bloco

i=0
while i <= (larguraTela/tx)+tx:
    gloc.append(i*tx)
    i = i+1


enemy_list = Level.bad(1, eloc )
ground_list = Level.terreno(1, gloc, tx, ty)
plat_list = Level.plataforma(1, tx, ty)

contPulo = 2
'''
Main loop
'''
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                heroi.controlaMovimento(-passos,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                heroi.controlaMovimento(passos,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                heroi.controlaMovimento(0, -passos)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                heroi.controlaMovimento(passos,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                heroi.controlaMovimento(-passos,0)
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()



    tela.blit(planoFundo, planoFundoBox)
    heroi.update()
    player_list.draw(tela)  # desenha o personagem
    enemy_list.draw(tela)  # desenha inimigos
    ground_list.draw(tela)  # desenha o chão
    plat_list.draw(tela)  # desenha as plataformas
    for e in enemy_list:
        e.movimentaMonstro()
    pygame.display.flip()
    clock.tick(fps)
