"""Aplicacion Flask para analizar expresiones booleanas con una CFG."""

from __future__ import annotations

import os

from flask import Flask, render_template, request

from backend.derivations import generate_derivations
from backend.grammar import IMPLEMENTATION_PRODUCTIONS, PRODUCTIONS
from backend.lexer import tokenize
from backend.parser import Parser
from backend.tree_utils import tree_to_ascii

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Muestra el formulario principal."""

    return render_template(
        "index.html",
        productions=PRODUCTIONS,
        implementation_productions=IMPLEMENTATION_PRODUCTIONS,
    )


@app.route("/analizar", methods=["POST"])
def analizar():
    """
    Recibe la expresion, ejecuta el lexer y parser, y muestra resultados.
    """

    expression = request.form.get("expression", "").strip()

    try:
        result = analyze_expression(expression)
        return render_template("resultados.html", **result)
    except SyntaxError as error:
        return render_template(
            "resultados.html",
            expression=expression,
            valid=False,
            token_table=[],
            tree=None,
            tree_root=None,
            left_derivation=[],
            right_derivation=[],
            final_string="",
            error=str(error),
        )


def analyze_expression(expression: str) -> dict[str, object]:
    """
    Ejecuta el flujo completo de analisis sobre una expresion.

    Args:
        expression: Cadena ingresada por el usuario.

    Returns:
        Datos listos para renderizar en la plantilla de resultados.

    Raises:
        SyntaxError: Si la cadena no pertenece a la gramatica.
    """

    tokens = tokenize(expression)
    parser = Parser(tokens)
    tree = parser.parse()
    derivations = generate_derivations(tree)

    token_table = [
        {"lexeme": token.lexeme, "token": token.type}
        for token in tokens
        if token.type != "EOF"
    ]

    return {
        "expression": expression,
        "valid": True,
        "token_table": token_table,
        "tree": tree_to_ascii(tree),
        "tree_root": tree,
        "left_derivation": derivations["left_derivation"],
        "right_derivation": derivations["right_derivation"],
        "final_string": derivations["final_string"],
        "error": None,
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True, port=port)
