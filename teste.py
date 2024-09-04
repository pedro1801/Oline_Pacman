import pygame
import sys

class DrawRect:
    def __init__(self):
        # Crie uma lista de retângulos
        self.rectangles = [
            pygame.Rect(90, 55, 60, 45), # quadro canto esquerdo superior
            pygame.Rect(90, 135, 60, 25), # quadro canto esquerdo inferior
            pygame.Rect(190, 55, 80, 45), # quadro canto esquerdo superior lado
            pygame.Rect(492, 55, 60, 45), # quadro canto direito superior
            pygame.Rect(492, 135, 60, 25), # quadro canto direito inferior
            pygame.Rect(372, 55, 80, 45), # quadro canto direito superior lado
            pygame.Rect(312, 5, 20, 90), # meio superior
            pygame.Rect(312, 5, 290, 12), # lado direito superior
            pygame.Rect(40, 5, 290, 12), # lado esquerdo superior 
            pygame.Rect(40, 5, 10, 200),
            pygame.Rect(595, 5, 10, 200),
            pygame.Rect(430, 135, 22, 145),
            pygame.Rect(190, 135, 20, 145),
            pygame.Rect(372, 195, 60, 25),
            pygame.Rect(210, 195, 60, 25),
            pygame.Rect(432, 320, 20, 80),
            pygame.Rect(190, 320, 20, 80),
            pygame.Rect(372, 441, 80, 20),
            pygame.Rect(190, 441, 80, 20),
            pygame.Rect(505, 441, 50, 20),
            pygame.Rect(493, 441, 22, 80),
            pygame.Rect(90, 441, 50, 20),
            pygame.Rect(128, 441, 22, 80),
            pygame.Rect(312, 135, 20, 85),
            pygame.Rect(250, 138, 142, 20),
            pygame.Rect(312, 380, 20, 82),
            pygame.Rect(250, 380, 142, 20),
            pygame.Rect(312, 501, 20, 82),
            pygame.Rect(250, 501, 142, 20),
            pygame.Rect(40, 400, 10, 230),
            pygame.Rect(595, 400, 10, 230),
            pygame.Rect(40, 620, 555, 10),
            pygame.Rect(40, 320, 100, 10),
            pygame.Rect(40, 390, 100, 10),
            pygame.Rect(40, 270, 100, 10),
            pygame.Rect(40, 198, 100, 10),
            pygame.Rect(140, 198, 10, 82),
            pygame.Rect(140, 321, 10, 80),
            pygame.Rect(500, 320, 100, 10),
            pygame.Rect(500, 390, 100, 10),
            pygame.Rect(500, 270, 100, 10),
            pygame.Rect(500, 198, 100, 10),
            pygame.Rect(495, 198, 10, 82),
            pygame.Rect(495, 321, 10, 80),
            pygame.Rect(90, 560, 180, 22),
            pygame.Rect(370, 560, 182, 22),
            pygame.Rect(432, 500, 20, 60),
            pygame.Rect(190, 500, 20, 60),
            pygame.Rect(550, 502, 50, 22),
            pygame.Rect(40, 502, 50, 22),
            pygame.Rect(250, 330, 145, 10),
            pygame.Rect(250, 255, 10, 75),
            pygame.Rect(250, 258, 50, 10),
            pygame.Rect(380, 255, 10, 75),
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
    rects.create_transparent_surface(rect.width, rect.height, (255, 255, 255, 128))  # 50% de transparência
    for rect in rects.rectangles
]

# Crie o quadrado controlável
square_size = 30
square = pygame.Rect(100, 100, square_size, square_size)
square_color = (0, 0, 255)  # Azul
square_speed = 1

# Função para verificar colisão com retângulos e ajustar a posição
def handle_collision(square, rectangles, dx, dy):
    original_x, original_y = square.topleft
    square.x += dx
    square.y += dy
    # Ajustar x se houver colisão com retângulos
    for rect in rectangles:
        if square.colliderect(rect):
            # Voltar para a posição original
            square.topleft = (original_x, original_y)
            # Ajustar a posição para evitar a colisão
            if dx > 0:  # Movimento para a direita
                square.right = rect.left
            elif dx < 0:  # Movimento para a esquerda
                square.left = rect.right
            if dy > 0:  # Movimento para baixo
                square.bottom = rect.top
            elif dy < 0:  # Movimento para cima
                square.top = rect.bottom
    return square

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtenha as teclas pressionadas
    keys = pygame.key.get_pressed()
    
    # Determine o deslocamento
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT]:
        dx = -square_speed
    if keys[pygame.K_RIGHT]:
        dx = square_speed
    if keys[pygame.K_UP]:
        dy = -square_speed
    if keys[pygame.K_DOWN]:
        dy = square_speed

    # Verifique e ajuste a posição do quadrado para evitar colisão
    square = handle_collision(square, rects.rectangles, dx, dy)

    # Preencha a tela com a imagem de fundo
    screen.blit(background_image, image_rect.topleft)
    
    # Desenhe todos os retângulos transparentes
    for i, rect in enumerate(rects.rectangles):
        screen.blit(transparent_surfaces[i], rect.topleft)

    # Desenhe o quadrado controlável
    pygame.draw.rect(screen, square_color, square)

    # Atualize a tela
    pygame.display.flip()
