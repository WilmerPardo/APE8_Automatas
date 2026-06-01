# Analizador CFG de expresiones booleanas

Aplicacion web desarrollada en Python con Flask para analizar expresiones logicas booleanas mediante una Gramatica Libre de Contexto (CFG). El programa recibe una cadena escrita por el usuario, la separa en tokens, valida su estructura sintactica, construye un arbol de derivacion y muestra las derivaciones por izquierda y por derecha.

El sistema esta pensado como una herramienta didactica para visualizar como una expresion booleana pertenece, o no, a una gramatica formal. Por eso no se limita a decir si la entrada es valida: tambien expone los lexemas reconocidos, la forma del arbol generado y los pasos de derivacion que producen la cadena final.

## Funcionamiento general

El flujo principal empieza en la interfaz web, donde se ingresa una expresion como:

```txt
A | B & ~C
id | ~ ( id & id )
(A | B) & C
```

Cuando el formulario se envia, Flask recibe la cadena y ejecuta el proceso completo de analisis:

```txt
Entrada del usuario
        ↓
Tokenizacion con backend/lexer.py
        ↓
Validacion sintactica con backend/parser.py
        ↓
Construccion del arbol de derivacion
        ↓
Generacion de derivaciones izquierda y derecha
        ↓
Renderizado de resultados en templates/resultados.html
```

Si la cadena pertenece al lenguaje, la pagina de resultados muestra la tabla de tokens, el arbol de derivacion en formato visual vertical, la cadena final y ambas derivaciones. Si existe un error lexico o sintactico, el sistema captura la excepcion `SyntaxError` y presenta un mensaje claro con la posicion donde se detecto el problema.

## Distribucion del proyecto

```txt
APE8_Automatas/
├── app.py
├── backend/
│   ├── __init__.py
│   ├── derivations.py
│   ├── grammar.py
│   ├── lexer.py
│   ├── parser.py
│   └── tree_utils.py
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── index.html
│   └── resultados.html
├── tests/
│   └── test_parser.py
├── requirements.txt
└── README.md
```

La organizacion separa la aplicacion web de la logica formal del analizador. `app.py` coordina las rutas HTTP y prepara la informacion para las plantillas, mientras que el paquete `backend/` contiene el nucleo de analisis lexico, sintactico y de representacion de resultados.

## Arquitectura

La aplicacion esta dividida en cuatro capas principales:

1. **Interfaz web:** formada por `templates/index.html`, `templates/resultados.html` y `static/css/styles.css`. Presenta el formulario de entrada, la gramatica, los ejemplos y los resultados del analisis.
2. **Orquestacion Flask:** ubicada en `app.py`. Define la ruta principal `/`, la ruta `/analizar` y la funcion `analyze_expression`, que ejecuta el flujo completo sobre una expresion.
3. **Nucleo del analizador:** ubicado en `backend/`. Aqui se encuentran el lexer, parser, definicion de gramatica, generador de derivaciones y utilidades para imprimir el arbol.
4. **Pruebas automatizadas:** ubicadas en `tests/test_parser.py`. Verifican cadenas validas, cadenas invalidas, la tabla de tokens y las derivaciones del caso principal.

Esta arquitectura evita mezclar HTML con reglas gramaticales o algoritmos de parsing. La interfaz solo consume estructuras ya procesadas por el backend.

## Componentes del backend

### `backend/grammar.py`

Centraliza la definicion formal de la gramatica:

- Simbolo inicial: `S`
- No terminales: `S`, `E`, `T`, `F`
- Terminales: `id`, `|`, `&`, `~`, `(`, `)`
- Producciones teoricas y producciones adaptadas para la implementacion
- Etiquetas legibles para los tokens usados en mensajes de error

### `backend/lexer.py`

Implementa el analizador lexico. Usa expresiones regulares para recorrer la cadena y transformarla en objetos `Token`, cada uno con tipo, lexema y posicion.

Tokens reconocidos:

| Token | Lexemas |
|---|---|
| `VAR` | Variables como `A`, `B`, `id`, `var1`, `dato_2` |
| `OR` | `|` |
| `AND` | `&` |
| `NOT` | `~` |
| `LPAREN` | `(` |
| `RPAREN` | `)` |
| `EOF` | Fin interno de cadena |

El terminal gramatical `id` se representa en la implementacion como `VAR`, lo que permite aceptar nombres de variables formados por letras, numeros y guion bajo, siempre que empiecen con una letra.

### `backend/parser.py`

Contiene un parser descendente recursivo implementado con la clase `Parser`. El parser consume la lista de tokens generada por el lexer y construye un arbol formado por nodos `Node`.

La gramatica teorica contiene recursividad izquierda:

```txt
S -> E
E -> E | T
E -> T
T -> T & F
T -> F
F -> ~ F
F -> ( E )
F -> id
```

Para implementarla con descenso recursivo, el codigo usa una forma equivalente sin recursividad izquierda:

```txt
S  -> E
E  -> T E'
E' -> | T E'
E' -> epsilon
T  -> F T'
T' -> & F T'
T' -> epsilon
F  -> ~ F
F  -> ( E )
F  -> id
```

La separacion entre `parse_expression`, `parse_term` y `parse_factor` conserva la precedencia natural de los operadores:

```txt
~  mayor precedencia
&  precedencia intermedia
|  menor precedencia
```

Asi, la expresion `A | B & ~C` se interpreta como:

```txt
A | (B & (~C))
```

### `backend/derivations.py`

Genera las derivaciones por izquierda y por derecha a partir del arbol construido por el parser. El modulo mantiene una forma sentencial interna y reemplaza siempre el simbolo pendiente mas a la izquierda o mas a la derecha, segun el tipo de derivacion.

Para `A | B & ~C`, la derivacion por izquierda termina en:

```txt
S
E
E | T
T | T
F | T
id | T
A | T
A | T & F
A | F & F
A | id & F
A | B & F
A | B & ~F
A | B & ~id
A | B & ~C
```

### `backend/tree_utils.py`

Convierte el arbol de nodos en una representacion de texto con ramas. La pagina de resultados tambien recibe el nodo raiz para dibujarlo como un arbol vertical con HTML y CSS.

Ejemplo de arbol para `A | B & ~C`:

```txt
S
└── E
    ├── E
    │   └── T
    │       └── F
    │           └── VAR(A)
    ├── OR(|)
    └── T
        ├── T
        │   └── F
        │       └── VAR(B)
        ├── AND(&)
        └── F
            ├── NOT(~)
            └── F
                └── VAR(C)
```

## Interfaz

La pantalla inicial (`templates/index.html`) contiene el formulario de entrada, ejemplos validos y una vista resumida de la gramatica. La pantalla de resultados (`templates/resultados.html`) organiza la respuesta en secciones:

- Estado de validacion de la cadena
- Tabla de lexemas y tokens
- Arbol de derivacion
- Cadena final generada
- Derivacion por izquierda
- Derivacion por derecha
- Mensaje de error, cuando la expresion no es valida

Los estilos se encuentran en `static/css/styles.css`. La interfaz usa un tema claro, una disposicion de paneles y grillas responsivas para que los resultados largos se puedan leer tanto en escritorio como en pantallas pequenas.

## Pruebas

El archivo `tests/test_parser.py` cubre el comportamiento central del analizador. Las pruebas validan expresiones correctas como `A | B & ~C`, `~A` y `(A | B) & C`; tambien comprueban errores en entradas como `A & | B`, `A | (B & C`, `A @ B` y la cadena vacia.

Ademas, existe una prueba especifica para el caso `A | B & ~C`, donde se verifica la tabla de tokens y las derivaciones esperadas.

## Ejecucion local

El proyecto depende de Flask, declarado en `requirements.txt`.

```bash
pip install -r requirements.txt
python app.py
```

Por defecto, la aplicacion se levanta en:

```txt
http://127.0.0.1:5000
```

Las pruebas pueden ejecutarse con:

```bash
python -m unittest discover -s tests
```

## Resumen

Este proyecto implementa un analizador CFG completo para expresiones booleanas. Su estructura modular permite distinguir claramente la entrada web, el analisis lexico, el analisis sintactico, la generacion de derivaciones y la representacion visual del arbol. El resultado es una aplicacion pequena pero completa para estudiar como una gramatica libre de contexto reconoce y produce cadenas de un lenguaje formal.
