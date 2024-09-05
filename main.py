import pygame
import sys
import os


# Classe que controla o PAC
class Pacman:
    def __init__(self):
        self.animationpacman = []
        self.path_imgpac = 'assets/player_images'
        self.imgsdir = os.listdir(self.path_imgpac)
        self.get_animation()

    def get_animation(self):
        for img_file in self.imgsdir:
            img_path = os.path.join(self.path_imgpac, img_file)
            self.animationpacman.append(pygame.transform.scale(pygame.image.load(img_path), (40, 40)))

    def animacao(self, posX, posY, direcao):
        animation = []
        for i, image in enumerate(self.animationpacman):
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

    def init_animacao(self, posX, posY):
        animation = []
        for i, image in enumerate(self.animationpacman):
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

        #screen.blit(fantasma.Fantasmas1,(260,285))
        #screen.blit(fantasma.Fantasmas2,(290,285))
        #screen.blit(fantasma.Fantasmas3,(320,285))
        #screen.blit(fantasma.Fantasmas4,(350,285))
    
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

# Inicialize o Pygame
pygame.init()

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
    rects.create_transparent_surface(rect.width, rect.height, (255, 255, 255, 128))  # 50% de transparência
    for rect in rects.rectangles
]

player = Pacman()
fantasma = Fantasminha()
# Inicializa a posição e a direção
posX = 640 // 2 
posY = 640 // 2 + 40
direcao = 'd'  # Direção inicial

# Inicializa a animação
animation = player.init_animacao(posX, posY)
clock = pygame.time.Clock()
animation_speed = 10
frame = 0

# Função para verificar colisão com retângulos e ajustar a posição do Pacman
def handle_collision_and_teleport(posX, posY, rectangles, dx, dy):
    # Armazena as posições originais
    original_x, original_y = posX, posY
    posX += dx
    posY += dy

    pacman_rect = pygame.Rect(posX - 12, posY - 12, 20, 25)  # Considerando a largura e altura da animação do Pacman
    # Verifique e ajuste a posição do Pacman para evitar colisão

    teleport_trigger_rect_esquerda = pygame.Rect(-20, 278, 5, 45)  # Retângulo do objeto de teleporte
    teleport_trigger_rect_direita = pygame.Rect(680, 278, 5, 45)

    # Verificar se Pacman colide com os objetos de teleporte
    if pacman_rect.colliderect(teleport_trigger_rect_esquerda):
        # Teleportar Pacman para o lado direito
        posX, posY = 640, 300  # Nova posição para teleporte
    elif pacman_rect.colliderect(teleport_trigger_rect_direita):
        # Teleportar Pacman para o lado esquerdo
        posX, posY = 0, 300  # Nova posição para teleporte

    # Ajustar a posição se houver colisão com retângulos normais
    else:
        for rect in rectangles:
            if pacman_rect.colliderect(rect):
                # Voltar para a posição original
                posX, posY = original_x, original_y
                # Ajustar a posição para evitar a colisão
                if dx > 0:  # Movimento para a direita
                    posX = rect.left - pacman_rect.width // 2
                elif dx < 0:  # Movimento para a esquerda
                    posX = rect.right + (pacman_rect.width + 5) // 2
                if dy > 0:  # Movimento para baixo
                    posY = rect.top - (pacman_rect.height + 5) // 2
                elif dy < 0:  # Movimento para cima
                    posY = rect.bottom + pacman_rect.height // 2
                break

    return posX, posY


# Loop principal do jogo com colisão no Pacman
running = True
dx, dy = 0, 0  # Movimento padrão
move = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtenha as teclas pressionadas
    keys = pygame.key.get_pressed()
    
    # Reinicie dx e dy antes de verificar as teclas
    dx, dy = 0, 0

    # Determine o deslocamento de acordo com a tecla pressionada
    if keys[pygame.K_LEFT]:
        move = 'esquerda'      
    elif keys[pygame.K_RIGHT]:
        move = 'direita'
    elif keys[pygame.K_UP]:
        move = 'cima'
    elif keys[pygame.K_DOWN]:
        move = 'baixo'
        
    dx,dy,direcao = player.move_pac(move)


    posX, posY = handle_collision_and_teleport(posX, posY, rects.rectangles, dx, dy)

    # Atualize a animação de acordo com a direção
    animation = player.animacao(posX, posY, direcao)

    # Preencha a tela com a imagem de fundo
    screen.blit(background_image, image_rect.topleft)
    # Desenhe todos os retângulos transparentes
    for i, rect in enumerate(rects.rectangles):
        screen.blit(transparent_surfaces[i], rect.topleft)

    # Desenha a imagem atual do Pacman na tela
    current_image, current_rect = animation[frame]
    screen.blit(current_image, current_rect.topleft)
    screen.blit(fantasma.Fantasmas1,(260,285))
    screen.blit(fantasma.Fantasmas2,(290,285))
    screen.blit(fantasma.Fantasmas3,(320,285))
    screen.blit(fantasma.Fantasmas4,(350,285))
    # Atualize a tela
    pygame.display.flip()

    # Controle a velocidade da animação
    clock.tick(animation_speed)

    # Avance para a próxima imagem na animação
    frame = (frame + 1) % len(animation)  # Reinicia o ciclo quando chega à última imagem