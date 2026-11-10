# Implementation Plan: Agente de Ethical Hacking y Digital Forensics

## Overview

Este plan convierte el diseño en pasos de código accionables para un proyecto académico de 13 alumnos organizados por equipo/rol (Líder Técnico 1, Red Team 3, Blue Team 3, Digital Forensics 4, GRC 1, Incident Responder 1). El lenguaje de implementación es **Python** (coincide con los scripts del starter y el diseño).

La construcción es incremental: primero la **base común** (estructura de carpetas, modelo de Power, guardia de allowlist, hooks `version: v1`, modelo de datos del engagement), luego el **Agente_Orquestador** y los **5 subagentes de fase**, después los **subagentes de rol y los Powers por equipo**, y finalmente la **integración del Líder Técnico**, la **verificación de cobertura** y las **pruebas**.

**Línea base de Powers ya construida (reutilizar, no recrear):** en `powers/` existen 9 Powers construidos que son el cimiento del proyecto. El enfoque de las tareas de Powers no es "crear desde cero" sino **reutilizar/extender lo existente** y **crear Power nuevo solo para los huecos** de cobertura:

| Power existente | Formato | Fase EC-Council / Etapa Flujo_Investigacion | Rol |
|---|---|---|---|
| `osint-passive-recon` | `POWER.md` + MCP + hooks | Reconnaissance (OSINT pasivo) | Red Team |
| `footprinting-enumeration` | `POWER.md` | Reconnaissance + Scanning (nmap, metodología 6 capas) | Red Team |
| `vulnerability-assessment` | `POWER.md` | Scanning / Gaining Access (Nessus, OpenVAS, CVSS) | Red Team |
| `exploitation-metasploit` | `POWER.md` | Gaining Access / Maintaining Access (Metasploit, msfvenom, Meterpreter) | Red Team |
| `dfir-linux` | `POWER.md` | Digital Forensics host (live response, dd/dc3dd, logs, persistencia, Autopsy) | Digital Forensics |
| `network-forensics` | `POWER.md` | Digital Forensics red (Wireshark, tcpdump, Snort, Suricata/NetFlow, TLS) | Digital Forensics |
| `grc-nist-csf` | `POWER.md` | GRC (NIST CSF 2.0, risk register, gap analysis, POA&M, LFPDPPP↔CIS) | GRC |
| `incident-handling-nist` | `POWER.md` | Incident Responder (NIST SP 800-61, Cyber Kill Chain, MITRE ATT&CK, cadena de custodia, playbooks) | Incident Responder |
| `incident-response-lab` | `POWER.md` + MCP | Incident Responder lab (TheHive, VirusTotal, Wazuh, Sysmon/PowerShell) | Incident Responder |

**Dos formatos soportados (realidad verificada en disco):** los 9 Powers base ya construidos están **todos** en formato `POWER.md` (frontmatter + "modos de trabajo"); ninguno usa `plugin.json`. El formato `plugin.json` (estilo agent-plugins.org) es el de la plantilla `powers/_template/` y una **opción para los Powers nuevos de alumnos**. El modelo estándar de Power y la validación de integración del Líder Técnico deben **aceptar ambos formatos** (el adaptador los soporta) o definir un adaptador/criterio equivalente para los campos `x-ethack`.

**Huecos de cobertura identificados (requieren Power nuevo):** la etapa **Covering Tracks** (Red Team) y los Powers de **detección/hardening del Blue Team** no tienen base existente dedicada; son los únicos que se crean desde cero (el Blue Team puede apoyarse en los logs de `dfir-linux` y en `network-forensics`).

**Regla transversal del proyecto (visible en las tareas):** cada alumno entrega un mínimo de **2 Powers con Herramienta_Real** (Req 9.6, 3.2, 4.2, 5.2, 6.2, 7.2).

**Política de laboratorio (aplica a todas las tareas):** toda actividad se dirige únicamente a objetivos de la `Allowlist_Objetivos`; nunca a producción; la autorización es simulada/didáctica (Req 11.1–11.3, 10.2).

**Reparto de construcción (docente vs alumnos):** El docente crea el `Repositorio_Base` con la estructura inicial y la **línea base** del proyecto: el andamiaje común (estructura de carpetas, modelo de Power, guardia de allowlist, hooks `version: v1`, modelo de datos del engagement — Task 1), el **Agente_Orquestador** y los **5 subagentes de fase** (Tasks 3 y 4), el **esqueleto de los subagentes de rol cableados a los 9 Powers existentes** (6.1, 7.1, 8.1 y el cableado de 10.1/11.1), el **tooling de integración** del Líder Técnico (13.1, 13.2, 13.3) y la **configuración de colaboración/validación local** de la Task 15. El docente deja deliberadamente los **huecos** reportados por el check de cobertura (13.3): la etapa **Covering Tracks** del Red Team y los Powers de **detección/hardening del Blue Team**. A partir de esa línea base, los **alumnos forkean** (topología de tres niveles) y **continúan** con la creación/extensión de Powers por equipo (6.2, 7.2, 8.2/8.4/8.6/8.8 y la extensión de 10.1/11.1), sus property tests y la verificación/validación colectiva (Task 14), culminando en el checkpoint final (Task 16). Este reparto describe quién construye cada pieza; no incluye rúbrica ni criterios de calificación.

> **Nota de ubicación (consolidación).** El código del agente generado por este
> spec vive bajo **`agent_ethack_dfir/`** (`agent_ethack_dfir/agents/`,
> `agent_ethack_dfir/scripts/`, `agent_ethack_dfir/engagements/`). Permanecen en
> la **raíz del repositorio** `powers/` y `.kiro/` (specs + hooks), y los archivos
> de raíz `CODEOWNERS`, `CONTRIBUTING.md`, `Makefile` y `.github/`. Las rutas de
> este plan ya reflejan esa ubicación.

## Tasks

- [x] 1. **[Baseline — Docente]** Establecer la base común del proyecto (estructura, scripts y engagement)
  - [x] 1.1 **[Baseline — Docente]** Crear la estructura de carpetas del proyecto integrado
    - Crear `agent_ethack_dfir/agents/` (con `orquestador/`, `fases/`, `roles/`), `powers/<equipo>/`, `agent_ethack_dfir/scripts/` y `agent_ethack_dfir/engagements/`
    - Añadir un `README.md` por carpeta describiendo su propósito y la convención de integración del Líder Técnico
    - Confirmar que los Powers base (`osint-passive-recon`, `footprinting-enumeration`, `exploitation-metasploit`, `vulnerability-assessment`) quedan referenciados desde `powers/` como cimiento
    - Crear/referenciar los dos Powers base de Digital Forensics como cimiento del equipo DF: `dfir-linux` (forense de host Linux) y `network-forensics` (forense de red), cada uno con `plugin.json` + `skills/<skill>/` (`SKILL.md` + `references/`) + `steering/` por fase; la relación es deriva red→host (`network-forensics` deriva a `dfir-linux` al identificar el host sospechoso)
    - Crear/referenciar el Power base `incident-handling-nist` como cimiento del Incident Responder, que guía el Proceso_Respuesta_Incidentes de cuatro fases de NIST SP 800-61 (Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity) — Req 7.5, 18.1
    - Crear/referenciar el Power base `grc-nist-csf` como cimiento del Responsable de GRC, que guía la gobernanza, el riesgo y el cumplimiento usando NIST CSF 2.0 como eje — Req 6.5, 19.1
    - _Requirements: 9.4, 13.1, 5.8, 6.5, 7.5, 18.1, 19.1_

  - [x] 1.2 **[Baseline — Docente]** Definir el modelo estándar de Power (plantilla `plugin.json` + `x-ethack`), compatible con ambos formatos
    - Crear una plantilla `powers/_template/plugin.json` con el bloque `x-ethack` (`kind`, `ecCouncilPhase`, `forensicsStage`, `team`, `owner`, `tools`, `allowlistValidation`, `producesActionLog`, `executionMode`, `documentation`)
    - Aceptar que los Powers existentes conviven en **dos formatos** (`plugin.json` y `POWER.md`): el modelo estándar define los campos `x-ethack` como contrato lógico y el adaptador de la tarea 1.10 mapea el frontmatter de `POWER.md` a ese mismo contrato, de modo que un Power en cualquiera de los dos formatos pueda validarse con criterios equivalentes — Req 8.2, 9.2
    - Añadir al bloque `x-ethack` el sub-bloque `executionMode` (`param: "Modo_Ejecucion"`, `allowed: [script-kiddie, green-hat, pro]`, `default: "script-kiddie"`) — Req 9.7, 14.1, 14.2
    - Añadir al bloque `x-ethack` el sub-bloque `documentation` (`root`, `required: [prompt.md, sessions/, feedback.md]`) y crear el esqueleto `powers/_template/docs/` con `prompt.md`, `sessions/` y `feedback.md` — Req 9.8, 15.1
    - Implementar `powers/_template/skills/<skill>/execution_mode.py` (`resolve_mode`: default `script-kiddie` para entrada ausente/vacía Req 14.2; `InvalidModeError` para valores fuera de `{script-kiddie, green-hat, pro}` Req 14.7) como utilidad compartida que se resuelve antes de invocar la Herramienta_Real
    - Crear `powers/_template/skills/<skill>/SKILL.md` y `powers/_template/steering/` como esqueleto reutilizable
    - Documentar las reglas del modelo: `tools` no vacío, `ecCouncilPhase` xor `forensicsStage`, `allowlistValidation.required == true`, `executionMode.allowed == {script-kiddie, green-hat, pro}` con default `script-kiddie`, y presencia de los Artefactos_Documentacion bajo `docs/`; estas reglas aplican por igual a Powers `plugin.json` y a Powers `POWER.md` vía el adaptador (1.10)
    - _Requirements: 8.2, 8.4, 9.1, 9.2, 9.3, 9.7, 9.8, 14.1, 14.2, 15.1_

  - [ ]* 1.8 **[Baseline — Docente (opcional)]** Escribir property test de selección/validación/default del Modo_Ejecucion
    - **Property 12: Selección, validación y default del Modo_Ejecucion**
    - **Validates: Requirements 14.1, 14.2, 14.7**
    - Generadores de strings arbitrarios (None/vacíos, variantes de mayúsculas/espacios y los tres valores válidos) sobre `resolve_mode`; verifica default, aceptación normalizada y rechazo con `InvalidModeError`; ≥100 iteraciones

  - [x] 1.3 **[Baseline — Docente]** Implementar la guardia de la Allowlist_Objetivos (`validate_target.py`)
    - Implementar `normalize_target()` (host/IP/URL → forma normalizada; rechazo de credenciales/esquemas no http(s)/IPv6 sin corchetes)
    - Implementar `scope_endpoints()` que resuelve el objetivo al **Contenedor_Objetivo**: construye el conjunto de endpoints válidos a partir de `target_host`/`target_hostname` (más `target_port` cuando aplique) de cada asset e **incluye el host EC2 anfitrión (`ec2_host`/`ec2_hostname`) solo si `host_is_target == true`** — Req 11.4, 12.2, 12.3
    - Implementar `target_in_scope()` y `run_tool_guarded()` que lanza `OutOfScopeError` si el objetivo no resuelve a un Contenedor_Objetivo autorizado (o a un host explícitamente autorizado) de la allowlist
    - Ubicar como utilidad compartida invocable por cada Power antes de ejecutar su Herramienta_Real
    - _Requirements: 9.5, 11.1, 11.2, 11.3, 11.4_

  - [ ]* 1.4 **[Baseline — Docente (opcional)]** Escribir property test de la guardia de allowlist
    - **Property 1: Guardia de alcance de la Allowlist_Objetivos**
    - **Validates: Requirements 9.5, 11.1, 11.2, 11.3, 11.4**
    - Generadores de objetivos (host/IP/URL con variantes de normalización) y de allowlists; incluir endpoints de Contenedor_Objetivo y de host EC2 anfitrión para verificar que el host subyacente queda fuera de alcance salvo `host_is_target == true` (Req 11.4); ≥100 iteraciones

  - [x] 1.5 **[Baseline — Docente]** Implementar los hooks `version: v1` y sus scripts
    - Crear `.kiro/hooks/governance.json` con `PreToolUse → agent_ethack_dfir/scripts/gate_mcp_sim.py` y `PostToolUse → agent_ethack_dfir/scripts/audit_event.py`, matcher `@mcp`
    - Implementar `agent_ethack_dfir/scripts/gate_mcp_sim.py` (variante didáctica no bloqueante: evalúa `EH_GRANT_PATH`, registra en `local-audit/authz.jsonl`, advierte y retorna `exit 0`)
    - Reutilizar/implementar `agent_ethack_dfir/scripts/audit_event.py` (resumen + `sha256` del evento en `local-audit/events.jsonl`) y extenderlo para anotar el campo `mode` con el Modo_Ejecucion aplicado por el Power (`evt["mode"]`/`tool_input.Modo_Ejecucion`, default `script-kiddie` si el evento no lo declara) — Req 14.6
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 14.6_

  - [x] 1.6 **[Baseline — Docente]** Implementar el modelo de datos del engagement
    - Crear `agent_ethack_dfir/engagements/dvwa-lab-ulsa/scope.yaml` (Allowlist_Objetivos, `status`, `authorized_window`, `ethical_principles`, `prohibited_actions`) con nodos EC2 Debian/DVWA de los casos de referencia
    - Modelar cada asset como el **Contenedor_Objetivo** sobre su host EC2 anfitrión: `kind: container`, `service`, `target_host`/`target_hostname`, `target_port`, `container_id`, `container_image`, y el host anfitrión (`ec2_host`/`ec2_hostname`) con `host_is_target: false` salvo autorización explícita — Req 12.1, 12.2, 12.3
    - Reflejar en `assets` el alta/baja de Contenedores_Objetivo o nodos para mantener los objetivos autorizados vigentes como único conjunto válido — Req 12.5, 12.6
    - Crear `state.json` (fase actual + `completed_phases`), `inventory.json` (Powers/agents ↔ fase/etapa ↔ responsable) e inicializar `evidence/`
    - Definir el formato de `evidence/<id>/record.json` (con `sha256`, `volatility_rank` 1–7 RFC 3227, comando/UTC/herramienta/versión/resultado) y `chain_of_custody.jsonl` (eslabones con `prev_sha256`)
    - Definir el registro de incidente `incidents/<id>/incident.json` del Incident Responder (`nist_phase` ∈ las cuatro fases NIST, `phase_history`, IOCs con `format` ∈ `{STIX, YARA, OpenIOC}` y mapeo a MITRE ATT&CK / Cyber Kill Chain, acciones de contención clasificadas `short-term`/`long-term` con `shutdown`/`preserves_evidence`, `escalations`, `evidence_refs`, `csf_subcategories`) y añadir el bloque `incident_response` en `state.json` (`active_incident`, `nist_phase`, `ir_iteration`) — Req 7.6, 7.7, 7.8, 7.9, 18.2, 18.5, 18.7, 18.9, 18.10
    - Definir los artefactos GRC `grc/risk_register.json` (riesgo con probabilidad×impacto, dueño, tratamiento, `residual_score`, `within_appetite`, `csf_subcategory`, `evidence_refs`) y `grc/csf_profile.json` (perfil actual/objetivo, `tier` objetivo 1–4, subcategorías con `gap`, POA&M) ligados al engagement — Req 6.7, 6.8, 6.9, 6.10, 19.3, 19.4, 19.5
    - _Requirements: 6.3, 6.7, 6.8, 6.9, 6.10, 7.6, 7.7, 7.8, 7.9, 11.4, 12.1, 12.2, 12.3, 12.5, 12.6, 13.4, 18.2, 18.5, 18.7, 18.9, 18.10, 19.3, 19.4, 19.5_

  - [ ]* 1.7 **[Baseline — Docente (opcional)]** Escribir property test del round-trip de la Allowlist_Objetivos
    - **Property 11: Round-trip de la Allowlist_Objetivos**
    - **Validates: Requirements 12.3, 12.4**
    - Generadores de secuencias de alta/baja de nodos; agregar y retirar devuelve el estado previo

  - [x] 1.9 **[Baseline — Docente]** Implementar el Catalogador como componente reutilizable (`agent_ethack_dfir/scripts/catalog.py`) y generar la línea base (`inventory.json`)
    - Implementar `agent_ethack_dfir/scripts/catalog.py` con `discover_powers()` y `build_inventory()`: `discover_powers()` **descubre ambos layouts** — Powers base en `powers/<nombre>/` (un nivel) y Powers de alumnos en `powers/<equipo>/<power>/` (dos niveles) — detectando toda carpeta que contenga `plugin.json` o `POWER.md`; `build_inventory()` construye `inventory.json` a partir de lo descubierto
    - Generar con `build_inventory()` la **línea base inicial (baseline)** registrando los 9 Powers ya construidos (`osint-passive-recon`, `footprinting-enumeration`, `vulnerability-assessment`, `exploitation-metasploit`, `dfir-linux`, `network-forensics`, `grc-nist-csf`, `incident-handling-nist`, `incident-response-lab`) como base disponible, no como entregables por crear
    - Para cada Power registrar: formato (`plugin.json` o `POWER.md`), fase EC-Council **o** etapa del Flujo_Investigacion que cubre, rol/equipo responsable, herramientas reales que envuelve y marca de origen (`baseline`/`extended`/`new`, con `baseline: true` para los 9 existentes)
    - Exponer en el inventario los métodos `coverage_gaps()` (huecos de fase EC-Council/etapa del Flujo_Investigacion que la línea base no satisface —Covering Tracks y detección/hardening del Blue Team— anotados con `gap: true` para orientar la creación de Powers nuevos) y `count_tooled_by_owner()` (conteo de Powers con Herramienta_Real por `owner`, para el mínimo de ≥2 por alumno — Req 9.6)
    - El Catalogador es **invocado por `make validate` y `make catalog`** para **regenerar `inventory.json` en cada validación** (no se edita a mano), de modo que el agregador de la Validacion_Local (15.4) reutilice `build_inventory()` y sus métodos en lugar de reimplementarlos
    - _Requirements: 9.4, 9.6, 13.1, 13.2, 13.4_

  - [x] 1.10 **[Baseline — Docente]** Definir el adaptador de convivencia de los dos formatos de Power (`plugin.json` ↔ `POWER.md`)
    - Documentar que coexisten dos formatos de empaquetado: `plugin.json` (estilo agent-plugins.org) y `POWER.md` (frontmatter + "modos de trabajo")
    - Implementar `agent_ethack_dfir/scripts/power_adapter.py` que normaliza ambos formatos a una vista común de los campos `x-ethack` (fase/etapa, `executionMode`, `documentation`, `allowlistValidation`, `tools`, `owner`), extrayéndolos del frontmatter de `POWER.md` cuando no exista `plugin.json`
    - Definir el criterio equivalente de validación para Powers en formato `POWER.md`: los mismos invariantes (`tools` no vacío, `ecCouncilPhase` xor `forensicsStage`, `allowlistValidation.required == true`, `executionMode.allowed == {script-kiddie, green-hat, pro}` con default `script-kiddie`, Artefactos_Documentacion presentes) expresados en su frontmatter o en su sección de modos de trabajo
    - _Requirements: 8.2, 8.4, 9.2, 9.7, 9.8_

  - [x] 1.11 **[Baseline — Docente]** Dotar de bloque `x-ethack` a los 9 Powers base (POWER.md)
    - Añadir al frontmatter YAML de cada uno de los 9 `POWER.md` base (`osint-passive-recon`, `footprinting-enumeration`, `vulnerability-assessment`, `exploitation-metasploit`, `dfir-linux`, `network-forensics`, `grc-nist-csf`, `incident-handling-nist`, `incident-response-lab`) un bloque `x-ethack` con los campos del contrato (`kind`, `ecCouncilPhase` xor `forensicsStage`, `team`, `owner`, `tools`, `allowlistValidation.required == true` con `source` al `scope.yaml`, `executionMode {allowed: [script-kiddie, green-hat, pro], default: script-kiddie}`, `documentation {root, required: [prompt.md, sessions/, feedback.md]}`), usando el mapeo de rol/fase del Catalogador (`agent_ethack_dfir/scripts/catalog.py` `BASELINE_KNOWLEDGE`) como fuente de verdad. Edición puramente **ADITIVA** al frontmatter: no alterar el resto del contenido del `POWER.md`
    - Tras dotarlos de `x-ethack`, regenerar `inventory.json` con el Catalogador (`make catalog` / `build_inventory`) para que queden con `xethack_declared == true`, y verificar con `power_adapter.validate_power` que los 9 pasan el contrato (o reportan solo docs faltantes)
    - _Requirements: 8.2, 9.1, 9.2, 9.5, 9.7, 9.8, 13.4_

- [ ] 2. **[Baseline — Docente]** Checkpoint — Validar la base común
  - Asegurar que todas las pruebas pasen; preguntar al usuario si surgen dudas.

- [x] 3. **[Baseline — Docente]** Implementar el Agente_Orquestador (custom agent)
  - [x] 3.1 **[Baseline — Docente]** Crear el custom agent `agent_ethack_dfir/agents/orquestador/` y su lógica de fases
    - Definir el agente que expone las 5 fases EC-Council como etapas seleccionables y aplica los Principios_Eticos como restricciones de comportamiento
    - Implementar la secuencia canónica por defecto Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks leyendo/escribiendo `state.json`
    - Identificar en la respuesta cada subagente invocado y la fase/rol que representa
    - _Requirements: 1.1, 1.2, 1.3, 1.6, 11.4_

  - [x] 3.2 **[Baseline — Docente]** Implementar la lógica de orden y consolidación
    - Calcular la fase "siguiente" por defecto y, ante una fase fuera de orden, reportar las fases previas no completadas antes de delegar
    - Consolidar los resultados de una fase antes de ofrecer la transición a la siguiente
    - _Requirements: 1.4, 1.5_

  - [ ]* 3.3 **[Baseline — Docente (opcional)]** Escribir property test de la secuencia canónica de fases
    - **Property 2: Secuencia canónica de fases por defecto**
    - **Validates: Requirements 1.3**

  - [ ]* 3.4 **[Baseline — Docente (opcional)]** Escribir property test del reporte de fases previas no completadas
    - **Property 3: Reporte de fases previas no completadas**
    - **Validates: Requirements 1.5**

- [x] 4. **[Baseline — Docente]** Implementar los 5 subagentes de fase (custom agents)
  - [x] 4.1 **[Baseline — Docente]** Crear subagente Reconnaissance
    - Custom agent en `agent_ethack_dfir/agents/fases/` que declara objetivo y alcance antes de invocar herramientas y usa ≥1 Power de reconocimiento (OSINT pasivo / footprinting)
    - _Requirements: 2.1, 2.2, 2.7_

  - [x] 4.2 **[Baseline — Docente]** Crear subagente Scanning
    - Custom agent que usa ≥1 Power de descubrimiento/enumeración de puertos y servicios sobre objetivos de la Allowlist_Objetivos
    - _Requirements: 2.1, 2.3, 2.7_

  - [x] 4.3 **[Baseline — Docente]** Crear subagente Gaining Access
    - Custom agent que usa ≥1 Power de evaluación de vulnerabilidades o explotación PoC limitada contra el Entorno_Laboratorio
    - _Requirements: 2.1, 2.4, 2.7_

  - [x] 4.4 **[Baseline — Docente]** Crear subagente Maintaining Access
    - Custom agent que usa ≥1 Power de persistencia/sesiones acotado al Entorno_Laboratorio
    - _Requirements: 2.1, 2.5, 2.7_

  - [x] 4.5 **[Baseline — Docente]** Crear subagente Covering Tracks
    - Custom agent que usa ≥1 Power de análisis/manipulación de rastros acotado al lab y registra todas las acciones para trazabilidad
    - _Requirements: 2.1, 2.6, 2.7_

  - [ ]* 4.6 **[Baseline — Docente (opcional)]** Escribir property test de declaración de alcance previa a la herramienta
    - **Property 4: Declaración de alcance precede a la herramienta**
    - **Validates: Requirements 2.7**

- [ ] 5. **[Baseline — Docente]** Checkpoint — Validar orquestador y subagentes de fase
  - Asegurar que todas las pruebas pasen; preguntar al usuario si surgen dudas.

- [ ] 6. Implementar el subagente y los Powers del Red Team (3 alumnos)
  - [x] 6.1 **[Baseline — Docente]** Crear el subagente de rol Red Team
    - Custom agent `agent_ethack_dfir/agents/roles/red-team/` que agrupa los Powers ofensivos de las 5 fases
    - _Requirements: 3.1_

  - [ ] 6.2 **[Alumnos]** Reutilizar/extender los Powers ofensivos del Red Team y crear solo el hueco (≥2 por alumno, 3 alumnos)
    - **Reutilizar como base existente** (no recrear): `osint-passive-recon` (Reconnaissance), `footprinting-enumeration` (Reconnaissance + Scanning), `vulnerability-assessment` (Scanning / Gaining Access) y `exploitation-metasploit` (Gaining Access / Maintaining Access); los alumnos los **extienden/parametrizan** (modos de ejecución, allowlist de contenedor, nuevos skills/steering) en lugar de empezar de cero
    - **Crear Power nuevo solo para el hueco de Covering Tracks** (análisis/manipulación de rastros acotado al lab), que no tiene base existente
    - Completar la cobertura con herramientas reales donde falte (nmap, Metasploit/msfvenom, nikto/Nuclei, sqlmap, Hydra, persistencia, análisis de rastros)
    - La regla de ≥2 Powers con Herramienta_Real por alumno puede cumplirse combinando Powers base **extendidos** y Powers **nuevos**
    - Cada Power (reutilizado o nuevo) valida el objetivo contra la Allowlist_Objetivos antes de ejecutar y produce un registro de acción consumible por Blue Team y Digital Forensics
    - Cada Power implementa los tres Modo_Ejecucion: `script-kiddie` (comandos predefinidos, default), `green-hat` (ejecuta y explica la lógica subyacente) y `pro` (lógica propia, puede generar scripts acotados al lab); resuelve el modo con `resolve_mode` y registra el modo aplicado para el Hook_Auditoria — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power entrega sus Artefactos_Documentacion bajo `docs/` (prompt de generación, sesiones de prueba con Kiro, realimentación al chat del Power) — Req 15.1, 15.2, 15.3, 15.4
    - **Regla transversal: mínimo 2 Powers con Herramienta_Real por cada integrante (Req 3.2, 9.6)**
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 9.1, 9.5, 9.7, 9.8, 14.3, 14.4, 14.5, 14.6, 15.1_

- [ ] 7. Implementar el subagente y los Powers del Blue Team (3 alumnos)
  - [x] 7.1 **[Baseline — Docente]** Crear el subagente de rol Blue Team
    - Custom agent `agent_ethack_dfir/agents/roles/blue-team/` para detección, análisis de logs y hardening
    - _Requirements: 4.1_

  - [ ] 7.2 **[Alumnos]** Crear los Powers de detección/defensa del Blue Team — hueco de cobertura (≥2 por alumno, 3 alumnos)
    - **Hueco identificado:** no existe Power base dedicado de detección/hardening; los alumnos **crean Powers nuevos desde cero**, pudiendo apoyarse en los logs producidos por `dfir-linux` y en `network-forensics` como insumo de datos
    - Powers de análisis de logs capaces de detectar la actividad registrada por el Red Team y de producir un hallazgo de detección con su evidencia de sustento
    - Powers de hardening del Entorno_Laboratorio
    - Cada Power implementa los tres Modo_Ejecucion: `script-kiddie` (comandos predefinidos, default), `green-hat` (ejecuta y explica la lógica subyacente) y `pro` (lógica propia, puede generar scripts acotados al lab); resuelve el modo con `resolve_mode` y registra el modo aplicado para el Hook_Auditoria — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power entrega sus Artefactos_Documentacion bajo `docs/` (prompt de generación, sesiones de prueba con Kiro, realimentación al chat del Power) — Req 15.1, 15.2, 15.3, 15.4
    - **Regla transversal: mínimo 2 Powers con Herramienta_Real por cada integrante (Req 4.2, 9.6)**
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 9.1, 9.5, 9.7, 9.8, 14.3, 14.4, 14.5, 14.6, 15.1_

- [ ] 8. Implementar el subagente y los Powers de Digital Forensics (4 alumnos)
  - [x] 8.1 **[Baseline — Docente]** Crear el subagente de rol Digital Forensics sobre los Powers base existentes
    - Custom agent `agent_ethack_dfir/agents/roles/digital-forensics/` que implementa el Flujo_Investigacion Detect → Isolate → Collect → Preserve → Analyze → Report
    - **Reutilizar como base existente** (no recrear): `dfir-linux` (forense de host Linux) y `network-forensics` (forense de red), con la relación de deriva red→host; los 4 alumnos **extienden/añaden** Powers sobre esta base para cubrir las 6 etapas del Flujo_Investigacion y cumplir el mínimo de ≥2 Powers con Herramienta_Real por alumno
    - _Requirements: 5.1_

  - [ ] 8.2 **[Alumnos]** Extender los Powers de recolección y preservación (Collect/Preserve) sobre `dfir-linux`/`network-forensics`
    - **Extender la base existente** (`dfir-linux` para adquisición de host, `network-forensics` para captura de red) en lugar de recrearla; añadir Powers nuevos solo donde la base no cubra la etapa
    - Powers de adquisición (dd/dc3dd/dcfldd, LiME/AVML, tcpdump, snapshot EBS) que calculan y registran el `sha256` de la evidencia en `record.json`
    - La recolección en la fase Collect respeta el **Orden_Volatilidad** (RFC 3227): recolectar primero lo más volátil (registros/caché → RAM → estado de red → procesos) y después lo menos volátil (disco → logs remotos → respaldo), fijando `volatility_rank` 1–7 por pieza — Req 5.6, 16.1
    - Para evidencia que reside en un Contenedor_Objetivo, tratarla como **evidencia efímera** y recolectarla mediante un procedimiento automatizado (snapshot + hash + copia al almacén forense) que preserve su integridad antes de que el contenedor desaparezca — Req 5.9, 16.8
    - Preservación en almacén solo-anexado / escritura única (S3 Object Lock) y arranque de la Cadena_Custodia (eslabón `seq 0`)
    - Cada Power implementa los tres Modo_Ejecucion (`script-kiddie` default, `green-hat` explica, `pro` lógica propia/scripts acotados al lab), resuelve con `resolve_mode` y registra el modo aplicado — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power entrega sus Artefactos_Documentacion bajo `docs/` (prompt, sesiones de prueba con Kiro, realimentación al chat) — Req 15.1, 15.2, 15.3, 15.4
    - _Requirements: 5.1, 5.3, 5.4, 5.6, 5.9, 9.5, 9.7, 9.8, 14.3, 14.4, 14.5, 14.6, 15.1, 16.1, 16.8_

  - [ ]* 8.3 **[Alumnos (opcional)]** Escribir property test del hash de verificación de evidencia
    - **Property 5: Hash de verificación de evidencia recolectada**
    - **Validates: Requirements 5.3**

  - [ ] 8.4 **[Alumnos]** Extender los Powers de análisis sin alteración (Detect/Isolate/Analyze) sobre la base existente
    - **Reutilizar/extender** las capacidades de triage y análisis de `dfir-linux` (host) y `network-forensics` (red); crear Powers nuevos solo para herramientas/etapas no cubiertas por la base
    - Limitar el alcance del análisis a **Linux y nube (AWS)**; si el host sospechoso es **Windows**, marcarlo **fuera de alcance** en vez de analizarlo — Req 5.7
    - Powers de triage/aislamiento y de análisis con las herramientas del proceso formal: **Volatility** (`linux.pslist`/`pstree`/`bash`/`sockstat`/`malfind`/`check_modules`), **Autopsy**/**TSK** (disco), **Plaso**/log2timeline (línea de tiempo), **Athena**/CloudTrail (logs de nube) y, para red, **Snort**/**Suricata**/**Wireshark**; todos operan sobre copias y verifican `hash_pre == hash_post` del original
    - Cada Power implementa los tres Modo_Ejecucion (`script-kiddie` default, `green-hat` explica, `pro` lógica propia/scripts acotados al lab), resuelve con `resolve_mode` y registra el modo aplicado — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power entrega sus Artefactos_Documentacion bajo `docs/` (prompt, sesiones de prueba con Kiro, realimentación al chat) — Req 15.1, 15.2, 15.3, 15.4
    - _Requirements: 5.1, 5.5, 5.7, 9.7, 9.8, 14.3, 14.4, 14.5, 14.6, 15.1_

  - [ ]* 8.5 **[Alumnos (opcional)]** Escribir property test de no alteración de la evidencia original
    - **Property 6: No alteración de la evidencia original**
    - **Validates: Requirements 5.5**

  - [ ] 8.6 **[Alumnos]** Implementar la Cadena_Custodia y el Power de reporte (Report)
    - Encadenar cada traspaso/transformación en `chain_of_custody.jsonl` (`seq > 0` referencia `prev_sha256`)
    - Power de reporte forense que renderiza hallazgos + `record.json` + `chain_of_custody.jsonl`
    - El Power de reporte implementa los tres Modo_Ejecucion (`script-kiddie` default, `green-hat` explica, `pro` lógica propia/scripts acotados al lab), resuelve con `resolve_mode` y registra el modo aplicado — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power entrega sus Artefactos_Documentacion bajo `docs/` (prompt, sesiones de prueba con Kiro, realimentación al chat) — Req 15.1, 15.2, 15.3, 15.4
    - **Regla transversal: mínimo 2 Powers con Herramienta_Real por cada integrante (Req 5.2, 9.6)**
    - _Requirements: 5.1, 5.2, 5.4, 5.10, 9.7, 9.8, 13.5, 14.3, 14.4, 14.5, 14.6, 15.1_

  - [ ]* 8.7 **[Alumnos (opcional)]** Escribir property test del encadenamiento de la Cadena_Custodia
    - **Property 7: Encadenamiento de la Cadena_Custodia**
    - **Validates: Requirements 5.4, 5.10, 16.3**

  - [ ] 8.8 **[Alumnos]** Aplicar los Principios_Forenses transversales como invariantes del equipo DF
    - Implementar los siete Principios_Forenses (7 principios; Documentation y Reproducibility se verifican juntas) como invariantes verificables en todas las fases del Flujo_Investigacion: **Evidence Integrity** (análisis sobre copia verificada por hash), **Chain of Custody** (registro de cada traspaso/ubicación), **Documentation/Reproducibility** (por cada paso: comando, hora UTC, herramienta, versión y resultado en `record.json`), **Minimization** (solo la evidencia necesaria para el alcance), **Objectivity** (registrar también la evidencia que contradice la hipótesis), **Legal Admissibility** (preservación con hash y almacenamiento de escritura única)
    - Cablear estos invariantes en los Powers de Collect/Preserve/Analyze/Report (8.2, 8.4, 8.6) y en el `record.json`/`chain_of_custody.jsonl` del modelo de datos
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8_

  - [ ]* 8.9 **[Alumnos (opcional)]** Escribir property test del Orden_Volatilidad en la fase Collect
    - **Property 14: Orden_Volatilidad en la fase Collect**
    - **Validates: Requirements 5.6, 16.1**
    - Generadores de conjuntos de evidencia con `volatility_rank` (1–7) y tiempos de recolección; verifica que la serie de `volatility_rank` en orden de recolección (`collected_at_utc`) es monótona no decreciente (RFC 3227); ≥100 iteraciones

  - [ ]* 8.10 **[Alumnos (opcional)]** Escribir property test de Evidence Integrity (análisis sobre copia verificada)
    - **Property 15: Evidence Integrity — análisis sobre copia verificada**
    - **Validates: Requirements 5.5, 16.2**
    - Generadores de evidencia original + copia; verifica `hash(copia) == record.sha256` y que el original permanece intacto tras la operación de análisis (complementa la Property 6); ≥100 iteraciones

- [ ] 9. Checkpoint — Validar Red/Blue/Digital Forensics
  - Asegurar que todas las pruebas pasen; preguntar al usuario si surgen dudas.

- [ ] 10. Implementar el subagente y los Powers de GRC (1 alumno)
  - [-] 10.1 **[Baseline — Docente (cableado) / Alumnos (extensión)]** Crear el subagente de rol GRC y sus artefactos de gobernanza (NIST CSF 2.0)
    - Custom agent `agent_ethack_dfir/agents/roles/grc/` que **reutiliza/extiende el Power base existente `grc-nist-csf`** (no lo recrea) con Powers/artefactos de autorización, definición de alcance, cumplimiento ético y Cadena_Custodia
    - Mantener la Allowlist_Objetivos (`scope.yaml`) como registro de objetivos autorizados y registrar alcance + Principios_Eticos al definir un engagement
    - Usar NIST CSF 2.0 como lenguaje común y mapear cada requisito (ley/contrato/norma/política) → subcategoría CSF → control → evidencia — Req 6.6, 19.2
    - Mantener el Registro_Riesgos (`grc/risk_register.json`) con probabilidad×impacto, dueño, opción de tratamiento (mitigar/transferir/aceptar/evitar) y riesgo residual por método estandarizado (GV.RM-06), verificando que el residual queda dentro del Apetito_Riesgo — Req 6.7, 6.8, 19.3
    - Producir el Perfil_CSF (`grc/csf_profile.json`) con perfil actual y objetivo (Tier 1–4) → gap analysis → POA&M; cada brecha genera además un riesgo en el Registro_Riesgos — Req 6.9, 19.4, 19.5
    - Vincular los hallazgos técnicos de Red/Blue/DF/VA a subcategorías CSF como evidencia para la segunda y tercera línea del Modelo_Tres_Lineas — Req 6.10, 19.6
    - Cada Power/artefacto implementa los tres Modo_Ejecucion (`script-kiddie` default, `green-hat` explica, `pro` lógica propia acotada al lab), resuelve con `resolve_mode` y registra el modo aplicado — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power/artefacto entrega sus Artefactos_Documentacion bajo `docs/` (prompt, sesiones de prueba con Kiro, realimentación al chat) — Req 15.1, 15.2, 15.3, 15.4
    - **Regla transversal: mínimo 2 Powers con herramientas/artefactos verificables (Req 6.2, 9.6)**
    - Docente: cablea el subagente al Power base existente. Alumnos (GRC/IR): completan los ≥2 Powers, artefactos y población de datos.
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 9.7, 9.8, 14.3, 14.4, 14.5, 14.6, 15.1, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6_

  - [ ]* 10.2 **[Alumnos (opcional)]** Escribir property test de la invariante GRC (riesgo residual y cobertura del POA&M)
    - **Property 17: Invariante GRC — riesgo residual dentro del apetito y cobertura del POA&M**
    - **Validates: Requirements 6.8, 6.9, 19.4, 19.5**
    - Generadores de Registro_Riesgos (scores residuales y `max_residual_score`) y de Perfil_CSF (subcategorías con/sin `gap`); verifica `within_appetite == (residual_score <= max_residual_score)` y que el conjunto de subcategorías del POA&M es exactamente el conjunto con `gap == true`; ≥100 iteraciones

- [ ] 11. Implementar el subagente y los Powers del Incident Responder (1 alumno)
  - [-] 11.1 **[Baseline — Docente (cableado) / Alumnos (extensión)]** Crear el subagente de rol Incident Responder (puente detección↔forense, NIST SP 800-61)
    - Custom agent `agent_ethack_dfir/agents/roles/incident-responder/` que **reutiliza/extiende los Powers base existentes** (no los recrea): `incident-handling-nist` (metodología NIST SP 800-61, Cyber Kill Chain, MITRE ATT&CK, cadena de custodia, playbooks) e `incident-response-lab` (lab con TheHive, VirusTotal, Wazuh, Sysmon/PowerShell); con Powers que vinculan los hallazgos del Blue Team con el Flujo_Investigacion del DF
    - Operar según las cuatro fases del Proceso_Respuesta_Incidentes NIST SP 800-61 (Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity) de forma cíclica e iterativa: Detection & Analysis y Containment/Eradication/Recovery se recorren en bucle y las lecciones de Post-Incident retroalimentan Preparation, actualizando `nist_phase`/`phase_history` en `incident.json` — Req 7.6, 18.2, 18.3, 18.4, 18.5, 18.6, 18.7
    - Power que inicia contención/respuesta acotada al lab ante un hallazgo, distinguiendo Contencion_Corto_Plazo (aísla el Contenedor_Objetivo sin apagar, `shutdown == false`, preserva evidencia) vs Contencion_Largo_Plazo (cambios persistentes); registra la acción y notifica al DF para recolección de evidencia — Req 7.3, 7.4, 7.7, 18.8
    - Mantener los IOCs del incidente en al menos uno de los formatos STIX/YARA/OpenIOC con su mapeo a tácticas/técnicas de MITRE ATT&CK y a etapas de la Cyber Kill Chain, y la Cadena_Custodia de la evidencia asociada — Req 7.8, 18.9, 18.10
    - Coordinarse con el Blue Team para datos de detección y con el DF para recolección/preservación; escalar y registrar el escalamiento ante movimiento lateral hacia otro sistema/departamento — Req 7.9, 18.8, 18.11
    - Cada Power implementa los tres Modo_Ejecucion (`script-kiddie` default, `green-hat` explica, `pro` lógica propia/scripts acotados al lab), resuelve con `resolve_mode` y registra el modo aplicado — Req 14.3, 14.4, 14.5, 14.6
    - Cada Power entrega sus Artefactos_Documentacion bajo `docs/` (prompt, sesiones de prueba con Kiro, realimentación al chat) — Req 15.1, 15.2, 15.3, 15.4
    - **Regla transversal: mínimo 2 Powers con Herramienta_Real (Req 7.2, 9.6)**
    - Docente: cablea el subagente al Power base existente. Alumnos (GRC/IR): completan los ≥2 Powers, artefactos y población de datos.
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 9.7, 9.8, 14.3, 14.4, 14.5, 14.6, 15.1, 18.1, 18.2, 18.3, 18.4, 18.5, 18.6, 18.7, 18.8, 18.9, 18.10, 18.11_

  - [ ]* 11.2 **[Alumnos (opcional)]** Escribir property test de clasificación de contención y ciclicidad de fases
    - **Property 16: Clasificación de contención y ciclicidad del Proceso_Respuesta_Incidentes**
    - **Validates: Requirements 7.7, 18.2, 18.5, 18.7**
    - Generadores de registros de incidente con acciones de contención (`short-term`/`long-term`) y secuencias de transición de fase; verifica que toda acción `short-term` cumple `shutdown == false` y `preserves_evidence == true`, que toda fase destino pertenece a las cuatro fases NIST y que el grafo admite el retorno Post-Incident→Preparation y Recovery→Detection & Analysis (ciclicidad/iteración); ≥100 iteraciones

- [x] 12. Implementar los hooks de autorización y auditoría a nivel de invocación
  - [x] 12.1 **[Baseline — Docente]** Cablear la evaluación del Hook_Autorizacion
    - Asegurar que `gate_mcp_sim.py` identifica herramienta y objetivo declarados y que la decisión "autorizada" se cumple sii grant aprobado, no caducado, herramienta en `allowed_tools` y objetivo en sus `targets`
    - _Requirements: 10.1, 10.2, 10.3_

  - [ ]* 12.2 **[Alumnos (opcional)]** Escribir property test de la decisión del Hook_Autorizacion
    - **Property 8: Decisión del Hook_Autorizacion**
    - **Validates: Requirements 10.1, 10.3**

  - [ ]* 12.3 **[Alumnos (opcional)]** Escribir property test del round-trip del hash de auditoría
    - **Property 9: Round-trip del hash de auditoría**
    - **Validates: Requirements 10.4**

- [x] 13. Integración del Líder Técnico y verificación de cobertura
  - [x] 13.1 **[Baseline — Docente]** Implementar la incorporación de Powers al inventario (acepta ambos formatos)
    - Script/flujo que valida un entregable contra el modelo de Powers aceptando **los dos formatos** vía el adaptador de la tarea 1.10: para `plugin.json` valida el esquema + `x-ethack`; para `POWER.md` valida los campos equivalentes extraídos del frontmatter / sección de modos de trabajo
    - Criterios equivalentes en ambos formatos: `x-ethack` presente (o su equivalente), `tools` no vacío, `ecCouncilPhase` xor `forensicsStage`, `allowlistValidation.required == true`, `executionMode.allowed == {script-kiddie, green-hat, pro}` con default `script-kiddie`
    - Implementar `agent_ethack_dfir/scripts/check_power_docs.py` que calcula `docStatus` del Power (presencia de `docs/prompt.md`, `docs/sessions/`, `docs/feedback.md`; `complete` y lista `missing`) y señala los artefactos faltantes al integrar — Req 15.6
    - Si cumple, registra el Power en `inventory.json` (formato, fase/etapa, subagente invocador, responsable, `executionModes`, `docStatus` y marca `baseline`/`extended`/`new`); para Powers existentes reutilizados actualiza su entrada de línea base en lugar de duplicarla; si faltan artefactos la integración procede marcada como documentación incompleta — Req 15.5, 15.6
    - Si no cumple el modelo (en cualquiera de los dos formatos) o la política ética, rechaza la integración e indica el incumplimiento (no se añade al inventario)
    - _Requirements: 8.1, 8.2, 8.4, 9.2, 13.2, 13.4, 15.5, 15.6_

  - [ ]* 13.5 **[Alumnos (opcional)]** Escribir property test de completitud de los Artefactos_Documentacion al integrar
    - **Property 13: Completitud de los Artefactos_Documentacion al integrar**
    - **Validates: Requirements 15.1, 15.6**
    - Generadores de subconjuntos de `{prompt.md, sessions/, feedback.md}` sobre `doc_status`/`check_power_docs.py`; verifica `complete` sii están los tres y que `missing` es exactamente el complemento de los presentes; ≥100 iteraciones

  - [x] 13.2 **[Baseline — Docente]** Implementar la habilitación de fases por cobertura
    - Cuando todos los entregables de una fase están integrados, habilitar esa fase en el Agente_Orquestador
    - Vincular reportes/artefactos de gobernanza o forenses con el engagement y su Cadena_Custodia
    - _Requirements: 8.3, 13.3, 13.5_

  - [x] 13.3 **[Baseline — Docente]** Implementar el check de cobertura de fases y etapas forenses
    - **Verifica** la cobertura consumiendo `coverage_gaps()` del inventario/Catalogador (tarea 1.9); confirma ≥1 Power por cada una de las 5 fases EC-Council y por cada una de las 6 etapas del Flujo_Investigacion y falla indicando los huecos. No reimplementa el descubrimiento ni el cálculo de cobertura (reside en el Catalogador)
    - **Contar tanto los Powers existentes reutilizados (`baseline`/`extended`) como los nuevos (`new`)**: la cobertura de una fase/etapa puede satisfacerse con un Power base ya presente (p. ej. Reconnaissance con `osint-passive-recon`/`footprinting-enumeration`, Scanning con `footprinting-enumeration`/`vulnerability-assessment`, Gaining/Maintaining con `exploitation-metasploit`, etapas forenses con `dfir-linux`/`network-forensics`)
    - **Marcar explícitamente los huecos que requieren Power nuevo**: Covering Tracks (Red Team) y detección/hardening del Blue Team; reportarlos como pendientes hasta que exista un Power nuevo que los cubra
    - Confirmar que todo Power del inventario declara responsable (equipo/alumno)
    - _Requirements: 8.3, 13.2, 13.4_

  - [ ]* 13.4 **[Alumnos (opcional)]** Escribir property test de la cobertura del inventario de entregables
    - **Property 10: Cobertura del inventario de entregables**
    - **Validates: Requirements 8.3, 13.2, 13.4**

- [ ] 14. Verificación estructural y de integración (no PBT)
  - [ ]* 14.1 **[Alumnos (opcional)]** Validar el esquema de Powers de cada entregable
    - Casos de ejemplo y edge cases sobre `plugin.json`/`x-ethack` (herramientas no vacías, fase xor etapa, allowlist requerida)
    - _Requirements: 9.1, 9.2_

  - [ ]* 14.2 **[Alumnos (opcional)]** Verificar el conteo de ≥2 Powers con Herramienta_Real por alumno
    - **Verifica** el conteo consumiendo `count_tooled_by_owner()` del inventario/Catalogador (tarea 1.9) y confirma el mínimo por integrante; no reimplementa el conteo (reside en el Catalogador)
    - **Contar tanto Powers base extendidos (`baseline`/`extended`) como Powers nuevos (`new`)**: el mínimo de ≥2 puede cumplirse combinando reutilización/extensión y creación, siempre que cada Power contado envuelva una Herramienta_Real
    - _Requirements: 3.2, 4.2, 5.2, 6.2, 7.2, 9.6_

  - [ ]* 14.3 **[Alumnos (opcional)]** Verificar el comportamiento no bloqueante del hook y el formato `version: v1`
    - Prueba de ejemplo: evento sin grant que cubra el objetivo → advertencia y `exit 0` (no aborta)
    - Validar que `.kiro/hooks/*.json` declara `version: v1` y triggers válidos
    - _Requirements: 10.2, 10.5_

  - [ ]* 14.4 **[Alumnos (opcional)]** Verificar los flujos cruzados Red → Blue → IR → DF
    - Pruebas de integración (1–3 ejemplos): acción ofensiva genera registro → Blue Team detecta → IR contiene y notifica → DF recolecta
    - _Requirements: 3.4, 4.3, 7.3, 7.4_

  - [ ]* 14.5 **[Alumnos (opcional)]** Verificar el comportamiento por Modo_Ejecucion y su registro en auditoría
    - Pruebas de ejemplo (cualitativas, no PBT): `script-kiddie` solo comandos predefinidos; `green-hat` incluye explicación de la lógica subyacente en la salida; `pro` puede emitir agent_ethack_dfir/scripts/comandos propios acotados al lab
    - Ejemplo del registro: un evento con `Modo_Ejecucion` produce un record de auditoría con el campo `mode` correspondiente (o `script-kiddie` por defecto)
    - _Requirements: 14.3, 14.4, 14.5, 14.6_

  - [ ]* 14.6 **[Alumnos (opcional)]** Verificar la asociación estructural de los Artefactos_Documentacion
    - Verificación estructural: `docs/` reside dentro del árbol del Power y el `owner` consta en `inventory.json`; `docStatus.missing` lista los artefactos ausentes al integrar
    - _Requirements: 15.5, 15.6_

  - [ ]* 14.7 **[Alumnos — validación colectiva]** Verificar el escenario GameDay breach-to-solution end-to-end (validación funcional)
    - Prueba de integración de alto nivel (por ejemplo/escenario, no PBT ni rúbrica): un incidente activo simulado recorre el sistema de principio a fin
    - El Agente_Orquestador coordina los Subagentes_Rol (Red Team → Blue Team → Incident Responder → Digital Forensics → GRC) e identifica cada subagente invocado y el rol que representa — Req 17.1, 17.2
    - La evidencia se preserva aplicando Evidence Integrity y Chain of Custody conforme al Req 16 (apoyada en las Properties 14, 15, 6 y 7) — Req 17.3
    - Se rastrean los IOCs mediante análisis de logs con el mapeo kill-chain → evidencia en AWS (Athena/CloudTrail sobre `event_history`, correlación con `dfir-linux`/`network-forensics`) — Req 17.4
    - Se aplica contención y hardening de la infraestructura manteniendo disponibles los servicios afectados (aislar no es apagar: sin apagar hosts ni dar de baja servicios) — Req 17.5
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 17.6_

  - [ ]* 14.8 **[Alumnos (opcional)]** Verificar el mapeo IOC→MITRE/kill-chain y la alineación CSF RS.*/RC.* ↔ fases NIST
    - Prueba de ejemplo (estructural): cada IOC de `incident.json` declara `format` ∈ `{STIX, YARA, OpenIOC}` y referencia una táctica/técnica de MITRE ATT&CK y una etapa de la Cyber Kill Chain — Req 18.9, 18.10
    - Prueba de ejemplo (estructural): el `incident.json` es coherente con el flujo cruzado Red → Blue → IR → DF y ejercitable dentro del GameDay — Req 18.11
    - Prueba de ejemplo (estructural): las subcategorías de las funciones RS (Respond) y RC (Recover) del Perfil_CSF se alinean con las fases del Proceso_Respuesta_Incidentes del Power `incident-handling-nist` — Req 19.7
    - _Requirements: 18.9, 18.10, 18.11, 19.7_

- [x] 15. **[Baseline — Docente]** Configurar la colaboración por GitHub (fork + PR) y la validación local
  - [x] 15.1 **[Baseline — Docente]** Documentar el flujo de colaboración de tres niveles y la sincronización upstream
    - Crear `CONTRIBUTING.md` que describa la topología de tres niveles: `Repositorio_Base` del docente (upstream) → `Repositorio_Integracion` del Líder Técnico (fork del base) → `Fork_Alumno` (fork del de integración)
    - Documentar que el alumno trabaja en una rama propia con el patrón `power/<equipo>-<iniciales>-<nombre-power>` y nunca sobre la rama base/de partida, y que contribuye exclusivamente por Pull Request desde su `Fork_Alumno` (sin escritura directa sobre el `Repositorio_Integracion`)
    - Documentar los pasos de sincronización upstream en los dos sentidos: el Líder Técnico sincroniza el `Repositorio_Integracion` desde el `Repositorio_Base` del docente, y el alumno sincroniza su `Fork_Alumno` desde el `Repositorio_Integracion`
    - _Requirements: 20.1, 20.2, 20.3, 20.10_

  - [x] 15.2 **[Baseline — Docente]** Crear el `CODEOWNERS` y la estructura de carpetas por equipo
    - Crear el archivo `CODEOWNERS` que asigne cada ruta `powers/<equipo>/<power>/` a su alumno/equipo responsable, de modo que cada contribución quede atribuida a su dueño
    - Asignar las rutas compartidas (`agent_ethack_dfir/agents/orquestador/`, `agent_ethack_dfir/scripts/`, `agent_ethack_dfir/engagements/`) al Líder Técnico para evitar escrituras no coordinadas sobre archivos comunes
    - Dejar establecida la estructura de carpetas `powers/<equipo>/` que respalda esta propiedad por ruta
    - _Requirements: 20.4_

  - [x] 15.3 **[Baseline — Docente]** Definir el contrato y la plantilla de Pull Request de entrega
    - Crear `.github/pull_request_template.md` (o equivalente) con el contrato de entrega de un Power: el PR trae el Power (`plugin.json` o `POWER.md` con el contrato `x-ethack`), sus directorios `skills/` y `steering/` y sus Artefactos_Documentacion bajo `docs/` (`prompt.md`, `sessions/`, `feedback.md`) del Req 15
    - Incluir un checklist de entrega que exija la Validacion_Local en verde antes de abrir el PR, la ubicación del Power en `powers/<equipo>/<power>/` y la rama `power/<equipo>-<iniciales>-<nombre-power>`
    - _Requirements: 20.5_

  - [x] 15.4 **[Baseline — Docente]** Implementar el punto de entrada único de la Validacion_Local (sin CI remota)
    - Implementar `agent_ethack_dfir/scripts/validate_all.py` y un `Makefile` con el objetivo `validate` como único punto de entrada que **encadena los componentes ya existentes** (no los reimplementa): `agent_ethack_dfir/scripts/power_adapter.py` para normalizar ambos formatos `plugin.json`/`POWER.md` (tarea 1.10), `agent_ethack_dfir/scripts/check_power_docs.py`/`docStatus` para los Artefactos_Documentacion (13.1) y la guardia de la Allowlist_Objetivos `validate_target.py` (1.3)
    - **Invocar `build_inventory()` del Catalogador (tarea 1.9)** para regenerar `inventory.json` (también expuesto como `make catalog`) y usar sus métodos `coverage_gaps()` (cobertura de fases EC-Council/etapas del Flujo_Investigacion) y `count_tooled_by_owner()` (conteo de ≥2 Powers con Herramienta_Real por alumno); la cobertura y el conteo se obtienen del propio inventario/Catalogador, **sin depender de las tareas de test opcionales 13.3/14.2** (esas solo verifican la lógica aquí reutilizada)
    - No depender de GitHub Actions ni de ningún servicio de integración continua remoto: toda comprobación corre localmente
    - _Requirements: 20.6, 20.8, 20.9, 20.11_

  - [x] 15.5 **[Baseline — Docente]** Definir el protocolo de compuerta (validación local + revisión humana)
    - Documentar el protocolo de compuerta en `CONTRIBUTING.md`: el alumno ejecuta `make validate` antes de abrir el Pull Request; el Líder Técnico ejecuta `make validate` y revisa el PR antes de integrar (merge)
    - Documentar que, si la Validacion_Local falla o la revisión del Líder Técnico no se supera, el PR no se integra y se indica el incumplimiento; la compuerta es exclusivamente Validacion_Local + revisión humana, sin CI remota
    - _Requirements: 20.7, 20.11_

  - [ ]* 15.6 **[Baseline — Docente (opcional)]** Verificación estructural del modelo de colaboración
    - Verificación estructural (ejemplos, no PBT ni rúbrica): existe `CONTRIBUTING.md`; el `CODEOWNERS` cubre todas las rutas `powers/<equipo>/`; la plantilla de PR está presente; y `make validate` agrega todas las comprobaciones (adaptador, docs, allowlist, cobertura, conteo por alumno) y corre sin CI remota
    - _Requirements: 20.1, 20.4, 20.5, 20.6_

- [ ] 16. **[Alumnos]** Checkpoint final — Ensamblaje completo
  - Asegurar que todas las pruebas pasen; preguntar al usuario si surgen dudas.

## Notes

- Las tareas marcadas con `*` son opcionales (pruebas) y pueden posponerse para un MVP más rápido.
- Cada tarea referencia requisitos específicos para trazabilidad; las pruebas de propiedad referencian su propiedad del diseño.
- Los checkpoints aseguran validación incremental por bloques (base → orquestación → equipos → integración).
- **Línea base de Powers existentes (reutilizar, no recrear):** en `powers/` existen 9 Powers ya construidos que son el cimiento del proyecto: `osint-passive-recon`, `footprinting-enumeration`, `vulnerability-assessment`, `exploitation-metasploit` (Red Team), `dfir-linux`, `network-forensics` (Digital Forensics), `grc-nist-csf` (GRC), `incident-handling-nist` e `incident-response-lab` (Incident Responder). La tarea 1.9 los cataloga en `inventory.json` con marca `baseline`. El trabajo de los alumnos es **extender/parametrizar** estos Powers y **crear Powers nuevos solo para los huecos**, no recrear la base.
- **Dos formatos de Power soportados (Req 8.2, 9.2):** la realidad verificada en disco es que los 9 Powers base están **todos** en formato `POWER.md` con frontmatter + "modos de trabajo" (`osint-passive-recon`, `footprinting-enumeration`, `vulnerability-assessment`, `exploitation-metasploit`, `dfir-linux`, `network-forensics`, `grc-nist-csf`, `incident-handling-nist`, `incident-response-lab`); ninguno usa `plugin.json`. El formato `plugin.json` (estilo agent-plugins.org) lo usa la plantilla `powers/_template/` y es una **opción para los Powers nuevos de alumnos**. El adaptador `agent_ethack_dfir/scripts/power_adapter.py` (tarea 1.10) normaliza ambos a la vista común `x-ethack`, y la validación de integración del Líder Técnico (13.1) acepta los dos con criterios equivalentes.
- **Huecos a cubrir con Power nuevo:** la etapa **Covering Tracks** (Red Team, tarea 6.2) y los Powers de **detección/hardening del Blue Team** (tarea 7.2) no tienen base existente y son los únicos que se crean desde cero. El check de cobertura (13.3) y el conteo por alumno (14.2) cuentan por igual Powers `baseline`/`extended` y `new`, y reportan estos huecos como pendientes hasta cubrirlos.
- **Regla transversal del proyecto:** cada alumno entrega mínimo 2 Powers con Herramienta_Real (Req 9.6); el mínimo puede cumplirse combinando Powers base extendidos y Powers nuevos.
- **Modo_Ejecucion (Req 14):** cada Power acepta `script-kiddie` (default), `green-hat` y `pro`, valida el valor con `resolve_mode` antes de ejecutar la Herramienta_Real y registra el modo aplicado para la auditoría; la distinción Black Hat/White Hat es ética (Req 11), no del modo.
- **Artefactos_Documentacion (Req 15):** cada Power entrega bajo `docs/` el prompt de generación, las sesiones de prueba con Kiro y la realimentación al chat; el Líder Técnico calcula `docStatus` y señala los artefactos faltantes al integrar.
- **Proceso formal de Digital Forensics (Req 5, 16):** el Flujo_Investigacion de seis fases se cimienta en dos Powers base, `dfir-linux` (host) y `network-forensics` (red); el alcance se limita a Linux y nube (AWS) con Windows fuera de alcance; la fase Collect respeta el Orden_Volatilidad (RFC 3227) y la evidencia de Contenedor_Objetivo se recolecta de forma automatizada por ser efímera; los siete Principios_Forenses operan como invariantes transversales.
- **Objetivos en contenedores (Req 11.4, 12):** cada asset modela el Contenedor_Objetivo sobre su host EC2 anfitrión (`host_is_target: false` salvo autorización explícita); la guardia `scope_endpoints()` dirige la prueba al contenedor/servicio y excluye el host subyacente salvo autorización.
- **Respuesta a incidentes NIST SP 800-61 (Req 7, 18):** el Incident Responder se cimienta en el Power base `incident-handling-nist` y opera las cuatro fases NIST de forma cíclica/iterativa; distingue Contencion_Corto_Plazo (aislar sin apagar, preservar evidencia) de Contencion_Largo_Plazo; mantiene IOCs en STIX/YARA/OpenIOC con mapeo a MITRE ATT&CK y Cyber Kill Chain, escala por movimiento lateral y registra todo en `incidents/<id>/incident.json` (más el bloque `incident_response` de `state.json`). La invariante de contención/ciclicidad se verifica con la Property 16.
- **Gobernanza NIST CSF 2.0 (Req 6, 19):** el Responsable de GRC se cimienta en el Power base `grc-nist-csf` y usa NIST CSF 2.0 como lenguaje común; mantiene el Registro_Riesgos (`grc/risk_register.json`) con riesgo residual dentro del Apetito_Riesgo y el Perfil_CSF (`grc/csf_profile.json`) actual/objetivo → gap analysis → POA&M (Tier 1–4); mapea requisito→subcategoría CSF→control→evidencia y vincula hallazgos de Red/Blue/DF/VA a subcategorías CSF. La invariante de riesgo residual y cobertura del POA&M se verifica con la Property 17.
- **Validación GameDay (Req 17):** el escenario breach-to-solution end-to-end es la prueba de integración funcional del sistema completo (tarea 14.7); es validación funcional, no rúbrica ni criterio de calificación.
- **Modelo de colaboración y entrega (Req 20, tarea 15):** la colaboración usa una topología de tres niveles por forks de GitHub (`Repositorio_Base` del docente → `Repositorio_Integracion` del Líder Técnico → `Fork_Alumno`) y Pull Request; cada alumno trabaja en su rama `power/<equipo>-<iniciales>-<nombre-power>` y entrega su Power en `powers/<equipo>/<power>/`. Por **decisión del usuario no se usa GitHub Actions ni CI remota**: la compuerta es `make validate` (Validacion_Local) + revisión del Líder Técnico antes del merge. `agent_ethack_dfir/scripts/validate_all.py` **encadena componentes ya definidos** (power_adapter 1.10, check_power_docs 13.1, validate_target 1.3) e **invoca el Catalogador** `agent_ethack_dfir/scripts/catalog.py` 1.9 —`build_inventory()` para regenerar `inventory.json` (también `make catalog`) y sus métodos `coverage_gaps()`/`count_tooled_by_owner()` para cobertura y conteo de ≥2 Powers con Herramienta_Real por alumno— en lugar de duplicarlos; no depende de las tareas de test opcionales 13.3/14.2, que solo verifican esa lógica. `inventory.json` se genera, no se edita a mano, para evitar conflictos de merge.
- **Política de laboratorio:** toda actividad se restringe a la Allowlist_Objetivos; se dirige al Contenedor_Objetivo y no al host; nunca producción; autorización simulada/didáctica.
- Este spec produce artefactos de diseño y planificación; la implementación de la funcionalidad no forma parte de este flujo.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3", "1.5", "1.6"] },
    { "id": 2, "tasks": ["1.4", "1.7", "1.8", "1.9", "1.10", "3.1", "12.1"] },
    { "id": 3, "tasks": ["1.11", "3.2", "4.1", "4.2", "4.3", "4.4", "4.5", "12.2", "12.3"] },
    { "id": 4, "tasks": ["3.3", "3.4", "4.6", "6.1", "7.1", "8.1", "10.1", "11.1"] },
    { "id": 5, "tasks": ["6.2", "7.2", "8.2", "8.4", "8.6", "10.2", "11.2"] },
    { "id": 6, "tasks": ["8.3", "8.5", "8.7", "8.8", "8.9", "8.10", "13.1"] },
    { "id": 7, "tasks": ["13.2", "13.3", "13.5", "15.4"] },
    { "id": 8, "tasks": ["13.4", "14.1", "14.2", "14.3", "14.4", "14.5", "14.6", "14.7", "14.8"] },
    { "id": 9, "tasks": ["15.1", "15.2", "15.3"] },
    { "id": 10, "tasks": ["15.5"] },
    { "id": 11, "tasks": ["15.6"] }
  ]
}
```
