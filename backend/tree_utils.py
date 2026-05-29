"""Utilidades para representar el arbol de derivacion."""

from __future__ import annotations

from backend.parser import Node


def tree_to_ascii(node: Node) -> str:
    """
    Convierte un arbol sintactico en una representacion visual de texto.

    Args:
        node: Nodo raiz del arbol.

    Returns:
        Cadena con el arbol en formato de ramas.
    """

    lines = [node.label]

    for index, child in enumerate(node.children):
        is_last = index == len(node.children) - 1
        _build_tree_lines(child, "", is_last, lines)

    return "\n".join(lines)


def _build_tree_lines(
    node: Node,
    prefix: str,
    is_last: bool,
    lines: list[str],
) -> None:
    """Agrega recursivamente las lineas del arbol."""

    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{node.label}")

    child_prefix = prefix + ("    " if is_last else "│   ")
    for index, child in enumerate(node.children):
        child_is_last = index == len(node.children) - 1
        _build_tree_lines(child, child_prefix, child_is_last, lines)

