# `powers/` — Kiro Powers (base + de alumnos)

Cada **Power** envuelve una o más Herramientas_Real de Kali Linux / seguridad y expone su capacidad al subagente que lo usa. Antes de ejecutar su Herramienta_Real, todo Power valida el objetivo contra la `Allowlist_Objetivos` del engagement.

## Dos layouts conviven (convención)

Esta carpeta mezcla **dos niveles de anidación** a propósito; el Catalogador (`scripts/catalog.py`, `discover_powers()`) descubre ambos:

1. **Powers base — un nivel: `powers/<nombre>/`**
   Son los 9 Powers ya construidos que forman el **cimiento** del proyecto. **No se mueven ni se recrean**: siguen viviendo donde están.
2. **Powers de alumnos — dos niveles: `powers/<equipo>/<power>/`**
   Las subcarpetas de equipo (`red-team/`, `blue-team/`, `digital-forensics/`, `grc/`, `incident-responder/`) alojan los Powers **nuevos o extendidos** que entregan los alumnos. El aislamiento por carpeta evita colisiones de merge entre los 13 alumnos (CODEOWNERS por ruta).

> Regla anti-conflictos: **`inventory.json` no se edita a mano**. Lo regenera el Catalogador recorriendo ambos layouts en cada `make validate` / `make catalog`.

## Los 9 Powers base (cimiento — reutilizar, no recrear)

| Power (`powers/<nombre>/`) | Formato | Fase EC-Council / Etapa forense | Equipo |
|---|---|---|---|
| `osint-passive-recon` | `POWER.md` + MCP + hooks | Reconnaissance (OSINT pasivo) | Red Team |
| `footprinting-enumeration` | `plugin.json` | Reconnaissance + Scanning | Red Team |
| `vulnerability-assessment` | `plugin.json` | Scanning / Gaining Access | Red Team |
| `exploitation-metasploit` | `plugin.json` | Gaining Access / Maintaining Access | Red Team |
| `dfir-linux` | `plugin.json` | Digital Forensics — **host** Linux | Digital Forensics |
| `network-forensics` | `plugin.json` | Digital Forensics — **red** | Digital Forensics |
| `grc-nist-csf` | `POWER.md` | GRC (NIST CSF 2.0) | GRC |
| `incident-handling-nist` | `POWER.md` | Incident Responder (NIST SP 800-61) | Incident Responder |
| `incident-response-lab` | `POWER.md` + MCP | Incident Responder (lab) | Incident Responder |

**Dos formatos de empaquetado:** los Powers base usan `plugin.json` (estilo agent-plugins.org) **o** `POWER.md` (frontmatter + "modos de trabajo"). El modelo estándar de Power trata los campos `x-ethack` como contrato lógico; un adaptador (`scripts/power_adapter.py`, Task 1.10) mapea el frontmatter de `POWER.md` a ese mismo contrato para validar ambos formatos con criterios equivalentes.

### Deriva red→host en Digital Forensics

`network-forensics` (forense de red) **deriva a** `dfir-linux` (forense de host) al identificar el host sospechoso: el análisis de tráfico señala un nodo, y la investigación continúa sobre ese host con las capacidades de `dfir-linux`.

## Huecos de cobertura (Powers nuevos desde cero)

La línea base **no** cubre la etapa **Covering Tracks** (Red Team) ni la **detección/hardening del Blue Team**; esos son los únicos Powers que los alumnos crean desde cero (el Blue Team puede apoyarse en los logs de `dfir-linux` y en `network-forensics`).

## Convención de integración (Líder Técnico)

El Líder Técnico valida cada entregable contra el modelo de Power (`x-ethack` presente, `tools` no vacío, `ecCouncilPhase` xor `forensicsStage`, `allowlistValidation.required == true`, `executionMode` con default `script-kiddie`, Artefactos_Documentacion bajo `docs/`). Si cumple, lo copia a `powers/<equipo>/` y lo registra en `inventory.json`; si no, rechaza la integración. Cada alumno aporta un mínimo de **2 Powers con Herramienta_Real** (Req 9.6).

_Referencias: design.md "Organización de carpetas y convenciones de integración" y "Aislamiento por carpetas y propiedad (CODEOWNERS)"; Req 9.4, 13.1, 5.8._
