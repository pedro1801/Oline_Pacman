import pygame
import sys
import game.comidinha as comidinha
import math
import paho.mqtt.client as mqtt
import socket
import time
from game.pacman import Pacman
from game.fantasminha import Fantasminha
from game.draw import DrawRect

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
                self.all_players_finished = True
            if msg.payload.decode() == 'StartGame':
                self.startGame = True
        
        self.all_players_finished = False
        self.alltime =[]
        self.startGame = False
        self.oponeteposX = 320
        self.oponeteposY = 360
        self.oponetedirecao = 'e'        
        
        self.local_ip = "192.168.1.12"
        
        self.client = mqtt.Client(client_id="Joao")

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
        
    # def reset_game(self):
    #     self.all_players_finished = False
    #     self.alltime = []
    #     self.startGame = False
    #     self.oponeteposX = 320
    #     self.oponeteposY = 360
    #     self.oponetedirecao = 'e'

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
pygame.display.set_caption("Main1")

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

# Função para desenhar placar de pontos
def desenha_placar(screen, scores):
    screen.fill((0, 0, 0))  # Preenche a tela com preto
    font = pygame.font.SysFont(None, 36)
    title = font.render("Placar Final", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

    for i, (tempo, ip) in enumerate(scores):
        text = font.render(f"{ip}: {tempo}s", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100 + i * 40))

    button_font = pygame.font.SysFont(None, 28)
    play_again_button = pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_again_button)
    play_again_text = button_font.render("Jogar Novamente", True, (0, 0, 0))
    screen.blit(play_again_text, (play_again_button.x + 20, play_again_button.y + 10))

    disconnect_button = pygame.Rect(screen_width // 2 - 100, screen_height - 40, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), disconnect_button)
    disconnect_text = button_font.render("Desconectar", True, (0, 0, 0))
    screen.blit(disconnect_text, (disconnect_button.x + 40, disconnect_button.y + 10))

    return play_again_button, disconnect_button

# Loop principal do jogo com colisão no Pacman
running = True
checktime = True
game_over = False

while running:
    if checktime and move != None:
        start_time = time.time()
        checktime = False
        
    if 5 == len(circulos_colidios):
        move = None
        end_time = time.time()
        tempo = int(end_time-start_time)
        client.alltime.append((tempo,client.local_ip))
        client.saveTime(tempo)
        posX = 640 // 2 
        posY = 640 // 2 + 40
        direcao = 'd'  # Direção inicial
        circulos_colidios = []
        game_over = True

    screen.blit(background_image, image_rect.topleft)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(checkpoints)
            pygame.quit()
            sys.exit()
        if game_over and client.all_players_finished:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_points.append(event.pos)
                # Se houver dois pontos, desenha a reta
                if len(click_points) % 2 == 0:
                # pygame.draw.line(screen, (255,255,255), click_points[0], click_points[1], 2)
                    checkpoints.append(tuple(click_points))
                    click_points = []
                if play_again_button.collidepoint(event.pos):
                    game_over = False
                    checktime = True
                    client.alltime = []
                elif disconnect_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    if not game_over:
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
    
    elif client.all_players_finished:
        play_again_button, disconnect_button = desenha_placar(screen, client.alltime)
    
    pygame.display.flip()
    clock.tick(animation_speed)

pygame.quit()
sys.exit()

pygame.quit()
sys.exit()