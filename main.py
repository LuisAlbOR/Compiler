
import pygame
import pyperclip
import numpy as np
import re
from lexer import lexer, tokens
import os

# Centrar la ventana antes de inicializar pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entrada del Compilador")
font = pygame.font.Font(None, 36)

def detectar_errores(entrada):
    """Detecta errores y devuelve mensajes junto con la posición exacta del error."""
    errores = []
    posiciones = set()  # Evita posiciones repetidas

    # Buscar caracteres inválidos
    for match in re.finditer(r'([^0-9xyz\s\+\-\=\(\)])', entrada):
        errores.append(f"Error: Caracter no válido '{match.group(1)}'")
        posiciones.add(match.start())

    # Verificar paréntesis
    num_abiertos = entrada.count('(')
    num_cerrados = entrada.count(')')

    if num_abiertos < 3:
        errores.append(f"Error: Faltan {3 - num_abiertos} paréntesis '('")
        posiciones.add(entrada.rfind(')') + 1 if ')' in entrada else len(entrada))

    if num_cerrados < 3:
        errores.append(f"Error: Faltan {3 - num_cerrados} paréntesis ')'")
        posiciones.add(entrada.rfind(')') if ')' in entrada else len(entrada))

    if errores:
        return errores, list(posiciones)
    return None, None

def mostrar_error_con_cursor(entrada, errores, posiciones):
    """Muestra la entrada con `^` debajo de los errores."""
    screen.fill(WHITE)

    text_surface = font.render("Entrada:", True, BLACK)
    screen.blit(text_surface, (20, 50))

    input_surface = font.render(entrada, True, RED)
    screen.blit(input_surface, (20, 100))

    marker_line = [" "] * len(entrada)
    for pos in posiciones:
        if 0 <= pos < len(marker_line):
            marker_line[pos] = "^"

    marker_text = "".join(marker_line)
    marker_surface = font.render(marker_text, True, RED)
    screen.blit(marker_surface, (20, 130))

    y_offset = 160
    for error in errores:
        error_surface = font.render(error, True, RED)
        screen.blit(error_surface, (20, y_offset))
        y_offset += 30

    pygame.display.flip()

def capturar_cadena():
    """Captura entrada de texto y permite correcciones."""
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

                elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    clipboard_text = pyperclip.paste()
                    input_text = input_text[:cursor_pos] + clipboard_text + input_text[cursor_pos:]
                    cursor_pos += len(clipboard_text)

                elif event.unicode.isprintable():
                    input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                    cursor_pos += 1

        clock.tick(30)

def extraer_matriz(entrada):
    """Extrae los coeficientes y términos independientes de la ecuación."""
    if not re.match(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', entrada, re.IGNORECASE):
        return ["Error: La instrucción inicial no es válida."], None

    entrada_limpia = re.sub(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', '', entrada, flags=re.IGNORECASE).strip()
    error_detectado, _ = detectar_errores(entrada_limpia)

    if error_detectado:
        return error_detectado, None

    patron = r'\(([-\dxyz\s\+\-]+)=([-\d]+)\)'
    ecuaciones = re.findall(patron, entrada_limpia)

    if len(ecuaciones) != 3:
        return ["Error: Se esperaban exactamente 3 ecuaciones."], None

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
    """Resuelve la matriz si es válida."""
    matriz_coef, matriz_const = extraer_matriz(entrada)

    if isinstance(matriz_coef, list):
        return "\n".join(matriz_coef)

    try:
        solucion = np.linalg.solve(matriz_coef, matriz_const)
        return f"x = {solucion[0]:.2f}, y = {solucion[1]:.2f}, z = {solucion[2]:.2f}"
    except np.linalg.LinAlgError:
        return "Error: El sistema no tiene solución única."

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
                    
def mostrar_error_con_cursor(entrada):
    """Recorre la cadena buscando errores y muestra `^` en la posición exacta."""
    errores = []
    posiciones = []

    palabras_clave = {'crea', 'genera', 'realiza', 'has'}  # Palabras clave válidas
    variables_validas = {'x', 'y', 'z'}  # Variables permitidas

    # Verificar si la palabra clave es incorrecta
    primera_palabra = entrada.split()[0]
    if primera_palabra.lower() not in palabras_clave:
        errores = [f"Error: Palabra no válida '{primera_palabra}'"]
        posiciones = [entrada.find(primera_palabra)]
    
    # Recorrer la cadena buscando errores
    for i in range(len(entrada) - 1):
        char = entrada[i]
        next_char = entrada[i + 1]

        # Detectar si falta un signo entre variables (ejemplo: `xy` en lugar de `x+y`)
        if char in variables_validas and next_char in variables_validas:
            errores = ["Error: Falta signo entre variables"]
            posiciones = [i + 1]
            break
        
        # Detectar si falta un número después de '='
        if char == '=' and not next_char.isdigit() and next_char not in {'+', '-'}:
            errores = ["Error: Falta número después de '='"]
            posiciones = [i + 1]
            break

    # Verificar paréntesis faltantes
    num_abiertos = entrada.count('(')
    num_cerrados = entrada.count(')')

    if num_abiertos < 3:
        errores = [f"Error: Falta {3 - num_abiertos} paréntesis '(' en la expresión."]
        posiciones = [entrada.find('(') if '(' in entrada else len(entrada)]
    
    if num_cerrados < 3:
        errores = [f"Error: Falta {3 - num_cerrados} paréntesis ')' en la expresión."]
        posiciones = [entrada.rfind(')') if ')' in entrada else len(entrada)]

    # Si hay errores, mostrar en pantalla
    if errores:
        while errores:
            screen.fill(WHITE)

            text_surface = font.render("Entrada:", True, BLACK)
            screen.blit(text_surface, (20, 50))

            input_surface = font.render(entrada, True, RED)
            screen.blit(input_surface, (20, 100))

            # Crear la línea de errores con '^'
            marker_line = [" "] * len(entrada)
            for pos in posiciones:
                if 0 <= pos < len(marker_line):
                    marker_line[pos] = "^"

            marker_text = "".join(marker_line)
            marker_surface = font.render(marker_text, True, RED)
            screen.blit(marker_surface, (20, 130))

            # Mostrar mensaje de error
            error_surface = font.render(errores[0], True, RED)  # Solo muestra 1 error claro
            screen.blit(error_surface, (20, 160))

            pygame.display.flip()
            pygame.time.delay(5000)  # Mantiene el error en pantalla por 3 segundos

            # Pedir nueva entrada hasta que sea correcta
            entrada = capturar_cadena()
            errores, posiciones = detectar_errores(entrada)

    return entrada  # Devuelve la cadena corregida

def main():
   while True:
        entrada = capturar_cadena()  # Captura la entrada del usuario

        # Validar errores antes de procesar
        entrada = mostrar_error_con_cursor(entrada)  # Ahora validamos antes de continuar

        # Resolver la matriz una vez corregida
        resultado = resolver_matriz(entrada)

        # Mostrar resultado en pantalla
        screen.fill(WHITE)
        resultado_surface = font.render(resultado, True, BLACK)
        screen.blit(resultado_surface, (20, 100))
        pygame.display.flip()
        pygame.time.delay(3000)

        # Preguntar si desea ingresar otra matriz
        if not preguntar_nueva_matriz():
            break

main()


#    crea la siguiente matriz(-4x-6y-6z=9)(5x+3y-2z=4)(x-2y+z=-1)

#   crea la siguiente matriz(2x-3y+5z=12)(-1x+4y-2z=-5)(3x+2y+1z=8)

#   crea la siguiente matriz(2x+3y-4z=10)(x-2y+5z=7)(-3x+y+z=5)

#  =============  errores ========================

#   crea la siguiente matriz(2x+3y=8)(-x+4y-2z=5)(3a+2b=7)

#   crea la siguiente matriz(3x+2y+@z=5)(-x+4y-2a=7)

#  crea la siguiente matriz(-4x-6y-6z=9)(-4x-6y-6z=9)(-4x-6y-6z=9)