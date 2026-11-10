"""Incorporación de Powers al inventario por el Líder Técnico — `scripts/integrate_power.py` (tarea 13.1).

Implementa el **flujo de aceptación de un entregable** de la "Convención de
integración de Powers (Líder Técnico)" (design.md), aceptando los **dos formatos**
de empaquetado (`plugin.json` y `POWER.md`) sin reimplementar su parseo ni la
validación del contrato: **reutiliza**

  - ``scripts/power_adapter`` (tarea 1.10) — ``load_power()`` normaliza ambos
    formatos a la vista común ``x-ethack`` y ``validate_power()`` aplica los
    invariantes del modelo con **criterios equivalentes** (Req 8.2, 8.4, 9.2);
  - ``scripts/check_power_docs`` (esta tarea) — ``doc_status()`` calcula el
    ``docStatus`` y señala los Artefactos_Documentacion faltantes (Req 15.6);
  - ``scripts/catalog`` (tarea 1.9) — el **Catalogador** (``build_inventory()``)
    **regenera** ``inventory.json`` desde el árbol ``powers/`` descubriendo ambos
    layouts; es el único componente que escribe el inventario (no se edita a mano).

Flujo (design.md "Convención de integración de Powers", Req 8.2, 8.4, 13.2, 13.4,
15.5, 15.6):

  1. Carga el entregable con el adaptador (detecta `plugin.json` o `POWER.md`).
  2. Valida contra el **modelo de Powers** y la **política ética/laboratorio** con
     ``validate_power``. Criterios equivalentes en ambos formatos: ``x-ethack``
     presente, ``tools`` no vacío, ``ecCouncilPhase`` **xor** ``forensicsStage``
     (con la excepción ya soportada ``governance``/``response`` + ``track``),
     ``allowlistValidation.required == true`` (compuerta ética: toda actividad va
     a la Allowlist_Objetivos, Req 11.1), ``executionMode.allowed == {script-kiddie,
     green-hat, pro}`` con default ``script-kiddie``.
  3. **Si cumple**, registra el Power en ``inventory.json`` **vía el Catalogador**
     (``build_inventory`` regenera el inventario desde el árbol, por lo que un Power
     ya presente **actualiza** su entrada en lugar de duplicarse — el descubrimiento
     visita cada carpeta una sola vez). Devuelve el **registro de integración** con
     formato, fase/etapa, subagente invocador, responsable, ``executionModes``,
     ``docStatus`` y la marca ``baseline``/``extended``/``new``. Si faltan
     Artefactos_Documentacion, la integración **procede** marcada como
     *documentación incompleta* (no bloquea, Req 15.6).
  4. **Si no cumple** el modelo o la política ética, **rechaza** la integración,
     indica el incumplimiento y **no** toca el inventario (Req 8.4).

Función pública:
  - :func:`integrate_power` — ``integrate_power(power_dir, powers_root=None,
    write_inventory=True) -> dict`` con el resultado de la integración.

y un CLI que integra uno o más entregables e informa el resultado.

Requisitos: 8.1, 8.2, 8.4, 9.2, 13.2, 13.4, 15.5, 15.6.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# Reutiliza el adaptador (1.10), el check de docs (13.1) y el Catalogador (1.9).
try:  # permite ejecutar como módulo o como script suelto
    from scripts import power_adapter, catalog
    from scripts.check_power_docs import doc_status
except ImportError:  # pragma: no cover - fallback cuando se corre dentro de scripts/
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import power_adapter  # type: ignore
    import catalog  # type: ignore
    from check_power_docs import doc_status  # type: ignore


def _execution_modes(view: dict) -> list[str]:
    """Extrae ``executionModes`` de la vista común para el registro de integración.

    Toma ``executionMode.allowed`` del contrato ``x-ethack`` normalizado (Req 14.1);
    devuelve ``[]`` si no está declarado, de modo que el registro refleje lo que el
    Power realmente expone.
    """
    em = view.get("executionMode") or {}
    allowed = em.get("allowed") if isinstance(em, dict) else None
    return list(allowed) if isinstance(allowed, (list, tuple)) else []


def _is_within(child: Path, parent: Path) -> bool:
    """¿``child`` está dentro del árbol ``parent``? (comparación por rutas resueltas)."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _origin_and_team(name: str, power_dir: Path, powers_root: Path, view: dict) -> tuple[str, bool, Optional[str]]:
    """Determina ``origin`` (``baseline``/``extended``/``new``), ``baseline`` y ``team``.

    Reutiliza el **mapeo de conocimiento** del Catalogador (``catalog.BASELINE_KNOWLEDGE``)
    y el layout en disco para clasificar el entregable, con la misma semántica que
    ``build_inventory``:

      - Power base conocido en **un nivel** (``powers/<nombre>/``) → ``baseline``.
      - Nombre coincidente con un Power base pero en **dos niveles**
        (``powers/<equipo>/<power>/``) → ``extended`` (extensión de la base).
      - Cualquier otro → ``new``.
    """
    within = _is_within(power_dir, powers_root)
    # level 1 si el padre del Power es directamente powers_root.
    try:
        level = len(power_dir.resolve().relative_to(powers_root.resolve()).parts)
    except ValueError:
        level = 0
    team = None
    if within and level == 2:
        team = power_dir.resolve().parent.name
    team = team or view.get("team") or (catalog.BASELINE_KNOWLEDGE.get(name, {}) or {}).get("team")

    if name in catalog.BASELINE_KNOWLEDGE and level == 1:
        return "baseline", True, team
    if name in catalog.BASELINE_KNOWLEDGE:
        return "extended", False, team
    return "new", False, team


def _registration_record(name: str, power_dir: Path, powers_root: Path, view: dict, docs: dict) -> dict:
    """Arma el registro de integración del Power aceptado (Req 13.2, 13.4, 15.5).

    Contiene lo que la tarea 13.1 pide registrar: formato, fase/etapa, subagente
    invocador, responsable, ``executionModes``, ``docStatus`` y la marca de origen.
    La fase/etapa y el ``invokedBy`` se derivan reutilizando el mapeo del Catalogador
    para los Powers base (que no declaran ejes en su ``POWER.md``) y la vista del
    adaptador para los Powers de alumnos que sí declaran ``x-ethack``.
    """
    origin, is_baseline, team = _origin_and_team(name, power_dir, powers_root, view)
    km = catalog.BASELINE_KNOWLEDGE.get(name, {}) if is_baseline else {}

    if is_baseline:
        ec = km.get("ec_primary")
        fx = km.get("forensics_primary")
        owner = view.get("owner") or catalog._BASELINE_OWNER_FALLBACK
        tools = list(km.get("tools", [])) or list(view.get("tools") or [])
        kind = km.get("kind") or view.get("kind")
        track = km.get("track")
    else:
        ec = view.get("ecCouncilPhase")
        fx = view.get("forensicsStage")
        owner = view.get("owner")
        tools = list(view.get("tools") or [])
        kind = view.get("kind")
        track = view.get("track")

    invoked_by = [v for v in [catalog._ROLE_SUBAGENT.get(team or "")] if v]

    return {
        "name": name,
        "format": view.get("format"),
        "origin": origin,
        "baseline": is_baseline,
        "team": team,
        "owner": owner,
        "kind": kind,
        "track": track,
        "ecCouncilPhase": ec,
        "forensicsStage": fx,
        "tools": tools,
        "invokedBy": invoked_by,
        "executionModes": _execution_modes(view),
        "docStatus": docs,
    }


def integrate_power(power_dir, powers_root=None, write_inventory: bool = True) -> dict:
    """Incorpora (o rechaza) un Power al inventario según el modelo y la política ética.

    Ejecuta el flujo de aceptación del Líder Técnico (ver módulo). Acepta los dos
    formatos vía el adaptador y, si el entregable cumple, lo registra regenerando
    ``inventory.json`` con el Catalogador (reutilización, sin duplicar lógica). La
    documentación incompleta **no** bloquea: la integración procede marcada como tal.

    Args:
        power_dir: Directorio del entregable (``plugin.json`` o ``POWER.md``).
        powers_root: Raíz del árbol ``powers/``. Por defecto ``<repo>/powers``.
        write_inventory: Si ``True`` (por defecto) y el Power está dentro de
            ``powers_root``, regenera ``inventory.json`` con el Catalogador para
            persistir la incorporación. Si ``False``, valida y arma el registro sin
            escribir el inventario (útil para verificación/pruebas en seco).

    Returns:
        ``dict`` con el resultado de la integración:

          - ``accepted`` (bool), ``status`` (``"integrated"`` /
            ``"integrated-docs-incomplete"`` / ``"rejected"``),
          - ``power`` (nombre), ``format``,
          - ``registered`` (bool: si quedó en el inventario),
          - ``documentation_incomplete`` (bool), ``docStatus`` (dict),
          - en aceptación: ``entry`` (registro de integración) y, si se escribió,
            ``inventory_path``;
          - en rechazo: ``problems`` (lista de incumplimientos del modelo/política).
    """
    power_dir = Path(power_dir)
    repo_root = Path(__file__).resolve().parent.parent
    powers_root = Path(powers_root) if powers_root else (
        repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")

    # 1) Cargar con el adaptador (ambos formatos).
    view = power_adapter.load_power(power_dir)
    name = view.get("name") or power_dir.name

    # 2) Validar el modelo + política ética (allowlistValidation.required == true).
    ok, problems = power_adapter.validate_power(view)

    # docStatus se calcula siempre: se reporta tanto si se acepta como si se rechaza.
    docs = doc_status(power_dir)

    # 4) Rechazo: no se añade al inventario (Req 8.4).
    if not ok:
        return {
            "accepted": False,
            "status": "rejected",
            "power": name,
            "format": view.get("format"),
            "registered": False,
            "documentation_incomplete": not docs["complete"],
            "docStatus": docs,
            "problems": problems,
        }

    # 3) Aceptación: armar el registro y registrar vía el Catalogador.
    entry = _registration_record(name, power_dir, powers_root, view, docs)
    incomplete = not docs["complete"]

    result = {
        "accepted": True,
        "status": "integrated-docs-incomplete" if incomplete else "integrated",
        "power": name,
        "format": view.get("format"),
        "registered": False,
        "documentation_incomplete": incomplete,
        "docStatus": docs,
        "entry": entry,
    }

    # Persistencia: solo el Catalogador escribe inventory.json y solo tiene sentido
    # si el Power vive dentro del árbol powers/ (de lo contrario debe colocarse en
    # powers/<equipo>/ primero — design.md paso 3).
    within = _is_within(power_dir, powers_root)
    if write_inventory and within:
        inv = catalog.build_inventory(powers_root, write=True)
        out = repo_root / catalog.INVENTORY_RELPATH
        # Confirma que el Power quedó en el inventario (actualizado, no duplicado).
        registered = any(p.get("name") == name for p in inv.powers)
        result["registered"] = registered
        result["inventory_path"] = str(out)
    elif not within:
        result["note"] = (
            "El entregable cumple el modelo pero está fuera de powers/; colóquelo en "
            "powers/<equipo>/<power>/ para que el Catalogador lo persista en inventory.json."
        )

    return result


def _print_result(res: dict, repo_root: Path) -> None:
    """Imprime el resultado de una integración de forma legible para el CLI."""
    power = res.get("power")
    if not res["accepted"]:
        print(f"[RECHAZADO] {power}  (formato={res.get('format')}) — no cumple el modelo/política ética:")
        for p in res.get("problems", []):
            print(f"    - {p}")
        return
    tag = "INTEGRADO" if res["status"] == "integrated" else "INTEGRADO (docs incompletos)"
    e = res["entry"]
    ciclo = e.get("ecCouncilPhase") or e.get("forensicsStage") or (e.get("track") and f"track:{e['track']}") or "—"
    print(f"[{tag}] {power}  fmt={e.get('format')}  origen={e.get('origin')}  "
          f"ciclo={ciclo}  owner={e.get('owner')}  invokedBy={e.get('invokedBy')}  "
          f"modes={e.get('executionModes')}")
    if res["documentation_incomplete"]:
        print(f"    docs faltantes: {', '.join(res['docStatus']['missing'])} (señalados, no bloquean — Req 15.6)")
    if res.get("registered"):
        print(f"    registrado en {Path(res['inventory_path']).relative_to(repo_root)} (vía Catalogador)")
    elif res.get("note"):
        print(f"    nota: {res['note']}")


def _main(argv: list[str]) -> int:
    """CLI: integra uno o más entregables e informa el resultado.

    Uso:
        python scripts/integrate_power.py <power_dir> [más...] [--powers-root PATH] [--no-write] [--json]

    Devuelve 0 si **todos** los entregables fueron aceptados; 2 si alguno fue
    rechazado por incumplir el modelo o la política ética.
    """
    repo_root = Path(__file__).resolve().parent.parent
    args = [a for a in argv[1:]]
    powers_root = None
    write = True
    as_json = False
    targets: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--powers-root":
            i += 1
            powers_root = args[i] if i < len(args) else None
        elif a == "--no-write":
            write = False
        elif a == "--json":
            as_json = True
        else:
            targets.append(a)
        i += 1

    if not targets:
        print("uso: python scripts/integrate_power.py <power_dir> [más...] "
              "[--powers-root PATH] [--no-write] [--json]")
        return 0

    results = [integrate_power(t, powers_root=powers_root, write_inventory=write) for t in targets]

    if as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for res in results:
            _print_result(res, repo_root)
        accepted = sum(1 for r in results if r["accepted"])
        print(f"\n{accepted}/{len(results)} entregables integrados; "
              f"{len(results) - accepted} rechazados.")

    return 0 if all(r["accepted"] for r in results) else 2


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
