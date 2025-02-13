# semantico.py

# Tabla de símbolos para almacenar variables y sus valores
tabla_simbolos = {}

def agregar_variable(nombre, valor):
    """Agrega una variable a la tabla de símbolos."""
    if nombre in tabla_simbolos:
        raise ValueError(f"Error semántico: La variable '{nombre}' ya está declarada.")
    tabla_simbolos[nombre] = valor

def obtener_valor(nombre):
    """Obtiene el valor de una variable desde la tabla de símbolos."""
    if nombre not in tabla_simbolos:
        raise ValueError(f"Error semántico: La variable '{nombre}' no está declarada.")
    return tabla_simbolos[nombre]

def validar_ecuacion(ecuacion):
    """Valida que la ecuación esté bien formada."""
    if not isinstance(ecuacion, str):
        raise ValueError("Error semántico: La ecuación no es una cadena válida.")
    partes = ecuacion.split()
    if len(partes) != 5 or partes[3] != '=':
        raise ValueError("Error semántico: La ecuación no está bien formada.")

def validar_termino(termino):
    """Valida que el término esté bien formado."""
    if not isinstance(termino, str):
        raise ValueError("Error semántico: El término no es una cadena válida.")
    if len(termino) < 2:
        raise ValueError("Error semántico: El término no está bien formado.")
    signo = termino[0]
    if signo not in ['+', '-']:
        raise ValueError("Error semántico: El signo no es válido.")