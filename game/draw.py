import os
import pygame
                        
class DrawRect:
    def __init__(self):
        # Crie uma lista de retângulos
        self.rectangles = [
            #Bloco dos quadrados da esquerda
            pygame.Rect(60, 50, 65, 40), 
            pygame.Rect(60, 135, 65, 18), 
            pygame.Rect(175, 50, 85, 40), 

            #Blocos dos quadrados da direita
            pygame.Rect(520, 50, 60, 40),
            pygame.Rect(520, 135, 60, 15), 
            pygame.Rect(382, 52, 83, 38), 
            
            #Bordas
            pygame.Rect(310, 0, 20, 85), 
            pygame.Rect(320, 0, 310, 12), 
            pygame.Rect(0, 0, 310, 12),
            pygame.Rect(0, 0, 10, 200),
            pygame.Rect(630, 0, 10, 200),

            pygame.Rect(0, 395, 10, 240),

            pygame.Rect(0, 320, 120, 10),
            pygame.Rect(0, 390, 120, 10),
            pygame.Rect(110, 321, 13, 80),
            
            pygame.Rect(0, 630, 640, 10),

            pygame.Rect(0, 268, 120, 10),
            pygame.Rect(0, 195, 120, 10),
            pygame.Rect(110, 195, 13, 80),

            pygame.Rect(630, 398, 10, 235), 

            pygame.Rect(515, 318, 125, 10),
            pygame.Rect(515, 392, 125, 10),
            pygame.Rect(515, 321, 10, 80),

            pygame.Rect(515, 269, 125, 10),
            pygame.Rect(515, 196, 125, 10),
            pygame.Rect(515, 198, 10, 80),

            pygame.Rect(587, 505, 35, 20),
            pygame.Rect(20, 505, 35, 20),

            #T cima
            pygame.Rect(313, 135, 15, 77),
            pygame.Rect(243, 135, 155, 15),

            pygame.Rect(450, 135, 15, 140),
            pygame.Rect(380, 198, 60, 15),

            pygame.Rect(176, 135, 15, 140),
            pygame.Rect(200, 198, 60, 15),

            pygame.Rect(314, 384, 15, 77),
            pygame.Rect(245, 384, 150, 15),

            pygame.Rect(314, 508, 15, 77),
            pygame.Rect(245, 508, 150, 15),

            #Barras Meio
            pygame.Rect(450, 321, 15, 79),
            pygame.Rect(177, 321, 15, 79),

            #Barras Baixo
            pygame.Rect(384, 447, 80, 15),
            pygame.Rect(178, 447, 80, 15),

            # L baixo
            pygame.Rect(530, 447, 50, 15),
            pygame.Rect(520, 447, 15, 75),

            pygame.Rect(60, 447, 50, 15),
            pygame.Rect(107, 447, 15, 75),

            # Cacetete Baixo
            pygame.Rect(63, 570, 195, 15),
            pygame.Rect(175, 508, 15, 55),

            pygame.Rect(382, 570, 195, 15),
            pygame.Rect(450, 508, 15, 55),
            

            # Quadrado Meio
            pygame.Rect(240, 330, 160, 10),
            pygame.Rect(240, 258, 10, 72),
            pygame.Rect(248, 258, 50, 10),
            pygame.Rect(390, 258, 10, 72),
            pygame.Rect(342, 258, 50, 10),

            # Adicione mais retângulos conforme necessário
        ]

    def create_transparent_surface(self, width, height, color):
        # Crie uma superfície com transparência
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Preencha a superfície com a cor e transparência
        surface.fill(color)
        return surface