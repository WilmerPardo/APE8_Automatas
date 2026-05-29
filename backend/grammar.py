"""Definicion formal de la gramatica usada por la aplicacion."""

START_SYMBOL = "S"

NON_TERMINALS = ("S", "E", "T", "F")

TERMINALS = ("id", "|", "&", "~", "(", ")")

PRODUCTIONS = (
    "S -> E",
    "E -> E | T",
    "E -> T",
    "T -> T & F",
    "T -> F",
    "F -> ~ F",
    "F -> ( E )",
    "F -> id",
)

IMPLEMENTATION_PRODUCTIONS = (
    "S -> E",
    "E -> T E'",
    "E' -> | T E'",
    "E' -> epsilon",
    "T -> F T'",
    "T' -> & F T'",
    "T' -> epsilon",
    "F -> ~ F",
    "F -> ( E )",
    "F -> id",
)

TOKEN_LABELS = {
    "VAR": "variable",
    "OR": "|",
    "AND": "&",
    "NOT": "~",
    "LPAREN": "(",
    "RPAREN": ")",
    "EOF": "fin de cadena",
}

