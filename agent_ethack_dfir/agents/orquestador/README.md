# `agents/orquestador/` — Agente_Orquestador

Agente principal (Kiro custom agent) que:

- Expone las **5 fases EC-Council** como etapas seleccionables y aplica los Principios_Eticos como restricciones de comportamiento.
- Implementa la secuencia canónica por defecto **Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks**, leyendo/escribiendo `engagements/<id>/state.json`.
- Ante una fase fuera de orden, reporta las fases previas no completadas antes de delegar.
- Identifica en su respuesta cada subagente invocado y la fase/rol que representa.

## Archivos

- `orquestador.md` — definición del custom agent (frontmatter `name`/`description`
  + rol/prompt del sistema): expone las 5 fases, aplica los Principios_Eticos como
  restricciones, describe la secuencia canónica sobre `state.json` e identifica en
  su respuesta cada subagente invocado y su fase/rol (Req 1.1, 1.2, 1.3, 1.6, 11.4).
- `phase_sequence.py` — helper determinista de la secuencia canónica:
  - Primitivas de orden (tarea 3.1): `CANONICAL_SEQUENCE`, `next_phase()`,
    `previous_incomplete()`, `default_next()` y lectura/escritura de
    `engagements/<id>/state.json` (`load_state()`/`save_state()`). Dan soporte a
    la secuencia por defecto (Req 1.3).
  - Orden y consolidación (tarea 3.2, **implementada**): `out_of_order_report()`
    produce la estructura/mensaje de reporte de fases previas no completadas ante
    una fase fuera de orden, antes de delegar (Req 1.5); `consolidate_phase()`
    registra el resultado de una fase, la marca en `completed_phases` y devuelve
    la transición ofrecida hacia la fase siguiente (Req 1.4). Ambas son funciones
    puras y deterministas (no mutan el estado recibido).

**Ruta compartida** mantenida por el Líder Técnico. Se construye en la línea base del docente (Tasks 3).

_Referencias: Req 1.1–1.6, 13.1._
