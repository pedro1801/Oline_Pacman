import pygame
import sys
import os
import comidinha
import math
import networkx as nx
import random
import paho.mqtt.client as mqtt
import socket
import time

class clienteserver:

    def __init__(self):     
        def on_connect(client, userdata, flags, rc):
            print(f"Conectado ao broker com código {rc}")
            # Inscreve-se no tópico onde as mensagens do subscriber serão publicadas
            client.subscribe(self.local_ip)
        def on_message(client, userdata, msg):
            vetor = msg.payload.decode().split(':')
            if vetor[-1] == 'checkPos':
                self.oponeteposX = int(vetor[0])
                self.oponeteposY = int(vetor[1])
                self.oponetedirecao = vetor[2] 
            elif vetor[-1] == 'endGame':
                valores = (vetor[0],vetor[1])
                self.alltime.append(valores)
                print(self.alltime)
                print('Cria PopUp')
            if msg.payload.decode() == 'StartGame':
                self.startGame = True
        self.alltime =[]
        self.startGame = False
        self.oponeteposX = 320
        self.oponeteposY = 360
        self.oponetedirecao = 'e'        
        
        self.local_ip = socket.gethostbyname(socket.gethostname())
        
        self.client = mqtt.Client(client_id="Pedro")

        self.client.on_connect = on_connect
        self.client.on_message = on_message

        # Conecta ao broker (modificar endereço do broker conforme necessário)
        self.client.connect("localhost", 1883, 60)

        # Inicia o loop em segundo plano para manter a conexão e escutar mensagens
        self.client.loop_start()

    def playersPos(self,posX,posY,direcao):
        msg = f'{posX}:{posY}:{direcao}:playersPos:{self.local_ip}'
        self.client.publish('ServerPac',msg)
        
    def saveIP(self):
        msg = f'SaveIP:{self.local_ip}'
        self.client.publish("ServerPac", msg)
    
    def saveTime(self,tempo):
        msg = f'{tempo}:saveTime:{self.local_ip}'
        self.client.publish("ServerPac",msg)
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


client = clienteserver()
client.saveIP()
player = Pacman()

fantasma = Fantasminha()
circulos = comidinha.circles
circulos_colidios = []

posX = 640 // 2 
posY = 640 // 2 + 40

direcao = 'd'  # Direção inicial

# Inicializa a animação
animation = player.init_animacao(posX, posY,player.animationpacman[0])

animation2 = player.init_animacao(client.oponeteposX,client.oponeteposY,player.animationpacman[1])

clock = pygame.time.Clock()

animation_speed = 25

frame = 0

dx, dy = 0, 0  # Movimento padrão
move = None
click_points = []
checkpoints = []

# Inicialize o Pygame
pygame.init()
pygame.display.set_caption("Main")

# Defina o tamanho da tela
screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# Carregue a imagem de fundo
background_image = pygame.image.load('assets/map.PNG')

# Redimensione a imagem de fundo para manter a proporção
background_image = pygame.transform.scale(background_image, (640, 640))

# Calcule a posição para centralizar a imagem
image_rect = background_image.get_rect(center=(screen_width / 2, screen_height / 2))

# Crie uma instância da classe DrawRect
rects = DrawRect()

# Prepare superfícies transparentes para os retângulos
transparent_surfaces = [
    rects.create_transparent_surface(rect.width, rect.height, (255, 255, 255, 0))  # 50% de transparência
    for rect in rects.rectangles
]

def distancia(p1, p2):
    """Calcula a distância euclidiana entre dois pontos."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def colisao_circulo(circulos, pacman_rect):
    """Verifica se o Pacman colide com algum dos círculos e retorna o círculo colidido."""
    for circulo in circulos:
        (cx, cy), raio, _ = circulo
        if distancia((cx, cy), (pacman_rect.centerx, pacman_rect.centery )) < raio + max(pacman_rect.width - 10 , pacman_rect.height - 10 ) // 2:
            return circulo
    return None

# Função para verificar colisão com retângulos e ajustar a posição do Pacman
def handle_collision_and_teleport(posX, posY, rectangles, circulos, dx, dy):
    # Armazena as posições originais
    original_x, original_y = posX, posY
    posX += dx
    posY += dy

    pacman_rect = pygame.Rect(posX - 12, posY - 12, 20, 25)  # Considerando a largura e altura da animação do Pacman

    # Retângulos dos objetos de teleporte
    teleport_trigger_rect_esquerda = pygame.Rect(-20, 278, 5, 45)  # Retângulo do objeto de teleporte
    teleport_trigger_rect_direita = pygame.Rect(680, 278, 5, 45)

    # Verificar se Pacman colide com os objetos de teleporte
    if pacman_rect.colliderect(teleport_trigger_rect_esquerda):
        # Teleportar Pacman para o lado direito
        posX, posY = 640, 300  # Nova posição para teleporte
    elif pacman_rect.colliderect(teleport_trigger_rect_direita):
        # Teleportar Pacman para o lado esquerdo
        posX, posY = 0, 300  # Nova posição para teleporte
    else:
        for rect in rectangles:
            if pacman_rect.colliderect(rect):
                # Voltar para a posição original
                posX, posY = original_x, original_y
                # Ajustar a posição para evitar a colisão
                if dx > 0:  # Movimento para a direita
                    posX = rect.left - (pacman_rect.width + 5) // 2
                elif dx < 0:  # Movimento para a esquerda
                    posX = rect.right + (pacman_rect.width + 5) // 2
                if dy > 0:  # Movimento para baixo
                    posY = rect.top - (pacman_rect.height + 5) // 2
                elif dy < 0:  # Movimento para cima
                    posY = rect.bottom + (pacman_rect.height + 5) // 2
                break

            # Verificar colisão com círculos
    colidado = colisao_circulo(circulos, pacman_rect)
    
    return posX, posY, colidado

def ghost_collision(move,playerPos,ghostPos1,ghostPos2,ghostPos3,ghostPos4):
        pacman_rect = pygame.Rect(playerPos[0] - 12, playerPos[1] - 12, 20, 25)
        ghost_rect1 = pygame.Rect(ghostPos1[0] - 12, ghostPos1[1] - 12, 20, 25)
        ghost_rect2 = pygame.Rect(ghostPos2[0] - 12, ghostPos2[1] - 12, 20, 25)
        ghost_rect3 = pygame.Rect(ghostPos3[0] - 12, ghostPos3[1] - 12, 20, 25)
        ghost_rect4 = pygame.Rect(ghostPos4[0] - 12, ghostPos4[1] - 12, 20, 25)
        if pacman_rect.colliderect(ghost_rect1) or pacman_rect.colliderect(ghost_rect2) or pacman_rect.colliderect(ghost_rect3) or pacman_rect.colliderect(ghost_rect4):
            return 640 // 2 ,640 // 2 + 40, False
        else:
            return posX, posY, move
# Função para desenhar a reta entre dois pontos
def desenha_reta(screen, start, end):
    pygame.draw.line(screen, (255,255,255), start, end, 2)  # 2 é a espessura da linha
# Loop principal do jogo com colisão no Pacman
running = True
checktime = True
while running:
    if checktime and move != None:
        start_time = time.time()
        checktime = False
        
    if 5 == len(circulos_colidios):
        end_time = time.time()
        tempo = int(end_time-start_time)
        client.alltime.append((tempo,client.local_ip))
        client.saveTime(tempo)
        move = None
        client.startGame = False
        posX = 640 // 2 
        posY = 640 // 2 + 40
        direcao = 'd'  # Direção inicial
        circulos_colidios = []

    screen.blit(background_image, image_rect.topleft) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(checkpoints)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_points.append(event.pos)
            # Se houver dois pontos, desenha a reta
            if len(click_points) % 2 == 0:
               # pygame.draw.line(screen, (255,255,255), click_points[0], click_points[1], 2)
                checkpoints.append(tuple(click_points))
                click_points = []


    # Obtenha as teclas pressionadas
    keys = pygame.key.get_pressed()
    
    # Reinicie dx e dy antes de verificar as teclas
    dx, dy = 0, 0

    # Determine o deslocamento de acordo com a tecla pressionada
    if client.startGame:
        if keys[pygame.K_LEFT]:
            move = 'esquerda'      
        elif keys[pygame.K_RIGHT]:
            move = 'direita'
        elif keys[pygame.K_UP]:
            move = 'cima'
        elif keys[pygame.K_DOWN]:
            move = 'baixo'
        
    dx,dy,direcao = player.move_pac(move)
    fantasma.Ghostmovement1(move)
    fantasma.Ghostmovement2(move)
    fantasma.Ghostmovement3(move)
    fantasma.Ghostmovement4(move)

    posX, posY ,comida = handle_collision_and_teleport(posX, posY, rects.rectangles,circulos, dx, dy)
    if comida not in circulos_colidios:
        circulos_colidios.append(comida)
    # Atualize a animação de acordo com a direção

    for circle in circulos:
        if circle in circulos_colidios:
            position, radius, width = circle
            pygame.draw.circle(screen, (0,0,0), position, radius, width)
        else:
            position, radius, width = circle
            pygame.draw.circle(screen, (255,255,255), position, radius, width)
    posX, posY, move = ghost_collision(move,(posX,posY),fantasma.initFantasma1,fantasma.initFantasma2,fantasma.initFantasma3,fantasma.initFantasma4)

    animation = player.animacao(posX, posY, direcao,player.animationpacman[0])
    
    animation2 = player.animacao(client.oponeteposX,client.oponeteposY,client.oponetedirecao,player.animationpacman[1])

    client.playersPos(posX,posY,direcao)

    # Desenhe todos os retângulos transparentes
    for i, rect in enumerate(rects.rectangles):
        screen.blit(transparent_surfaces[i], rect.topleft)

    # Desenha a imagem atual do Pacman na tela
    current_image, current_rect = animation[frame]
    screen.blit(current_image, current_rect.topleft)
    
    current_image, current_rect = animation2[frame]
    screen.blit(current_image, current_rect.topleft)
    
    screen.blit(fantasma.Fantasmas1,(fantasma.initFantasma1[0]-15,fantasma.initFantasma1[1]-15))
    screen.blit(fantasma.Fantasmas2,(fantasma.initFantasma2[0]-15,fantasma.initFantasma2[1]-15))
    screen.blit(fantasma.Fantasmas3,(fantasma.initFantasma3[0]-15,fantasma.initFantasma3[1]-15))
    screen.blit(fantasma.Fantasmas4,(fantasma.initFantasma4[0]-15,fantasma.initFantasma4[1]-15))

    # Desenha todas as retas da lista
    #for reta in comidinha.reta_pares:
    #    start, end = reta
    #    pygame.draw.line(screen, (255, 255, 255), start, end, 2)  # 2 é a espessura da linha        
    for reta in checkpoints:
        start, end = reta
        pygame.draw.line(screen, (255, 0, 0), start, end, 2)  # 2 é a espessura da linha     
    # Atualize a tela
    pygame.display.flip()

    # Controle a velocidade da animação
    clock.tick(animation_speed)

    # Avance para a próxima imagem na animação
    frame = (frame + 1) % len(animation)  # Reinicia o ciclo quando chega à última imagem