# `agents/` — Custom agents de Kiro

Contiene los **custom agents** del sistema de Ethical Hacking y Digital Forensics. Se organiza en tres capas:

| Subcarpeta | Propósito |
|---|---|
| `orquestador/` | **Agente_Orquestador**: agente principal que coordina el ciclo EC-Council, delega en los subagentes de fase/rol, lee/escribe `state.json` y consolida entregables. |
| `fases/` | **5 subagentes de fase** EC-Council: Reconnaissance, Scanning, Gaining Access, Maintaining Access, Covering Tracks. Cada uno declara objetivo y alcance antes de invocar herramientas. |
| `roles/` | **Subagentes de rol** por equipo: Red Team, Blue Team, Digital Forensics, GRC e Incident Responder. Agrupan los Powers de su equipo. |

## Convención de integración (Líder Técnico)

El **Líder Técnico** (Req 13.1) integra los entregables de los 13 alumnos (Red Team 3 · Blue Team 3 · Digital Forensics 4 · GRC 1 · Incident Responder 1 · Líder Técnico 1). Los agentes de esta carpeta son **rutas compartidas**: las mantiene el Líder Técnico en el `Repositorio_Integracion` y no son propiedad de un alumno individual. Los agentes de fase/rol se cablean a los Powers descubiertos en `powers/` a través del inventario (`inventory.json`), que el Catalogador regenera de forma determinista.

_Referencias: design.md "Organización de carpetas y convenciones de integración"; Req 9.4, 13.1._
