import pygame
import pyperclip
import os
from sintactico import manejar_errores, resolver_matriz, extraer_matriz

WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entrada del Compilador")
font = pygame.font.Font(None, 36)

def capturar_cadena():
    """Captura entrada de texto y permite correcciones con soporte para movimiento del cursor."""
    input_text = ""
    cursor_pos = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        text_surface = font.render("Ingrese la matriz:", True, BLACK)
        screen.blit(text_surface, (20, 50))

        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (20, 100))

        cursor_x = font.size(input_text[:cursor_pos])[0] + 20
        pygame.draw.line(screen, BLACK, (cursor_x, 100), (cursor_x, 130), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text

                elif event.key == pygame.K_BACKSPACE and cursor_pos > 0:
                    input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                    cursor_pos -= 1

                elif event.key == pygame.K_LEFT and cursor_pos > 0:
                    cursor_pos -= 1  # Mueve el cursor a la izquierda
                
                elif event.key == pygame.K_RIGHT and cursor_pos < len(input_text):
                    cursor_pos += 1  # Mueve el cursor a la derecha

                elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    clipboard_text = pyperclip.paste()
                    input_text = input_text[:cursor_pos] + clipboard_text + input_text[cursor_pos:]
                    cursor_pos += len(clipboard_text)

                elif event.unicode.isprintable():
                    input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                    cursor_pos += 1

        clock.tick(30)
        
def preguntar_nueva_matriz():
    """Pregunta si el usuario quiere ingresar otra matriz."""
    screen.fill(WHITE)
    mensaje = font.render("¿Desea ingresar otra matriz? (S/N)", True, BLACK)
    screen.blit(mensaje, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
                elif event.key == pygame.K_n:
                    pygame.quit()
                    exit()

def main():
    while True:
        entrada = capturar_cadena()  # Captura la entrada del usuario

        # 🔹 Validar errores antes de procesar
        entrada_validada = manejar_errores(entrada, screen, font)

        # 🔹 Si la validación falló, volver a capturar la entrada
        if not entrada_validada:
            continue  # Se vuelve a capturar una nueva entrada sin resolver la matriz

        # 🔹 Resolver la matriz una vez corregida
        resultado = resolver_matriz(entrada_validada)

        # 🔹 Mostrar resultado en pantalla
        screen.fill(WHITE)
        resultado_surface = font.render(resultado, True, BLACK)
        screen.blit(resultado_surface, (20, 100))
        pygame.display.flip()
        pygame.time.delay(3000)

        # 🔹 Preguntar si desea ingresar otra matriz
        if not preguntar_nueva_matriz():
            break

main()


#  crea la siguiente matriz(-4x-6y-6z=9)(5x+3y-2z=4)(x-2y+z=-1)

#   crea la siguiente matriz(2x-3y+5z=12)(-1x+4y-2z=-5)(3x+2y+1z=8)

#   crea la siguiente matriz(2x+3y-4z=10)(x-2y+5z=7)(-3x+y+z=5)

#  =============  errores ========================

#   crea la siguiente matriz(2x+3y=8)(-x+4y-2z=5)(3a+2b=7)

#   crea la siguiente matriz(3x+2y+@z=5)(-x+4y-2a=7)

#  crea la siguiente matriz(-4x-6y-6z=9)(-4x-6y-6z=9)(-4x-6y-6z=9)