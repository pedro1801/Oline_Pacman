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

class DrawRect:
    def __init__(self):
        # Crie uma lista de retângulos
        self.rectangles = [
            #Bloco dos quadrados da esquerda
            pygame.Rect(85, 50, 55, 40), 
            pygame.Rect(85, 135, 55, 18), 
            pygame.Rect(190, 50, 75, 40), 
            #Blocos dos quadrados da direita
            pygame.Rect(500, 50, 55, 40),
            pygame.Rect(500, 135, 55, 15), 
            pygame.Rect(375, 52, 78, 38), 
            #Bordas
            pygame.Rect(312, 5, 20, 85), 
            pygame.Rect(320, 5, 290, 12), 
            pygame.Rect(30, 5, 290, 12),
            pygame.Rect(30, 5, 10, 200),
            pygame.Rect(600, 5, 10, 200),

            pygame.Rect(30, 395, 10, 240),

            pygame.Rect(10, 320, 120, 10),
            pygame.Rect(30, 390, 100, 10),
            pygame.Rect(130, 321, 13, 80),
            
            pygame.Rect(30, 630, 575, 10),

            pygame.Rect(10, 268, 120, 10),
            pygame.Rect(30, 195, 100, 10),
            pygame.Rect(130, 195, 13, 80),

            pygame.Rect(600, 398, 10, 235), 

            pygame.Rect(508, 318, 120, 10),
            pygame.Rect(508, 392, 100, 10),
            pygame.Rect(500, 321, 10, 80),

            pygame.Rect(508, 269, 120, 10),
            pygame.Rect(508, 196, 100, 10),
            pygame.Rect(500, 198, 10, 80),

            pygame.Rect(562, 505, 35, 20),
            pygame.Rect(45, 505, 35, 20),

            #T cima
            pygame.Rect(313, 135, 15, 77),
            pygame.Rect(252, 135, 139, 15),

            pygame.Rect(438, 135, 15, 140),
            pygame.Rect(375, 198, 60, 15),

            pygame.Rect(189, 135, 15, 140),
            pygame.Rect(207, 198, 60, 15),

            pygame.Rect(314, 384, 15, 77),
            pygame.Rect(252, 384, 138, 15),

            pygame.Rect(314, 508, 15, 77),
            pygame.Rect(252, 508, 138, 15),

            #Barras Meio
            pygame.Rect(438, 321, 15, 79),
            pygame.Rect(189, 321, 15, 79),

            #Barras Baixo
            pygame.Rect(376, 447, 76, 15),
            pygame.Rect(190, 447, 76, 15),

            # L baixo
            pygame.Rect(505, 447, 50, 15),
            pygame.Rect(500, 447, 15, 75),

            pygame.Rect(88, 447, 50, 15),
            pygame.Rect(127, 447, 15, 75),

            # Cacetete Baixo
            pygame.Rect(85, 570, 180, 15),
            pygame.Rect(189, 508, 15, 55),

            pygame.Rect(375, 570, 180, 15),
            pygame.Rect(438, 508, 15, 55),
            

            # Quadrado Meio
            pygame.Rect(250, 330, 140, 10),
            pygame.Rect(250, 258, 10, 72),
            pygame.Rect(250, 258, 50, 10),
            pygame.Rect(380, 258, 10, 72),
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

# Obtenha as dimensões da imagem original
original_width, original_height = background_image.get_size()

# Calcule a nova dimensão mantendo a proporção
if original_width / original_height > screen_width / screen_height:
    new_width = screen_width
    new_height = int(screen_width * original_height / original_width)
else:
    new_height = screen_height
    new_width = int(screen_height * original_width / original_height)

# Redimensione a imagem de fundo para manter a proporção
background_image = pygame.transform.scale(background_image, (new_width, new_height))

# Calcule a posição para centralizar a imagem
image_rect = background_image.get_rect(center=(screen_width / 2, screen_height / 2))

# Crie uma instância da classe DrawRect
rects = DrawRect()

# Prepare superfícies transparentes para os retângulos
transparent_surfaces = [
    rects.create_transparent_surface(rect.width, rect.height, (255, 255, 255, 0))  # 50% de transparência
    for rect in rects.rectangles
]

player = Pacman()
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
def handle_collision(posX, posY, rectangles, dx, dy):
    # Armazena as posições originais
    original_x, original_y = posX, posY
    posX += dx
    posY += dy

    pacman_rect = pygame.Rect(posX - 12, posY - 12, 25, 25)  # Considerando a largura e altura da animação do Pacman

    # Ajustar a posição se houver colisão com retângulos
    for rect in rectangles:
        if pacman_rect.colliderect(rect):
            # Voltar para a posição original
            posX, posY = original_x, original_y
            # Ajustar a posição para evitar a colisão
            if dx > 0:  # Movimento para a direita
                posX = rect.left - pacman_rect.width // 2
            elif dx < 0:  # Movimento para a esquerda
                posX = rect.right + pacman_rect.width // 2
            if dy > 0:  # Movimento para baixo
                posY = rect.top - pacman_rect.height // 2
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
    # Verifique e ajuste a posição do Pacman para evitar colisão
    posX, posY = handle_collision(posX, posY, rects.rectangles, dx, dy)

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

    # Atualize a tela
    pygame.display.flip()

    # Controle a velocidade da animação
    clock.tick(animation_speed)

    # Avance para a próxima imagem na animação
    frame = (frame + 1) % len(animation)  # Reinicia o ciclo quando chega à última imagem