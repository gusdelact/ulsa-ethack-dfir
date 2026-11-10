<!--
  Plantilla de Pull Request de entrega de un Power
  Proyecto: Agente de Ethical Hacking & Digital Forensics (ULSA)
  Flujo: Fork_Alumno -> Repositorio_Integracion (Líder Técnico) vía Pull Request.
  Compuerta de calidad: Validacion_Local (`make validate`) en verde + revisión humana del Líder Técnico.
  No hay CI remota (ni GitHub Actions): toda comprobación corre localmente. (Req 20.5, 20.6, 20.11)
-->

## Entrega de Power

- **Equipo:** <!-- red-team | blue-team | digital-forensics | grc | incident-responder -->
- **Alumno (owner) e iniciales:** <!-- Nombre Apellido — INI -->
- **Nombre del Power:** <!-- <nombre-power> -->
- **Ubicación:** `powers/<equipo>/<power>/`
- **Rama:** `power/<equipo>-<iniciales>-<nombre-power>`
- **Formato del Power:** <!-- plugin.json | POWER.md -->
- **Origen:** <!-- new (nuevo) | extended (extiende un Power base) -->
- **Fase EC-Council _o_ Etapa del Flujo_Investigacion que cubre:** <!-- p.ej. Scanning | Collect -->

## Resumen

<!-- Qué hace el Power, qué Herramienta_Real envuelve y a qué fase/etapa y rol responde. -->

## Contrato de entrega (qué trae este PR)

Un PR de entrega de un Power DEBE incluir (Req 20.5, Req 15):

- [ ] El **Power**: `plugin.json` **o** `POWER.md` con el bloque de contrato `x-ethack`.
- [ ] Su directorio **`skills/`** (al menos un `skills/<skill>/SKILL.md`).
- [ ] Su directorio **`steering/`**.
- [ ] Sus **Artefactos_Documentacion** bajo **`docs/`**:
  - [ ] `docs/prompt.md` — prompt de generación del Power.
  - [ ] `docs/sessions/` — sesiones de prueba con Kiro.
  - [ ] `docs/feedback.md` — realimentación al chat del Power.

## Checklist de entrega (completar antes de abrir el PR)

### Validación local y ubicación
- [ ] `make validate` corre **en verde** localmente (Validacion_Local, sin CI remota).
- [ ] El Power está ubicado en `powers/<equipo>/<power>/` (dos niveles: equipo/power).
- [ ] La rama sigue el patrón `power/<equipo>-<iniciales>-<nombre-power>` y **no** se trabajó sobre la rama base/de partida.

### Contrato `x-ethack` completo
- [ ] `tools` **no vacío** (envuelve al menos una Herramienta_Real).
- [ ] Declara **`ecCouncilPhase` XOR `forensicsStage`** (una fase EC-Council **o** una etapa del Flujo_Investigacion, no ambas).
- [ ] `allowlistValidation.required == true` con `source` al `scope.yaml` del engagement.
- [ ] `executionMode.allowed == [script-kiddie, green-hat, pro]` con **`default: script-kiddie`**.
- [ ] `documentation` declara `root` y `required: [prompt.md, sessions/, feedback.md]`.
- [ ] Declara `owner` (equipo/alumno responsable).

### Modos de ejecución (Req 14)
- [ ] **`script-kiddie`** (default): solo comandos predefinidos.
- [ ] **`green-hat`**: ejecuta y explica la lógica subyacente.
- [ ] **`pro`**: lógica propia, puede generar scripts acotados al lab.
- [ ] El modo se resuelve con `resolve_mode` y el modo aplicado se registra para el Hook_Auditoria.

### Alcance y ética (Req 11, 12)
- [ ] El Power valida el objetivo contra la **Allowlist_Objetivos** antes de ejecutar su Herramienta_Real.
- [ ] El objetivo se dirige al **Contenedor_Objetivo**, **no al host EC2 anfitrión** (salvo `host_is_target == true` explícito).
- [ ] Ninguna actividad apunta a producción; la autorización es simulada/didáctica.
- [ ] El Power produce un registro de acción consumible por Blue Team / Digital Forensics.

## Notas para el Líder Técnico

<!--
  El Líder Técnico ejecuta `make validate` y revisa este PR antes de integrar (merge).
  Si la Validacion_Local falla o la revisión no se supera, el PR NO se integra y se indica el incumplimiento.
  Recordatorio: `inventory.json` se regenera con el Catalogador (make catalog), no se edita a mano.
-->
