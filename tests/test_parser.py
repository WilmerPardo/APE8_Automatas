"""Pruebas del analizador CFG booleano."""

from __future__ import annotations

import unittest

from backend.derivations import generate_derivations
from backend.lexer import tokenize
from backend.parser import Parser


def parse_expression(expression: str):
    """Tokeniza y parsea una expresion."""

    return Parser(tokenize(expression)).parse()


class BooleanCFGParserTest(unittest.TestCase):
    """Casos obligatorios de validacion del README."""

    def test_valid_expressions(self):
        valid_cases = [
            "A | B & ~C",
            "id | ~ ( id & id )",
            "A | B & C",
            "~A",
            "(A | B) & C",
        ]

        for expression in valid_cases:
            with self.subTest(expression=expression):
                tree = parse_expression(expression)
                self.assertEqual(tree.name, "S")

    def test_invalid_expressions(self):
        invalid_cases = [
            "A & | B",
            "A | (B & C",
            "A @ B",
            "",
        ]

        for expression in invalid_cases:
            with self.subTest(expression=expression):
                with self.assertRaises(SyntaxError):
                    parse_expression(expression)

    def test_token_table_for_readme_case(self):
        tokens = [token for token in tokenize("A | B & ~C") if token.type != "EOF"]
        table = [(token.lexeme, token.type) for token in tokens]

        self.assertEqual(
            table,
            [
                ("A", "VAR"),
                ("|", "OR"),
                ("B", "VAR"),
                ("&", "AND"),
                ("~", "NOT"),
                ("C", "VAR"),
            ],
        )

    def test_derivations_for_readme_case(self):
        tree = parse_expression("A | B & ~C")
        derivations = generate_derivations(tree)

        self.assertEqual(
            derivations["left_derivation"],
            [
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
                "A | B & ~C",
            ],
        )

        self.assertEqual(
            derivations["right_derivation"],
            [
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
                "A | B & ~C",
            ],
        )


if __name__ == "__main__":
    unittest.main()

