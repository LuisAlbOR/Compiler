
import pygame
import pyperclip
import numpy as np
import re

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 550
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entrada del Compilador")
font = pygame.font.Font(None, 36)

def detectar_errores(entrada):
    errores = []
    caracteres_invalidos = re.findall(r'([^0-9xyz\s\+\-\=\(\)])', entrada)
    if caracteres_invalidos:
        errores.append(f"Error: Caracteres no válidos encontrados: {', '.join(set(caracteres_invalidos))}")
    num_abiertos = entrada.count('(')
    num_cerrados = entrada.count(')')
    if num_abiertos < 3:
        errores.append(f"Error: Faltan {3 - num_abiertos} paréntesis '('")
    elif num_abiertos > 3:
        errores.append(f"Error: Tienes {num_abiertos - 3} paréntesis '(' de más")
    if num_cerrados < 3:
        errores.append(f"Error: Faltan {3 - num_cerrados} paréntesis ')'")
    elif num_cerrados > 3:
        errores.append(f"Error: Tienes {num_cerrados - 3} paréntesis ')' de más")
    return errores if errores else None

def extraer_matriz(entrada):
    if not re.match(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', entrada, re.IGNORECASE):
        return ["Error: La instrucción inicial no es válida."], None
    entrada_limpia = re.sub(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', '', entrada, flags=re.IGNORECASE).strip()
    error_detectado = detectar_errores(entrada_limpia)
    if error_detectado:
        return error_detectado, None
    patron = r'\(([-\dxyz\s\+\-]+)=([-\d]+)\)'
    ecuaciones = re.findall(patron, entrada_limpia)
    if not ecuaciones:
        return ["Error: No se encontró una matriz válida."], None
    coeficientes = []
    constantes = []
    def convertir_coef(coef):
        if coef is None:
            return 0
        coef_valor = coef.group(1)
        if coef_valor in ["", "+"]:
            return 1
        elif coef_valor == "-":
            return -1
        return int(coef_valor)
    for izquierda, derecha in ecuaciones:
        coef_x = convertir_coef(re.search(r'([-+]?\d*)x', izquierda))
        coef_y = convertir_coef(re.search(r'([-+]?\d*)y', izquierda))
        coef_z = convertir_coef(re.search(r'([-+]?\d*)z', izquierda))
        coeficientes.append([coef_x, coef_y, coef_z])
        constantes.append(int(derecha))
    return np.array(coeficientes, dtype=float), np.array(constantes, dtype=float)

def resolver_matriz(entrada):
    matriz_coef, matriz_const = extraer_matriz(entrada)
    if isinstance(matriz_coef, list):
        mostrar_mensaje("\n".join(matriz_coef), RED)
        return
    try:
        solucion = np.linalg.solve(matriz_coef, matriz_const)
        resultado = f"x = {solucion[0]:.2f}, y = {solucion[1]:.2f}, z = {solucion[2]:.2f}"
        mostrar_mensaje(resultado, BLACK)
    except np.linalg.LinAlgError:
        mostrar_mensaje("Error: El sistema no tiene solución única.", RED)

def mostrar_mensaje(mensaje, color):
    screen.fill(WHITE)
    line_height = 40
    lines = mensaje.split("\n")
    y = HEIGHT // 3  # Posición inicial

    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (40, y))
        y += line_height  # Espaciado entre líneas

    pygame.display.flip()
    pygame.time.delay(3000)

def preguntar_nueva_matriz():
    screen.fill(WHITE)
    mensaje = font.render("¿Desea realizar otra matriz? (S/N)", True, BLACK)
    screen.blit(mensaje, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    esperando_respuesta = True
    while esperando_respuesta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    esperando_respuesta = False
                elif event.key == pygame.K_n:
                    pygame.quit()
                    exit()

def main():
    while True:
        screen.fill(WHITE)
        input_text = ""
        cursor_pos = 0
        cursor_visible = True
        clock = pygame.time.Clock()
        cursor_timer = 0
        text_surface = font.render("Ingrese la cadena:", True, BLACK)
        screen.blit(text_surface, (20, 50))
        pygame.display.flip()
        capturando_texto = True
        while capturando_texto:
            screen.fill(WHITE)
            screen.blit(text_surface, (20, 50))
            input_surface = font.render(input_text, True, BLACK)
            screen.blit(input_surface, (20, 100))
            cursor_x = font.size(input_text[:cursor_pos])[0] + 20
            cursor_timer += clock.get_time()
            if cursor_timer >= 500:
                cursor_visible = not cursor_visible
                cursor_timer = 0
            if cursor_visible:
                pygame.draw.line(screen, BLACK, (cursor_x, 100), (cursor_x, 130), 2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        capturando_texto = False
                        resolver_matriz(input_text)
                        preguntar_nueva_matriz()
                    elif event.key == pygame.K_BACKSPACE and cursor_pos > 0:
                        input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                        cursor_pos -= 1
                    elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        clipboard_text = pyperclip.paste()
                        input_text = input_text[:cursor_pos] + clipboard_text + input_text[cursor_pos:]
                        cursor_pos += len(clipboard_text)
                    else:
                        input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                        cursor_pos += 1
            clock.tick(30)

main()




#    crea la siguiente matriz(-4x-6y-6z=9)(5x+3y-2z=4)(x-2y+z=-1)

#   crea la siguiente matriz(2x-3y+5z=12)(-1x+4y-2z=-5)(3x+2y+1z=8)

#   crea la siguiente matriz(2x+3y-4z=10)(x-2y+5z=7)(-3x+y+z=5)

#  =============  errores ========================

#   crea la siguiente matriz(2x+3y=8)(-x+4y-2z=5)(3a+2b=7)

#   crea la siguiente matriz(3x+2y+@z=5)(-x+4y-2a=7)

#  crea la siguiente matriz(-4x-6y-6z=9)(-4x-6y-6z=9)(-4x-6y-6z=9)
