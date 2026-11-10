"""Punto de entrada único de la Validacion_Local — `scripts/validate_all.py` (tarea 15.4).

La **Validacion_Local** es la única compuerta automatizada del proyecto y corre
**enteramente en local**: no depende de GitHub Actions ni de ningún servicio de
integración continua remoto (Req 20.6, 20.11). El alumno la ejecuta antes de abrir
su Pull_Request y el Líder Técnico la ejecuta antes de integrar (Req 20.8, 20.9).

Este agregador **no reimplementa** ninguna comprobación: **encadena** en un solo
comando los componentes ya existentes de `scripts/` y **reutiliza** el Catalogador
y los métodos del inventario (design.md "Validacion_Local: única compuerta
automatizada"):

  1. **Adaptador de formatos** (`power_adapter`, tarea 1.10): carga y valida cada
     Power en **ambos formatos** (`plugin.json` y `POWER.md`) con criterios
     equivalentes. Los 9 Powers base en `POWER.md` **no declaran `x-ethack`**: son
     *no declarados esperados* y no rompen la validación; un Power que **sí** declara
     el contrato pero resulta inválido, o un Power de alumno sin contrato, es un
     problema **inesperado** (fatal).
  2. **Artefactos_Documentacion** (`check_power_docs.doc_status`, tarea 13.1): calcula
     el `docStatus` de cada Power. La documentación incompleta se **señala**, no
     bloquea (Req 15.6).
  3. **Guardia de la Allowlist_Objetivos** (`validate_target`, tarea 1.3): *self-check*
     de que la guardia importa y funciona — un objetivo dentro de alcance se admite y
     uno fuera se rechaza (Req 11.1, 11.2).
  4. **Catalogador** (`catalog.build_inventory`, tarea 1.9): **regenera**
     `inventory.json` (nunca se edita a mano) y se usan sus métodos
     `coverage_gaps()` (cobertura de fases EC-Council / etapas del Flujo_Investigacion)
     y `count_tooled_by_owner()` (≥2 Powers con Herramienta_Real por alumno, Req 9.6).
     La clasificación de huecos esperados vs. inesperados y la comprobación de que
     todo Power declara responsable se delega en `check_coverage.check_coverage`
     (tarea 13.3), que a su vez consume esos mismos métodos.

Veredicto (exit code):
  - **0** si la baseline es válida: sin Powers inválidos inesperados, sin huecos de
    cobertura inesperados y sin Powers sin responsable. Los **2 huecos esperados**
    de la línea base (Covering Tracks del Red Team y detección/hardening del Blue
    Team) se reportan como **pendientes**, no como fallo.
  - **!= 0** ante un problema real: un Power inválido inesperado, un hueco de
    cobertura inesperado o un Power sin responsable.

Uso::

    python3 scripts/validate_all.py [powers_root] [--strict]
    make validate

Requisitos: 20.6, 20.8, 20.9, 20.11.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reutiliza los componentes existentes de scripts/ (no los reimplementa).
try:  # permite ejecutar como módulo (`python -m scripts.validate_all`) o script suelto
    from scripts import power_adapter, check_power_docs, check_coverage, catalog, validate_target
except ImportError:  # pragma: no cover - fallback cuando se corre dentro de scripts/
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import power_adapter  # type: ignore
    import check_power_docs  # type: ignore
    import check_coverage  # type: ignore
    import catalog  # type: ignore
    import validate_target  # type: ignore

try:
    import yaml  # para leer scope.yaml en el self-check de la guardia
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
SCOPE_RELPATH = Path("engagements") / catalog.ENGAGEMENT_ID / "scope.yaml"


# ---------------------------------------------------------------------------
# Paso 1 — Adaptador de formatos: carga y valida ambos formatos de cada Power.
# ---------------------------------------------------------------------------

def check_power_formats(powers_root: Path) -> dict:
    """Carga y valida cada Power con el adaptador (tarea 1.10), en ambos formatos.

    Clasifica cada Power descubierto por el Catalogador en:

      - ``valid``: declara ``x-ethack`` y pasa :func:`power_adapter.validate_power`.
      - ``expected_undeclared``: Power **base** (nivel 1, conocido por
        :data:`catalog.BASELINE_KNOWLEDGE`) en ``POWER.md`` sin ``x-ethack`` — es el
        caso esperado de la línea base y **no** es fatal.
      - ``unexpected_invalid``: cualquier otro Power inválido (formato desconocido,
        contrato declarado pero inválido, o Power de alumno sin contrato) — **fatal**.

    Reutiliza :func:`catalog.discover_powers` para el descubrimiento canónico de
    ambos layouts y :func:`power_adapter.load_power`/:func:`power_adapter.validate_power`
    para la normalización y validación (no reimplementa ninguna).
    """
    valid: list[dict] = []
    expected_undeclared: list[dict] = []
    unexpected_invalid: list[dict] = []

    for found in catalog.discover_powers(powers_root):
        power_dir = found["dir"]
        name = found["name"]
        view = power_adapter.load_power(power_dir)
        ok, problems = power_adapter.validate_power(view)
        rel = _rel(power_dir)
        rec = {"name": name, "dir": str(rel), "format": view.get("format"),
               "declared": bool(view.get("declared")), "problems": problems}
        if ok:
            valid.append(rec)
        elif (not view.get("declared")
              and found["level"] == 1
              and name in catalog.BASELINE_KNOWLEDGE):
            expected_undeclared.append(rec)
        else:
            unexpected_invalid.append(rec)

    total = len(valid) + len(expected_undeclared) + len(unexpected_invalid)
    return {
        "total": total,
        "valid": valid,
        "expected_undeclared": expected_undeclared,
        "unexpected_invalid": unexpected_invalid,
        "ok": not unexpected_invalid,
    }


# ---------------------------------------------------------------------------
# Paso 2 — Artefactos_Documentacion: docStatus por Power (señala, no bloquea).
# ---------------------------------------------------------------------------

def check_docs(powers_root: Path) -> dict:
    """Calcula el ``docStatus`` de cada Power con ``check_power_docs.doc_status`` (13.1).

    La documentación incompleta se **señala** (lista ``incomplete``) pero **no**
    bloquea la validación (Req 15.6): ``ok`` siempre es ``True`` aquí.
    """
    complete: list[str] = []
    incomplete: list[dict] = []
    for found in catalog.discover_powers(powers_root):
        st = check_power_docs.doc_status(found["dir"])
        rel = str(_rel(found["dir"]))
        if st["complete"]:
            complete.append(rel)
        else:
            incomplete.append({"dir": rel, "missing": st["missing"]})
    return {"complete": complete, "incomplete": incomplete, "ok": True}


# ---------------------------------------------------------------------------
# Paso 3 — Guardia de la Allowlist_Objetivos: self-check de import + funcionamiento.
# ---------------------------------------------------------------------------

def check_allowlist_guard() -> dict:
    """Self-check de la guardia ``validate_target`` (tarea 1.3): importa y funciona.

    Confirma que la guardia de la Allowlist_Objetivos se puede invocar y decide
    correctamente: un objetivo **dentro** del alcance se admite y uno **fuera** se
    rechaza (Req 11.1, 11.2). Usa los assets reales de ``scope.yaml`` si están
    disponibles; si no, cae a un asset sintético para no depender del engagement.

    Devuelve ``ok == False`` solo si la guardia no importa o no se comporta como se
    espera (eso sí sería un problema real de la baseline).
    """
    checks: list[str] = []
    ok = True

    scope_path = REPO_ROOT / SCOPE_RELPATH
    assets: list[dict] = []
    source = "sintético"
    if yaml is not None and scope_path.is_file():
        try:
            data = yaml.safe_load(scope_path.read_text(encoding="utf-8")) or {}
            assets = data.get("assets") or []
            source = str(_rel(scope_path))
        except Exception as exc:  # degradación con gracia
            checks.append(f"no se pudo leer {_rel(scope_path)}: {exc}; se usa asset sintético")
            assets = []

    if not assets:
        assets = [{
            "kind": "container",
            "target_host": "10.0.10.21",
            "target_hostname": "dvwa-01.lab.ulsa",
            "ec2_host": "10.0.10.21",
            "ec2_hostname": "ec2-dvwa-01.lab.ulsa",
            "host_is_target": False,
        }]

    endpoints = validate_target.scope_endpoints(assets)
    if not endpoints:
        ok = False
        checks.append("scope_endpoints() no resolvió ningún endpoint del alcance")
        return {"ok": ok, "source": source, "endpoints": sorted(endpoints), "checks": checks}

    # a) un objetivo dentro de alcance se admite.
    in_scope = sorted(endpoints)[0]
    if validate_target.target_in_scope(in_scope, assets):
        checks.append(f"en alcance admitido: {in_scope!r} → True")
    else:
        ok = False
        checks.append(f"FALLO: {in_scope!r} debería estar en alcance y fue rechazado")

    # b) un objetivo fuera de alcance se rechaza.
    out_scope = "ejemplo-fuera-de-alcance.example.com"
    if not validate_target.target_in_scope(out_scope, assets):
        checks.append(f"fuera de alcance rechazado: {out_scope!r} → False")
    else:
        ok = False
        checks.append(f"FALLO: {out_scope!r} debería estar fuera de alcance y fue admitido")

    # c) run_tool_guarded lanza OutOfScopeError fuera de alcance (no ejecuta la herramienta).
    try:
        validate_target.run_tool_guarded(out_scope, assets, lambda t: "NO-DEBERÍA-EJECUTARSE")
        ok = False
        checks.append("FALLO: run_tool_guarded no lanzó OutOfScopeError fuera de alcance")
    except validate_target.OutOfScopeError:
        checks.append("run_tool_guarded abortó fuera de alcance (OutOfScopeError)")

    return {"ok": ok, "source": source, "endpoints": sorted(endpoints), "checks": checks}


# ---------------------------------------------------------------------------
# Paso 4 — Catalogador + cobertura + conteo por owner.
# ---------------------------------------------------------------------------

def check_catalog_coverage(powers_root: Path, strict: bool = False) -> dict:
    """Regenera ``inventory.json`` y evalúa cobertura y conteo (tareas 1.9 + 13.3).

    Invoca ``check_coverage.check_coverage`` que, a su vez, llama a
    ``catalog.build_inventory`` (regenera el inventario) y usa
    ``Inventory.coverage_gaps()`` para clasificar huecos **esperados** vs
    **inesperados** y detectar Powers sin responsable. Además expone el conteo de
    ``Inventory.count_tooled_by_owner()`` y los owners por debajo del mínimo de ≥2
    (Req 9.6) como información (pendiente), no como fallo de la baseline.
    """
    report = check_coverage.check_coverage(powers_root, strict=strict)
    inv = report["inventory"]
    report["tooled_by_owner"] = inv.count_tooled_by_owner()
    report["owners_below_minimum"] = inv.owners_below_minimum(2)
    report["inventory_path"] = str(_rel(REPO_ROOT / catalog.INVENTORY_RELPATH))
    return report


# ---------------------------------------------------------------------------
# Orquestación y reporte.
# ---------------------------------------------------------------------------

def run(powers_root: Path, strict: bool = False) -> dict:
    """Ejecuta los cuatro pasos de la Validacion_Local y devuelve el agregado."""
    formats = check_power_formats(powers_root)
    docs = check_docs(powers_root)
    guard = check_allowlist_guard()
    coverage = check_catalog_coverage(powers_root, strict=strict)

    ok = formats["ok"] and docs["ok"] and guard["ok"] and coverage["ok"]
    return {
        "formats": formats,
        "docs": docs,
        "guard": guard,
        "coverage": coverage,
        "ok": ok,
    }


def _rel(path: Path) -> Path:
    """Ruta relativa a la raíz del repo cuando sea posible (para un reporte legible)."""
    path = Path(path)
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def _print_report(result: dict) -> None:
    """Imprime el resumen de la Validacion_Local, paso por paso, y el veredicto."""
    formats = result["formats"]
    docs = result["docs"]
    guard = result["guard"]
    cov = result["coverage"]

    print("=" * 74)
    print("VALIDACION_LOCAL (make validate) — compuerta automatizada local (sin CI remota)")
    print("=" * 74)

    # Paso 1 — adaptador de formatos.
    print("\n[1/4] Adaptador de formatos (plugin.json ↔ POWER.md) — power_adapter (1.10)")
    print(f"      Powers descubiertos: {formats['total']} "
          f"| válidos: {len(formats['valid'])} "
          f"| base no declarados (esperado): {len(formats['expected_undeclared'])} "
          f"| inválidos inesperados: {len(formats['unexpected_invalid'])}")
    for rec in formats["expected_undeclared"]:
        print(f"      · base sin x-ethack (esperado): {rec['dir']} [{rec['format']}]")
    for rec in formats["unexpected_invalid"]:
        print(f"      ✗ INVÁLIDO INESPERADO: {rec['dir']} [{rec['format']}]")
        for p in rec["problems"]:
            print(f"          - {p}")

    # Paso 2 — Artefactos_Documentacion.
    print("\n[2/4] Artefactos_Documentacion (docStatus) — check_power_docs (13.1) — señala, no bloquea")
    print(f"      Completos: {len(docs['complete'])} | incompletos: {len(docs['incomplete'])}")
    for rec in docs["incomplete"]:
        print(f"      · faltan en {rec['dir']}: {', '.join(rec['missing'])}")

    # Paso 3 — guardia de allowlist.
    print("\n[3/4] Guardia de la Allowlist_Objetivos — validate_target (1.3) — self-check")
    print(f"      Fuente de assets: {guard['source']} | endpoints en alcance: {len(guard['endpoints'])}")
    for c in guard["checks"]:
        mark = "✗" if c.startswith("FALLO") else "·"
        print(f"      {mark} {c}")

    # Paso 4 — catalogador + cobertura + conteo.
    print("\n[4/4] Catalogador + cobertura + conteo — catalog.build_inventory (1.9) / check_coverage (13.3)")
    print(f"      inventory.json regenerado: {cov['inventory_path']}")
    print(f"      Fases EC-Council cubiertas: {cov['covered_ec_phases']}")
    print(f"      Etapas Flujo_Investigacion cubiertas: {cov['covered_forensics_stages']}")
    print(f"      Huecos esperados de baseline (pendientes, no fatales): {len(cov['expected_gaps'])}")
    for g in cov["expected_gaps"]:
        team = f" [{g['team']}]" if g.get("team") else ""
        print(f"        - PENDIENTE{team} [{g['axis']}] {g['name']} (gap=true)")
    if cov["unexpected_gaps"]:
        print(f"      ✗ Huecos INESPERADOS: {len(cov['unexpected_gaps'])}")
        for g in cov["unexpected_gaps"]:
            print(f"        - [{g['axis']}] {g['name']} — {g.get('reason', '')}")
    if cov["powers_without_owner"]:
        print(f"      ✗ Powers SIN responsable: {len(cov['powers_without_owner'])} (Req 13.4)")
        for p in cov["powers_without_owner"]:
            print(f"        - {p.get('name')} (origin={p.get('origin')})")
    else:
        print("      ✔ Todos los Powers declaran responsable (owner/team).")
    print("      Conteo de Powers con Herramienta_Real por owner (≥2 por alumno — Req 9.6):")
    for owner, n in sorted(cov["tooled_by_owner"].items()):
        flag = "" if n >= 2 else "  (pendiente: <2)"
        print(f"        - {owner}: {n}{flag}")

    # Veredicto.
    print("\n" + "-" * 74)
    if result["ok"]:
        print("RESULTADO: ✔ VERDE — baseline válida. "
              f"Quedan {len(cov['expected_gaps'])} hueco(s) esperado(s) como pendientes (exit 0).")
    else:
        motivos = []
        if not formats["ok"]:
            motivos.append(f"{len(formats['unexpected_invalid'])} Power(s) inválido(s) inesperado(s)")
        if cov["unexpected_gaps"]:
            motivos.append(f"{len(cov['unexpected_gaps'])} hueco(s) inesperado(s)")
        if cov["powers_without_owner"]:
            motivos.append(f"{len(cov['powers_without_owner'])} Power(s) sin responsable")
        if not guard["ok"]:
            motivos.append("la guardia de Allowlist_Objetivos no superó el self-check")
        print(f"RESULTADO: ✗ FALLO — {'; '.join(motivos)} (exit != 0).")
    print("-" * 74)


def _main(argv: list[str]) -> int:
    """CLI de la Validacion_Local (tarea 15.4).

    Uso:
        python3 scripts/validate_all.py [powers_root] [--strict]

    Sin ``powers_root`` usa ``powers/`` relativo a la raíz del repo. ``--strict``
    hace fatales también los huecos esperados de baseline (tras integrar los Powers
    de alumnos). Devuelve 0 si la baseline es válida; distinto de 0 ante un problema
    real.
    """
    strict = "--strict" in argv[1:]
    positional = [a for a in argv[1:] if not a.startswith("--")]
    powers_root = Path(positional[0]) if positional else (
        REPO_ROOT / "powers" if (REPO_ROOT / "powers").is_dir() else REPO_ROOT.parent / "powers")

    result = run(powers_root, strict=strict)
    _print_report(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
