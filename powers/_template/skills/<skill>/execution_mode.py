"""Resolución y validación del Modo_Ejecucion de un Power.

Utilidad compartida del modelo estándar de Power. Se resuelve **antes** de
invocar la Herramienta_Real para fijar el nivel técnico de ejecución
(script-kiddie | green-hat | pro). Es un parámetro técnico, ortogonal a la
ética (la distinción Black Hat / White Hat la resuelve la Política ética,
Req 11, no el modo — Req 14.8).

Requisitos:
- Req 14.1: el Power acepta el parámetro Modo_Ejecucion con los tres valores.
- Req 14.2: si no se indica (None/vacío), se aplica el default `script-kiddie`.
- Req 14.7: si el valor no pertenece a {script-kiddie, green-hat, pro}, se
  rechaza con InvalidModeError sin ejecutar la herramienta.

Copiar este archivo a powers/<equipo>/<power>/skills/<skill>/ junto al Power.
"""

from __future__ import annotations

ALLOWED_MODES = ("script-kiddie", "green-hat", "pro")
DEFAULT_MODE = "script-kiddie"


class InvalidModeError(ValueError):
    """Modo_Ejecucion fuera del conjunto admitido (Req 14.7)."""

    pass


def resolve_mode(requested: str | None) -> str:
    """Resuelve el Modo_Ejecucion solicitado a un valor canónico.

    Req 14.2 (default para entrada ausente/vacía) y Req 14.7 (rechazo de
    valores inválidos). Normaliza espacios y mayúsculas antes de comparar.
    """
    if requested is None or (isinstance(requested, str) and not requested.strip()):
        return DEFAULT_MODE
    if not isinstance(requested, str):
        raise InvalidModeError(
            f"Modo_Ejecucion inválido: {requested!r}. "
            f"Admitidos: {', '.join(ALLOWED_MODES)}."
        )
    mode = requested.strip().lower()
    if mode not in ALLOWED_MODES:
        raise InvalidModeError(
            f"Modo_Ejecucion inválido: {requested!r}. "
            f"Admitidos: {', '.join(ALLOWED_MODES)}."
        )
    return mode
