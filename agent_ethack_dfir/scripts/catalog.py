"""Catalogador reutilizable del proyecto — `scripts/catalog.py` (tarea 1.9).

El **Catalogador** es el único componente que produce
`engagements/dvwa-lab-ulsa/inventory.json`. **No se edita a mano**: lo regenera
de forma determinista en cada validación (`make validate`/`make catalog`, tarea
15.4) recorriendo el árbol `powers/`. Cumple dos roles con el mismo código
(design.md "Inventario de entregables — `inventory.json`"):

  (a) genera la **línea base** (`baseline`) a partir de los 9 Powers base ya
      presentes en el workspace, y
  (b) **regenera** el inventario completo en cada corrida, representando por igual
      los Powers base y los Powers nuevos/extendidos de los alumnos.

Descubre **ambos layouts** reutilizando `power_adapter.load_power()` para leer cada
Power (NO reimplementa el parseo de formatos — tarea 1.10):

  - **Powers base**: `powers/<nombre>/` (un nivel) — forman la `baseline`.
  - **Powers de alumnos**: `powers/<equipo>/<power>/` (dos niveles) — Req 20.4.

Detecta como Power toda carpeta con `plugin.json` **o** `POWER.md`; excluye la
plantilla `powers/_template/` y las carpetas de equipo vacías.

**Realidad del disco (verificada):** los 9 Powers base están TODOS en formato
`POWER.md` y **ninguno declara el bloque `x-ethack`**. Por eso el Catalogador
mantiene un **mapeo de conocimiento** (`BASELINE_KNOWLEDGE`) que asigna a cada
Power base su fase EC-Council / etapa del Flujo_Investigacion, rol/equipo, owner y
herramientas reales, marcando `xethack_declared: false` y dejando en `null` lo que
el propio `POWER.md` no declara (`declared_ecCouncilPhase` / `declared_forensicsStage`).
Los Powers de alumnos que **sí** declaran `x-ethack` (vía `plugin.json` o
frontmatter de `POWER.md`) se catalogan directamente desde la vista del adaptador.

Métodos del objeto de inventario (design.md "Cobertura y conteo como métodos del
inventario"): la Validacion_Local (15.4) **invoca** estos métodos, no los
reimplementa:

  - :meth:`Inventory.coverage_gaps` — huecos de las 5 fases EC-Council ∪ 6 etapas
    del Flujo_Investigacion no cubiertos por la baseline (más el hueco defensivo del
    Blue Team), anotados con ``gap: true`` (Req 13.3).
  - :meth:`Inventory.count_tooled_by_owner` — Powers con Herramienta_Real por
    `owner`, para el mínimo de ≥2 por alumno (Req 9.6).

Requisitos: 9.4, 9.6, 13.1, 13.2, 13.4.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Reutiliza el adaptador de la tarea 1.10 para leer cada Power (no reimplementa parseo).
try:  # permite ejecutar como módulo o como script suelto
    from scripts import power_adapter
except ImportError:  # pragma: no cover - fallback cuando se corre dentro de scripts/
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import power_adapter  # type: ignore

# ---------------------------------------------------------------------------
# Ejes canónicos del ciclo (design.md Overview).
# ---------------------------------------------------------------------------

# Las 5 fases EC-Council en su orden canónico (Reconnaissance → … → Covering Tracks).
EC_COUNCIL_PHASES = (
    "Reconnaissance",
    "Scanning",
    "Gaining Access",
    "Maintaining Access",
    "Covering Tracks",
)

# Las 6 etapas del Flujo_Investigacion forense (Detect → … → Report).
FORENSICS_STAGES = (
    "Detect",
    "Isolate",
    "Collect",
    "Preserve",
    "Analyze",
    "Report",
)

ENGAGEMENT_ID = "dvwa-lab-ulsa"
INVENTORY_RELPATH = Path("engagements") / ENGAGEMENT_ID / "inventory.json"

# ---------------------------------------------------------------------------
# Mapeo de conocimiento de la baseline (tarea 1.9).
#
# Los 9 POWER.md base NO declaran x-ethack; esta tabla les asigna su ubicación en
# el ciclo, rol/equipo y herramientas reales. `covers_ec`/`covers_forensics` son los
# conjuntos de fases/etapas que cada Power cubre para el cálculo de cobertura
# (un Power puede cubrir más de una, p. ej. footprinting cubre Recon + Scanning;
# los dos Powers forenses base cubren, en conjunto, las 6 etapas del flujo — tarea
# 8.1: la base DF es el cimiento de las 6 etapas, los alumnos la extienden).
# `ec_primary`/`forensics_primary` es la ubicación primaria que se refleja como
# ecCouncilPhase/forensicsStage en el inventario. `track` ubica los Powers que no
# caen en ninguno de los dos ejes (GRC / Incident Response).
# ---------------------------------------------------------------------------

BASELINE_KNOWLEDGE: dict[str, dict] = {
    "osint-passive-recon": {
        "team": "red-team", "role": "Red Team", "kind": "offensive",
        "ec_primary": "Reconnaissance",
        "covers_ec": ["Reconnaissance"],
        "tools": ["RDAP", "WHOIS", "DNS", "crt.sh", "Wayback Machine", "ExifTool", "GitHub dorks"],
    },
    "footprinting-enumeration": {
        "team": "red-team", "role": "Red Team", "kind": "offensive",
        "ec_primary": "Scanning",
        "covers_ec": ["Reconnaissance", "Scanning"],
        "tools": ["nmap"],
    },
    "vulnerability-assessment": {
        "team": "red-team", "role": "Red Team", "kind": "offensive",
        "ec_primary": "Gaining Access",
        "covers_ec": ["Scanning", "Gaining Access"],
        "tools": ["Nessus", "OpenVAS", "CVSS"],
    },
    "exploitation-metasploit": {
        "team": "red-team", "role": "Red Team", "kind": "offensive",
        "ec_primary": "Gaining Access",
        "covers_ec": ["Gaining Access", "Maintaining Access"],
        "tools": ["Metasploit", "msfvenom", "Meterpreter"],
    },
    "dfir-linux": {
        "team": "digital-forensics", "role": "Digital Forensics", "kind": "forensics",
        "forensics_primary": "Analyze",
        # Cimiento host del Flujo_Investigacion completo (tarea 8.1).
        "covers_forensics": ["Detect", "Isolate", "Collect", "Preserve", "Analyze", "Report"],
        "tools": ["dd", "dc3dd", "LiME", "Volatility 3", "Autopsy", "auditd"],
    },
    "network-forensics": {
        "team": "digital-forensics", "role": "Digital Forensics", "kind": "forensics",
        "forensics_primary": "Collect",
        "covers_forensics": ["Detect", "Collect", "Analyze", "Report"],
        "tools": ["Wireshark", "tcpdump", "Snort", "Suricata", "Zeek"],
    },
    "grc-nist-csf": {
        "team": "grc", "role": "GRC", "kind": "governance", "track": "GRC",
        "tools": ["NIST CSF 2.0", "risk-register", "gap-analysis", "POA&M"],
    },
    "incident-handling-nist": {
        "team": "incident-responder", "role": "Incident Responder", "kind": "response",
        "track": "IR",
        "tools": ["NIST SP 800-61", "MITRE ATT&CK", "Cyber Kill Chain", "playbooks"],
    },
    "incident-response-lab": {
        "team": "incident-responder", "role": "Incident Responder", "kind": "response",
        "track": "IR",
        "tools": ["TheHive", "VirusTotal", "Wazuh", "Sysmon"],
    },
}

# Owner por defecto de la baseline cuando el POWER.md no trae autor.
_BASELINE_OWNER_FALLBACK = "docente-baseline"

# Subagentes que invocan cada Power, derivados de su fase/etapa/track (Req 9.3).
_ROLE_SUBAGENT = {
    "red-team": "subagente-red-team",
    "blue-team": "subagente-blue-team",
    "digital-forensics": "subagente-digital-forensics",
    "grc": "subagente-grc",
    "incident-responder": "subagente-incident-responder",
}


# ---------------------------------------------------------------------------
# Descubrimiento de ambos layouts.
# ---------------------------------------------------------------------------

def _is_power_dir(path: Path) -> bool:
    """¿La carpeta contiene un marcador de Power (`plugin.json` o `POWER.md`)?"""
    return (path / "plugin.json").is_file() or (path / "POWER.md").is_file()


def discover_powers(powers_root) -> list[dict]:
    """Descubre los Powers en **ambos layouts** bajo ``powers_root``.

    Recorre ``powers/<nombre>/`` (un nivel, Powers base) y ``powers/<equipo>/<power>/``
    (dos niveles, Powers de alumnos), detectando toda carpeta que contenga
    ``plugin.json`` o ``POWER.md``. Excluye ``powers/_template/`` y las carpetas de
    equipo vacías (sin ningún Power dentro). No desciende dentro de un Power ya
    detectado (evita anidar un Power dentro de otro).

    Args:
        powers_root: Ruta de la carpeta ``powers/``.

    Returns:
        Lista de dicts ``{"dir", "name", "level", "team"}`` ordenada por ruta.
        ``level`` es 1 (base) o 2 (alumno); ``team`` es el nombre de la carpeta de
        equipo para el nivel 2, o ``None`` para el nivel 1.
    """
    powers_root = Path(powers_root)
    found: list[dict] = []
    if not powers_root.is_dir():
        return found

    for entry in sorted(powers_root.iterdir(), key=lambda p: p.name):
        if not entry.is_dir() or entry.name == "_template":
            continue

        if _is_power_dir(entry):
            # Nivel 1: Power base en powers/<nombre>/.
            found.append({"dir": entry, "name": entry.name, "level": 1, "team": None})
            continue

        # Carpeta de equipo (nivel 2): buscar Powers un nivel más abajo.
        for sub in sorted(entry.iterdir(), key=lambda p: p.name):
            if sub.is_dir() and sub.name != "_template" and _is_power_dir(sub):
                found.append({"dir": sub, "name": sub.name, "level": 2, "team": entry.name})

    return found


# ---------------------------------------------------------------------------
# Construcción de una entrada de Power del inventario.
# ---------------------------------------------------------------------------

def _doc_status(power_dir: Path, view: dict) -> dict:
    """Calcula el estado de los Artefactos_Documentacion bajo ``docs/`` (Req 15.5)."""
    doc_cfg = view.get("documentation") or {}
    root_rel = doc_cfg.get("root") if isinstance(doc_cfg, dict) else None
    docs_dir = Path(root_rel) if root_rel else (power_dir / "docs")
    if not docs_dir.is_absolute():
        # root suele venir relativo a la raíz del repo; probar ambas.
        candidate = power_dir / "docs"
        docs_dir = candidate if candidate.exists() else docs_dir
    has_prompt = (docs_dir / "prompt.md").is_file()
    has_sessions = (docs_dir / "sessions").is_dir()
    has_feedback = (docs_dir / "feedback.md").is_file()
    missing = [
        n for n, ok in (("prompt.md", has_prompt), ("sessions/", has_sessions), ("feedback.md", has_feedback))
        if not ok
    ]
    return {
        "root": str(docs_dir),
        "prompt": has_prompt,
        "sessions": has_sessions,
        "feedback": has_feedback,
        "complete": not missing,
        "missing": missing,
    }


def _baseline_entry(name: str, power_dir: Path, view: dict) -> dict:
    """Construye la entrada de un Power base usando el mapeo de conocimiento.

    El ``POWER.md`` base no declara ``x-ethack``, así que la fase/etapa, el rol/equipo
    y las herramientas provienen de :data:`BASELINE_KNOWLEDGE`. Se registra en
    ``null`` lo que el propio Power declara (``declared_*``) y se marca
    ``xethack_declared: false`` (tarea 1.9).
    """
    km = BASELINE_KNOWLEDGE.get(name, {})
    owner = view.get("owner") or _BASELINE_OWNER_FALLBACK
    team = km.get("team")
    ec_primary = km.get("ec_primary")
    fx_primary = km.get("forensics_primary")
    return {
        "name": name,
        "format": view.get("format"),
        "origin": "baseline",
        "baseline": True,
        "xethack_declared": bool(view.get("declared")),  # False para los 9 base
        "team": team,
        "role": km.get("role"),
        "owner": owner,
        "kind": km.get("kind") or view.get("kind"),
        "track": km.get("track"),
        # Ubicación en el ciclo: la declarada por el Power (null) y la efectiva (mapeo).
        "declared_ecCouncilPhase": view.get("ecCouncilPhase"),
        "declared_forensicsStage": view.get("forensicsStage"),
        "ecCouncilPhase": ec_primary,
        "forensicsStage": fx_primary,
        "phase_source": "knowledge-map",
        "covers_ec_phases": list(km.get("covers_ec", [p for p in [ec_primary] if p])),
        "covers_forensics_stages": list(km.get("covers_forensics", [s for s in [fx_primary] if s])),
        "tools": list(km.get("tools", [])),
        "tooled": bool(km.get("tools")),
        "invokedBy": [v for v in [_ROLE_SUBAGENT.get(team)] if v],
        "docStatus": _doc_status(power_dir, view),
        "notes": (
            "POWER.md base sin x-ethack; fase/etapa/rol/tools asignados por el mapeo "
            "de conocimiento del Catalogador (xethack_declared=false)."
        ),
    }


def _student_entry(name: str, team: Optional[str], power_dir: Path, view: dict) -> dict:
    """Construye la entrada de un Power de alumno a partir de la vista del adaptador.

    Si el Power declara ``x-ethack`` (``plugin.json`` o frontmatter de ``POWER.md``),
    sus campos se toman tal cual de la vista común. El origen es ``extended`` cuando
    el nombre coincide con un Power base (extensión de la base) o ``new`` en otro caso.
    """
    origin = "extended" if name in BASELINE_KNOWLEDGE else "new"
    ec = view.get("ecCouncilPhase")
    fx = view.get("forensicsStage")
    tools = view.get("tools") or []
    return {
        "name": name,
        "format": view.get("format"),
        "origin": origin,
        "baseline": False,
        "xethack_declared": bool(view.get("declared")),
        "team": team or view.get("team"),
        "role": None,
        "owner": view.get("owner"),
        "kind": view.get("kind"),
        "track": None,
        "declared_ecCouncilPhase": ec,
        "declared_forensicsStage": fx,
        "ecCouncilPhase": ec,
        "forensicsStage": fx,
        "phase_source": "x-ethack" if view.get("declared") else "undeclared",
        "covers_ec_phases": [ec] if ec else [],
        "covers_forensics_stages": [fx] if fx else [],
        "tools": list(tools),
        "tooled": bool(tools),
        "invokedBy": [v for v in [_ROLE_SUBAGENT.get(team or "")] if v],
        "docStatus": _doc_status(power_dir, view),
        "notes": None,
    }


# ---------------------------------------------------------------------------
# Objeto de inventario con los métodos de cobertura y conteo.
# ---------------------------------------------------------------------------

class Inventory:
    """Inventario de entregables con cobertura y conteo como métodos (design.md).

    Encapsula la lista de Powers catalogados y expone :meth:`coverage_gaps` y
    :meth:`count_tooled_by_owner`, que la Validacion_Local (15.4) **invoca** en
    lugar de reimplementar.
    """

    def __init__(self, engagement_id: str, powers: list[dict], agents: Optional[list[dict]] = None):
        self.engagement_id = engagement_id
        self.powers = powers
        self.agents = agents or []

    # -- cobertura ---------------------------------------------------------

    def covered_ec_phases(self) -> set[str]:
        """Fases EC-Council cubiertas por al menos un Power del inventario."""
        covered: set[str] = set()
        for p in self.powers:
            covered.update(p.get("covers_ec_phases") or [])
        return covered

    def covered_forensics_stages(self) -> set[str]:
        """Etapas del Flujo_Investigacion cubiertas por al menos un Power."""
        covered: set[str] = set()
        for p in self.powers:
            covered.update(p.get("covers_forensics_stages") or [])
        return covered

    def coverage_gaps(self) -> list[dict]:
        """Devuelve los huecos de cobertura, cada uno anotado con ``gap: true`` (Req 13.3).

        Un hueco es una fase EC-Council o etapa del Flujo_Investigacion que **ningún**
        Power del inventario cubre, más el hueco **defensivo del Blue Team** (detección
        /hardening), que no corresponde a ninguno de los dos ejes pero es un entregable
        que la baseline no satisface. Sobre la baseline de los 9 Powers, los huecos
        esperados son **Covering Tracks** (Red Team) y **Blue Team detección/hardening**.
        """
        gaps: list[dict] = []

        covered_ec = self.covered_ec_phases()
        for phase in EC_COUNCIL_PHASES:
            if phase not in covered_ec:
                gaps.append({
                    "axis": "ecCouncilPhase",
                    "name": phase,
                    "gap": True,
                    "team": "red-team" if phase == "Covering Tracks" else None,
                    "reason": f"Ninguna base cubre la fase EC-Council '{phase}'.",
                })

        covered_fx = self.covered_forensics_stages()
        for stage in FORENSICS_STAGES:
            if stage not in covered_fx:
                gaps.append({
                    "axis": "forensicsStage",
                    "name": stage,
                    "gap": True,
                    "team": "digital-forensics",
                    "reason": f"Ninguna base cubre la etapa del Flujo_Investigacion '{stage}'.",
                })

        # Hueco defensivo del Blue Team: no existe Power base de detección/hardening.
        has_defensive = any(
            (p.get("kind") == "defensive") or (p.get("team") == "blue-team")
            for p in self.powers
        )
        if not has_defensive:
            gaps.append({
                "axis": "defensive",
                "name": "Blue Team detección/hardening",
                "gap": True,
                "team": "blue-team",
                "reason": "No hay Power base de detección/hardening del Blue Team; se crea desde cero.",
            })

        return gaps

    # -- conteo ------------------------------------------------------------

    def count_tooled_by_owner(self) -> dict[str, int]:
        """Cuenta los Powers con Herramienta_Real por ``owner`` (Req 9.6).

        Base del mínimo de ≥2 Powers con Herramienta_Real por alumno. Solo cuenta
        Powers con ``tooled == True`` (``tools`` no vacío).
        """
        counts: dict[str, int] = {}
        for p in self.powers:
            if not p.get("tooled"):
                continue
            owner = p.get("owner") or "<sin-owner>"
            counts[owner] = counts.get(owner, 0) + 1
        return counts

    def owners_below_minimum(self, minimum: int = 2) -> dict[str, int]:
        """Owners que no alcanzan el mínimo de Powers con Herramienta_Real (Req 9.6)."""
        return {o: n for o, n in self.count_tooled_by_owner().items() if n < minimum}

    # -- serialización -----------------------------------------------------

    def to_dict(self, generated_at_utc: Optional[str] = None) -> dict:
        """Serializa el inventario al esquema de ``inventory.json`` (design.md)."""
        return {
            "_comment": (
                "NO EDITAR A MANO. Generado por el Catalogador (scripts/catalog.py::build_inventory) "
                "en cada validación via 'make validate'/'make catalog' a partir del árbol powers/ "
                "(Req 9.4, 13.1, 13.2, 13.4). coverage_gaps y tooled_by_owner son instantáneas de los "
                "métodos del inventario; la lógica vive en la clase Inventory."
            ),
            "engagement_id": self.engagement_id,
            "generated_by": "scripts/catalog.py::build_inventory",
            "generated_at_utc": generated_at_utc,
            "axes": {
                "ecCouncilPhases": list(EC_COUNCIL_PHASES),
                "forensicsStages": list(FORENSICS_STAGES),
            },
            "summary": {
                "total_powers": len(self.powers),
                "baseline_powers": sum(1 for p in self.powers if p.get("baseline")),
                "tooled_powers": sum(1 for p in self.powers if p.get("tooled")),
                "covered_ec_phases": sorted(self.covered_ec_phases()),
                "covered_forensics_stages": sorted(self.covered_forensics_stages()),
            },
            "powers": self.powers,
            "agents": self.agents,
            "coverage_gaps": self.coverage_gaps(),
            "tooled_by_owner": self.count_tooled_by_owner(),
        }


# ---------------------------------------------------------------------------
# build_inventory — construye, escribe y devuelve el inventario.
# ---------------------------------------------------------------------------

def build_inventory(powers_root, assets=None, write: bool = True, output_path=None) -> Inventory:
    """Construye el inventario desde ``powers_root``, lo escribe y lo devuelve.

    Descubre ambos layouts con :func:`discover_powers`, lee cada Power con
    ``power_adapter.load_power()`` (no reimplementa el parseo — tarea 1.10) y arma
    una entrada por Power: los 9 base se resuelven con :data:`BASELINE_KNOWLEDGE`
    (``baseline: true``, ``xethack_declared: false``); los de alumnos se toman de la
    vista del adaptador (``extended``/``new``). Escribe el resultado determinista en
    ``engagements/dvwa-lab-ulsa/inventory.json`` (salvo ``write=False``).

    Args:
        powers_root: Ruta de la carpeta ``powers/``.
        assets: Reservado para enriquecer el inventario con los Contenedores_Objetivo
            del ``scope.yaml`` (no requerido por la baseline; se acepta por firma del
            diseño ``build_inventory(powers_root, assets)``).
        write: Si ``True`` (por defecto) escribe ``inventory.json``.
        output_path: Ruta de salida explícita; por defecto
            ``<repo>/engagements/dvwa-lab-ulsa/inventory.json``.

    Returns:
        La instancia :class:`Inventory` resultante.
    """
    powers_root = Path(powers_root)
    repo_root = powers_root.parent

    entries: list[dict] = []
    for found in discover_powers(powers_root):
        power_dir = found["dir"]
        name = found["name"]
        view = power_adapter.load_power(power_dir)
        if found["level"] == 1 and name in BASELINE_KNOWLEDGE:
            entries.append(_baseline_entry(name, power_dir, view))
        elif found["level"] == 1 and not view.get("declared"):
            # Power base desconocido (no mapeado) y sin x-ethack: catalogar como new/undeclared.
            entries.append(_student_entry(name, None, power_dir, view))
        else:
            entries.append(_student_entry(name, found["team"], power_dir, view))

    # Orden determinista: baseline primero, luego por nombre.
    entries.sort(key=lambda e: (not e.get("baseline"), e.get("name") or ""))

    inv = Inventory(ENGAGEMENT_ID, entries)

    if write:
        out = Path(output_path) if output_path else (repo_root / INVENTORY_RELPATH)
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = inv.to_dict(generated_at_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return inv


def _main(argv: list[str]) -> int:
    """CLI del Catalogador: regenera ``inventory.json`` y reporta cobertura/conteo.

    Uso:
        python scripts/catalog.py [powers_root]

    Sin argumentos usa ``powers/`` relativo a la raíz del repo. Imprime cuántos
    Powers se catalogaron, la cobertura por eje, los huecos detectados y el conteo
    de Powers con Herramienta_Real por owner.
    """
    repo_root = Path(__file__).resolve().parent.parent
    powers_root = Path(argv[1]) if len(argv) > 1 else (
        repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")

    inv = build_inventory(powers_root)
    out = repo_root / INVENTORY_RELPATH

    print(f"Catalogador — inventario regenerado en {out.relative_to(repo_root)}")
    print(f"  Powers catalogados: {len(inv.powers)} "
          f"(baseline={sum(1 for p in inv.powers if p.get('baseline'))}, "
          f"con herramienta real={sum(1 for p in inv.powers if p.get('tooled'))})")
    print(f"  Fases EC-Council cubiertas: {sorted(inv.covered_ec_phases())}")
    print(f"  Etapas Flujo_Investigacion cubiertas: {sorted(inv.covered_forensics_stages())}")

    gaps = inv.coverage_gaps()
    print(f"  Huecos de cobertura ({len(gaps)}):")
    for g in gaps:
        print(f"    - [{g['axis']}] {g['name']}  (gap=true)")

    print("  Powers con Herramienta_Real por owner:")
    for owner, n in sorted(inv.count_tooled_by_owner().items()):
        print(f"    - {owner}: {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
