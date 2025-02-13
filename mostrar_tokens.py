import pygame
from lexer import get_tokens

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ======= PROCESAR TOKENS =======
def mostrar_tokens(entrada):
    tokens = get_tokens(entrada)  # Obtener tokens desde el lexer

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tabla de Tokens")

    font = pygame.font.Font(None, 18)
    running = True

    while running:
        screen.fill(BLACK)

        # Encabezados de la tabla
        header_token = font.render("TOKEN", True, WHITE)
        header_valor = font.render("VALOR", True, WHITE)
        screen.blit(header_token, (50, 50))
        screen.blit(header_valor, (300, 50))

        # Configuración de la pantalla
        y_offset = 100  # Posición inicial en Y
        col1_x = 50     # Primera columna
        col2_x = 300    # Segunda columna
        col3_x = 550    # Tercera columna
        row_spacing = 30  # Espaciado entre filas

        # Determinar la cantidad de tokens por fila
        tokens_por_fila = (len(tokens) + 2) // 3  # Se divide en 3 filas

        for i, token in enumerate(tokens):
            token_name = font.render(token.type, True, WHITE)
            token_value = font.render(str(token.value), True, WHITE)

            if i % 3 == 0:  # Primera columna
                screen.blit(token_name, (col1_x, y_offset))
                screen.blit(token_value, (col1_x + 100, y_offset))
            elif i % 3 == 1:  # Segunda columna
                screen.blit(token_name, (col2_x, y_offset))
                screen.blit(token_value, (col2_x + 100, y_offset))
            else:  # Tercera columna
                screen.blit(token_name, (col3_x, y_offset))
                screen.blit(token_value, (col3_x + 100, y_offset))
                y_offset += row_spacing  # Aumentamos el espacio después de cada fila completa


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()