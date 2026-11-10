"""Check de cobertura de fases y etapas forenses — `scripts/check_coverage.py` (tarea 13.3).

Este check **verifica** —no calcula— la cobertura del inventario de entregables.
Toda la lógica de descubrimiento de Powers y de cálculo de cobertura vive en el
**Catalogador** (`scripts/catalog.py`, tarea 1.9); este módulo se limita a
**consumir** sus resultados:

  - :func:`catalog.build_inventory` regenera ``inventory.json`` recorriendo el árbol
    ``powers/`` (ambos layouts) y devuelve un :class:`catalog.Inventory`.
  - :meth:`catalog.Inventory.coverage_gaps` entrega los huecos ya anotados con
    ``gap: true`` (fases EC-Council / etapas del Flujo_Investigacion no cubiertas por
    **ningún** Power, más el hueco defensivo del Blue Team).

Qué confirma el check (Req 8.3, 13.2, 13.4):

  1. **Cobertura de las 5 fases EC-Council** (Reconnaissance → … → Covering Tracks):
     ≥1 Power por fase, contando por igual Powers ``baseline``/``extended``/``new``
     (la cuenta la hace ``coverage_gaps()`` sobre ``covers_ec_phases`` de cada Power,
     sin importar su origen).
  2. **Cobertura de las 6 etapas del Flujo_Investigacion** (Detect → … → Report):
     ≥1 Power por etapa, con el mismo criterio de conteo.
  3. **Responsable declarado**: todo Power del inventario declara ``owner`` **o**
     ``team``; se reportan los que no (Req 13.4).

Huecos esperados de la línea base vs. error fatal
-------------------------------------------------
El docente deja **deliberadamente** dos huecos en la baseline, que el proyecto
cubre con Powers nuevos de alumnos (tasks 6.2 y 7.2):

  - **Covering Tracks** (fase EC-Council, Red Team).
  - **Blue Team detección/hardening** (hueco defensivo).

Estos dos se reportan como **pendientes esperados**, no como fallo fatal: con la
baseline actual el check termina en ``exit 0``. Cualquier **otro** hueco (una fase
o etapa que debería estar cubierta por la base y no lo está) **sí** es fatal, al
igual que cualquier Power **sin responsable**. El flag ``--strict`` endurece el
criterio y hace fatal también los huecos esperados (útil cuando ya se espera
cobertura total tras integrar los Powers de alumnos).

Uso::

    python scripts/check_coverage.py [powers_root] [--strict]

Exit code: ``0`` si no hay huecos inesperados ni Powers sin responsable (los huecos
esperados de baseline no cuentan como error salvo ``--strict``); distinto de ``0``
en caso contrario.

Requisitos: 8.3, 13.2, 13.4.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reutiliza el Catalogador (tarea 1.9): NO reimplementa descubrimiento ni cobertura.
try:  # permite ejecutar como módulo o como script suelto
    from scripts import catalog
except ImportError:  # pragma: no cover - fallback cuando se corre dentro de scripts/
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import catalog  # type: ignore


# Huecos conocidos de la línea base que el docente deja a propósito para los alumnos
# (tasks 6.2 y 7.2). Se identifican por (axis, name) tal como los emite
# Inventory.coverage_gaps(). No son error fatal: se reportan como pendientes
# esperados.
EXPECTED_BASELINE_GAPS: frozenset[tuple[str, str]] = frozenset({
    ("ecCouncilPhase", "Covering Tracks"),
    ("defensive", "Blue Team detección/hardening"),
})


def _gap_key(gap: dict) -> tuple[str, str]:
    """Clave (axis, name) de un hueco para compararlo con los esperados."""
    return (gap.get("axis") or "", gap.get("name") or "")


def _has_responsible(power: dict) -> bool:
    """¿El Power declara responsable? Vale ``owner`` o ``team`` no vacío (Req 13.4)."""
    return bool((power.get("owner") or "").strip() or (power.get("team") or "").strip())


def check_coverage(powers_root, strict: bool = False) -> dict:
    """Verifica la cobertura consumiendo el Catalogador y devuelve un reporte.

    Regenera el inventario con :func:`catalog.build_inventory`, obtiene los huecos
    con :meth:`catalog.Inventory.coverage_gaps` y los clasifica en **esperados**
    (los de :data:`EXPECTED_BASELINE_GAPS`) e **inesperados**. Además recorre los
    Powers para reportar los que no declaran responsable.

    Args:
        powers_root: Ruta de la carpeta ``powers/``.
        strict: Si ``True``, los huecos esperados de baseline también cuentan como
            fallo (``ok == False``).

    Returns:
        ``dict`` con el detalle: inventario, huecos esperados/inesperados, Powers sin
        responsable, cobertura por eje y el veredicto ``ok``.
    """
    inv = catalog.build_inventory(powers_root)
    gaps = inv.coverage_gaps()

    expected_gaps = [g for g in gaps if _gap_key(g) in EXPECTED_BASELINE_GAPS]
    unexpected_gaps = [g for g in gaps if _gap_key(g) not in EXPECTED_BASELINE_GAPS]

    powers_without_owner = [p for p in inv.powers if not _has_responsible(p)]

    # Veredicto: fatal por huecos inesperados o Powers sin responsable; en --strict,
    # también por los huecos esperados.
    ok = not unexpected_gaps and not powers_without_owner
    if strict and expected_gaps:
        ok = False

    return {
        "inventory": inv,
        "gaps": gaps,
        "expected_gaps": expected_gaps,
        "unexpected_gaps": unexpected_gaps,
        "powers_without_owner": powers_without_owner,
        "covered_ec_phases": sorted(inv.covered_ec_phases()),
        "covered_forensics_stages": sorted(inv.covered_forensics_stages()),
        "strict": strict,
        "ok": ok,
    }


def _print_report(report: dict) -> None:
    """Imprime el reporte del check de forma legible (fases, etapas, huecos, owners)."""
    inv = report["inventory"]

    print("Check de cobertura (tarea 13.3) — consume coverage_gaps() del Catalogador")
    print(f"  Powers en inventario: {len(inv.powers)} "
          f"(baseline={sum(1 for p in inv.powers if p.get('baseline'))}, "
          f"extended={sum(1 for p in inv.powers if p.get('origin') == 'extended')}, "
          f"new={sum(1 for p in inv.powers if p.get('origin') == 'new')})")

    # Cobertura por eje (≥1 Power por fase/etapa).
    print("\n  Fases EC-Council (5):")
    for phase in catalog.EC_COUNCIL_PHASES:
        covered = phase in report["covered_ec_phases"]
        print(f"    [{'✔' if covered else '✗'}] {phase}")
    print("  Etapas Flujo_Investigacion (6):")
    for stage in catalog.FORENSICS_STAGES:
        covered = stage in report["covered_forensics_stages"]
        print(f"    [{'✔' if covered else '✗'}] {stage}")

    # Huecos esperados de baseline (pendientes, no fatales salvo --strict).
    exp = report["expected_gaps"]
    print(f"\n  Huecos esperados de baseline ({len(exp)}) — pendientes para Powers nuevos de alumnos:")
    for g in exp:
        team = f" [{g['team']}]" if g.get("team") else ""
        print(f"    - PENDIENTE{team} [{g['axis']}] {g['name']}  (gap=true) — {g.get('reason', '')}")
    if not exp:
        print("    (ninguno)")

    # Huecos inesperados (fatales).
    unexp = report["unexpected_gaps"]
    if unexp:
        print(f"\n  ✗ Huecos INESPERADOS ({len(unexp)}) — FALLO:")
        for g in unexp:
            print(f"    - [{g['axis']}] {g['name']}  (gap=true) — {g.get('reason', '')}")

    # Powers sin responsable (fatales).
    noown = report["powers_without_owner"]
    if noown:
        print(f"\n  ✗ Powers SIN responsable ({len(noown)}) — FALLO (Req 13.4):")
        for p in noown:
            print(f"    - {p.get('name')} (origin={p.get('origin')})")
    else:
        print("\n  ✔ Todos los Powers declaran responsable (owner/team).")

    # Veredicto.
    print()
    if report["ok"]:
        if exp:
            print("RESULTADO: OK — sin huecos inesperados ni Powers sin responsable. "
                  f"Quedan {len(exp)} hueco(s) esperado(s) de baseline como pendientes (exit 0).")
        else:
            print("RESULTADO: OK — cobertura completa, sin huecos ni Powers sin responsable (exit 0).")
    else:
        motivos = []
        if unexp:
            motivos.append(f"{len(unexp)} hueco(s) inesperado(s)")
        if noown:
            motivos.append(f"{len(noown)} Power(s) sin responsable")
        if report["strict"] and exp:
            motivos.append(f"{len(exp)} hueco(s) esperado(s) bajo --strict")
        print(f"RESULTADO: FALLO — {'; '.join(motivos)} (exit != 0).")


def _main(argv: list[str]) -> int:
    """CLI del check de cobertura (tarea 13.3).

    Uso:
        python scripts/check_coverage.py [powers_root] [--strict]

    Sin ``powers_root`` usa ``powers/`` relativo a la raíz del repo. Devuelve 0 si no
    hay huecos inesperados ni Powers sin responsable (los huecos esperados de baseline
    no son fatales salvo ``--strict``); distinto de 0 en caso contrario.
    """
    repo_root = Path(__file__).resolve().parent.parent
    strict = "--strict" in argv[1:]
    positional = [a for a in argv[1:] if not a.startswith("--")]
    powers_root = Path(positional[0]) if positional else (
        repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")

    report = check_coverage(powers_root, strict=strict)
    _print_report(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
