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

def extraer_matriz(entrada):
    """ Extrae las ecuaciones de la matriz y las convierte en una matriz NumPy """

    # Forzar eliminación de "crea la siguiente matriz"
    entrada_limpia = re.sub(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', '', entrada, flags=re.IGNORECASE).strip()

    # Validar si hay caracteres no permitidos en las ecuaciones
    if re.search(r'[^0-9xyz\s\+\-\=\(\)]', entrada_limpia):
        return "Error: Se encontraron caracteres no válidos en la entrada.", None

    # Filtrar solo lo que está dentro de los paréntesis
    patron = r'\(([-\dxyz\s\+\-]+)=([-\d]+)\)'
    ecuaciones = re.findall(patron, entrada_limpia)

    if not ecuaciones:
        return "Error: No se encontró una matriz válida en la entrada.", None

    coeficientes = []
    constantes = []

    def convertir_coef(coef):
        """ Convierte un coeficiente extraído en un número entero """
        if coef is None:
            return 0  # Si la variable no aparece en la ecuación, su coeficiente es 0
        coef_valor = coef.group(1)
        if coef_valor == "" or coef_valor == "+":
            return 1  # Si no hay número o solo "+", es 1
        elif coef_valor == "-":
            return -1  # Si es solo "-", es -1
        return int(coef_valor)  # Convertir a número entero

    for izquierda, derecha in ecuaciones:
        # Extraer coeficientes de x, y, z
        coef_x = re.search(r'([-+]?\d*)x', izquierda)
        coef_y = re.search(r'([-+]?\d*)y', izquierda)
        coef_z = re.search(r'([-+]?\d*)z', izquierda)

        coef_x = convertir_coef(coef_x)
        coef_y = convertir_coef(coef_y)
        coef_z = convertir_coef(coef_z)

        coeficientes.append([coef_x, coef_y, coef_z])
        constantes.append(int(derecha))

    return np.array(coeficientes, dtype=float), np.array(constantes, dtype=float)

def resolver_matriz(entrada):
    """ Procesa la entrada, resuelve la matriz y muestra el resultado en pantalla """

    matriz_coef, matriz_const = extraer_matriz(entrada)

    if isinstance(matriz_coef, str):  # Verificar si hay un error en la entrada
        mostrar_mensaje(matriz_coef, RED)
        return

    try:
        solucion = np.linalg.solve(matriz_coef, matriz_const)
        resultado = f"x = {solucion[0]:.2f}, y = {solucion[1]:.2f}, z = {solucion[2]:.2f}"
        mostrar_mensaje(resultado, BLACK)
    except np.linalg.LinAlgError:
        mostrar_mensaje("Error: El sistema no tiene solución única.", RED)

def mostrar_mensaje(mensaje, color):
    """ Muestra un mensaje en la pantalla """
    screen.fill(WHITE)
    text_surface = font.render(mensaje, True, color)
    screen.blit(text_surface, (20, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(5000)  # Mantener el mensaje en pantalla por 5 segundos

# ======= PRIMERA PANTALLA: INGRESO DE TEXTO =======
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
            if event.key == pygame.K_RETURN:  # Enter -> Procesar entrada
                running = False
                resolver_matriz(input_text)  # Resolver la matriz

            elif event.key == pygame.K_BACKSPACE:  
                if cursor_pos > 0:
                    input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                    cursor_pos -= 1

            elif event.key == pygame.K_DELETE:  
                if cursor_pos < len(input_text):
                    input_text = input_text[:cursor_pos] + input_text[cursor_pos + 1:]

            elif event.key == pygame.K_LEFT:  
                if cursor_pos > 0:
                    cursor_pos -= 1

            elif event.key == pygame.K_RIGHT:  
                if cursor_pos < len(input_text):
                    cursor_pos += 1

            elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_META or pygame.key.get_mods() & pygame.KMOD_CTRL):
                clipboard_text = pyperclip.paste()
                input_text = input_text[:cursor_pos] + clipboard_text + input_text[cursor_pos:]
                cursor_pos += len(clipboard_text)

            elif event.key == pygame.K_c and (pygame.key.get_mods() & pygame.KMOD_META or pygame.key.get_mods() & pygame.KMOD_CTRL):
                pyperclip.copy(input_text)

            else:  
                input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                cursor_pos += 1

    clock.tick(30)  

pygame.quit()



#  crea la siguiente matriz(-4x-6y-6z=9)(5x+3y-2z=4)(x-2y+z=-1)

# crea la siguiente matriz(-4x-6y-6z=9)(-4x-6y-6z=9)(-4x-6y-6z=9)

#crea la siguiente matriz(2x-3y+5z=12)(-1x+4y-2z=-5)(3x+2y+1z=8)

#crea la siguiente matriz(2x+3y-4z=10)(x-2y+5z=7)(-3x+y+z=5)

#  =============  errores ========================

#crea la siguiente matriz(2x+3y=8)(-x+4y-2z=5)(3a+2b=7)

#crea la siguiente matriz(3x+2y+@z=5)(-x+4y-2z=7)
