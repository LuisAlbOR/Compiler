import pygame
import pyperclip  # Biblioteca para acceder al portapapeles
from paser import parse_input
from lexer import get_tokens  # Importamos el lexer para obtener los tokens
from mostrar_tokens import mostrar_tokens

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 550
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entrada del Compilador")

font = pygame.font.Font(None, 36)

# Variables para capturar el texto
input_text = ""
cursor_pos = 0  # Posición del cursor dentro del texto
running = True
cursor_visible = True
clock = pygame.time.Clock()

# Temporizador para parpadeo del cursor
cursor_timer = 0

# ======= PRIMERA PANTALLA: INGRESO DE TEXTO =======
while running:
    screen.fill(WHITE)
    
    text_surface = font.render("Ingrese la cadena:", True, BLACK)
    input_surface = font.render(input_text, True, BLACK)
    
    screen.blit(text_surface, (20, 50))
    screen.blit(input_surface, (20, 100))
    
    # Obtener la posición del cursor en píxeles
    cursor_x = font.size(input_text[:cursor_pos])[0] + 20  # Calcular el ancho hasta el cursor
    
    # Hacer parpadear el cursor cada 500ms
    cursor_timer += clock.get_time()
    if cursor_timer >= 500:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    # Dibujar cursor si está visible
    if cursor_visible:
        pygame.draw.line(screen, BLACK, (cursor_x, 100), (cursor_x, 130), 2)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter -> Procesar entrada
                running = False
                mostrar_tokens(input_text)
            elif event.key == pygame.K_BACKSPACE:  # Borrar caracter antes del cursor
                if cursor_pos > 0:
                    input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                    cursor_pos -= 1
            elif event.key == pygame.K_DELETE:  # Borrar caracter después del cursor
                if cursor_pos < len(input_text):
                    input_text = input_text[:cursor_pos] + input_text[cursor_pos + 1:]
            elif event.key == pygame.K_LEFT:  # Mover cursor a la izquierda
                if cursor_pos > 0:
                    cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:  # Mover cursor a la derecha
                if cursor_pos < len(input_text):
                    cursor_pos += 1
            elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_META or pygame.key.get_mods() & pygame.KMOD_CTRL):
                # Pegar texto (Cmd+V en Mac / Ctrl+V en Windows/Linux)
                clipboard_text = pyperclip.paste()
                input_text = input_text[:cursor_pos] + clipboard_text + input_text[cursor_pos:]
                cursor_pos += len(clipboard_text)
            elif event.key == pygame.K_c and (pygame.key.get_mods() & pygame.KMOD_META or pygame.key.get_mods() & pygame.KMOD_CTRL):
                # Copiar texto (Cmd+C en Mac / Ctrl+C en Windows/Linux)
                pyperclip.copy(input_text)
            else:  # Insertar caracter en la posición actual del cursor
                input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                cursor_pos += 1

    clock.tick(30)  # Control de velocidad de actualización

pygame.quit()
# crea la siguiente matriz(-4x-6y-6z=9)(-4x-6y-6z=9)(-4x-6y-6z=9)
