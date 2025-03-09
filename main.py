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

# Variables para capturar el texto
input_text = ""
cursor_pos = 0
running = True
cursor_visible = True
clock = pygame.time.Clock()
cursor_timer = 0

def detectar_errores(entrada):
    """Detecta errores específicos en la entrada y devuelve un mensaje detallado."""
    errores = []
    
    # Caracteres inválidos
    caracteres_invalidos = re.findall(r'([^0-9xyz\s\+\-\=\(\)])', entrada)
    if caracteres_invalidos:
        errores.append(f"Error: Caracteres no válidos encontrados: {', '.join(set(caracteres_invalidos))}")
    
    # Verificar exactamente 3 pares de paréntesis
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
    """Extrae las ecuaciones de la matriz y las convierte en una matriz NumPy."""
    if not re.match(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', entrada, re.IGNORECASE):
        return ["Error: La instrucción inicial no es válida. Usa 'crea', 'genera', 'realiza' o 'has la siguiente matriz'."], None
    
    entrada_limpia = re.sub(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', '', entrada, flags=re.IGNORECASE).strip()
    error_detectado = detectar_errores(entrada_limpia)
    if error_detectado:
        return error_detectado, None
    
    patron = r'\(([-\dxyz\s\+\-]+)=([-\d]+)\)'
    ecuaciones = re.findall(patron, entrada_limpia)
    if not ecuaciones:
        return ["Error: No se encontró una matriz válida en la entrada."], None
    
    coeficientes = []
    constantes = []
    
    def convertir_coef(coef):
        if coef is None:
            return 0
        coef_valor = coef.group(1)
        if coef_valor == "" or coef_valor == "+":
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
    """Procesa la entrada, resuelve la matriz y muestra el resultado en pantalla."""
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
    """Muestra un mensaje en la pantalla con ajuste automático de texto para que no se recorte."""
    screen.fill(WHITE)
    max_ancho = WIDTH - 80  # Define un margen para evitar cortes
    palabras = mensaje.split(" ")  # Divide el mensaje en palabras
    lineas = []
    linea_actual = ""

    # Construcción de líneas con ajuste automático
    for palabra in palabras:
        if font.size(linea_actual + palabra)[0] < max_ancho:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    if linea_actual:
        lineas.append(linea_actual.strip())

    # Mostrar cada línea correctamente en pantalla
    y_pos = HEIGHT // 3
    for linea in lineas:
        text_surface = font.render(linea, True, color)
        screen.blit(text_surface, (40, y_pos))  # Asegura margen izquierdo
        y_pos += 50  # Aumenta espacio entre líneas para más claridad

    pygame.display.flip()
    pygame.time.delay(5000)



while running:
    screen.fill(WHITE)
    
    text_surface = font.render("Ingrese la cadena:", True, BLACK)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (20, 50))
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
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False
                resolver_matriz(input_text)
            elif event.key == pygame.K_BACKSPACE and cursor_pos > 0:
                input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                cursor_pos -= 1
            elif event.key == pygame.K_DELETE and cursor_pos < len(input_text):
                input_text = input_text[:cursor_pos] + input_text[cursor_pos + 1:]
            elif event.key == pygame.K_LEFT and cursor_pos > 0:
                cursor_pos -= 1
            elif event.key == pygame.K_RIGHT and cursor_pos < len(input_text):
                cursor_pos += 1
            elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                clipboard_text = pyperclip.paste()
                input_text = input_text[:cursor_pos] + clipboard_text + input_text[cursor_pos:]
                cursor_pos += len(clipboard_text)
            else:
                input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                cursor_pos += 1
    
    clock.tick(30)

pygame.quit()





#    crea la siguiente matriz(-4x-6y-6z=9)(5x+3y-2z=4)(x-2y+z=-1)

#   crea la siguiente matriz(2x-3y+5z=12)(-1x+4y-2z=-5)(3x+2y+1z=8)

#   crea la siguiente matriz(2x+3y-4z=10)(x-2y+5z=7)(-3x+y+z=5)

#  =============  errores ========================

#   crea la siguiente matriz(2x+3y=8)(-x+4y-2z=5)(3a+2b=7)

#   crea la siguiente matriz(3x+2y+@z=5)(-x+4y-2z=7)

#  crea la siguiente matriz(-4x-6y-6z=9)(-4x-6y-6z=9)(-4x-6y-6z=9)
