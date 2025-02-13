import pygame
from paser import parse_input
from lexer import get_tokens  # Importamos el lexer para obtener los tokens
from mostrar_tokens import mostrar_tokens

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entrada del Compilador")

font = pygame.font.Font(None, 36)

# Variables para capturar el texto
input_text = ""
running = True

# ======= PRIMERA PANTALLA: INGRESO DE TEXTO =======
while running:
    screen.fill(WHITE)
    
    text_surface = font.render("Ingrese la cadena:", True, BLACK)
    input_surface = font.render(input_text, True, BLACK)
    
    screen.blit(text_surface, (20, 50))
    screen.blit(input_surface, (20, 100))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter -> Procesar entrada
                running = False
                mostrar_tokens(input_text)
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

pygame.quit()
