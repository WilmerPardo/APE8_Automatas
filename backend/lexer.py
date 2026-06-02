"""Convierte la entrada del usuario en una secuencia de tokens"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    """
    Representa un token generado por el analizador lexico.

    Attributes:
        type: Tipo del token, por ejemplo VAR, OR, AND o NOT.
        lexeme: Texto original reconocido en la expresion.
        position: Posicion inicial del lexema dentro de la cadena.
    """

    type: str
    lexeme: str
    position: int


TOKEN_SPECS = [
    ("WHITESPACE", r"\s+"),
    ("OR", r"\|"),
    ("AND", r"&"),
    ("NOT", r"~"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("VAR", r"[A-Za-z][A-Za-z0-9_]*"),
    ("MISMATCH", r"."),
]

TOKEN_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS)
)


def tokenize(text: str) -> list[Token]:
    """
    Convierte una cadena de entrada en una lista de tokens.
    Args:
        text: Expresion logica ingresada por el usuario.
    Returns:
        Lista de tokens validos mas un token EOF al final.
    Raises:
        SyntaxError: Si aparece un simbolo que no pertenece al lenguaje.
    """

    tokens: list[Token] = []

    for match in TOKEN_REGEX.finditer(text):
        token_type = match.lastgroup
        lexeme = match.group()
        position = match.start()

        if token_type == "WHITESPACE":
            continue

        if token_type == "MISMATCH":
            raise SyntaxError(
                f"Simbolo invalido '{lexeme}' en la posicion {position}."
            )

        if token_type is not None:
            tokens.append(Token(token_type, lexeme, position))

    tokens.append(Token("EOF", "", len(text)))
    return tokens

