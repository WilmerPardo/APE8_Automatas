"""Verifica si la cadena cumple con la gramatica"""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.grammar import TOKEN_LABELS
from backend.lexer import Token


@dataclass
class Node:
    """
    Nodo del arbol de derivacion.

    Attributes:
        name: Nombre del simbolo o token, por ejemplo E, T, F, VAR.
        value: Valor opcional para terminales, por ejemplo A, | o &.
        children: Lista de nodos hijos.
    """

    name: str
    value: str | None = None
    children: list["Node"] = field(default_factory=list)

    @property
    def label(self) -> str:
        """Devuelve una etiqueta legible para mostrar en el arbol."""

        if self.value is None:
            return self.name
        return f"{self.name}({self.value})"


class Parser:
    """
    Analizador sintactico descendente recursivo.

    La implementacion evita recursividad izquierda, pero construye un arbol
    compatible con la gramatica teorica:
        S -> E
        E -> E | T | T
        T -> T & F | F
        F -> ~F | (E) | id
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def current(self) -> Token:
        """Devuelve el token actual sin consumirlo."""

        return self.tokens[self.position]

    def consume(self, expected_type: str) -> Token:
        """
        Consume el token actual si coincide con el tipo esperado.
        Args:
            expected_type: Tipo de token que se espera encontrar.
        Returns:
            Token consumido.
        Raises:
            SyntaxError: Si el token actual no coincide con el esperado.
        """

        token = self.current()
        if token.type != expected_type:
            expected = TOKEN_LABELS.get(expected_type, expected_type)
            found = self._describe_token(token)
            raise SyntaxError(
                f"Se esperaba {expected}, pero se encontro {found} "
                f"en la posicion {token.position}."
            )

        self.position += 1
        return token

    def parse(self) -> Node:
        """
        Inicia el analisis sintactico desde el simbolo inicial S.
        Returns:
            Nodo raiz del arbol de derivacion.
        Raises:
            SyntaxError: Si sobran tokens luego de analizar la expresion.
        """

        expression_node = self.parse_expression()
        root = Node("S", children=[expression_node])

        if self.current().type != "EOF":
            token = self.current()
            raise SyntaxError(
                f"Token inesperado {self._describe_token(token)} "
                f"en la posicion {token.position}."
            )

        return root

    def parse_expression(self) -> Node:
        """
        Analiza expresiones con OR.

        Equivale a:
            E -> T E'
            E' -> | T E' | epsilon
        """

        left = Node("E", children=[self.parse_term()])

        while self.current().type == "OR":
            operator = self.consume("OR")
            right = self.parse_term()
            left = Node(
                "E",
                children=[
                    left,
                    Node("OR", value=operator.lexeme),
                    right,
                ],
            )

        return left

    def parse_term(self) -> Node:
        """
        Analiza terminos con AND.
        Equivale a:
            T -> F T'
            T' -> & F T' | epsilon
        """

        left = Node("T", children=[self.parse_factor()])

        while self.current().type == "AND":
            operator = self.consume("AND")
            right = self.parse_factor()
            left = Node(
                "T",
                children=[
                    left,
                    Node("AND", value=operator.lexeme),
                    right,
                ],
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

        if token.type == "NOT":
            operator = self.consume("NOT")
            factor = self.parse_factor()
            return Node(
                "F",
                children=[
                    Node("NOT", value=operator.lexeme),
                    factor,
                ],
            )

        if token.type == "LPAREN":
            left_paren = self.consume("LPAREN")
            expression = self.parse_expression()
            right_paren = self.consume("RPAREN")
            return Node(
                "F",
                children=[
                    Node("LPAREN", value=left_paren.lexeme),
                    expression,
                    Node("RPAREN", value=right_paren.lexeme),
                ],
            )

        if token.type == "VAR":
            variable = self.consume("VAR")
            return Node(
                "F",
                children=[
                    Node("VAR", value=variable.lexeme),
                ],
            )

        raise SyntaxError(
            "Se esperaba una variable, '~' o '(', "
            f"pero se encontro {self._describe_token(token)} "
            f"en la posicion {token.position}."
        )

    @staticmethod
    def _describe_token(token: Token) -> str:
        """Devuelve una descripcion clara del token para errores."""

        if token.type == "EOF":
            return "fin de cadena"
        return f"'{token.lexeme}'"

