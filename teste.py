import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configura a tela
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Exemplo de Pop-up")

# Define cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Função para desenhar o pop-up
def draw_popup(screen, message):
    # Dimensões do pop-up
    popup_width = 400
    popup_height = 200

    # Calcula a posição central do pop-up
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2

    # Desenha um retângulo para o pop-up
    pygame.draw.rect(screen, GRAY, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 5)

    # Fonte para o texto
    font = pygame.font.SysFont(None, 36)

    # Renderiza o texto
    text = font.render(message, True, BLACK)
    
    # Centraliza o texto no pop-up
    text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
    screen.blit(text, text_rect)

    # Botão de "OK"
    button_rect = pygame.Rect(popup_x + popup_width // 2 - 50, popup_y + popup_height - 60, 100, 40)
    pygame.draw.rect(screen, WHITE, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)
    
    button_text = font.render("OK", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    return button_rect

# Loop principal
running = True
popup_active = True
while running:
    screen.fill(WHITE)

    # Se o pop-up está ativo, desenhá-lo
    if popup_active:
        button_rect = draw_popup(screen, "Este é um pop-up!")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and popup_active:
            # Verifica se o botão "OK" foi clicado
            if button_rect.collidepoint(event.pos):
                popup_active = False

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
