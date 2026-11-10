# `scripts/` — Utilidades compartidas del proyecto

Scripts transversales que invocan los Powers, los hooks y la Validacion_Local. Son **rutas compartidas** mantenidas por el Líder Técnico (no propiedad de un alumno).

Utilidades previstas por la línea base:

| Script | Propósito | Task |
|---|---|---|
| `validate_target.py` | Guardia de la `Allowlist_Objetivos` (`normalize_target`, `scope_endpoints`, `target_in_scope`, `run_tool_guarded`); invocada por cada Power antes de su Herramienta_Real. | 1.3 |
| `gate_mcp_sim.py` | Hook `PreToolUse` de autorización simulada (no bloqueante; registra en `local-audit/authz.jsonl`). | 1.5 |
| `audit_event.py` | Hook `PostToolUse` de auditoría (resumen + `sha256` del evento en `local-audit/events.jsonl`, anota el `mode`). | 1.5 |
| `catalog.py` | Catalogador: `discover_powers()` (ambos layouts) + `build_inventory()`; regenera `inventory.json`. | 1.9 |
| `power_adapter.py` | Adaptador de los dos formatos de Power (`plugin.json` ↔ `POWER.md`) a la vista común `x-ethack`. | 1.10 |
| `check_power_docs.py` | Calcula `docStatus` al integrar (señala Artefactos_Documentacion faltantes). | 13.x |

_Referencias: design.md "Organización de carpetas"; Req 9.4, 13.1._

## Catalogador (`catalog.py`) — genera `inventory.json`

El Catalogador es el **único** componente que produce
`engagements/dvwa-lab-ulsa/inventory.json`. **No se edita a mano**: lo regenera
de forma determinista en cada validación. Lo invocan `make validate` (paso 4 de
la Validacion_Local, tarea 15.4) y `make catalog`; la Validacion_Local **reutiliza**
`build_inventory()` y los métodos del inventario en lugar de reimplementarlos.

```bash
python3 scripts/catalog.py            # regenera inventory.json y reporta cobertura/conteo
```

API pública:

- `discover_powers(powers_root)` — descubre **ambos layouts**: Powers base en
  `powers/<nombre>/` (un nivel) y Powers de alumnos en `powers/<equipo>/<power>/`
  (dos niveles); detecta `plugin.json` **o** `POWER.md`; excluye `_template/` y las
  carpetas de equipo vacías.
- `build_inventory(powers_root, assets=None)` — lee cada Power con
  `power_adapter.load_power()` (no reimplementa el parseo), construye el objeto
  `Inventory`, lo **escribe** en `inventory.json` y lo **devuelve**.
- `Inventory.coverage_gaps()` — huecos de las 5 fases EC-Council ∪ 6 etapas del
  Flujo_Investigacion no cubiertos por la baseline (más el hueco defensivo del Blue
  Team), anotados con `gap: true`. Sobre la baseline: **Covering Tracks** y
  **Blue Team detección/hardening**.
- `Inventory.count_tooled_by_owner()` — Powers con Herramienta_Real por `owner`
  (base del mínimo de ≥2 por alumno, Req 9.6).

Los 9 Powers base están en formato `POWER.md` y **no declaran `x-ethack`**: el
Catalogador les asigna fase/etapa/rol/owner/tools desde un **mapeo de conocimiento**
(`BASELINE_KNOWLEDGE`) y los marca `baseline: true`, `xethack_declared: false`,
dejando en `null` lo que el Power no declara (`declared_ecCouncilPhase`/
`declared_forensicsStage`). Los Powers de alumnos que declaran `x-ethack` se
catalogan directamente desde la vista del adaptador (`origin: extended`/`new`).
