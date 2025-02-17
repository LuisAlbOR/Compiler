# lexer.py
import ply.lex as lex
from error_lexer import mostrar_error_lexico

# Definir los tokens
tokens = (
    'PALABRA_CLAVE',
    'LA',
    'SIGUIENTE',
    'MATRIZ',
    'PARENTESIS_IZQ',
    'SIGNO',
    'NUMERO',
    'VARIABLE',
    'IGUAL',
    'PARENTESIS_DER',
)

# Expresiones regulares para los tokens
t_LA = r'la'
t_SIGUIENTE = r'siguiente'
t_MATRIZ = r'matriz'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_SIGNO = r'[\+\-]'
t_NUMERO = r'\d+'
t_VARIABLE = r'[xyz]'
t_IGUAL = r'='

# Palabras clave con reglas especiales
def t_PALABRA_CLAVE(t):
    r'crea|genera|realiza|has'
    return t

# Ignorar espacios y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores del lexer
def t_error(t):
    print("Error léxico: ", t.value)
    mostrar_error_lexico(t.value)
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Función para procesar la cadena de entrada
def get_tokens(input_data):
    lexer.input(input_data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens
