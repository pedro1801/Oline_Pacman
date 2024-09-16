import os
import pygame
import networkx as nx
import random
from game import comidinha


# Classe para controle dos Fantasmas
class Fantasminha:
    def __init__(self):
        self.Fantasmas1 = pygame.image.load('assets/ghost_images/blue.png')
        self.Fantasmas1 = pygame.transform.scale(self.Fantasmas1,(30,30))
        self.Fantasmas2 = pygame.image.load('assets/ghost_images/red.png')
        self.Fantasmas2 = pygame.transform.scale(self.Fantasmas2,(30,30))
        self.Fantasmas3 = pygame.image.load('assets/ghost_images/pink.png')
        self.Fantasmas3 = pygame.transform.scale(self.Fantasmas3,(30,30))
        self.Fantasmas4 = pygame.image.load('assets/ghost_images/orange.png')
        self.Fantasmas4 = pygame.transform.scale(self.Fantasmas4,(30,30))
        
        self.qtdCaminhoanterior1 = 0
        self.qtdCaminhoposterior1 = 0
        self.qtdCaminhoanterior2 = 0
        self.qtdCaminhoposterior2 = 0
        self.qtdCaminhoanterior3 = 0
        self.qtdCaminhoposterior3 = 0
        self.qtdCaminhoanterior4 = 0
        self.qtdCaminhoposterior4 = 0
        
        self.caminho1 = []
        self.caminho2 = []
        self.caminho3 = []
        self.caminho4 = []
        
        self.start1 = 320
        self.end1 = 295
        
        self.start2 = 320
        self.end2 = 295
        self.start3 = 320
        self.end3 = 295
        self.start4 = 320
        self.end4 = 295
        
        self.initFantasma1 = (self.start1, self.end1)
        self.initFantasma2 = (self.start2, self.end2)
        self.initFantasma3 = (self.start3, self.end3)
        self.initFantasma4 = (self.start4, self.end4)
        
        self.chegada1 = self.initFantasma1
        self.chegada2 = self.initFantasma1
        self.chegada3 = self.initFantasma1
        self.chegada4 = self.initFantasma1
        
        self.G = nx.Graph()
        
        self.retas = comidinha.reta_pares
        # Adiciona as arestas (linhas entre os pontos)
        for (p1, p2) in self.retas:
            self.G.add_edge(p1, p2)

    def Ghostmovement1(self,move):
        if move:
            start = self.initFantasma1
            end = self.retas[random.randint(0,int(len(self.retas)-1))][0]
            
            if self.chegada1 == self.initFantasma1:
                try:
                    self.caminho1 = nx.shortest_path(self.G, source=start, target=end)
                except nx.NetworkXNoPath:
                    print(f"Não existe caminho entre {start} e {end}")
                self.chegada1 = end
                self.qtdCaminhoanterior1 = 0
                self.qtdCaminhoposterior1 = 1
            else:
                if self.caminho1[self.qtdCaminhoanterior1][0] == self.caminho1[self.qtdCaminhoposterior1][0]:
                    if self.caminho1[self.qtdCaminhoanterior1][1] < self.caminho1[self.qtdCaminhoposterior1][1]:
                        self.end1+=5
                    else:
                        self.end1-=5
                    if self.end1 == self.caminho1[self.qtdCaminhoposterior1][1]:
                        self.qtdCaminhoanterior1+=1
                        self.qtdCaminhoposterior1+=1
                    self.initFantasma1 = (self.start1,self.end1)
                else:
                    if self.start1 < self.caminho1[self.qtdCaminhoposterior1][0]:
                        self.start1+=5
                    else:
                        self.start1-=5
                    if self.start1 == self.caminho1[self.qtdCaminhoposterior1][0]:
                        self.qtdCaminhoanterior1+=1
                        self.qtdCaminhoposterior1+=1
                    self.initFantasma1 = (self.start1,self.end1)
    
    def Ghostmovement2(self,move):
        if move:
            start = self.initFantasma2
            end = self.retas[random.randint(0,int(len(self.retas)-1))][0]
            
            if self.chegada2 == self.initFantasma2:
                try:
                    self.caminho2 = nx.shortest_path(self.G, source=start, target=end)
                except nx.NetworkXNoPath:
                    print(f"Não existe caminho entre {start} e {end}")
                self.chegada2 = end
                self.qtdCaminhoanterior2 = 0
                self.qtdCaminhoposterior2 = 1
            else:
                if self.caminho2[self.qtdCaminhoanterior2][0] == self.caminho2[self.qtdCaminhoposterior2][0]:
                    if self.caminho2[self.qtdCaminhoanterior2][1] < self.caminho2[self.qtdCaminhoposterior2][1]:
                        self.end2+=5
                    else:
                        self.end2-=5
                    if self.end2 == self.caminho2[self.qtdCaminhoposterior2][1]:
                        self.qtdCaminhoanterior2+=1
                        self.qtdCaminhoposterior2+=1
                    self.initFantasma2 = (self.start2,self.end2)
                else:
                    if self.start2 < self.caminho2[self.qtdCaminhoposterior2][0]:
                        self.start2+=5
                    else:
                        self.start2-=5
                    if self.start2 == self.caminho2[self.qtdCaminhoposterior2][0]:
                        self.qtdCaminhoanterior2+=1
                        self.qtdCaminhoposterior2+=1
                    self.initFantasma2 = (self.start2,self.end2)
                
    def Ghostmovement3(self,move):
        if move:
            start = self.initFantasma3
            end = self.retas[random.randint(0,int(len(self.retas)-1))][0]
            
            if self.chegada3 == self.initFantasma3:
                try:
                    self.caminho3 = nx.shortest_path(self.G, source=start, target=end)
                except nx.NetworkXNoPath:
                    print(f"Não existe caminho entre {start} e {end}")
                self.chegada3 = end
                self.qtdCaminhoanterior3 = 0
                self.qtdCaminhoposterior3 = 1
            else:
                if self.caminho3[self.qtdCaminhoanterior3][0] == self.caminho3[self.qtdCaminhoposterior3][0]:
                    if self.caminho3[self.qtdCaminhoanterior3][1] < self.caminho3[self.qtdCaminhoposterior3][1]:
                        self.end3+=5
                    else:
                        self.end3-=5
                    if self.end3 == self.caminho3[self.qtdCaminhoposterior3][1]:
                        self.qtdCaminhoanterior3+=1
                        self.qtdCaminhoposterior3+=1
                    self.initFantasma3 = (self.start3,self.end3)
                else:
                    if self.start3 < self.caminho3[self.qtdCaminhoposterior3][0]:
                        self.start3+=5
                    else:
                        self.start3-=5
                    if self.start3 == self.caminho3[self.qtdCaminhoposterior3][0]:
                        self.qtdCaminhoanterior3+=1
                        self.qtdCaminhoposterior3+=1
                    self.initFantasma3 = (self.start3,self.end3)

    def Ghostmovement4(self,move):
        if move:
            start = self.initFantasma4
            end = self.retas[random.randint(0,int(len(self.retas)-1))][0]
            
            if self.chegada4 == self.initFantasma4:
                try:
                    self.caminho4 = nx.shortest_path(self.G, source=start, target=end)
                except nx.NetworkXNoPath:
                    print(f"Não existe caminho entre {start} e {end}")
                self.chegada4 = end
                self.qtdCaminhoanterior4 = 0
                self.qtdCaminhoposterior4 = 1
            else:
                if self.caminho4[self.qtdCaminhoanterior4][0] == self.caminho4[self.qtdCaminhoposterior4][0]:
                    if self.caminho4[self.qtdCaminhoanterior4][1] < self.caminho4[self.qtdCaminhoposterior4][1]:
                        self.end4+=5
                    else:
                        self.end4-=5
                    if self.end4 == self.caminho4[self.qtdCaminhoposterior4][1]:
                        self.qtdCaminhoanterior4+=1
                        self.qtdCaminhoposterior4+=1
                    self.initFantasma4 = (self.start4,self.end4)
                else:
                    if self.start4 < self.caminho4[self.qtdCaminhoposterior4][0]:
                        self.start4+=5
                    else:
                        self.start4-=5
                    if self.start4 == self.caminho4[self.qtdCaminhoposterior4][0]:
                        self.qtdCaminhoanterior4+=1
                        self.qtdCaminhoposterior4+=1
                    self.initFantasma4 = (self.start4,self.end4)