# `agents/fases/` — Subagentes de fase (EC-Council)

Cinco custom agents, uno por fase del ciclo EC-Council. Cada subagente **declara objetivo y alcance antes de invocar cualquier Herramienta_Real** y usa ≥1 Power de la fase correspondiente, siempre contra objetivos de la `Allowlist_Objetivos`.

| Subagente | Powers base de apoyo |
|---|---|
| Reconnaissance | `osint-passive-recon`, `footprinting-enumeration` |
| Scanning | `footprinting-enumeration`, `vulnerability-assessment` |
| Gaining Access | `vulnerability-assessment`, `exploitation-metasploit` |
| Maintaining Access | `exploitation-metasploit` |
| Covering Tracks | _hueco de cobertura_: Power nuevo (análisis/manipulación de rastros acotado al lab) |

**Ruta compartida** mantenida por el Líder Técnico (línea base docente, Task 4).

_Referencias: Req 2.1–2.7, 13.1._
