import pygame

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
screen = pygame.display.set_mode((640, 480))

# Define as cores em formato RGB
white = (255, 255, 255)
blue = (255, 255, 255)

circles = [

    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
    ((100, 100), 5, 0),   # Círculo preenchido com raio 30
    ((200, 150), 5, 0),   # Círculo com contorno de espessura 5 e raio 50
    ((300, 250), 5, 0),   # Círculo preenchido com raio 40
    ((400, 300), 5, 0),  # Círculo com contorno de espessura 10 e raio 60
    ((500, 350), 5, 0),   # Círculo com contorno de espessura 3 e raio 20
]

# Loop principal do Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preenche o fundo com branco
    screen.fill(white)

    # Desenha todos os círculos da lista
    for circle in circles:
        position, radius, width = circle
        pygame.draw.circle(screen, blue, position, radius, width)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
