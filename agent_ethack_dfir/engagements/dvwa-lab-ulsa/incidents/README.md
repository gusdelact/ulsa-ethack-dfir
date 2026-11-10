# `incidents/` — Registros de incidente del Incident Responder

Una carpeta por incidente: `incidents/<incident-id>/incident.json`. El Incident
Responder mantiene un registro por cada incidente gestionado según el
Proceso_Respuesta_Incidentes de NIST SP 800-61 (Req 7.6, 18.2).

`inc-0001/incident.json` es una **plantilla/ejemplo documentada**; los Powers del
Incident Responder la pueblan durante el ejercicio.

## Formato de `incident.json`

Ver design.md "Registro de incidente — `incidents/<incident-id>/incident.json`".

| Campo | Descripción | Req |
|---|---|---|
| `nist_phase` | Fase NIST actual ∈ `{Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity}`. | 7.6, 18.2 |
| `phase_history` | Entradas de fase; el ciclo es iterativo y las lecciones retroalimentan Preparation. | 18.5, 18.7 |
| `iocs[]` | Cada IOC con `format` ∈ `{STIX, YARA, OpenIOC}` y mapeo a MITRE ATT&CK (`attack`) y Cyber Kill Chain (`kill_chain_stage`). | 7.8, 18.9, 18.10 |
| `containment_actions[]` | Clasificadas `short-term` / `long-term`. Una `short-term` cumple `shutdown == false` y `preserves_evidence == true`. | 7.7, 18.5 |
| `escalations[]` | Escalamiento registrado ante movimiento lateral. | 7.9, 18.5 |
| `evidence_refs[]` | Enlaces a evidencia preservada por Digital Forensics (`evidence/<id>`). | 7.4, 7.8, 18.8 |
| `csf_subcategories[]` | Alineación con funciones RS/RC del NIST CSF. | 19.7 |
| `post_incident` | Reporte final y lecciones aprendidas. | 18.6, 18.7 |

Invariantes (design.md):
- `nist_phase` ∈ las 4 fases NIST y `phase_history` registra cada entrada.
- Cada acción `short-term` no apaga el sistema y preserva evidencia.
- Cada IOC declara `format` válido y su mapeo ATT&CK / Kill Chain.

_Referencias: Req 7.6, 7.7, 7.8, 7.9, 18.2, 18.5, 18.7, 18.9, 18.10._
