import os
import pygame

# Classe que controla o PAC
class Pacman:
    def __init__(self):
        self.animationpacman = []
        self.path_imgpac = 'assets/player_images'
        self.path_dir = os.listdir(self.path_imgpac)
        self.get_animation()

    def get_animation(self):
        for path in self.path_dir:
            imgs_path = os.path.join(self.path_imgpac,path) 
            lista = []
            for img_file in os.listdir(imgs_path):
                img_path = os.path.join(imgs_path,img_file)
                lista.append(pygame.transform.scale(pygame.image.load(img_path), (40, 40)))
            self.animationpacman.append(lista)
                      
    def animacao(self, posX, posY, direcao,animations):
        animation = []
        for i, image in enumerate(animations):
            image_rect = image.get_rect()
            image_rect.center = (posX, posY)
            if direcao == 'e':
                image = pygame.transform.rotate(image, 180)
            elif direcao == 'd':
                image = pygame.transform.rotate(image, 360)
            elif direcao == 'b':
                image = pygame.transform.rotate(image, 270)
            elif direcao == 'u':
                image = pygame.transform.rotate(image, 90)
            animation.append((image, image_rect))
        return animation

    def init_animacao(self, posX, posY,animations):
        animation = []
        for i, image in enumerate(animations):
            image_rect = image.get_rect()
            image_rect.center = (posX, posY)
            animation.append((image, image_rect))
        return animation
    
    def move_pac(self,move):
        dx = 0
        dy = 0
        direcao = 'e'
        if move == 'esquerda':
            dx = -5
            direcao = 'e'
        elif move == 'direita':
            move = 'direita'
            dx = 5
            direcao = 'd'
        elif move == 'cima':
            move = 'cima'
            dy = -5
            direcao = 'u'
        elif move == 'baixo':
            move = 'baixo'
            dy = 5
            direcao = 'b'
        else:
            pass
        return dx,dy,direcao