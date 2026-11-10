"""Lógica determinista de la secuencia canónica de fases del Agente_Orquestador.

Este módulo es el *helper* de apoyo del Agente_Orquestador
(`agents/orquestador/orquestador.md`). Centraliza, como lógica pura y
determinista, el conocimiento de la **secuencia canónica EC-Council**
(Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering
Tracks) y la lectura/escritura del estado del engagement en `state.json`.

Alcance de la tarea 3.1 (primitivas de orden):
  - `CANONICAL_SEQUENCE`, `next_phase()`, `previous_incomplete()` y
    `default_next()` dan soporte determinista a la secuencia por defecto
    (Req 1.3) y sirven de base a la lógica de orden/consolidación de 3.2.
  - `load_state()` / `save_state()` leen y escriben
    `engagements/<id>/state.json` preservando el resto del documento
    (Req 1.1, 1.3).

Alcance de la tarea 3.2 (orden y consolidación — Req 1.4, 1.5):
  - `out_of_order_report()` envuelve `previous_incomplete()` para producir la
    estructura/mensaje de reporte de fases previas no completadas que el
    Agente_Orquestador emite ante una fase solicitada fuera de orden, antes de
    delegar (Req 1.5).
  - `consolidate_phase()` registra el resultado de una fase y la marca en
    `completed_phases`, devolviendo la transición ofrecida hacia la fase
    siguiente (Req 1.4). Es una función pura: no muta el estado recibido.

Referencia de diseño: design.md, secciones "Flujo de delegación", "Estado del
engagement — state.json" y "Property 2 / Property 3".
"""

from __future__ import annotations

import copy
import json
import os
from typing import Dict, List, Optional

# --- Secuencia canónica EC-Council (Req 1.1, 1.3) ----------------------------
# Orden secuencial por defecto que el Agente_Orquestador mantiene. Es la única
# fuente de verdad del orden de fases para el helper y para el agente.
CANONICAL_SEQUENCE: List[str] = [
    "Reconnaissance",
    "Scanning",
    "Gaining Access",
    "Maintaining Access",
    "Covering Tracks",
]


class UnknownPhaseError(ValueError):
    """La fase indicada no pertenece a la secuencia canónica EC-Council."""


def _require_known(phase: str) -> str:
    """Valida que ``phase`` sea una fase canónica y la devuelve sin cambios."""
    if phase not in CANONICAL_SEQUENCE:
        raise UnknownPhaseError(
            f"Fase desconocida: {phase!r}. Fases válidas: {CANONICAL_SEQUENCE}"
        )
    return phase


def phase_index(phase: str) -> int:
    """Posición (0-based) de ``phase`` en la secuencia canónica."""
    return CANONICAL_SEQUENCE.index(_require_known(phase))


def next_phase(phase: str) -> Optional[str]:
    """Devuelve la fase sucesora en la secuencia canónica (Req 1.3).

    Para cualquier fase, su sucesora por defecto es exactamente la siguiente en
    Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering
    Tracks. ``Covering Tracks`` no tiene sucesora y devuelve ``None``
    (Property 2 del diseño).
    """
    idx = phase_index(phase)
    if idx + 1 < len(CANONICAL_SEQUENCE):
        return CANONICAL_SEQUENCE[idx + 1]
    return None


def predecessors(phase: str) -> List[str]:
    """Fases que preceden a ``phase`` en la secuencia canónica, en orden."""
    return CANONICAL_SEQUENCE[: phase_index(phase)]


def previous_incomplete(requested: str, completed_phases) -> List[str]:
    """Predecesoras de ``requested`` que aún no están completadas (Req 1.5).

    Dada una fase solicitada y el conjunto de fases ya completadas, devuelve las
    predecesoras de la fase en la secuencia canónica que no estén en
    ``completed_phases``, preservando el orden canónico. El Agente_Orquestador
    reporta esta lista antes de delegar una fase fuera de orden (Property 3 del
    diseño). Las entradas desconocidas de ``completed_phases`` se ignoran.
    """
    completed = set(completed_phases or [])
    return [p for p in predecessors(requested) if p not in completed]


def is_in_order(requested: str, completed_phases) -> bool:
    """¿La fase solicitada está en orden (sin predecesoras pendientes)?

    ``True`` cuando no quedan predecesoras sin completar; en ese caso la fase es
    la siguiente que correspondería delegar directamente (Req 1.2, 1.3).
    """
    return not previous_incomplete(requested, completed_phases)


def default_next(completed_phases) -> Optional[str]:
    """Siguiente fase por defecto dado el conjunto de fases completadas.

    Devuelve la primera fase de la secuencia canónica que aún no esté
    completada; ``None`` si todas lo están. Primitiva de apoyo para la lógica de
    la tarea 3.2.
    """
    completed = set(completed_phases or [])
    for phase in CANONICAL_SEQUENCE:
        if phase not in completed:
            return phase
    return None


# --- Lógica de orden y consolidación de la tarea 3.2 (Req 1.4, 1.5) ----------

def out_of_order_report(requested: str, completed_phases) -> Dict[str, object]:
    """Reporte de fases previas no completadas ante una solicitud (Req 1.5).

    Envuelve :func:`previous_incomplete` para producir la estructura de reporte
    que el Agente_Orquestador emite *antes de delegar* cuando el usuario pide una
    fase: registra la fase solicitada, indica si está en orden y, si no lo está,
    enumera —en orden canónico— las predecesoras que aún no se completaron
    (Property 3 del diseño). Función pura y determinista: no toca `state.json`.

    Devuelve un diccionario con:
      - ``requested``: la fase solicitada (validada contra la secuencia canónica).
      - ``in_order``: ``True`` si no hay predecesoras pendientes.
      - ``pending_previous``: lista ordenada de predecesoras no completadas.
      - ``message``: narrativa lista para incluir en la respuesta al usuario.
    """
    pending = previous_incomplete(_require_known(requested), completed_phases)
    if not pending:
        message = (
            f"La fase '{requested}' está en orden: no hay fases previas "
            f"pendientes. Se procede a delegar."
        )
    else:
        message = (
            f"La fase solicitada '{requested}' está fuera de orden. "
            f"Fases previas no completadas (orden canónico): "
            f"{', '.join(pending)}. Se registran y reportan antes de delegar."
        )
    return {
        "requested": requested,
        "in_order": not pending,
        "pending_previous": pending,
        "message": message,
    }


def consolidate_phase(state: dict, phase: str, results) -> Dict[str, object]:
    """Consolida una fase y ofrece la transición a la siguiente (Req 1.4).

    Cuando un Subagente_Fase finaliza, el Agente_Orquestador consolida los
    resultados de esa fase *antes* de ofrecer la transición a la fase siguiente.
    Esta función pura y determinista hace esa consolidación sobre una **copia**
    del estado (no muta el ``state`` recibido):

      1. Registra ``results`` bajo ``phase`` en el bloque ``phase_results`` del
         estado consolidado.
      2. Marca ``phase`` en ``completed_phases`` (idempotente) y reordena esa
         lista según la secuencia canónica.
      3. Calcula la transición ofrecida hacia la fase siguiente con
         :func:`default_next` sobre las fases ya completadas (la primera fase no
         completada en orden canónico; ``None`` si todas lo están) y fija
         ``phase`` del estado consolidado a esa fase cuando exista.

    Devuelve un diccionario con:
      - ``state``: el estado consolidado (copia; apto para ``save_state``).
      - ``offered_transition``: la fase siguiente ofrecida (``None`` si se
        completó Covering Tracks / todas las fases).
      - ``successor``: la sucesora canónica estricta de ``phase``
        (:func:`next_phase`), informativa para distinguir la siguiente lineal de
        la siguiente por defecto cuando hubo completados fuera de orden.
      - ``completed_phases``: la lista consolidada de fases completadas.
    """
    _require_known(phase)
    consolidated = copy.deepcopy(state)

    already = set(consolidated.get("completed_phases", []))
    already.add(phase)
    completed = [p for p in CANONICAL_SEQUENCE if p in already]
    consolidated["completed_phases"] = completed

    phase_results = dict(consolidated.get("phase_results", {}))
    phase_results[phase] = results
    consolidated["phase_results"] = phase_results

    offered = default_next(completed)
    if offered is not None:
        consolidated["phase"] = offered

    return {
        "state": consolidated,
        "offered_transition": offered,
        "successor": next_phase(phase),
        "completed_phases": completed,
    }


# --- Lectura/escritura del estado del engagement (Req 1.1, 1.3) --------------

def state_path(engagement_id: str = "dvwa-lab-ulsa", root: Optional[str] = None) -> str:
    """Ruta a ``engagements/<id>/state.json``.

    ``root`` por defecto es la raíz del repositorio (dos niveles por encima de
    este archivo: ``agents/orquestador/`` → raíz).
    """
    if root is None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, "engagements", engagement_id, "state.json")


def load_state(engagement_id: str = "dvwa-lab-ulsa", root: Optional[str] = None) -> dict:
    """Carga el ``state.json`` del engagement (fase actual + completed_phases)."""
    with open(state_path(engagement_id, root), "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_state(state: dict, engagement_id: str = "dvwa-lab-ulsa", root: Optional[str] = None) -> None:
    """Escribe ``state`` en ``state.json`` preservando el resto del documento.

    El Agente_Orquestador modifica únicamente ``phase`` y ``completed_phases``;
    esta función reescribe el documento completo tal cual se le entrega, por lo
    que el llamador debe partir de ``load_state()`` y mutar solo esos campos.
    """
    path = state_path(engagement_id, root)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def completed_phases(state: dict) -> List[str]:
    """Extrae ``completed_phases`` del estado (lista vacía si falta)."""
    return list(state.get("completed_phases", []))


def current_phase(state: dict) -> Optional[str]:
    """Extrae la fase actual (``phase``) del estado."""
    return state.get("phase")
