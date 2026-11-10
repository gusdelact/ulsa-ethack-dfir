# `evidence/` — Registro de evidencia y Cadena_Custodia

Una carpeta por pieza de evidencia: `evidence/<evidence-id>/`. El equipo de
Digital Forensics la puebla durante el Flujo_Investigacion (Collect → Preserve →
Analyze → Report). Esta carpeta se inicializa en la tarea 1.6; los Powers de DF
(tareas 8.2/8.4/8.6) producen los registros reales.

Cada carpeta contiene dos artefactos:

| Archivo | Propósito |
|---|---|
| `record.json` | Registro de la pieza de evidencia. |
| `chain_of_custody.jsonl` | Cadena_Custodia: una línea JSON por traspaso/transformación. |

El subárbol `mem-dvwa-01-0001/` es una **plantilla de ejemplo documentada** con
la estructura esperada; no es evidencia real.

## Formato de `record.json`

Campos (design.md "Registro de evidencia y Cadena_Custodia"; Req 5.3, 16.1, 16.4):

| Campo | Descripción | Req |
|---|---|---|
| `evidence_id` | Identificador único de la pieza. | — |
| `source_asset` | `id` del asset de `scope.yaml` del que proviene. | 12.3 |
| `collected_by` | Actor que recolectó. | 16.3 |
| `collected_at_utc` | **Hora UTC** de recolección (ISO-8601 Z). | 16.4 |
| `tool` | **Herramienta** usada. | 16.4 |
| `tool_version` | **Versión** de la herramienta. | 16.4 |
| `command` | **Comando** exacto ejecutado (reproducibilidad). | 16.4 |
| `result` | **Resultado** / resumen de la salida. | 16.4 |
| `sha256` | **Hash de verificación** de la evidencia (Evidence Integrity). | 5.3 |
| `volatility_rank` | Posición 1–7 en el Orden_Volatilidad RFC 3227 (ver abajo). | 5.6, 16.1 |
| `storage` | Ubicación en almacén de escritura única / solo-anexado. | 5.4 |

### `volatility_rank` — Orden_Volatilidad RFC 3227 (Req 5.6, 16.1)

En la fase Collect se recolecta primero lo más volátil (rank bajo) y después lo
menos volátil (rank alto). La serie de `volatility_rank` ordenada por
`collected_at_utc` debe ser monótona no decreciente.

| Rank | Tipo de evidencia |
|---|---|
| 1 | Registros de CPU y caché |
| 2 | Memoria RAM |
| 3 | Estado de red (conexiones, ARP, rutas) |
| 4 | Procesos en ejecución |
| 5 | Disco |
| 6 | Logs remotos y monitoreo |
| 7 | Medios de respaldo / archivo |

## Formato de `chain_of_custody.jsonl`

Una línea JSON por eslabón. El eslabón `seq: 0` es la recolección inicial
(`prev_sha256: null`); cada eslabón `seq > 0` referencia el hash del estado
anterior en `prev_sha256`, de modo que recorrer la cadena reconstruye el orden
de custodia (Req 5.4, 5.10, 16.3).

Campos por eslabón: `seq`, `action` (`collect` | `transfer` | `analyze` | …),
`actor`, `ts_utc`, `sha256`, `prev_sha256` (`null` solo en `seq 0`), y
opcionalmente `link`/`note`.

Invariantes del modelo forense (design.md):
- `collect` registra el hash de verificación (Req 5.3).
- El análisis opera sobre copia y conserva el `sha256` del original
  (`prev == actual`) (Req 5.5, 16.2).
- Cada `seq > 0` referencia el eslabón previo por `prev_sha256` (Req 5.4, 16.3).
- Evidencia en un Contenedor_Objetivo = evidencia efímera: recolección
  automatizada (snapshot + hash + copia) antes de que el contenedor desaparezca
  (Req 5.9, 16.8).

_Referencias: design.md "Data Models"; Req 5.3, 5.4, 5.5, 5.6, 5.9, 5.10,
16.1–16.4, 16.8._
