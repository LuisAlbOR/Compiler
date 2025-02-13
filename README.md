# Compilador con PLY y Pygame

Este proyecto implementa un compilador en Python utilizando **PLY (Python Lex-Yacc)** para el análisis léxico y sintáctico, y **Pygame** para la interfaz gráfica. El compilador recibe ecuaciones en formato de matriz 3x3 y las procesa para su análisis.

## 📌 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instaladas las siguientes dependencias:

- Python 3.10 o superior
- PLY (Python Lex-Yacc)
- Pygame

Para instalarlas, ejecuta:

```bash
pip install ply pygame
```

## 📂 Estructura del Proyecto

```
Compilador/
│-- lexer.py            # Análisis léxico
│-- parser.py           # Análisis sintáctico
│-- main.py             # Interfaz y ejecución del compilador
│-- mostrar_tokens.py   # Pantalla de visualización de tokens
│-- error_lexico.py     # Pantalla para mostrar errores léxicos
│-- README.md           # Documentación del proyecto
```

## 🚀 Ejecución

Para ejecutar el compilador, abre una terminal en el directorio del proyecto y ejecuta:

```bash
python main.py
```

### 🔹 Funcionamiento

1. Se abre una ventana para ingresar la cadena de entrada.
2. Al presionar **Enter**, se procesa la entrada con el lexer y parser.
3. Si la entrada es válida, se muestra una tabla con los tokens generados.
4. Si hay un error léxico, se muestra una pantalla indicando el error.
5. Una vez validadas las ecuaciones, se pueden manipular para su resolución.

## ⚙️ Tecnologías Usadas

- **Python**: Lenguaje de programación principal.
- **PLY**: Implementación de Lex y Yacc en Python.
- **Pygame**: Creación de interfaces gráficas.

## 📌 Notas

- El lexer y el parser están diseñados específicamente para procesar matrices 3x3 en formato de ecuaciones lineales.
- El código se puede ampliar para soportar otras estructuras matemáticas y análisis más complejos.

## 📜 Licencia

Este proyecto es de código abierto y se distribuye bajo la licencia MIT.

