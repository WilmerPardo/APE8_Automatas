"""Generacion de derivaciones izquierda y derecha desde el arbol."""

from __future__ import annotations

from dataclasses import dataclass

from backend.grammar import NON_TERMINALS
from backend.parser import Node


@dataclass(frozen=True)
class NonTerminalSlot:
    """Simbolo no terminal pendiente de expandir."""

    node: Node


@dataclass(frozen=True)
class VariableSlot:
    """Terminal id pendiente de sustituirse por su lexema real."""

    value: str


SententialSymbol = str | NonTerminalSlot | VariableSlot

TOKEN_VALUES = {
    "OR": "|",
    "AND": "&",
    "NOT": "~",
    "LPAREN": "(",
    "RPAREN": ")",
}


def generate_derivations(tree: Node) -> dict[str, list[str] | str]:
    """
    Genera derivaciones por izquierda y por derecha.

    Args:
        tree: Arbol de derivacion generado por el parser.

    Returns:
        Diccionario con derivacion izquierda, derecha y cadena final.
    """

    left_derivation = _derive(tree, direction="left")
    right_derivation = _derive(tree, direction="right")

    return {
        "left_derivation": left_derivation,
        "right_derivation": right_derivation,
        "final_string": left_derivation[-1] if left_derivation else "",
    }


def _derive(tree: Node, direction: str) -> list[str]:
    """Ejecuta la derivacion reemplazando siempre a la izquierda o derecha."""

    form: list[SententialSymbol] = [NonTerminalSlot(tree)]
    steps = [_format_sentential_form(form)]

    while _has_pending_symbol(form):
        index = _select_pending_index(form, direction)
        selected = form[index]
        form = form[:index] + _expand_symbol(selected) + form[index + 1 :]

        current_step = _format_sentential_form(form)
        if current_step != steps[-1]:
            steps.append(current_step)

    return steps


def _has_pending_symbol(form: list[SententialSymbol]) -> bool:
    """Indica si aun existen no terminales o variables por resolver."""

    return any(isinstance(item, (NonTerminalSlot, VariableSlot)) for item in form)


def _select_pending_index(form: list[SententialSymbol], direction: str) -> int:
    """Selecciona el indice pendiente segun el tipo de derivacion."""

    indexes = range(len(form)) if direction == "left" else range(len(form) - 1, -1, -1)

    for index in indexes:
        if isinstance(form[index], (NonTerminalSlot, VariableSlot)):
            return index

    raise ValueError("No hay simbolos pendientes para derivar.")


def _expand_symbol(symbol: SententialSymbol) -> list[SententialSymbol]:
    """Expande un no terminal o resuelve un id a su lexema."""

    if isinstance(symbol, VariableSlot):
        return [symbol.value]

    if isinstance(symbol, str):
        return [symbol]

    return _expand_node(symbol.node)


def _expand_node(node: Node) -> list[SententialSymbol]:
    """Convierte los hijos de un nodo en una forma sentencial."""

    expanded: list[SententialSymbol] = []

    for child in node.children:
        if child.name in NON_TERMINALS:
            expanded.append(NonTerminalSlot(child))
        elif child.name == "VAR":
            expanded.append(VariableSlot(child.value or "id"))
        else:
            expanded.append(child.value or TOKEN_VALUES.get(child.name, child.name))

    return expanded


def _format_sentential_form(form: list[SententialSymbol]) -> str:
    """Da formato legible a una forma sentencial."""

    symbols = [_symbol_to_text(symbol) for symbol in form]
    return _join_symbols(symbols)


def _symbol_to_text(symbol: SententialSymbol) -> str:
    """Convierte un simbolo interno en texto visible."""

    if isinstance(symbol, NonTerminalSlot):
        return symbol.node.name
    if isinstance(symbol, VariableSlot):
        return "id"
    return symbol


def _join_symbols(symbols: list[str]) -> str:
    """Une simbolos dejando espacios naturales para operadores y parentesis."""

    result = ""
    previous = ""

    for symbol in symbols:
        if not result:
            result = symbol
        elif symbol == ")":
            result += symbol
        elif previous in {"(", "~"}:
            result += symbol
        elif symbol in {"|", "&"}:
            result += f" {symbol}"
        elif previous in {"|", "&"}:
            result += f" {symbol}"
        elif symbol == "(":
            result += f" {symbol}"
        else:
            result += f" {symbol}"

        previous = symbol

    return result

