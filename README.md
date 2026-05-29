# README - Analizador de Gramáticas Libres de Contexto para Expresiones Booleanas

## 1. Descripción general

Este proyecto consiste en desarrollar una aplicación web para **leer, analizar y validar cadenas de texto que representen expresiones lógicas booleanas** mediante una **Gramática Libre de Contexto (CFG)**.

La aplicación debe permitir que el usuario ingrese expresiones como:

```txt
A | B & ~C
id | ~ ( id & id )
A | B & C
```

El sistema debe realizar:

- Análisis léxico de la cadena.
- Identificación de lexemas y tokens.
- Validación sintáctica usando una CFG.
- Respeto de la precedencia de operadores:
  - `~` tiene la mayor precedencia.
  - `&` tiene precedencia intermedia.
  - `|` tiene la menor precedencia.
- Generación de derivaciones.
- Generación del árbol de derivación.
- Presentación de resultados en una interfaz web clara.

---

## 2. Objetivo del sistema

Construir un programa capaz de validar expresiones lógicas booleanas usando una Gramática Libre de Contexto, mostrando al usuario el proceso de análisis de forma clara y ordenada.

El sistema debe servir como apoyo para comprender:

- Componentes de una CFG.
- Terminales y no terminales.
- Reglas de producción.
- Análisis léxico.
- Análisis sintáctico.
- Derivación por izquierda.
- Derivación por derecha.
- Árbol de derivación.
- Ambigüedad gramatical básica.

---

## 3. Tecnologías requeridas

### Backend

El backend debe implementarse en **Python**.

Este backend se encargará de:

- Recibir la cadena ingresada.
- Ejecutar el analizador léxico.
- Ejecutar el analizador sintáctico.
- Construir el árbol de derivación.
- Generar las derivaciones.
- Devolver los resultados al frontend.

### Frontend

El frontend debe desarrollarse usando **Flask con plantillas Jinja2**, HTML y CSS.

Aunque Flask es un framework web de Python, en este proyecto se usará para renderizar la interfaz visual del sistema mediante:

- `templates/index.html`
- `templates/resultados.html`
- `static/css/styles.css`

La interfaz debe usar un **tema claro**, con colores suaves, buena legibilidad y distribución ordenada de la información.

---

## 4. Arquitectura propuesta

La arquitectura recomendada es modular, separando responsabilidades para mantener código limpio.

```txt
analizador_cfg/
│
├── app.py
│
├── backend/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── grammar.py
│   ├── derivations.py
│   └── tree_utils.py
│
├── templates/
│   ├── index.html
│   └── resultados.html
│
├── static/
│   └── css/
│       └── styles.css
│
├── tests/
│   └── test_parser.py
│
└── README.md
```

---

## 5. Funcionamiento general del programa

El sistema debe seguir este flujo:

```txt
Usuario ingresa una expresión
        ↓
Flask recibe la cadena desde el formulario
        ↓
lexer.py divide la cadena en lexemas y tokens
        ↓
parser.py valida la cadena usando la gramática
        ↓
Se genera el árbol de derivación
        ↓
Se generan las derivaciones por izquierda y derecha
        ↓
Flask muestra los resultados en una página clara
```

---

## 6. Gramática Libre de Contexto original

La gramática base para expresiones booleanas es:

```txt
S      -> E

E      -> E | T
E      -> T

T      -> T & F
T      -> F

F      -> ~ F
F      -> ( E )
F      -> id
```

Donde:

- `S` es el símbolo inicial.
- `E` representa expresiones con OR.
- `T` representa términos con AND.
- `F` representa factores, negaciones, paréntesis o variables.
- `id` representa una variable como `A`, `B`, `C`, `X`, `Y`, `id`, etc.

---

## 7. Componentes formales de la CFG

Una Gramática Libre de Contexto se define como:

```txt
G = (V, Σ, R, S)
```

### 7.1 No terminales

```txt
V = { S, E, T, F }
```

### 7.2 Terminales

```txt
Σ = { id, |, &, ~, (, ) }
```

### 7.3 Reglas de producción

```txt
R:
S -> E
E -> E | T
E -> T
T -> T & F
T -> F
F -> ~ F
F -> ( E )
F -> id
```

### 7.4 Símbolo inicial

```txt
S
```

---

## 8. Gramática recomendada para implementación

La gramática original tiene recursividad izquierda en:

```txt
E -> E | T
T -> T & F
```

Esa forma es correcta a nivel teórico, pero puede causar problemas si se implementa un parser descendente recursivo.

Por eso, para programar el analizador sintáctico se recomienda usar una versión equivalente sin recursividad izquierda:

```txt
S       -> E

E       -> T E'
E'      -> | T E'
E'      -> ε

T       -> F T'
T'      -> & F T'
T'      -> ε

F       -> ~ F
F       -> ( E )
F       -> id
```

Esta versión conserva la precedencia:

```txt
~  mayor precedencia
&  precedencia intermedia
|  menor precedencia
```

---

## 9. Lexemas y tokens

El analizador léxico debe recorrer la cadena ingresada y convertir cada lexema en un token.

Ejemplo de entrada:

```txt
A | B & ~C
```

Tabla esperada:

| Lexema | Token |
|---|---|
| `A` | `VAR` |
| `|` | `OR` |
| `B` | `VAR` |
| `&` | `AND` |
| `~` | `NOT` |
| `C` | `VAR` |

---

## 10. Expresiones regulares recomendadas

Se deben utilizar expresiones regulares para reconocer los lexemas.

```python
TOKEN_SPECS = [
    ("WHITESPACE", r"\s+"),                  # Espacios en blanco que serán ignorados
    ("OR",         r"\|"),                   # Operador OR
    ("AND",        r"&"),                    # Operador AND
    ("NOT",        r"~"),                    # Operador NOT
    ("LPAREN",     r"\("),                   # Paréntesis izquierdo
    ("RPAREN",     r"\)"),                   # Paréntesis derecho
    ("VAR",        r"[A-Za-z][A-Za-z0-9_]*"),# Variables: A, B, C, id, var1, etc.
    ("MISMATCH",   r"."),                    # Cualquier símbolo no reconocido
]
```

### Variables permitidas

El terminal `id` de la gramática no significa que la entrada solo pueda contener la palabra `id`.

En la implementación, `id` representa cualquier variable válida, por ejemplo:

```txt
A
B
C
X
Y
id
var1
dato_2
```

Por eso, el token `VAR` se relaciona con el terminal gramatical `id`.

---

## 11. Código base del analizador léxico

Archivo sugerido:

```txt
backend/lexer.py
```

Código base:

```python
import re
from dataclasses import dataclass


@dataclass
class Token:
    """
    Representa un token generado por el analizador léxico.

    Atributos:
        type: tipo de token, por ejemplo VAR, OR, AND, NOT.
        lexeme: texto original encontrado en la cadena.
        position: posición inicial del lexema dentro de la cadena.
    """
    type: str
    lexeme: str
    position: int


# Definición de tokens usando expresiones regulares.
TOKEN_SPECS = [
    ("WHITESPACE", r"\s+"),                   # Espacios en blanco
    ("OR",         r"\|"),                    # Operador OR
    ("AND",        r"&"),                     # Operador AND
    ("NOT",        r"~"),                     # Operador NOT
    ("LPAREN",     r"\("),                    # Paréntesis izquierdo
    ("RPAREN",     r"\)"),                    # Paréntesis derecho
    ("VAR",        r"[A-Za-z][A-Za-z0-9_]*"), # Variables como A, B, id, var1
    ("MISMATCH",   r"."),                     # Caracteres inválidos
]


def tokenize(text: str) -> list[Token]:
    """
    Convierte una cadena de entrada en una lista de tokens.

    Args:
        text: expresión lógica ingresada por el usuario.

    Returns:
        Lista de tokens válidos.

    Raises:
        SyntaxError: si encuentra un símbolo no reconocido.
    """

    # Se combinan todas las expresiones regulares en una sola.
    token_regex = "|".join(
        f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS
    )

    tokens = []

    # Se recorren todas las coincidencias encontradas en la cadena.
    for match in re.finditer(token_regex, text):
        token_type = match.lastgroup
        lexeme = match.group()
        position = match.start()

        # Los espacios no se agregan a la lista de tokens.
        if token_type == "WHITESPACE":
            continue

        # Si el símbolo no pertenece al lenguaje, se genera error.
        if token_type == "MISMATCH":
            raise SyntaxError(
                f"Símbolo inválido '{lexeme}' en la posición {position}"
            )

        tokens.append(Token(token_type, lexeme, position))

    # Token especial para indicar el final de la cadena.
    tokens.append(Token("EOF", "", len(text)))

    return tokens
```

---

## 12. Código base del parser

Archivo sugerido:

```txt
backend/parser.py
```

El parser debe usar la gramática sin recursividad izquierda:

```txt
E  -> T E'
T  -> F T'
F  -> ~F | (E) | id
```

Código base:

```python
from dataclasses import dataclass, field
from backend.lexer import Token


@dataclass
class Node:
    """
    Nodo del árbol de derivación o árbol sintáctico.

    Atributos:
        name: nombre del nodo, por ejemplo E, T, F, OR, AND, VAR.
        value: valor opcional del nodo, por ejemplo A, B o C.
        children: lista de nodos hijos.
    """
    name: str
    value: str | None = None
    children: list["Node"] = field(default_factory=list)


class Parser:
    """
    Analizador sintáctico descendente recursivo.

    Respeta la precedencia:
        1. NOT
        2. AND
        3. OR
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def current(self) -> Token:
        """Devuelve el token actual."""
        return self.tokens[self.position]

    def consume(self, expected_type: str) -> Token:
        """
        Consume el token actual si coincide con el tipo esperado.

        Args:
            expected_type: tipo de token que se espera encontrar.

        Returns:
            Token consumido.

        Raises:
            SyntaxError: si el token actual no coincide con el esperado.
        """

        token = self.current()

        if token.type != expected_type:
            raise SyntaxError(
                f"Se esperaba {expected_type}, "
                f"pero se encontró '{token.lexeme}' en posición {token.position}"
            )

        self.position += 1
        return token

    def parse(self) -> Node:
        """
        Inicia el análisis sintáctico desde el símbolo inicial S.

        Returns:
            Nodo raíz del árbol.

        Raises:
            SyntaxError: si sobran tokens luego de analizar la expresión.
        """

        expression_node = self.parse_expression()
        root = Node("S", children=[expression_node])

        # Al terminar, solo debe quedar el token EOF.
        if self.current().type != "EOF":
            token = self.current()
            raise SyntaxError(
                f"Token inesperado '{token.lexeme}' en posición {token.position}"
            )

        return root

    def parse_expression(self) -> Node:
        """
        Analiza expresiones con operador OR.

        Equivale a:
            E -> T E'
            E' -> | T E' | ε
        """

        left = self.parse_term()

        # Mientras se encuentren operadores OR, se agrupan expresiones.
        while self.current().type == "OR":
            operator = self.consume("OR")
            right = self.parse_term()

            left = Node(
                "E",
                children=[
                    left,
                    Node("OR", value=operator.lexeme),
                    right
                ]
            )

        return left

    def parse_term(self) -> Node:
        """
        Analiza términos con operador AND.

        Equivale a:
            T -> F T'
            T' -> & F T' | ε
        """

        left = self.parse_factor()

        # Mientras se encuentren operadores AND, se agrupan factores.
        while self.current().type == "AND":
            operator = self.consume("AND")
            right = self.parse_factor()

            left = Node(
                "T",
                children=[
                    left,
                    Node("AND", value=operator.lexeme),
                    right
                ]
            )

        return left

    def parse_factor(self) -> Node:
        """
        Analiza factores.

        Equivale a:
            F -> ~F
            F -> (E)
            F -> id
        """

        token = self.current()

        # Caso F -> ~F
        if token.type == "NOT":
            operator = self.consume("NOT")
            factor = self.parse_factor()

            return Node(
                "F",
                children=[
                    Node("NOT", value=operator.lexeme),
                    factor
                ]
            )

        # Caso F -> (E)
        if token.type == "LPAREN":
            left_paren = self.consume("LPAREN")
            expression = self.parse_expression()
            right_paren = self.consume("RPAREN")

            return Node(
                "F",
                children=[
                    Node("LPAREN", value=left_paren.lexeme),
                    expression,
                    Node("RPAREN", value=right_paren.lexeme)
                ]
            )

        # Caso F -> id
        if token.type == "VAR":
            variable = self.consume("VAR")

            return Node(
                "F",
                children=[
                    Node("VAR", value=variable.lexeme)
                ]
            )

        raise SyntaxError(
            f"Se esperaba una variable, '~' o '(', "
            f"pero se encontró '{token.lexeme}' en posición {token.position}"
        )
```

---

## 13. Generación del árbol de derivación

Archivo sugerido:

```txt
backend/tree_utils.py
```

El árbol puede mostrarse como texto ASCII en el frontend.

Ejemplo para:

```txt
A | B & ~C
```

Árbol esperado:

```txt
S
└── E
    ├── F
    │   └── VAR(A)
    ├── OR(|)
    └── T
        ├── F
        │   └── VAR(B)
        ├── AND(&)
        └── F
            ├── NOT(~)
            └── F
                └── VAR(C)
```

Código base para imprimir el árbol:

```python
def tree_to_ascii(node, prefix: str = "", is_last: bool = True) -> str:
    """
    Convierte un árbol sintáctico en una representación ASCII.

    Args:
        node: nodo raíz del árbol.
        prefix: prefijo usado para dibujar las ramas.
        is_last: indica si el nodo actual es el último hijo.

    Returns:
        Cadena con el árbol en formato visual.
    """

    # Se muestra el nombre del nodo y, si existe, su valor.
    label = node.name if node.value is None else f"{node.name}({node.value})"

    connector = "└── " if is_last else "├── "
    result = prefix + connector + label + "\n"

    # Se actualiza el prefijo para los hijos.
    new_prefix = prefix + ("    " if is_last else "│   ")

    for index, child in enumerate(node.children):
        child_is_last = index == len(node.children) - 1
        result += tree_to_ascii(child, new_prefix, child_is_last)

    return result
```

---

## 14. Derivación por izquierda

La derivación por izquierda siempre reemplaza primero el no terminal más a la izquierda.

Para la cadena:

```txt
A | B & ~C
```

Derivación esperada:

```txt
S
=> E
=> E | T
=> T | T
=> F | T
=> id | T
=> A | T
=> A | T & F
=> A | F & F
=> A | id & F
=> A | B & F
=> A | B & ~F
=> A | B & ~id
=> A | B & ~C
```

---

## 15. Derivación por derecha

La derivación por derecha siempre reemplaza primero el no terminal más a la derecha.

Para la cadena:

```txt
A | B & ~C
```

Derivación esperada:

```txt
S
=> E
=> E | T
=> E | T & F
=> E | T & ~F
=> E | T & ~id
=> E | T & ~C
=> E | F & ~C
=> E | id & ~C
=> E | B & ~C
=> T | B & ~C
=> F | B & ~C
=> id | B & ~C
=> A | B & ~C
```

---

## 16. Generación de derivaciones en el programa

Archivo sugerido:

```txt
backend/derivations.py
```

Para el desarrollo inicial, se recomienda que las derivaciones se generen a partir del árbol sintáctico.

El sistema debe mostrar como mínimo:

- Derivación por izquierda.
- Derivación por derecha.
- Cadena final generada.

Estrategia recomendada:

```txt
1. Construir el árbol sintáctico.
2. Recorrer el árbol reemplazando no terminales.
3. Para derivación por izquierda:
   - Reemplazar siempre el primer no terminal pendiente.
4. Para derivación por derecha:
   - Reemplazar siempre el último no terminal pendiente.
5. Guardar cada paso en una lista.
6. Mostrar la lista en el frontend.
```

Ejemplo de estructura de salida:

```python
{
    "left_derivation": [
        "S",
        "E",
        "E | T",
        "T | T",
        "F | T",
        "id | T",
        "A | T",
        "A | T & F",
        "A | F & F",
        "A | id & F",
        "A | B & F",
        "A | B & ~F",
        "A | B & ~id",
        "A | B & ~C"
    ],
    "right_derivation": [
        "S",
        "E",
        "E | T",
        "E | T & F",
        "E | T & ~F",
        "E | T & ~id",
        "E | T & ~C",
        "E | F & ~C",
        "E | id & ~C",
        "E | B & ~C",
        "T | B & ~C",
        "F | B & ~C",
        "id | B & ~C",
        "A | B & ~C"
    ]
}
```

---

## 17. Código base de Flask

Archivo sugerido:

```txt
app.py
```

Código base:

```python
from flask import Flask, render_template, request
from backend.lexer import tokenize
from backend.parser import Parser
from backend.tree_utils import tree_to_ascii


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    Muestra el formulario principal donde el usuario ingresa la expresión.
    """
    return render_template("index.html")


@app.route("/analizar", methods=["POST"])
def analizar():
    """
    Recibe la expresión enviada desde el formulario,
    ejecuta el análisis léxico y sintáctico,
    y muestra los resultados.
    """

    expression = request.form.get("expression", "")

    try:
        # 1. Análisis léxico
        tokens = tokenize(expression)

        # 2. Análisis sintáctico
        parser = Parser(tokens)
        tree = parser.parse()

        # 3. Conversión del árbol a texto visual
        ascii_tree = tree_to_ascii(tree)

        # 4. Tabla de lexemas y tokens, excluyendo EOF
        token_table = [
            {"lexeme": token.lexeme, "token": token.type}
            for token in tokens
            if token.type != "EOF"
        ]

        # 5. Resultado exitoso
        return render_template(
            "resultados.html",
            expression=expression,
            valid=True,
            token_table=token_table,
            tree=ascii_tree,
            error=None
        )

    except SyntaxError as error:
        # Si existe un error léxico o sintáctico, se muestra al usuario.
        return render_template(
            "resultados.html",
            expression=expression,
            valid=False,
            token_table=[],
            tree=None,
            error=str(error)
        )


if __name__ == "__main__":
    # Modo debug solo para desarrollo.
    app.run(debug=True)
```

---

## 18. Interfaz principal

Archivo sugerido:

```txt
templates/index.html
```

Código base:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Analizador CFG Booleano</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <main class="container">
        <section class="card">
            <h1>Analizador de Expresiones Booleanas</h1>

            <p>
                Ingresa una expresión lógica usando variables, OR, AND,
                NOT y paréntesis.
            </p>

            <form action="/analizar" method="POST">
                <label for="expression">Expresión:</label>

                <input
                    type="text"
                    id="expression"
                    name="expression"
                    placeholder="Ejemplo: A | B & ~C"
                    required
                >

                <button type="submit">Analizar</button>
            </form>

            <div class="examples">
                <h2>Ejemplos válidos</h2>
                <ul>
                    <li><code>A | B & ~C</code></li>
                    <li><code>id | ~ ( id & id )</code></li>
                    <li><code>A | B & C</code></li>
                </ul>
            </div>
        </section>
    </main>
</body>
</html>
```

---

## 19. Interfaz de resultados

Archivo sugerido:

```txt
templates/resultados.html
```

Código base:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultados del análisis</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <main class="container">
        <section class="card">
            <h1>Resultados del análisis</h1>

            <p>
                <strong>Expresión ingresada:</strong>
                <code>{{ expression }}</code>
            </p>

            {% if valid %}
                <p class="success">La cadena es válida según la gramática.</p>

                <h2>Tabla de lexemas y tokens</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Lexema</th>
                            <th>Token</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in token_table %}
                            <tr>
                                <td><code>{{ item.lexeme }}</code></td>
                                <td><code>{{ item.token }}</code></td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>

                <h2>Árbol de derivación</h2>
                <pre>{{ tree }}</pre>

                <h2>Derivación por izquierda</h2>
                <p>
                    Aquí se debe imprimir la lista de pasos generada
                    desde <code>backend/derivations.py</code>.
                </p>

                <h2>Derivación por derecha</h2>
                <p>
                    Aquí se debe imprimir la lista de pasos generada
                    desde <code>backend/derivations.py</code>.
                </p>

            {% else %}
                <p class="error">La cadena no es válida.</p>
                <p><strong>Error:</strong> {{ error }}</p>
            {% endif %}

            <a href="/">Analizar otra expresión</a>
        </section>
    </main>
</body>
</html>
```

---

## 20. Estilos claros para el frontend

Archivo sugerido:

```txt
static/css/styles.css
```

Código base:

```css
/* Tema claro general */
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f5f7fb;
    color: #1f2937;
}

/* Contenedor principal */
.container {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
}

/* Tarjeta visual principal */
.card {
    background: #ffffff;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

/* Títulos */
h1, h2 {
    color: #111827;
}

/* Campo de entrada */
input {
    width: 100%;
    padding: 12px;
    margin-top: 8px;
    margin-bottom: 16px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 16px;
}

/* Botón principal */
button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 12px 18px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
}

/* Cambio visual al pasar el cursor */
button:hover {
    background: #1d4ed8;
}

/* Tabla de lexemas y tokens */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
}

th, td {
    border: 1px solid #d1d5db;
    padding: 10px;
    text-align: left;
}

th {
    background: #e5e7eb;
}

/* Bloques de árbol y derivaciones */
pre {
    background: #f3f4f6;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
}

/* Mensajes de validación */
.success {
    color: #047857;
    font-weight: bold;
}

.error {
    color: #b91c1c;
    font-weight: bold;
}
```

---

## 21. Casos de prueba obligatorios

El sistema debe probarse como mínimo con las siguientes cadenas:

| Cadena | Resultado esperado |
|---|---|
| `A | B & ~C` | Válida |
| `id | ~ ( id & id )` | Válida |
| `A | B & C` | Válida |
| `~A` | Válida |
| `(A | B) & C` | Válida |
| `A & | B` | Inválida |
| `A | (B & C` | Inválida |
| `A @ B` | Inválida |

---

## 22. Resultado esperado para el caso `A | B & ~C`

### 22.1 Tabla de tokens

| Lexema | Token |
|---|---|
| `A` | `VAR` |
| `|` | `OR` |
| `B` | `VAR` |
| `&` | `AND` |
| `~` | `NOT` |
| `C` | `VAR` |

### 22.2 Validación

```txt
La cadena es válida según la gramática.
```

### 22.3 Árbol sintáctico esperado

```txt
S
└── E
    ├── F
    │   └── VAR(A)
    ├── OR(|)
    └── T
        ├── F
        │   └── VAR(B)
        ├── AND(&)
        └── F
            ├── NOT(~)
            └── F
                └── VAR(C)
```

### 22.4 Interpretación de precedencia

La cadena:

```txt
A | B & ~C
```

Debe interpretarse como:

```txt
A | (B & (~C))
```

No debe interpretarse como:

```txt
(A | B) & ~C
```

---

## 23. Criterios de aceptación

El proyecto estará completo cuando cumpla con lo siguiente:

- Permite ingresar expresiones booleanas desde una interfaz web.
- Usa Flask para mostrar formularios y resultados.
- Usa Python para el análisis léxico y sintáctico.
- Reconoce variables como `A`, `B`, `C`, `id`, `var1`, etc.
- Usa expresiones regulares para identificar tokens.
- Muestra una tabla con lexema y token.
- Valida correctamente cadenas válidas e inválidas.
- Respeta la precedencia de `~`, `&` y `|`.
- Genera derivación por izquierda.
- Genera derivación por derecha.
- Genera árbol de derivación.
- Incluye comentarios en funciones y partes importantes del código.
- Mantiene una estructura modular.
- Usa una interfaz clara y ordenada.

---

## 24. Reglas de código limpio

El código debe cumplir estas reglas:

1. Usar nombres claros para variables, funciones y clases.
2. Separar el lexer, parser, árbol y aplicación Flask en archivos diferentes.
3. Comentar funciones con docstrings.
4. Comentar bloques de código que representen partes importantes del análisis.
5. Evitar funciones demasiado largas.
6. Manejar errores con mensajes comprensibles para el usuario.
7. No mezclar lógica de análisis con HTML.
8. No escribir todo el programa dentro de `app.py`.
9. Mantener los estilos CSS separados en `static/css/styles.css`.

---

## 25. Prompt base para desarrollar el programa

Este prompt puede usarse como guía para solicitar la implementación completa del sistema:

```txt
Desarrolla una aplicación web en Python usando Flask para analizar expresiones lógicas booleanas mediante una Gramática Libre de Contexto.

La gramática teórica es:

S -> E
E -> E | T | T
T -> T & F | F
F -> ~F | (E) | id

Para la implementación usa una versión equivalente sin recursividad izquierda:

S -> E
E -> T E'
E' -> | T E' | ε
T -> F T'
T' -> & F T' | ε
F -> ~F | (E) | id

El sistema debe permitir ingresar expresiones como:
A | B & ~C
id | ~ ( id & id )
A | B & C

Requisitos:
1. Crear un analizador léxico con expresiones regulares.
2. Reconocer tokens VAR, OR, AND, NOT, LPAREN, RPAREN y EOF.
3. El token VAR debe aceptar variables como A, B, C, id, var1 y similares.
4. Mostrar una tabla con columnas Lexema y Token.
5. Crear un parser descendente recursivo que respete la precedencia:
   NOT > AND > OR.
6. Validar si la cadena pertenece o no a la gramática.
7. Generar el árbol de derivación.
8. Generar derivación por izquierda.
9. Generar derivación por derecha.
10. Usar Flask con plantillas HTML y CSS.
11. Diseñar una interfaz de tema claro.
12. Separar el código en módulos:
    - app.py
    - backend/lexer.py
    - backend/parser.py
    - backend/derivations.py
    - backend/tree_utils.py
    - templates/index.html
    - templates/resultados.html
    - static/css/styles.css
13. Incluir comentarios y docstrings en el código para mantener código limpio.
14. Incluir casos de prueba para cadenas válidas e inválidas.
```

---

## 26. Comando de ejecución

Instalar Flask:

```bash
pip install flask
```

Ejecutar el sistema:

```bash
python app.py
```

Abrir en el navegador:

```txt
http://127.0.0.1:5000
```

---

## 27. Conclusión

Este README define la guía base para construir una aplicación web que permita validar expresiones booleanas usando una CFG. La solución combina análisis léxico, análisis sintáctico, derivaciones y árbol de derivación, cumpliendo con los objetivos de comprender e implementar gramáticas libres de contexto en un entorno computacional.
