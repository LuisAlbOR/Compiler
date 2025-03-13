import re
import numpy as np
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.font.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((1000, 600))

def manejar_errores(entrada, screen, font):
    """Detecta errores en la entrada, muestra los errores con `^` y devuelve la entrada corregida."""
    while True:
        errores = []
        posiciones = []

        # 🔹 1. Verificar si la frase inicial tiene errores
        palabras_clave = {'crea', 'genera', 'realiza'}
        estructura_correcta = re.match(r'^(crea|genera|realiza) la siguiente matriz', entrada)

        if not estructura_correcta:
            errores.append("Error: La frase inicial debe ser 'crea/genera/realiza la siguiente matriz'.")
            posiciones.append(0)

        # 🔹 2. Extraer ecuaciones dentro de paréntesis
        ecuaciones = re.findall(r'\(([^)]+)\)', entrada)

        # 🔹 3. Identificar en qué ecuación falta '(' o ')'
        abrir_par = [m.start() for m in re.finditer(r'\(', entrada)]  # Lista de posiciones de '('
        cerrar_par = [m.start() for m in re.finditer(r'\)', entrada)]  # Lista de posiciones de ')'

        if len(abrir_par) != len(cerrar_par):  # Si hay más '(' que ')', falta un ')'
            for i, pos in enumerate(abrir_par):
                if i >= len(cerrar_par):  # Si hay un '(' sin su correspondiente ')'
                    errores.append(f"Error: Falta ')' en la ecuación {i+1}.")
                    posiciones.append(pos)

        if len(cerrar_par) != len(abrir_par):  # Si hay más ')' que '(', falta un '('
            for i, pos in enumerate(cerrar_par):
                if i >= len(abrir_par):  # Si hay un ')' sin su correspondiente '('
                    errores.append(f"Error: Falta '(' en la ecuación {i+1}.")
                    posiciones.append(pos)

        # 🔹 3. Extraer ecuaciones dentro de paréntesis
        ecuaciones = re.findall(r'\(([^)]+)\)', entrada)

        # 🔹 4. Validar ecuaciones individualmente
        for i, ecuacion in enumerate(ecuaciones):
            ecuacion_sin_espacios = ecuacion.replace(" ", "")

            # 🔹 5. Verificar si faltan variables x, y, z
            if 'x' not in ecuacion_sin_espacios:
                errores.append(f"Error: Falta 'x' en la ecuación {i+1}.")
                posiciones.append(entrada.find(ecuacion))

            if 'y' not in ecuacion_sin_espacios:
                errores.append(f"Error: Falta 'y' en la ecuación {i+1}.")
                posiciones.append(entrada.find(ecuacion))

            if 'z' not in ecuacion_sin_espacios:
                errores.append(f"Error: Falta 'z' en la ecuación {i+1}.")
                posiciones.append(entrada.find(ecuacion))

            # 🔹 6. Verificar caracteres inválidos
            if re.search(r'[^0-9xyz\s\+\-\=\(\)]', ecuacion):
                errores.append(f"Error: Caracter no permitido en la ecuación {i+1}.")
                posiciones.append(entrada.find(ecuacion))

            # 🔹 7. Verificar caracteres extra después de x, y, z
            for match in re.finditer(r'([xyz])(\d+|[^+\-=])', ecuacion_sin_espacios):  
                errores.append(f"Error: Caracter inesperado '{match.group(2)}' después de '{match.group(1)}' en ecuación {i+1}.")
                posiciones.append(entrada.find(match.group(2)))

            # 🔹 8. Verificar si falta un número después del `=`
            if re.search(r'=\s*$', ecuacion_sin_espacios):  
                errores.append(f"Error: Falta un número después de '=' en ecuación {i+1}.")
                posiciones.append(entrada.find('='))

        # 🔹 Si hay errores, mostrarlos en pygame y permitir corrección
        if errores:
            while True:
                screen.fill((255, 255, 255))  # Fondo blanco

                # 🔹 Mostrar texto de entrada
                text_surface = font.render("Entrada:", True, (0, 0, 0))  # Texto negro
                screen.blit(text_surface, (20, 50))

                input_surface = font.render(entrada, True, (255, 0, 0))  # Texto rojo
                screen.blit(input_surface, (20, 100))

                # 🔹 Crear línea de errores con `^`
                marker_line = [" "] * len(entrada)
                for pos in posiciones:
                    if 0 <= pos < len(marker_line):
                        marker_line[pos] = "^"

                marker_text = "".join(marker_line)
                marker_surface = font.render(marker_text, True, (255, 0, 0))  # Texto rojo
                screen.blit(marker_surface, (20, 130))

                # 🔹 Mostrar mensajes de error
                y_offset = 160
                for error in errores:
                    error_surface = font.render(error, True, (255, 0, 0))  # Texto rojo
                    screen.blit(error_surface, (20, y_offset))
                    y_offset += 30

                pygame.display.flip()
                pygame.time.delay(5000)

                # 🔹 Capturar nueva entrada sin cerrar la ventana
                from main import capturar_cadena
                entrada = capturar_cadena()

                # 🔹 Volver a validar la nueva entrada
                errores.clear()
                posiciones.clear()
                return entrada

        else:
            return entrada  # Devuelve la entrada corregida si no hay errores

def extraer_matriz(entrada):
    """Extrae los coeficientes y términos independientes de la ecuación después de que la entrada ha sido validada."""

    # 🔹 1. Eliminar la frase inicial para dejar solo las ecuaciones
    entrada_limpia = re.sub(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', '', entrada, flags=re.IGNORECASE).strip()

    # 🔹 2. Extraer ecuaciones en formato `(-4x-6y-6z=9)`
    patron = r'\(([-\dxyz\s\+\-]+)=([-\d]+)\)'  
    ecuaciones = re.findall(patron, entrada_limpia)

    coeficientes = []
    constantes = []

    def convertir_coef(coef):
        """Convierte coeficientes en enteros (maneja `-x`, `+x`, `x`, `2x`, etc.)."""
        if coef is None:
            return 0
        coef_valor = coef.group(1)
        if coef_valor in ["", "+"]:
            return 1
        elif coef_valor == "-":
            return -1
        return int(coef_valor)

    # 🔹 3. Extraer coeficientes de x, y, z y el término independiente
    for izquierda, derecha in ecuaciones:
        coef_x = convertir_coef(re.search(r'([-+]?\d*)x', izquierda))
        coef_y = convertir_coef(re.search(r'([-+]?\d*)y', izquierda))
        coef_z = convertir_coef(re.search(r'([-+]?\d*)z', izquierda))

        coeficientes.append([coef_x, coef_y, coef_z])
        constantes.append(int(derecha))

    # 🔹 4. Devolver las matrices en formato `numpy.array`
    return np.array(coeficientes, dtype=float), np.array(constantes, dtype=float)

def resolver_matriz(entrada):
    """Extrae la matriz y la resuelve."""
    
    # 🔹 Extraer la matriz después de que la entrada haya sido validada en `main()`
    matriz_coef, matriz_const = extraer_matriz(entrada)

    # 🔹 Si extraer_matriz devuelve errores, mostrar mensaje
    if isinstance(matriz_coef, list):  # Esto significa que hubo un error en la extracción
        return "\n".join(matriz_coef)  

    try:
        # 🔹 Resolver la matriz con numpy
        solucion = np.linalg.solve(matriz_coef, matriz_const)
        return f"x = {solucion[0]:.2f}, y = {solucion[1]:.2f}, z = {solucion[2]:.2f}"
    
    except np.linalg.LinAlgError:
        return "Error: El sistema no tiene solución única."