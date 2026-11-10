# `agents/roles/` — Subagentes de rol (equipos)

Un custom agent por equipo/rol. Cada subagente de rol agrupa los Powers de su equipo y se cablea a la carpeta de equipo correspondiente en `powers/<equipo>/`.

| Rol / subagente | Carpeta de Powers | Powers base de cimiento |
|---|---|---|
| Red Team | `powers/red-team/` | `osint-passive-recon`, `footprinting-enumeration`, `vulnerability-assessment`, `exploitation-metasploit` |
| Blue Team | `powers/blue-team/` | _sin base dedicada_; se apoya en logs de `dfir-linux` y en `network-forensics` |
| Digital Forensics | `powers/digital-forensics/` | `dfir-linux` (host), `network-forensics` (red) — **deriva red→host** |
| GRC | `powers/grc/` | `grc-nist-csf` |
| Incident Responder | `powers/incident-responder/` | `incident-handling-nist`, `incident-response-lab` |

El subagente Digital Forensics implementa el Flujo_Investigacion **Detect → Isolate → Collect → Preserve → Analyze → Report**.

**Rutas compartidas** (los subagentes) mantenidas por el Líder Técnico; los Powers de cada equipo pertenecen a sus alumnos.

_Referencias: Req 3.1, 4.1, 5.1, 6.5, 7.5, 13.1._
