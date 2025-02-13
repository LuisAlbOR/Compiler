import ply.yacc as yacc
from lexer import tokens  # Importar tokens del lexer
from  seman import validar_ecuacion, validar_termino  # Importar funciones semánticas

# Reglas del parser
def p_expresion_matriz(p):
    '''expresion : PALABRA_CLAVE LA SIGUIENTE MATRIZ ecuacion ecuacion ecuacion'''
    p[0] = [p[5], p[6], p[7]]  # Guardar las ecuaciones en una lista
    # Aquí puedes agregar validaciones semánticas adicionales si es necesario

def p_ecuacion(p):
    '''ecuacion : PARENTESIS_IZQ termino termino termino IGUAL NUMERO PARENTESIS_DER'''
    ecuacion = f"{p[2]} {p[3]} {p[4]} = {p[6]}"  # Formatear la ecuación
    validar_ecuacion(ecuacion)  # Validación semántica
    p[0] = ecuacion

def p_termino(p):
    '''termino : SIGNO NUMERO VARIABLE'''
    termino = f"{p[1]}{p[2]}{p[3]}"  # Formatear el término
    validar_termino(termino)  # Validación semántica
    p[0] = termino

def p_error(p):
    if p:
        print(f"Error de sintaxis: token inesperado '{p.value}' en la posición {p.lexpos}")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

# Construir el parser
parser = yacc.yacc()

# Función para procesar la entrada del parser
def parse_input(input_data):
    try:
        resultado = parser.parse(input_data)
        return resultado
    except ValueError as e:
        print(f"Error semántico: {e}")
        return None