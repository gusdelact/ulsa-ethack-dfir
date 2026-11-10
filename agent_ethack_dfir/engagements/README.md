# `engagements/` — Estado y evidencia por engagement

Un subdirectorio por engagement (`engagements/<id>/`) con el alcance autorizado, el estado del flujo y la evidencia. Es una **ruta compartida** del Líder Técnico.

Estructura prevista de cada `engagements/<id>/`:

| Artefacto | Propósito |
|---|---|
| `scope.yaml` | `Allowlist_Objetivos`, `status`, `authorized_window`, `ethical_principles`, `prohibited_actions`; Contenedores_Objetivo sobre nodos EC2 Debian/DVWA (host no-objetivo salvo `host_is_target: true`). |
| `state.json` | Fase actual + `completed_phases`; bloque `incident_response`. |
| `inventory.json` | Inventario de Powers/agents ↔ fase/etapa ↔ responsable. **Lo regenera el Catalogador**, no se edita a mano. |
| `evidence/<id>/record.json` | Registro de evidencia con `sha256`, `volatility_rank` (1–7, RFC 3227), comando/UTC/herramienta/versión/resultado. |
| `evidence/<id>/chain_of_custody.jsonl` | Cadena_Custodia encadenada por `prev_sha256`. |
| `incidents/<id>/incident.json` | Registro de incidente del Incident Responder (fases NIST SP 800-61, IOCs, contención, escalaciones). |
| `grc/risk_register.json`, `grc/csf_profile.json` | Artefactos GRC ligados al engagement (Registro_Riesgos, Perfil_CSF, POA&M). |

Engagement de referencia: `engagements/dvwa-lab-ulsa/` (Task 1.6).

_Referencias: design.md "Organización de carpetas"; Req 9.4, 13.1._
