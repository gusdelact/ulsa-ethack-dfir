# Modelo estándar de Power — plantilla (`powers/_template/`)

Plantilla reutilizable del **modelo estándar de Power** del proyecto Ethical
Hacking & Digital Forensics (ULSA). Copia esta carpeta a
`powers/<equipo>/<power>/`, renombra y completa los TODO.

## Estructura

```
powers/_template/
├── plugin.json                 # metadatos + contrato x-ethack (fase/etapa, tools, allowlist, modo, docs)
├── skills/
│   └── <skill>/
│       ├── SKILL.md            # qué hace el skill y cómo se invoca
│       └── execution_mode.py   # resolve_mode(): default + validación del Modo_Ejecucion
├── steering/                   # guías de conocimiento cargables bajo demanda (*.md)
└── docs/                       # Artefactos_Documentacion (Req 15.1)
    ├── prompt.md               # prompt de generación (Req 15.2)
    ├── sessions/               # sesiones de prueba con Kiro (Req 15.3) — contiene .gitkeep
    └── feedback.md             # realimentación del resultado (Req 15.4)
```

## Contrato `x-ethack` (bloque del `plugin.json`)

| Campo | Significado |
|---|---|
| `kind` | `offensive` \| `defensive` \| `forensics` \| `governance` \| `response` |
| `ecCouncilPhase` | una de las 5 fases EC-Council, **o** `null` si es forense |
| `forensicsStage` | `Detect`\|`Isolate`\|`Collect`\|`Preserve`\|`Analyze`\|`Report`, **o** `null` |
| `team` / `owner` | equipo y alumno responsable (se refleja en `inventory.json`) |
| `tools` | Herramienta(s)_Real envuelta(s) — lista **no vacía** |
| `allowlistValidation` | `required`, `source` (→ `scope.yaml#assets`), `targetParams` |
| `producesActionLog` | registro consumible por Blue Team / Digital Forensics |
| `executionMode` | `param: "Modo_Ejecucion"`, `allowed`, `default` |
| `documentation` | `root` y `required` (Artefactos_Documentacion) |

## Reglas del modelo (invariantes verificables)

Un Power es válido cuando cumple **todas** estas reglas (Req 8.2, 8.4, 9.1,
9.2, 9.3, 9.7, 9.8, 14.1, 14.2, 15.1):

1. **`tools` no vacío** — envuelve al menos una Herramienta_Real (Req 9.1).
2. **`ecCouncilPhase` XOR `forensicsStage`** — declara exactamente una ubicación
   en el ciclo; el otro campo en `null` (Req 9.2).
3. **`allowlistValidation.required == true`** apuntando al `scope.yaml` del
   engagement; el Power resuelve/normaliza el objetivo y valida su pertenencia
   a la Allowlist_Objetivos antes de ejecutar (Req 9.5, 11.1–11.4).
4. **`executionMode.allowed == {script-kiddie, green-hat, pro}`** con
   `default == "script-kiddie"`; el Power acepta `Modo_Ejecucion` y aplica el
   default cuando no se indica (Req 9.7, 14.1, 14.2); valores inválidos se
   rechazan con `InvalidModeError` (Req 14.7).
5. **Artefactos_Documentacion presentes** bajo `documentation.root` (`docs/`):
   `prompt.md`, `sessions/`, `feedback.md` (Req 9.8, 15.1).
6. El Power es **invocable** por al menos un subagente de fase o de rol (se
   refleja en el inventario) (Req 9.3).

## Compatibilidad con los dos formatos (`plugin.json` ↔ `POWER.md`)

El proyecto admite **dos formatos** de empaquetado de Power:

- `plugin.json` (estilo `agent-plugins.org`) — este `_template`.
- `POWER.md` (frontmatter + "modos de trabajo") — usado por varios Powers base.

El contrato `x-ethack` es la **vista lógica común**. Las seis reglas de arriba
aplican **por igual** a ambos formatos: para un Power en `POWER.md`, los mismos
invariantes se expresan en su frontmatter / sección de modos de trabajo. El
**adaptador** `scripts/power_adapter.py` (tarea 1.10) normaliza cualquiera de
los dos formatos a esta vista común, de modo que la Validacion_Local los valide
con criterios equivalentes (Req 8.2, 8.4, 9.2).
