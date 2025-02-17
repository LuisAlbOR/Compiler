import pygame
import os
from lexer import get_tokens

# ====== Centramos la ventana ======
os.environ["SDL_VIDEO_CENTERED"] = "1"  # Centrar la ventana en Windows, Linux y Mac

# Configuración de la ventana
WIDTH, HEIGHT = 1400, 800  # Tamaño de la ventana
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def mostrar_tokens(entrada):
    tokens = get_tokens(entrada)  # Obtener tokens desde el lexer

    pygame.init()

    # Crear ventana centrada y ajustable
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Tabla de Tokens")

    font = pygame.font.Font(None, 28)  # Fuente más grande para mejor lectura
    running = True

    # Número de columnas y cálculo de filas necesarias
    columnas = 3  # Número de columnas para organizar los datos
    filas = (len(tokens) + columnas - 1) // columnas  # Cantidad de filas necesarias

    # Configuración de la pantalla
    margin_x = 50  # Margen izquierdo
    margin_y = 120  # Margen superior
    col_width = WIDTH // columnas  # Espacio por columna
    row_spacing = 45  # Más espacio entre filas para mayor claridad

    while running:
        screen.fill(BLACK)

        # Dibujar Encabezados con más espacio entre TOKEN y VALOR
        for i in range(columnas):
            header_token = font.render("TOKEN", True, WHITE)
            header_valor = font.render("VALOR", True, WHITE)
            screen.blit(header_token, (margin_x + i * col_width, 50))
            screen.blit(header_valor, (margin_x + i * col_width + 200, 50))  # Más espacio entre TOKEN y VALOR

        # Dibujar línea separadora
        pygame.draw.line(screen, WHITE, (margin_x, 80), (WIDTH - margin_x, 80), 2)  # Línea horizontal

        # Dibujar contenido de la tabla
        y_offset = margin_y  # Posición inicial en Y
        x_offset = margin_x  # Posición inicial en X

        for i, token in enumerate(tokens):
            token_name = font.render(token.type, True, WHITE)
            token_value = font.render(str(token.value), True, WHITE)

            screen.blit(token_name, (x_offset, y_offset))
            screen.blit(token_value, (x_offset + 200, y_offset))  # Más espacio entre TOKEN y VALOR

            y_offset += row_spacing  # Aumentamos el espacio entre filas

            # Si llegamos al final de una columna, saltamos a la siguiente
            if (i + 1) % filas == 0:
                x_offset += col_width
                y_offset = margin_y  # Reiniciar la posición en Y para la nueva columna

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
