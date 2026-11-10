"""Habilitación de fases por cobertura — `scripts/enable_phases.py` (tarea 13.2).

Cierra el flujo de integración del Líder Técnico (design.md "Convención de
integración de Powers", paso 5): **cuando todos los entregables de una fase/etapa
están integrados (hay ≥1 Power que la cubre en el inventario), el Agente_Orquestador
habilita esa fase**; una fase/etapa con hueco de cobertura queda **deshabilitada**
hasta que exista su Power (Req 8.3, 13.3).

No reimplementa el descubrimiento ni el cálculo de cobertura: **reutiliza** el
Catalogador (`scripts/catalog.py`, tarea 1.9) — ``build_inventory()`` regenera el
inventario desde el árbol ``powers/`` y el objeto :class:`~scripts.catalog.Inventory`
expone ``covered_ec_phases()``, ``covered_forensics_stages()`` y ``coverage_gaps()``.
A partir de esa cobertura deriva dos bloques que escribe en el ``state.json`` del
engagement, **preservando el resto del estado**:

  - ``enabled_phases`` — una entrada por cada una de las **5 fases EC-Council**
    (``enabled`` ⇔ la fase está cubierta por ≥1 Power del inventario).
  - ``enabled_forensics_stages`` — una entrada por cada una de las **6 etapas del
    Flujo_Investigacion** (``enabled`` ⇔ la etapa está cubierta).

Sobre la baseline de los 9 Powers, el resultado esperado es: **Reconnaissance,
Scanning, Gaining Access y Maintaining Access habilitadas**; **Covering Tracks
deshabilitada** (hueco Red Team); **las 6 etapas forenses habilitadas** (cubiertas
por ``dfir-linux``/``network-forensics``); y el hueco **defensivo del Blue Team
marcado como pendiente**.

**Vínculo de gobernanza/forense con el engagement y la Cadena_Custodia** (Req 13.5):
deja el **gancho** para que el estado referencie los artefactos de gobernanza
(``grc/``), de respuesta a incidentes (``incidents/``) y la evidencia forense
(``evidence/``) con su ``record.json`` y su ``chain_of_custody.jsonl``. El bloque
``artifact_links`` del estado indexa esos artefactos relativos al engagement, de
modo que un reporte o artefacto quede vinculado al engagement y a su Cadena_Custodia
(design.md "Registro de evidencia y Cadena_Custodia").

Funciones públicas:
  - :func:`derive_phase_enablement` — ``(inventory) -> dict`` con ``enabled_phases``,
    ``enabled_forensics_stages`` y ``pending_coverage`` derivados de la cobertura.
  - :func:`build_artifact_links` — ``(engagement_dir) -> dict`` con el índice de
    artefactos de ``grc/``/``incidents/``/``evidence/`` y la Cadena_Custodia.
  - :func:`enable_phases` — orquesta todo: regenera el inventario, deriva los bloques
    y los escribe en ``state.json`` preservando el resto.

Requisitos: 8.3, 13.3, 13.5.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Reutiliza el Catalogador (1.9): cobertura y huecos viven en la clase Inventory.
try:  # permite ejecutar como módulo o como script suelto
    from scripts import catalog
except ImportError:  # pragma: no cover - fallback cuando se corre dentro de scripts/
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import catalog  # type: ignore


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Derivación de la habilitación de fases/etapas desde la cobertura.
# ---------------------------------------------------------------------------

def derive_phase_enablement(inventory: "catalog.Inventory") -> dict:
    """Deriva ``enabled_phases`` y ``enabled_forensics_stages`` desde la cobertura.

    Para cada una de las 5 fases EC-Council y de las 6 etapas del Flujo_Investigacion,
    una entrada queda ``enabled: true`` si y solo si algún Power del inventario la
    cubre (≥1 Power que la cubre). Para las deshabilitadas se anota el hueco. Incluye
    además ``pending_coverage`` con los huecos del Catalogador (``coverage_gaps()``),
    donde queda el hueco **defensivo del Blue Team** marcado como pendiente.

    Args:
        inventory: Instancia :class:`~scripts.catalog.Inventory` regenerada.

    Returns:
        ``dict`` con ``enabled_phases``, ``enabled_forensics_stages`` y
        ``pending_coverage`` listos para escribir en ``state.json``.
    """
    covered_ec = inventory.covered_ec_phases()
    covered_fx = inventory.covered_forensics_stages()
    gaps = inventory.coverage_gaps()

    # Índice de qué Powers cubren cada fase/etapa (trazabilidad del "quién habilita").
    ec_by_phase: dict[str, list[str]] = {p: [] for p in catalog.EC_COUNCIL_PHASES}
    fx_by_stage: dict[str, list[str]] = {s: [] for s in catalog.FORENSICS_STAGES}
    for power in inventory.powers:
        name = power.get("name")
        for phase in power.get("covers_ec_phases") or []:
            if phase in ec_by_phase:
                ec_by_phase[phase].append(name)
        for stage in power.get("covers_forensics_stages") or []:
            if stage in fx_by_stage:
                fx_by_stage[stage].append(name)

    gap_names = {(g.get("axis"), g.get("name")): g for g in gaps}

    enabled_phases: dict[str, dict] = {}
    for phase in catalog.EC_COUNCIL_PHASES:
        is_enabled = phase in covered_ec
        entry = {
            "enabled": is_enabled,
            "covered_by": sorted(ec_by_phase[phase]),
        }
        if not is_enabled:
            g = gap_names.get(("ecCouncilPhase", phase))
            entry["gap"] = True
            entry["reason"] = (g or {}).get("reason", f"Sin Power que cubra '{phase}'.")
            entry["pending_team"] = (g or {}).get("team")
        enabled_phases[phase] = entry

    enabled_forensics_stages: dict[str, dict] = {}
    for stage in catalog.FORENSICS_STAGES:
        is_enabled = stage in covered_fx
        entry = {
            "enabled": is_enabled,
            "covered_by": sorted(fx_by_stage[stage]),
        }
        if not is_enabled:
            g = gap_names.get(("forensicsStage", stage))
            entry["gap"] = True
            entry["reason"] = (g or {}).get("reason", f"Sin Power que cubra '{stage}'.")
            entry["pending_team"] = (g or {}).get("team")
        enabled_forensics_stages[stage] = entry

    # Huecos pendientes (incluye el defensivo del Blue Team, axis == "defensive").
    pending = [
        {
            "axis": g.get("axis"),
            "name": g.get("name"),
            "team": g.get("team"),
            "reason": g.get("reason"),
        }
        for g in gaps
    ]

    return {
        "enabled_phases": enabled_phases,
        "enabled_forensics_stages": enabled_forensics_stages,
        "pending_coverage": pending,
    }


# ---------------------------------------------------------------------------
# Vínculo de artefactos de gobernanza/forenses con el engagement (Req 13.5).
# ---------------------------------------------------------------------------

def build_artifact_links(engagement_dir) -> dict:
    """Indexa los artefactos de gobernanza/forenses del engagement y su Cadena_Custodia.

    Deja el **gancho** del Req 13.5: el estado referencia ``grc/``, ``incidents/`` y
    ``evidence/`` (con ``record.json`` y ``chain_of_custody.jsonl`` por pieza de
    evidencia), de modo que todo reporte/artefacto de gobernanza o forense quede
    vinculado al engagement y a su Cadena_Custodia. Las rutas se registran relativas
    al directorio del engagement. No altera ningún artefacto: solo los enumera.

    Args:
        engagement_dir: Directorio del engagement (``engagements/<id>/``).

    Returns:
        ``dict`` con ``grc``, ``incidents`` y ``evidence`` (cada evidencia con sus
        refs a ``record.json`` y a su eslabón de Cadena_Custodia cuando existan).
    """
    engagement_dir = Path(engagement_dir)

    def _rel(p: Path) -> str:
        return str(p.relative_to(engagement_dir))

    # Gobernanza: artefactos GRC ligados al engagement (Req 6.7–6.10, 13.5).
    grc_dir = engagement_dir / "grc"
    grc_files = sorted(_rel(f) for f in grc_dir.glob("*.json")) if grc_dir.is_dir() else []

    # Respuesta a incidentes: un registro por incidente (Req 7.6, 18.2).
    incidents_dir = engagement_dir / "incidents"
    incidents: list[dict] = []
    if incidents_dir.is_dir():
        for inc in sorted(p for p in incidents_dir.iterdir() if p.is_dir()):
            rec = inc / "incident.json"
            incidents.append({
                "id": inc.name,
                "incident": _rel(rec) if rec.is_file() else None,
            })

    # Evidencia forense: cada pieza con su record.json y su Cadena_Custodia (Req 5.3, 5.4).
    evidence_dir = engagement_dir / "evidence"
    evidence: list[dict] = []
    if evidence_dir.is_dir():
        for ev in sorted(p for p in evidence_dir.iterdir() if p.is_dir()):
            record = ev / "record.json"
            coc = ev / "chain_of_custody.jsonl"
            evidence.append({
                "id": ev.name,
                "record": _rel(record) if record.is_file() else None,
                "chain_of_custody": _rel(coc) if coc.is_file() else None,
            })

    return {
        "_comment": (
            "Gancho de vínculo gobernanza/forense ↔ engagement y Cadena_Custodia "
            "(Req 13.5). Rutas relativas al directorio del engagement; el estado "
            "referencia grc/, incidents/ y evidence/ (record.json + chain_of_custody.jsonl)."
        ),
        "grc": grc_files,
        "incidents": incidents,
        "evidence": evidence,
    }


# ---------------------------------------------------------------------------
# Orquestación: regenerar inventario, derivar bloques y escribir state.json.
# ---------------------------------------------------------------------------

def enable_phases(
    powers_root=None,
    state_path=None,
    engagement_dir=None,
    write: bool = True,
    regenerate_inventory: bool = True,
) -> dict:
    """Habilita las fases cubiertas en el ``state.json`` del engagement.

    Regenera el inventario con el Catalogador (salvo ``regenerate_inventory=False``),
    deriva ``enabled_phases``/``enabled_forensics_stages``/``pending_coverage`` desde
    la cobertura y el bloque ``artifact_links`` de gobernanza/forense, y los escribe
    en ``state.json`` **preservando el resto del estado** (merge no destructivo).

    Args:
        powers_root: Raíz de ``powers/``. Por defecto ``<repo>/powers``.
        state_path: Ruta del ``state.json``. Por defecto el del engagement baseline.
        engagement_dir: Directorio del engagement (para ``artifact_links``). Por
            defecto el directorio que contiene ``state_path``.
        write: Si ``True`` (por defecto) escribe ``state.json``.
        regenerate_inventory: Si ``True`` (por defecto) regenera ``inventory.json``
            desde el árbol; si ``False`` lo lee del inventario ya presente.

    Returns:
        ``dict`` con ``state`` (el estado resultante), ``enablement`` (bloques
        derivados), ``artifact_links`` y ``state_path``.
    """
    repo_root = Path(__file__).resolve().parent.parent
    powers_root = Path(powers_root) if powers_root else (
        repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")
    state_path = Path(state_path) if state_path else (
        repo_root / "engagements" / catalog.ENGAGEMENT_ID / "state.json"
    )
    engagement_dir = Path(engagement_dir) if engagement_dir else state_path.parent

    # 1) Cobertura desde el Catalogador (reutilización, no reimplementación).
    inv = catalog.build_inventory(powers_root, write=regenerate_inventory)

    # 2) Derivar la habilitación por cobertura y el índice de artefactos.
    enablement = derive_phase_enablement(inv)
    artifact_links = build_artifact_links(engagement_dir)

    # 3) Merge no destructivo sobre el state.json existente (preserva el resto).
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        state = {"engagement_id": catalog.ENGAGEMENT_ID}

    state["enabled_phases"] = enablement["enabled_phases"]
    state["enabled_forensics_stages"] = enablement["enabled_forensics_stages"]
    state["pending_coverage"] = enablement["pending_coverage"]
    state["artifact_links"] = artifact_links
    state["phase_enablement_meta"] = {
        "_comment": (
            "Derivado de la cobertura del inventario por scripts/enable_phases.py "
            "(tarea 13.2, Req 8.3, 13.3, 13.5). Una fase/etapa se habilita cuando ≥1 "
            "Power del inventario la cubre; los huecos quedan deshabilitados y pendientes."
        ),
        "generated_by": "scripts/enable_phases.py::enable_phases",
        "generated_at_utc": _now_utc(),
        "source_inventory": str(catalog.INVENTORY_RELPATH),
        "enabled_ec_phases": sorted(
            p for p, v in enablement["enabled_phases"].items() if v["enabled"]
        ),
        "enabled_forensics_stages": sorted(
            s for s, v in enablement["enabled_forensics_stages"].items() if v["enabled"]
        ),
    }

    if write:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    return {
        "state": state,
        "enablement": enablement,
        "artifact_links": artifact_links,
        "state_path": str(state_path),
    }


def _main(argv: list[str]) -> int:
    """CLI: regenera el inventario, habilita fases por cobertura y actualiza state.json.

    Uso:
        python scripts/enable_phases.py [powers_root] [--no-write] [--no-regen]
    """
    repo_root = Path(__file__).resolve().parent.parent
    args = argv[1:]
    write = "--no-write" not in args
    regen = "--no-regen" not in args
    positional = [a for a in args if not a.startswith("--")]
    powers_root = Path(positional[0]) if positional else (
        repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")

    res = enable_phases(powers_root=powers_root, write=write, regenerate_inventory=regen)
    ep = res["enablement"]["enabled_phases"]
    ef = res["enablement"]["enabled_forensics_stages"]

    print(f"enable_phases — state.json actualizado en "
          f"{Path(res['state_path']).relative_to(repo_root)}")
    print("  Fases EC-Council:")
    for phase in catalog.EC_COUNCIL_PHASES:
        v = ep[phase]
        mark = "HABILITADA" if v["enabled"] else "deshabilitada (hueco)"
        extra = f"  ← {', '.join(v['covered_by'])}" if v["enabled"] else ""
        print(f"    - {phase}: {mark}{extra}")
    print("  Etapas Flujo_Investigacion:")
    for stage in catalog.FORENSICS_STAGES:
        v = ef[stage]
        mark = "HABILITADA" if v["enabled"] else "deshabilitada (hueco)"
        print(f"    - {stage}: {mark}")
    print("  Pendientes de cobertura:")
    for g in res["enablement"]["pending_coverage"]:
        print(f"    - [{g['axis']}] {g['name']} (team={g.get('team')})")

    links = res["artifact_links"]
    print(f"  Artefactos vinculados: grc={len(links['grc'])} "
          f"incidents={len(links['incidents'])} evidence={len(links['evidence'])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
