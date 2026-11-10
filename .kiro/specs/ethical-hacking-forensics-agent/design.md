# Design Document

## Overview

Este diseño describe cómo se construye el **Agente de Ethical Hacking y Digital Forensics** de la Universidad La Salle sobre Kiro. El sistema es un **Agente_Orquestador** (Kiro custom agent) que recorre el ciclo de EC-Council (Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks) delegando en **subagentes de fase** y **subagentes de rol**, también custom agents. Cada subagente consume **Powers** del proyecto que envuelven herramientas reales de Kali Linux (PenTest y Digital Forensics). Toda la actividad se restringe al **Entorno_Laboratorio** mediante la **Allowlist_Objetivos**, y se acompaña de hooks de autorización simulada (`PreToolUse`, patrón `EH_GRANT_PATH`) y auditoría (`PostToolUse`).

El Entorno_Laboratorio está compuesto por nodos **EC2 con Debian** que ejecutan los servicios vulnerables (DVWA y los servicios de referencia) **dentro de contenedores Docker**. Toda prueba de penetración apunta al **Contenedor_Objetivo** que expone el servicio, **no al host EC2 subyacente**, salvo que la Allowlist_Objetivos autorice ese host explícitamente (Req 11.4, 12.1–12.3). El proceso de Digital Forensics sigue el **Flujo_Investigacion** formal de seis fases (Detect → Isolate → Collect → Preserve → Analyze → Report) con alcance limitado a **Linux y nube (AWS)** — Windows queda fuera de alcance (Req 5.7) — y se apoya en dos Powers base de forense: **Power_DFIR_Linux** (`dfir-linux`) y **Power_Network_Forensics** (`network-forensics`). La validación funcional del sistema completo se realiza mediante un **GameDay** de seguridad con escenarios "de la brecha a la solución" (Req 17).

Dos roles se asientan sobre **Powers base de proceso** que rigen su método de trabajo: el **Subagente Incident Responder** se cimenta en **Power_Incident_Handling** (`incident-handling-nist`) y recorre el **Proceso_Respuesta_Incidentes** de cuatro fases de **NIST SP 800-61** (Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity), cíclico e iterativo (Req 7.5, 7.6, 18); el **Subagente GRC** se cimenta en **Power_GRC_CSF** (`grc-nist-csf`) y gobierna el engagement con **NIST CSF 2.0** como lenguaje común de gobierno, riesgo y cumplimiento (Req 6, 19). Ambos se integran con el flujo cruzado existente Red → Blue → IR → DF y con la validación por GameDay, y comparten terminología: las funciones **RS** (Respond) y **RC** (Recover) de CSF 2.0 se alinean con las fases de respuesta a incidentes de NIST SP 800-61 (Req 19.7).

El diseño reutiliza la base real del workspace:

- **Powers base** en `powers/` (`osint-passive-recon`, `footprinting-enumeration`, `exploitation-metasploit`, `vulnerability-assessment`), con estructura `POWER.md` + `skills/` + `steering/`. Verificado en disco: los **9 Powers base usan `POWER.md`**; ninguno usa `plugin.json`. El formato `plugin.json` es el de la plantilla `powers/_template/` y una opción disponible para los Powers **nuevos** de los alumnos. El adaptador (`agent_ethack_dfir/scripts/power_adapter.py`) y el Catalogador soportan ambos formatos por igual.
- **Starter SDD** en `kiroethicalhacking/kiro-ethical-hacking-sdd-starter/`: Power Director, hooks `.kiro/hooks/*.json` en formato `version: v1`, patrón `EH_GRANT_PATH`, scripts (`gate_mcp.py`, `audit_event.py`) y `engagements/<id>/` con `scope.yaml` y `state.json`.
- **Casos de referencia** en `ethicalhacking/`, `footprinting/` y `nmap_enumeration/` como fuente de objetivos y escenarios.

Lenguaje de ejemplos de código: **Python** (coincide con los scripts de hooks del starter: `gate_mcp.py`, `audit_event.py`, `new_engagement.py`).

Alcance: este documento describe el comportamiento del sistema de agentes, Powers, hooks, modelo de datos e integración. **No** incluye rúbrica ni criterios de calificación.

> **Nota de ubicación (consolidación).** El código del agente generado por este
> spec vive bajo **`agent_ethack_dfir/`** (`agent_ethack_dfir/agents/`,
> `agent_ethack_dfir/scripts/`, `agent_ethack_dfir/engagements/`). Permanecen en
> la **raíz del repositorio** `powers/` y `.kiro/` (specs + hooks), y los archivos
> que GitHub lee desde la raíz: `CODEOWNERS`, `CONTRIBUTING.md`, `Makefile` y
> `.github/`. Las rutas de este documento ya reflejan esa ubicación.

## Architecture

### Arquitectura general

El sistema tiene tres capas: **orquestación** (un custom agent coordinador), **subagentes** (fase y rol) y **capacidades** (Powers que envuelven herramientas de Kali). Transversalmente operan los **hooks** de autorización/auditoría y el **modelo de datos de engagement** (allowlist, estado, evidencia, cadena de custodia).

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           USUARIO / DOCENTE / LÍDER TÉCNICO                 │
└───────────────────────────────┬────────────────────────────────────────────┘
                                 │ solicita iniciar/avanzar fase
                                 ▼
                  ┌───────────────────────────────────┐
                  │        AGENTE_ORQUESTADOR          │  (Kiro custom agent)
                  │  - expone 5 fases EC-Council       │  Req 1
                  │  - mantiene secuencia por defecto  │
                  │  - delega y consolida resultados   │
                  │  - aplica Principios_Eticos        │  Req 11
                  └───┬───────────────┬────────────────┘
          delega fase │               │ delega rol
                      ▼               ▼
   ┌──────────────────────────┐   ┌──────────────────────────────────────┐
   │   SUBAGENTES DE FASE (5)  │   │          SUBAGENTES DE ROL            │
   │  Recon  Scan  Gain        │   │  Red  Blue  DigitalForensics  GRC  IR │
   │  Maintain  Cover          │   │                                        │
   └───────────┬──────────────┘   └───────────────────┬───────────────────┘
               │ invoca Power                          │ invoca Power
               ▼                                       ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │                               POWERS                                      │
   │  POWER.md | plugin.json + skills/ + steering/ (declaran fase/etapa+allowlist)│  Req 9
   │  osint-passive-recon · footprinting-enumeration · exploitation-metasploit │
   │  vulnerability-assessment · <Powers nuevos de los 13 alumnos>             │
   └───────────┬────────────────────────────────────────────────┬────────────┘
               │ ejecuta Herramienta_Real                        │
               ▼                                                 ▼
   ┌───────────────────────────┐                   ┌──────────────────────────┐
   │  HERRAMIENTAS KALI PENTEST │                   │  HERRAMIENTAS FORENSES    │
   │  nmap, Metasploit, nikto…  │                   │  Volatility, Autopsy…     │
   └───────────────────────────┘                   └──────────────────────────┘
               ▲                                                 ▲
               │                                                 │
   ┌───────────┴─────────────────────────────────────────────────┴────────────┐
   │  HOOKS (.kiro/hooks/*.json, version v1)                                    │  Req 10
   │  PreToolUse → gate_mcp.py (EH_GRANT_PATH, simulado, no bloqueante)         │
   │  PostToolUse → audit_event.py (resumen + hash SHA-256)                     │
   └────────────────────────────────────────────────────────────────────────────┘
               ▲
               │ consulta / actualiza
   ┌───────────┴────────────────────────────────────────────────────────────────┐
   │  MODELO DE DATOS DEL ENGAGEMENT  (agent_ethack_dfir/engagements/<id>/)                          │  Req 5,6,12,13
   │  scope.yaml (Allowlist_Objetivos) · state.json · evidence/ · chain_of_custody │
   │  inventory.json (Powers/agents ↔ fase/etapa ↔ responsable)                    │
   └────────────────────────────────────────────────────────────────────────────┘
```

### Flujo de delegación

1. El usuario pide **iniciar o avanzar** una fase. El Agente_Orquestador consulta `state.json` del engagement activo para conocer la fase y las fases completadas (Req 1.1).
2. El Orquestador decide la fase objetivo:
   - Si es la **siguiente en la secuencia** canónica, delega directamente en el Subagente_Fase (Req 1.2, 1.3).
   - Si está **fuera de orden**, registra la solicitud e informa las fases previas no completadas antes de delegar (Req 1.5).
3. El **Subagente_Fase** declara objetivo y alcance (Req 2.7), selecciona un Power apropiado para su fase (Req 2.2–2.6) y lo invoca pasando el objetivo.
4. Antes de que el Power ejecute la Herramienta_Real, el **Hook_Autorizacion** (`PreToolUse`) evalúa `EH_GRANT_PATH` y registra la decisión (Req 10.1–10.3). El Power además **valida el objetivo contra la Allowlist_Objetivos** (Req 9.5, 11.1, 11.2).
5. Tras la ejecución, el **Hook_Auditoria** (`PostToolUse`) registra un resumen con hash (Req 10.4) y el Power produce un **registro de acción** consumible por Blue Team y Digital Forensics (Req 3.4).
6. El Orquestador **consolida** los resultados de la fase y ofrece la transición a la siguiente (Req 1.4), identificando en su respuesta cada subagente invocado y la fase/rol que representa (Req 1.6).
7. Los subagentes de rol se activan en flujos cruzados: una acción ofensiva genera registros → Blue Team detecta (Req 4.3) → Incident Responder contiene y notifica (Req 7.3, 7.4) → Digital Forensics recolecta y preserva evidencia (Req 5).

### Mapa de componentes de agentes

| Componente | Tipo Kiro | Responsabilidad | Requisitos |
|---|---|---|---|
| Agente_Orquestador | Custom agent | Coordina fases, delega, consolida, aplica principios | 1, 8, 11 |
| Subagente Recon | Custom agent (fase) | Reconocimiento del objetivo autorizado | 2.2 |
| Subagente Scanning | Custom agent (fase) | Descubrimiento y enumeración de puertos/servicios | 2.3 |
| Subagente Gaining Access | Custom agent (fase) | Evaluación de vulnerabilidades / explotación PoC | 2.4 |
| Subagente Maintaining Access | Custom agent (fase) | Persistencia/sesiones acotadas al lab | 2.5 |
| Subagente Covering Tracks | Custom agent (fase) | Análisis/manipulación de rastros + registro | 2.6 |
| Subagente Red Team | Custom agent (rol) | Agrupa Powers ofensivos de las 5 fases | 3 |
| Subagente Blue Team | Custom agent (rol) | Detección, análisis de logs, hardening | 4 |
| Subagente Digital Forensics | Custom agent (rol) | Flujo_Investigacion Detect→…→Report | 5 |
| Subagente GRC | Custom agent (rol) | Autorización, alcance, cumplimiento, custodia; GRC con NIST CSF 2.0 (Registro_Riesgos, Perfil_CSF) sobre `grc-nist-csf` | 6, 19 |
| Subagente Incident Responder | Custom agent (rol) | Puente detección↔forense, contención; Proceso_Respuesta_Incidentes NIST SP 800-61 sobre `incident-handling-nist` | 7, 18 |

## Mapa Fase EC-Council ↔ Subagente ↔ Powers ↔ Herramientas

### Fases ofensivas (EC-Council)

| Fase EC-Council | Subagente_Fase | Powers (base → nuevos) | Herramientas Kali concretas | Req |
|---|---|---|---|---|
| Reconnaissance | Subagente Recon | `osint-passive-recon`, `footprinting-enumeration` | theHarvester, whois/dig, dnsrecon, (OSINT MCP pasivo) | 2.2, 9.4 |
| Scanning | Subagente Scanning | `footprinting-enumeration` + Power nuevo de escaneo | **nmap** (`-sV`, `-sC`, NSE), masscan, netcat | 2.3, 9.4 |
| Gaining Access | Subagente Gaining Access | `vulnerability-assessment`, `exploitation-metasploit` | nikto, Nuclei, **Metasploit** (msfconsole/msfvenom), sqlmap, Hydra (contra DVWA) | 2.4, 9.4 |
| Maintaining Access | Subagente Maintaining Access | Power nuevo de persistencia/sesiones | Meterpreter (sesiones/jobs), cron/systemd en lab, SSH keys de laboratorio | 2.5 |
| Covering Tracks | Subagente Covering Tracks | Power nuevo de análisis de rastros | análisis de `auth.log`/`syslog`, `wtmp`/`utmp`, timestomp (acotado y **registrado**) | 2.6 |

Notas de diseño:
- Los Powers base se reutilizan como **cimiento o referencia** de los Powers nuevos (Req 9.4). Por ejemplo, un Power de escaneo nuevo hereda las convenciones de steering de `footprinting-enumeration`.
- Covering Tracks **siempre registra** sus acciones para trazabilidad (Req 2.6), incluso cuando manipula rastros; esto alimenta la auditoría y la cadena de custodia.

### Flujo de investigación forense (Digital Forensics)

El Subagente Digital Forensics implementa el **Flujo_Investigacion** formal de seis fases Detect → Isolate → Collect → Preserve → Analyze → Report, alineado con `digitalforensic/proceso-digital-forensic.md` (presentación La Salle 2026 + material HTB). Cada etapa tiene al menos un Power (Req 5.1, 8.3). El **alcance se limita a Linux y nube (AWS); Windows queda fuera de alcance** (Req 5.7). Las herramientas por fase son las concretas del proceso formal.

| Etapa | Objetivo | Powers (base → alumnos DF) | Herramientas forenses (proceso formal) | Req |
|---|---|---|---|---|
| **Detect** | Confirmar el incidente, abrir caso e inventariar fuentes de evidencia | Power de triage de alertas (sobre `dfir-linux`) | GuardDuty/SIEM/EDR, análisis de logs, grep/jq sobre `event_history` (CloudTrail) | 5.1, 7.1 |
| **Isolate** | Contener sin destruir evidencia (**aislar no es apagar**: apagar borra la RAM volátil) | Power de aislamiento (coordinado con IR) | aislamiento de red por Security Group sin reglas + NACL, protección contra terminación EC2, desactivar access keys/sesiones | 5.1, 7.3 |
| **Collect** | Recolectar copias forenses respetando el **Orden_Volatilidad** (RFC 3227) | Power de adquisición (`dfir-linux`, `network-forensics`) | **dd**/`dc3dd`/`dcfldd` (disco), **LiME**/**AVML** (memoria), `tcpdump`/**Wireshark** (red), snapshot EBS en AWS | 5.1, 5.3, 5.6 |
| **Preserve** | Preservar íntegra la evidencia desde la adquisición | Power de preservación | **SHA-256** (`sha256sum`), S3 Object Lock / almacenamiento de escritura única, write-blocker lógico, timestamps UTC | 5.3, 5.4, 5.5 |
| **Analyze** | Reconstruir los hechos **siempre sobre copias** | Power de análisis (`dfir-linux`, `network-forensics`) | **Volatility** (`linux.pslist`/`pstree`/`bash`/`sockstat`/`malfind`/`check_modules`), **Autopsy**/**TSK** (disco), **Plaso**/log2timeline (línea de tiempo), **Athena**/CloudTrail (logs nube), **Snort**/**Suricata** NetFlow (red) | 5.5 |
| **Report** | Reporte con hallazgos + evidencia + cadena de custodia + IOCs/TTPs | Power de reporte forense | plantilla de reporte, render de `chain_of_custody`, exportes de línea de tiempo | 5.10, 13.5 |

**Orden_Volatilidad en Collect (RFC 3227).** La fase Collect recolecta primero lo más volátil y después lo menos volátil, en este orden: (1) registros de CPU y caché → (2) **memoria RAM** → (3) estado de red (conexiones, ARP, rutas) → (4) procesos en ejecución → (5) **disco** → (6) logs remotos y monitoreo → (7) medios de respaldo/archivo (Req 5.6, 16.1). Por eso Isolate nunca apaga el host: preserva la RAM antes de que Collect la vuelque.

Reglas transversales forenses (Principios_Forenses, Req 16):
- **Evidence Integrity:** todo Power de análisis opera en **copias** y verifica `hash_pre == hash_post` sobre la evidencia original (Req 5.5, 16.2).
- **Minimization:** se recolecta solo la evidencia necesaria para el alcance (Req 16.5).
- **Documentation / Reproducibility:** cada paso registra comando, hora UTC, herramienta, versión y resultado (Req 16.4).
- **Objectivity:** se documenta también la evidencia que contradice la hipótesis (Req 16.6).
- **Legal Admissibility:** preservación con hash y almacenamiento de escritura única (Req 16.7).

**Forense de contenedores (evidencia efímera).** Cuando la evidencia reside en un Contenedor_Objetivo, el Digital_Forensics_Team la trata como **evidencia efímera** y la recolecta mediante un **procedimiento automatizado** (snapshot + hash + copia a la cuenta/almacén forense) que preserva su integridad **antes de que el contenedor desaparezca** (Req 5.9, 16.8). Esto cubre capas de imagen, eventos de runtime y datos volátiles del contenedor.

### Powers base de Digital Forensics (host y red)

El equipo de Digital Forensics usa como **cimiento** los dos Powers propuestos en `digitalforensic/propuesta-powers-digital-forensic.md` (Req 5.8, 16). Ambos son **Knowledge Base Powers** (sin servidor MCP: herramientas de CLI/GUI de laboratorio) y comparten la misma guía corta de metodología con las seis fases, remitiendo a `proceso-digital-forensic.md`.

| Power base | Nombre | Dominio / evidencia | Estructura | Herramientas | Req |
|---|---|---|---|---|---|
| **Power_DFIR_Linux** | `dfir-linux` | Forense de **host Linux**: live response, sistemas de archivos, imagen y hashes, persistencia, logs | `POWER.md` + `skills/dfir-linux/` (`SKILL.md` + `references/`) + `steering/` por fase | `dd`/`dc3dd`, LiME, `ps`/`lsof`/`ss`, `auth.log`/`audit.log`/`wtmp`, Autopsy/TSK, Volatility `linux.*` | 5.8 |
| **Power_Network_Forensics** | `network-forensics` | Forense de **red**: captura, análisis de tráfico, NetFlow, firmas, TLS | `POWER.md` + `skills/network-forensics/` (`SKILL.md` + `references/`) + `steering/` por fase | tcpdump/Wireshark (BPF), Suricata NetFlow, Snort, análisis TLS/SSL | 5.8 |

**Relación entre ambos (deriva red → host).** `network-forensics` **deriva a** `dfir-linux` cuando el análisis de tráfico/NetFlow identifica el **host sospechoso** (para examinar su endpoint), y `dfir-linux` remite a `network-forensics` para analizar capturas asociadas. Si el host sospechoso es Windows, el agente lo marca **fuera de alcance** en vez de analizarlo (Req 5.7). Los Powers de los 4 alumnos DF se construyen sobre estos dos como base para forense de host y de red respectivamente.

## Proceso de Respuesta a Incidentes (NIST SP 800-61)

El Subagente Incident Responder implementa el **Proceso_Respuesta_Incidentes** de NIST SP 800-61 como cimiento de método, usando el Power base **Power_Incident_Handling** (`incident-handling-nist`) (Req 7.5, 18.1). El proceso tiene **cuatro fases** y es **cíclico e iterativo**: las lecciones aprendidas de la última fase retroalimentan la primera, y las dos fases centrales se recorren en bucle mientras aparezca evidencia nueva (Req 18.2, 18.5, 18.7).

```
 ┌───────────────┐   ┌────────────────────────┐   ┌──────────────────────────────────┐   ┌───────────────────────┐
 │1. Preparation │ → │2. Detection & Analysis │ ⇄ │3. Containment, Eradication &     │ → │4. Post-Incident       │
 │  (pre-incidente)│  │  (contexto + timeline) │   │   Recovery                       │   │   Activity (lecciones)│
 └───────▲───────┘   └────────────────────────┘   └──────────────────────────────────┘   └───────────┬───────────┘
         │                                                                                            │
         └──────────────────────────── lecciones aprendidas (retroalimentación) ──────────────────────┘
```

### Las cuatro fases y su diseño

| Fase NIST SP 800-61 | Qué hace el Incident Responder | Coordinación | Req |
|---|---|---|---|
| **1. Preparation** | Mantiene disponibles **antes** del incidente la documentación, los contactos/roles y las herramientas de respuesta (jump bag, playbooks, cuentas privilegiadas bajo demanda, baselines). | GRC (alcance, roles) | 18.3 |
| **2. Detection & Analysis** | Al recibir un evento con consecuencia negativa, establece **contexto y línea de tiempo** del incidente, clasifica severidad y alcance. | Se nutre del **Blue_Team** (hallazgos de detección, logs) | 7.1, 18.4, 18.8 |
| **3. Containment, Eradication & Recovery** | Contiene (corto y largo plazo), erradica la causa raíz y recupera los servicios bajo monitoreo intensivo. | **IR → DF** para preservar evidencia; Blue para hardening | 7.3, 7.4, 18.5, 18.8 |
| **4. Post-Incident Activity** | Produce el **reporte final** y una sesión de **lecciones aprendidas**, que retroalimentan Preparation (ciclo). | GRC (mejora, ID.IM), todo el equipo | 18.6, 18.7 |

**Iteración de las fases centrales (Req 18.5).** Mientras el proceso está en Detection & Analysis o en Containment, Eradication & Recovery, el Incident Responder ejecuta el ciclo de investigación de tres pasos de forma iterativa: (1) **crear y usar IOC** → (2) **identificar nuevas pistas y sistemas impactados** → (3) **recolectar y analizar datos** → vuelve al paso 1. Si durante la recuperación siguen apareciendo IOCs, el proceso **regresa** a investigación (Detection & Analysis), lo que materializa el carácter iterativo (Property 16).

### Mapeo del flujo cruzado Red → Blue → IR → DF a las fases NIST

El flujo cruzado ya definido (una acción ofensiva genera registros → Blue detecta → IR contiene y notifica → DF recolecta y preserva) se proyecta sobre las fases NIST (Req 18.11):

| Flujo cruzado | Fase NIST SP 800-61 | Nota de diseño |
|---|---|---|
| **Red_Team** reproduce/continúa la acción ofensiva acotada al Contenedor_Objetivo | (genera el incidente a investigar) | Produce registros consumibles (Req 3.4) |
| **Blue_Team** detecta analizando logs y emite hallazgo | **Detection & Analysis** | Insumo primario de la fase; establece contexto y timeline (Req 7.1, 18.4) |
| **Incident Responder** toma el hallazgo e inicia contención | **Containment, Eradication & Recovery** | Distingue contención corto vs largo plazo (abajo) |
| **Digital_Forensics_Team** recolecta y preserva evidencia | nutre el **backup substage** de la contención | La evidencia preservada (Req 16) va al Flujo_Investigacion DF |

### Contención: corto plazo vs largo plazo (Req 7.7, 18.5)

El Incident Responder distingue dos tipos de contención con criterios de diseño verificables:

| Tipo | Objetivo | Acciones típicas | ¿Apaga el sistema? | ¿Preserva evidencia? |
|---|---|---|---|---|
| **Contencion_Corto_Plazo** | Mínima huella; ganar tiempo y **preservar evidencia** | Mover a VLAN aislada, desconectar la red, redirigir/sinkhole del DNS del C2, **aislar el Contenedor_Objetivo sin apagarlo** | **No** (apagar borra la RAM volátil) | **Sí** |
| **Contencion_Largo_Plazo** | Cambios **persistentes** | Cambio de contraseñas, reglas de firewall, parches, hardening, apagado autorizado de sistemas | Puede apagar (autorizado) | No es su propósito |

**Aplicación al laboratorio (DVWA en contenedor).** La contención de corto plazo **aísla el Contenedor_Objetivo sin apagar el host EC2**: aplica un Security Group de cuarentena sin reglas + NACL, desconecta el contenedor de su red Docker y protege la instancia contra terminación, de modo que la RAM y el estado volátil se preserven para que el Digital_Forensics_Team los vuelque (coherente con "aislar no es apagar" de la fase Isolate del Flujo_Investigacion y con Req 17.5). Solo tras preservar la evidencia se procede a erradicación/parcheo (contención de largo plazo).

### Manejo de IOCs y mapeo a MITRE ATT&CK / Cyber Kill Chain

El Incident Responder **crea, documenta y comparte** los indicadores de compromiso en formatos estándar y **mapea** la actividad del incidente a marcos de comportamiento adversario (Req 18.9, 18.10):

- **Formatos de IOC** (Req 18.9): el IR documenta cada IOC en al menos uno de **STIX** (JSON para intercambio de CTI), **YARA** (reglas para identificar artefactos) u **OpenIOC** (lenguaje de documentación/compartición). El registro de incidente guarda el IOC y su formato.
- **Mapeo a marcos** (Req 18.10): cada actividad observada se mapea a **tácticas/técnicas de MITRE ATT&CK** (p. ej. T1190 Exploit Public-Facing Application, T1003.001 LSASS, T1021 Remote Services) y a una **etapa de la Cyber Kill Chain** (Recon → Weaponize → Delivery → Exploitation → Installation → C2 → Actions on Objectives).
- **Conexión con el rastreo de IOCs del GameDay (Req 17.4)** y con el **mapeo kill-chain → evidencia AWS** del proceso DF: las etapas de la kill chain a las que el IR mapea la actividad son las mismas que guían la búsqueda de evidencia en CloudTrail/VPC Flow Logs (ver tabla "Rastreo de IOCs" en la sección GameDay). Así, el IOC creado por el IR dirige el análisis de logs del Blue/DF y, a la inversa, un hit de log alimenta un nuevo IOC — cerrando el ciclo iterativo de la fase Detection & Analysis.

### Escalamiento por movimiento lateral (Req 18.5 / 7.9)

Si el Incident Responder detecta **movimiento lateral** hacia otro sistema o departamento (p. ej. `AssumeRole` hacia otra cuenta, RDP/SSH a un host nuevo), **escala** el incidente y **registra el escalamiento** en el registro de incidente (campo `escalations`). Que el sistema pertenezca a otra área no es motivo para no escalar.

## Gobernanza con NIST CSF 2.0 (GRC)

El Subagente GRC gobierna el engagement sobre el Power base **Power_GRC_CSF** (`grc-nist-csf`), usando **NIST CSF 2.0** (NIST CSWP 29) como **lenguaje común** de gobierno, riesgo y cumplimiento (Req 6.5, 6.6, 19.1). El Core de CSF 2.0 organiza los resultados en **seis funciones**: **GV** Govern (rodea a las demás), **ID** Identify, **PR** Protect, **DE** Detect, **RS** Respond y **RC** Recover; 22 categorías y 106 subcategorías (p. ej. `GV.RM-06`, `ID.RA`, `RS.AN`).

### Cadena de trazabilidad GRC (requisito → subcategoría → control → evidencia)

El Responsable_GRC usa CSF 2.0 como eje: cada requisito de ley, contrato, norma o política se **mapea a una subcategoría CSF**, de ahí a un **control** concreto (SP 800-53, ISO 27001 Anexo A, CIS v8, control de AWS) y del control a su **evidencia**; una brecha genera un riesgo en el Registro_Riesgos y una entrada en el POA&M (Req 19.2, 19.5).

```
 Requisito (ley/contrato/norma/política)
        │  se mapea a
        ▼
 Subcategoría CSF (resultado esperado)  ◄── evaluada en Perfil actual / objetivo
        │  se logra con
        ▼
 Control (SP 800-53 / ISO 27001 / CIS v8 / AWS)
        │  se demuestra con
        ▼
 Evidencia (config, log, ticket, acta, reporte, hallazgo técnico)
        │  si falta o falla
        ▼
 Brecha ─► Riesgo en el Registro_Riesgos (GV.RM-06) ─► Tratamiento ─► POA&M
```

### Registro_Riesgos (GV.RM-06)

El Registro_Riesgos documenta cada riesgo con **probabilidad × impacto**, **dueño**, **opción de tratamiento** (mitigar | transferir | aceptar | evitar) y **riesgo residual**, calculado con un método estandarizado conforme a **GV.RM-06** (Req 6.7, 19.3). El **riesgo residual** de cada riesgo debe quedar **dentro del Apetito_Riesgo** declarado para el engagement (Req 6.8); esta es la invariante que verifica la Property 17.

### Perfil_CSF, gap analysis y POA&M

El Responsable_GRC produce un **Perfil_CSF** con un **perfil actual** (resultados logrados hoy, con evidencia) y un **perfil objetivo** (resultados deseados, priorizados por riesgo), y declara un **Tier objetivo** entre los niveles 1–4 (Partial, Risk Informed, Repeatable, Adaptive) (Req 6.9, 19.4). La **comparación** actual vs objetivo produce el **gap analysis**; cada brecha se registra en el **POA_M** (Plan of Action and Milestones) y genera un riesgo asociado en el Registro_Riesgos (Req 6.9, 19.5).

### Hallazgos técnicos como evidencia CSF

Los hallazgos de Red_Team, Blue_Team, Digital_Forensics_Team y de las evaluaciones de vulnerabilidades se **vinculan a subcategorías CSF** como evidencia para la segunda y tercera línea del Modelo_Tres_Lineas (Req 6.10, 19.2, 19.6). Mapeo módulo → subcategorías:

| Módulo / fuente del hallazgo | Subcategorías CSF que alimenta | Función |
|---|---|---|
| OSINT y footprinting (Recon) | `ID.AM` (inventario/exposición), `ID.RA` (amenazas), `GV.SC` (terceros visibles) | ID / GV |
| Scanning / Vulnerability Assessment | `ID.RA` (vulnerabilidades priorizadas), `PR.PS` (parches/config), `ID.IM` (mejora) | ID / PR |
| Pentest con Metasploit (Gaining Access) | `ID.RA` (validación de explotabilidad), `ID.IM` | ID |
| Blue Team (detección, logs) | `DE.CM` (monitoreo continuo), `DE.AE` (análisis de eventos adversos) | DE |
| DFIR (host, red) | `RS.AN` (análisis forense, preservación de evidencia) | RS |
| Incident Handling (NIST SP 800-61) | `RS.MA`, `RS.AN`, `RS.CO`, `RS.MI`, `RC.RP`, `RC.CO`, `ID.IM` (lecciones) | RS / RC |

### Alineación RS/RC (CSF 2.0) ↔ fases NIST SP 800-61

Para mantener un lenguaje único entre GRC e Incident Responder (Req 19.7), las funciones de respuesta/recuperación de CSF 2.0 se alinean con las fases del Power_Incident_Handling:

| Función/categoría CSF 2.0 | Fase NIST SP 800-61 | Significado compartido |
|---|---|---|
| `RS.MA` Incident Management | Detection & Analysis (gestión del incidente) | Triage, asignación, contexto |
| `RS.AN` Incident Analysis | Detection & Analysis | Línea de tiempo, IOCs, forense (con DF) |
| `RS.CO` Reporting & Communication | Transversal (Detection→Post-Incident) | Comunicación, escalamiento |
| `RS.MI` Incident Mitigation | Containment, Eradication & Recovery | Contención corto/largo plazo, erradicación |
| `RC.RP` Recovery Plan Execution | Containment, Eradication & Recovery (Recovery) | Restauración bajo monitoreo |
| `RC.CO` Recovery Communication | Post-Incident Activity | Comunicación de recuperación |
| `ID.IM` Improvement | Post-Incident Activity | Lecciones aprendidas → Preparation |

## Components and Interfaces

### Modelo estándar de un Power del proyecto

Los Powers nuevos reutilizan la estructura de los Powers base (`skills/` + `steering/`) y declaran su contrato `x-ethack` en un manifiesto que puede ser **`POWER.md`** (formato de los 9 Powers base, verificado en disco) **o** **`plugin.json`** (formato de la plantilla `powers/_template/`, disponible para los Powers nuevos). Ambos corresponden al esquema `agent-plugins.org` y el adaptador los normaliza por igual.

```
powers/<nombre-power>/
├── POWER.md | plugin.json   # manifiesto + contrato x-ethack (fase/etapa + binding de allowlist)
├── skills/                  # SKILL.md por capacidad (qué hace y cómo se invoca)
│   └── <skill>/SKILL.md
└── steering/                # guías de conocimiento cargables bajo demanda (*.md)
```

### Contrato `x-ethack` del proyecto (`POWER.md` o `plugin.json`)

El contrato `x-ethack` se declara en el frontmatter de `POWER.md` (como en los 9 Powers base, p. ej. `powers/exploitation-metasploit/POWER.md`) o en la clave `x-ethack` de un `plugin.json` (plantilla `_template`, opción para Powers nuevos). En cualquiera de los dos formatos se añaden los campos del proyecto para declarar fase/etapa, equipo responsable, herramientas envueltas y la política de allowlist (Req 9.1, 9.2, 9.3). El ejemplo siguiente usa `plugin.json`; el equivalente en `POWER.md` lleva los mismos campos bajo `x-ethack` en su frontmatter.

```jsonc
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "scanning-nmap-services",
  "version": "0.1.0",
  "description": "Descubrimiento y enumeración de puertos/servicios con nmap sobre el lab.",
  "author": { "name": "Alumno Red Team 2 — ULSA" },
  "keywords": ["scanning", "nmap", "enumeration", "ethical-hacking"],

  "x-ethack": {
    "kind": "offensive",                 // offensive | defensive | forensics | governance | response
    "ecCouncilPhase": "Scanning",        // una de las 5 fases, o null si es forense
    "forensicsStage": null,              // Detect|Isolate|Collect|Preserve|Analyze|Report, o null
    "team": "red-team",
    "owner": "alumno-2",
    "tools": [                           // Herramienta_Real envuelta (≥1)  Req 9.1
      { "name": "nmap", "binary": "nmap", "category": "pentest" }
    ],
    "allowlistValidation": {             // cómo valida el objetivo  Req 9.5, 11.1
      "required": true,
      "source": "agent_ethack_dfir/engagements/${ENGAGEMENT_ID}/scope.yaml#assets",
      "targetParams": ["target", "host", "hostname", "domain", "url"]
    },
    "producesActionLog": true,           // registro consumible por Blue/DF  Req 3.4

    "executionMode": {                   // Modo_Ejecucion  Req 14.1, 14.2
      "param": "Modo_Ejecucion",         // nombre del parámetro aceptado al invocar
      "allowed": ["script-kiddie", "green-hat", "pro"],
      "default": "script-kiddie"
    },
    "documentation": {                   // Artefactos_Documentacion  Req 15.1, 15.5
      "root": "powers/${TEAM}/${POWER}/docs",
      "required": ["prompt.md", "sessions/", "feedback.md"]
    }
  }
}
```

Reglas del modelo (Req 9):
1. Cada Power envuelve **al menos una** Herramienta_Real de Kali (`x-ethack.tools` no vacío) — Req 9.1.
2. Cada Power declara **exactamente una** ubicación en el ciclo: `ecCouncilPhase` **o** `forensicsStage` (el otro en `null`) — Req 9.2.
3. Cada Power es invocable por al menos un subagente de fase o de rol (se refleja en el inventario) — Req 9.3.
4. Antes de ejecutar, el Power **resuelve y normaliza** el objetivo y comprueba su pertenencia a la Allowlist_Objetivos declarada en `allowlistValidation.source` — Req 9.5, 11.1, 11.2.
5. Cada Power **acepta** el parámetro `Modo_Ejecucion` con los valores de `executionMode.allowed` y aplica `executionMode.default` cuando no se indica — Req 9.7, 14.1, 14.2.
6. Cada Power **declara** sus Artefactos_Documentacion bajo `documentation.root` — Req 9.8, 15.1.

### Modo_Ejecucion — selección, validación y comportamiento por modo

El `Modo_Ejecucion` fija el nivel técnico con el que el Power ejecuta su tarea. Es un parámetro **técnico**, ortogonal a la ética: la distinción Black Hat / White Hat se resuelve por la Política ética (Req 11) y no por el modo (Req 14.8); `pro` describe únicamente el nivel técnico.

**Cómo se pasa y se valida.** El subagente invoca el Power pasando `Modo_Ejecucion` como argumento. El Power lo normaliza y valida contra `x-ethack.executionMode.allowed` **antes** de tocar la Herramienta_Real:

- Si no se indica, se aplica `script-kiddie` (default) — Req 14.2.
- Si el valor no está en `{script-kiddie, green-hat, pro}`, el Power **rechaza** la invocación e indica los valores admitidos, sin ejecutar la herramienta — Req 14.7.

```python
# skills/<skill>/execution_mode.py  (resuelto antes de invocar la Herramienta_Real)
ALLOWED_MODES = ("script-kiddie", "green-hat", "pro")
DEFAULT_MODE = "script-kiddie"

class InvalidModeError(ValueError):
    pass

def resolve_mode(requested: str | None) -> str:
    """Req 14.2 (default) y Req 14.7 (rechazo de valores inválidos)."""
    if requested is None or (isinstance(requested, str) and not requested.strip()):
        return DEFAULT_MODE
    mode = requested.strip().lower()
    if mode not in ALLOWED_MODES:
        raise InvalidModeError(
            f"Modo_Ejecucion inválido: {requested!r}. Admitidos: {', '.join(ALLOWED_MODES)}.")
    return mode
```

**Comportamiento por modo** (Req 14.3–14.5):

| Modo | Comportamiento del Power | Salida | Req |
|---|---|---|---|
| `script-kiddie` (default) | Ejecuta la Herramienta_Real mediante **comandos predefinidos automatizados**, sin lógica propia de análisis | resultado crudo de la herramienta | 14.2, 14.3 |
| `green-hat` | Ejecuta la Herramienta_Real **y explica** la lógica subyacente de los comandos/herramientas empleados (redes, SO, scripting) | resultado + explicación didáctica | 14.4 |
| `pro` | Aplica **lógica propia avanzada** que razona sobre la arquitectura del objetivo; **puede generar comandos o scripts propios** además de invocar la herramienta | resultado + razonamiento + artefactos generados (acotados al lab) | 14.5 |

Reglas transversales del modo: cualquiera que sea el modo, la guardia de Allowlist_Objetivos (Req 11.2) y la autorización simulada (Req 10) se aplican igual; el modo `pro` que genera scripts propios los acota al Entorno_Laboratorio y nunca a producción (Req 11.3). El Power **registra el modo aplicado** en su registro de ejecución para el Hook_Auditoria (Req 14.6, ver Hook_Auditoria).

### Artefactos_Documentacion — estructura de entrega por Power

Cada Power entrega sus Artefactos_Documentacion junto a su código, bajo `docs/` del propio Power, asociados al Power y a su alumno responsable (Req 15.1, 15.5):

```
powers/<equipo>/<power>/
├── plugin.json
├── skills/  steering/
└── docs/                       # Artefactos_Documentacion  Req 15.1
    ├── prompt.md               # prompt de generación del Power  Req 15.2
    ├── sessions/               # sesiones de interacción con Kiro al probarlo  Req 15.3
    │   └── <fecha>-<tema>.md
    └── feedback.md             # realimentación del resultado al chat/contexto  Req 15.4
```

La asociación Power ↔ alumno se materializa en `inventory.json` (campo `owner`) y en `x-ethack.owner`; `docs/` vive dentro del árbol del Power, por lo que la correspondencia Power ↔ artefactos es estructural (Req 15.5).

### Validación de la Allowlist_Objetivos en el Power

La guardia reutiliza la lógica de normalización del starter (`gate_mcp.py`): se acepta host/IP/URL, se normaliza (minúsculas, sin punto final, sin corchetes IPv6, hostname de la URL) y se compara contra la allowlist normalizada.

Como los `assets` modelan ahora el **Contenedor_Objetivo** sobre su host EC2, la guardia **resuelve el objetivo al contenedor/servicio**: construye el conjunto de endpoints válidos a partir de `target_host`/`target_hostname` (más `target_port` cuando el objetivo lo incluye) de cada asset, y **excluye el `ec2_host` anfitrión salvo que `host_is_target` sea `true`** (Req 11.4, 12.2, 12.3). Así, apuntar al host EC2 subyacente de un servicio en contenedor queda fuera de alcance a menos que la Allowlist lo autorice explícitamente.

```python
# skills/<skill>/validate_target.py  (invocado por el Power antes de la herramienta)
import ipaddress, urllib.parse

def normalize_target(v: str) -> str | None:
    if not isinstance(v, str) or not v.strip():
        return None
    v = v.strip()
    if "://" in v:
        u = urllib.parse.urlsplit(v)
        if u.scheme not in ("http", "https") or u.username or u.password or not u.hostname:
            return None
        v = u.hostname
    else:
        if any(c in v for c in "/\\?#@; "):
            return None
        if ":" in v and not v.startswith("["):
            ipaddress.ip_address(v)        # valida IPv6 sin corchetes
    return v.strip("[]").rstrip(".").lower()

def scope_endpoints(assets: list[dict]) -> set[str]:
    """Resuelve el alcance al Contenedor_Objetivo; incluye el host EC2 solo si está autorizado.

    Req 11.4, 12.2, 12.3: el objetivo autorizado es el contenedor/servicio
    (target_host/target_hostname); el ec2_host anfitrión queda fuera de alcance
    salvo host_is_target == true.
    """
    allowed: set[str] = set()
    for a in assets:
        for key in ("target_host", "target_hostname"):
            n = normalize_target(a.get(key, ""))
            if n:
                allowed.add(n)
        if a.get("host_is_target") is True:          # host autorizado explícitamente
            for key in ("ec2_host", "ec2_hostname"):
                n = normalize_target(a.get(key, ""))
                if n:
                    allowed.add(n)
    return allowed

def target_in_scope(target: str, assets: list[dict]) -> bool:
    t = normalize_target(target)
    return t is not None and t in scope_endpoints(assets)

def run_tool_guarded(target, assets, run_tool):
    """Ejecuta la Herramienta_Real solo si el objetivo resuelve a un Contenedor_Objetivo
    autorizado (o a un host explícitamente autorizado) de la allowlist (Req 11.2, 11.4)."""
    if not target_in_scope(target, assets):
        raise OutOfScopeError(
            f"Objetivo fuera de alcance autorizado (contenedor/servicio): {target!r}")
    return run_tool(target)
```

## Diseño de los Hooks

Los hooks viven en `.kiro/hooks/*.json` del workspace con formato independiente **`version: v1`** (Kiro CLI V3 / IDE), siguiendo el `governance.json` real del starter (Req 10.5). Los scripts se reutilizan de `agent_ethack_dfir/scripts/`.

### Hook_Autorizacion — `PreToolUse` (simulado, no bloqueante estricto)

Demuestra "Authorization First" con el patrón `EH_GRANT_PATH`: una autorización externa, fuera del workspace y custodiada por el docente. En modo **didáctico**, el hook **registra y advierte** sin abortar de forma dura el ejercicio (Req 10.1, 10.2, 10.3).

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "autorizacion-simulada-pretool",
      "trigger": "PreToolUse",
      "matcher": "@mcp",
      "action": { "type": "command", "command": "python3 agent_ethack_dfir/scripts/gate_mcp_sim.py" },
      "timeout": 10
    },
    {
      "name": "auditoria-posttool",
      "trigger": "PostToolUse",
      "matcher": "@mcp",
      "action": { "type": "command", "command": "python3 agent_ethack_dfir/scripts/audit_event.py" },
      "timeout": 10
    }
  ]
}
```

Diferencia con el starter (`gate_mcp.py`, fail-closed → `exit 2`): la variante **simulada** del aula emite una advertencia didáctica y **no bloquea** (`exit 0`), conservando el mismo registro de evaluación (herramienta + objetivo + resultado de cada condición).

```python
# agent_ethack_dfir/scripts/gate_mcp_sim.py  — variante DIDÁCTICA, no bloqueante (Req 10.1–10.3)
import datetime, json, os, sys
from pathlib import Path

def warn(msg):  # advertencia didáctica, NO bloquea
    print(f"[AUTORIZACIÓN SIMULADA] {msg}", file=sys.stderr)

def evaluate(evt):
    tool = evt.get("tool_name", "")
    params = evt.get("tool_input", {}) if isinstance(evt.get("tool_input"), dict) else {}
    target = next((params[k] for k in ("target","host","hostname","domain","url") if k in params), None)
    reasons = {}
    path = os.environ.get("EH_GRANT_PATH")
    grant = {}
    if path and os.path.isabs(path) and os.path.exists(path):
        try: grant = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError): reasons["grant_legible"] = False
    else:
        reasons["grant_presente"] = False
    reasons["aprobado"] = grant.get("status") == "approved"
    reasons["tool_permitido"] = tool in (grant.get("allowed_tools") or {})
    cubre = reasons["tool_permitido"] and target in (
        (grant.get("allowed_tools", {}).get(tool, {}) or {}).get("targets", []))
    reasons["objetivo_cubierto"] = bool(cubre)
    return tool, target, reasons

def main():
    try: evt = json.load(sys.stdin)
    except (ValueError, UnicodeDecodeError): warn("evento JSON inválido"); return 0
    tool, target, reasons = evaluate(evt)
    autorizado = all(reasons.values())
    record = {"time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "tool": tool, "target": target, "reasons": reasons, "authorized": autorizado}
    Path("local-audit").mkdir(exist_ok=True)
    (Path("local-audit") / "authz.jsonl").open("a", encoding="utf-8").write(
        json.dumps(record, ensure_ascii=False) + "\n")
    if not autorizado:
        warn(f"'{tool}' sobre '{target}' no está cubierto por la autorización simulada. "
             "En producción esto se bloquearía (fail-closed).")
    return 0   # modo didáctico: nunca bloquea

if __name__ == "__main__":
    sys.exit(main())
```

### Hook_Auditoria — `PostToolUse` (resumen + hash + modo)

Se reutiliza `audit_event.py` del starter, extendido con un campo **`mode`** que captura el Modo_Ejecucion aplicado por el Power en esa invocación (Req 14.6). El registro mantiene `time_utc`, evento, herramienta y **`sha256`** del evento serializado en `local-audit/events.jsonl` (Req 10.4). El registro es trazabilidad didáctica, no evidencia forense inmutable; la evidencia forense real se preserva aparte (Req 5.4, 5.5).

El Power expone el modo aplicado en su registro de ejecución (p. ej. en `tool_input.Modo_Ejecucion` o en un campo `mode` del evento) y el Hook_Auditoria lo propaga al record. Si el evento no trae modo, se asume el default `script-kiddie` para la anotación.

```python
# agent_ethack_dfir/scripts/audit_event.py  — extensión: anota el Modo_Ejecucion aplicado (Req 14.6)
import datetime, hashlib, json, sys
from pathlib import Path

DEFAULT_MODE = "script-kiddie"

def extract_mode(evt: dict) -> str:
    """Modo_Ejecucion aplicado; cae al default si el evento no lo declara (Req 14.2, 14.6)."""
    ti = evt.get("tool_input") if isinstance(evt.get("tool_input"), dict) else {}
    return evt.get("mode") or ti.get("Modo_Ejecucion") or DEFAULT_MODE

def main() -> int:
    try:
        evt = json.load(sys.stdin)
    except (ValueError, UnicodeDecodeError):
        return 0
    payload = json.dumps(evt, ensure_ascii=False, sort_keys=True)
    record = {
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tool": evt.get("tool_name", ""),
        "mode": extract_mode(evt),                 # Modo_Ejecucion aplicado  Req 14.6
        "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),  # Req 10.4
    }
    Path("local-audit").mkdir(exist_ok=True)
    (Path("local-audit") / "events.jsonl").open("a", encoding="utf-8").write(
        json.dumps(record, ensure_ascii=False) + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Data Models

Todo el estado operativo vive bajo `agent_ethack_dfir/engagements/<id>/`, siguiendo el starter.

### Allowlist_Objetivos — `scope.yaml`

Única fuente de objetivos válidos (Req 6.3, 11.1, 12.3, 12.5). Cada asset modela el **Contenedor_Objetivo** (unidad de la prueba de penetración) sobre su **host EC2 Debian anfitrión**. El host se declara como **no-objetivo** (`host_is_target: false`) salvo que se autorice explícitamente; así la guardia dirige la actividad al contenedor/servicio y se abstiene de explotar el host subyacente (Req 11.4, 12.2, 12.3).

```yaml
engagement_id: dvwa-lab-ulsa
owner: lider-tecnico
status: approved          # draft | approved | closed
assets:                   # Allowlist_Objetivos: Contenedores_Objetivo autorizados  Req 12.3, 12.5
  - id: dvwa-01
    kind: container                      # unidad objetivo = Contenedor_Objetivo  Req 12.2
    service: dvwa-web
    # --- objetivo autorizado: el contenedor/servicio ---
    target_host: 10.0.10.21              # endpoint por el que se alcanza el servicio
    target_hostname: dvwa-01.lab.ulsa
    target_port: 8080                    # puerto publicado del contenedor
    container_id: dvwa_web_1             # identificador del contenedor Docker
    container_image: vulnerables/web-dvwa
    # --- host EC2 anfitrión: NO-objetivo salvo autorización explícita  Req 11.4, 12.3 ---
    ec2_host: 10.0.10.21
    ec2_hostname: ec2-dvwa-01.lab.ulsa
    host_is_target: false                # true solo si la Allowlist autoriza el host
    source_case: ethicalhacking          # caso de referencia  Req 12.4
authorized_window: { start: "2026-02-01T00:00:00Z", end: "2026-06-30T23:59:59Z" }
ethical_principles:       # Req 6.4, 11.4
  - authorization-first
  - scope-discipline
  - do-no-harm
  - confidentiality
  - full-disclosure
  - legal-compliance
prohibited_actions:
  - acceder_a_produccion
  - persistencia_oculta
  - exfiltracion
  - denegacion_de_servicio
```

Agregar/retirar un Contenedor_Objetivo o un nodo del Entorno_Laboratorio actualiza `assets` para reflejar los objetivos vigentes (Req 12.6).

### Estado del engagement — `state.json`

Extiende el `state.json` del starter con las fases completadas (para la lógica de orden del Orquestador, Req 1.3, 1.5).

```json
{
  "engagement_id": "dvwa-lab-ulsa",
  "status": "active",
  "phase": "Scanning",
  "completed_phases": ["Reconnaissance"],
  "ooda_phase": "OBSERVE",
  "iteration": 2,
  "findings": [],
  "last_evidence": null,
  "human_review": "approved",
  "incident_response": {
    "active_incident": "inc-0001",
    "nist_phase": "Detection & Analysis",
    "ir_iteration": 1
  }
}
```

El bloque `incident_response` enlaza el estado del engagement con el registro de incidente activo y la **fase NIST actual** del Proceso_Respuesta_Incidentes (Req 18.2). `nist_phase` toma uno de `{Preparation, Detection & Analysis, Containment, Eradication & Recovery, Post-Incident Activity}`; `ir_iteration` cuenta las vueltas del ciclo iterativo de investigación (Req 18.5, 18.7).

### Inventario de entregables — `inventory.json`

Asocia cada Power / custom agent con su fase o etapa y su responsable (Req 8.4, 13.2, 13.4). Es la fuente de la verificación de cobertura (Req 8.3).

`inventory.json` **no se edita a mano**: lo produce el **Catalogador**, un componente **reutilizable** implementado en `agent_ethack_dfir/scripts/catalog.py` cuya función `build_inventory(powers_root, assets)` recorre el árbol `powers/` y devuelve un objeto de inventario. El Catalogador cumple dos roles con el mismo código: (a) genera la **línea base inicial** (`baseline`) del inventario a partir de los Powers base ya presentes en el workspace, y (b) **regenera** `inventory.json` de forma determinista en **cada validación** — es el mismo `build_inventory()` que invocan `make validate` (paso 4 de la Validacion_Local) y `make catalog`. No es un catalogado único de una sola vez: cada corrida recalcula el inventario completo desde el árbol `powers/`, de modo que los Powers base de la `baseline` y los Powers nuevos de los alumnos quedan representados por igual.

**Descubrimiento de ambos layouts.** El árbol `powers/` mezcla dos layouts y `build_inventory` descubre **ambos** detectando dónde hay `plugin.json` o `POWER.md`:

- **Powers base** (los 9 del workspace, p. ej. `osint-passive-recon`, `exploitation-metasploit`, `dfir-linux`, `grc-nist-csf`): viven en **un nivel**, `powers/<nombre>/`, usan **`POWER.md`** (verificado en disco) y forman la `baseline`.
- **Powers de alumnos**: viven en **dos niveles**, `powers/<equipo>/<power>/` (aislamiento por equipo/alumno, Req 20.4), y usan `POWER.md` o `plugin.json`.

El Catalogador recorre tanto `powers/*/` como `powers/*/*/` y considera Power a toda carpeta que contenga `plugin.json` o `POWER.md` (sin anidar uno dentro de otro). Así, la cobertura de fases/etapas (Req 8.3, 13.3) y el conteo por alumno (Req 9.6) cuentan por igual los Powers base y los nuevos.

**Nota (baseline y `x-ethack`).** Los 9 `POWER.md` base **no** declaraban originalmente el bloque de contrato `x-ethack`; el proyecto lo **añade a su frontmatter** (ver la subtarea de baseline en `tasks.md`) para que validen por contrato igual que los Powers nuevos. Mientras esa subtarea no se complete, el Catalogador cubre los Powers base mediante un **mapeo de conocimiento** (fase/etapa y herramientas conocidas por nombre de Power), de modo que la `baseline` y la cobertura permanecen correctas.

**Cobertura y conteo como métodos del inventario.** La lógica de cobertura de fases/etapas y el conteo de ≥2 Powers con Herramienta_Real por alumno son **métodos del propio objeto de inventario** que produce el Catalogador (p. ej. `inv.coverage_gaps()` sobre las 5 fases EC-Council ∪ 6 etapas del Flujo_Investigacion, e `inv.count_tooled_by_owner()` por campo `owner`). No son lógica de las tareas de test: el agregador de la Validacion_Local **invoca** estos métodos (pasos 5 y 6), y las tareas de test opcionales (p. ej. 13.3 cobertura y 14.2) solo **verifican** este comportamiento, sin reimplementarlo. La cobertura y el conteo quedan disponibles siempre que exista el inventario, al margen de que se escriban o no esas pruebas.

```json
{
  "engagement_id": "dvwa-lab-ulsa",
  "powers": [
    { "name": "scanning-nmap-services", "team": "red-team", "owner": "alumno-2",
      "ecCouncilPhase": "Scanning", "forensicsStage": null,
      "tools": ["nmap"], "invokedBy": ["subagente-scanning", "subagente-red-team"],
      "executionModes": ["script-kiddie", "green-hat", "pro"],   // Req 14.1
      "docStatus": {                                             // Artefactos_Documentacion  Req 15.5, 15.6
        "root": "powers/red-team/scanning-nmap-services/docs",
        "prompt": true, "sessions": true, "feedback": true,
        "complete": true, "missing": []
      }
    }
  ],
  "agents": [
    { "name": "subagente-scanning", "kind": "phase", "represents": "Scanning" }
  ]
}
```

### Registro de evidencia y Cadena_Custodia

Cada pieza de evidencia recolectada registra su hash (Req 5.3) y cada traspaso/transformación se encadena (Req 5.4). El encadenamiento enlaza cada eslabón con el hash del estado anterior, de modo que recorrer la cadena reconstruye el orden de custodia.

```json
// agent_ethack_dfir/engagements/<id>/evidence/<evidence-id>/record.json
{
  "evidence_id": "mem-dvwa-01-0001",
  "source_asset": "dvwa-01",
  "collected_by": "alumno-df-1",
  "collected_at_utc": "2026-03-10T14:03:22Z",
  "tool": "LiME",
  "sha256": "9f2c…",                         // hash de verificación  Req 5.3
  "storage": "append-only://evidence/mem-dvwa-01-0001/dump.lime"
}
```

```json
// agent_ethack_dfir/engagements/<id>/evidence/<evidence-id>/chain_of_custody.jsonl  (una línea por traspaso)
{ "seq": 0, "action": "collect",  "actor": "alumno-df-1", "ts_utc": "2026-03-10T14:03:22Z",
  "sha256": "9f2c…", "prev_sha256": null }
{ "seq": 1, "action": "transfer", "actor": "alumno-df-2", "ts_utc": "2026-03-10T15:10:00Z",
  "sha256": "9f2c…", "prev_sha256": "9f2c…", "link": "sha256(seq0)" }
{ "seq": 2, "action": "analyze",  "actor": "alumno-df-3", "ts_utc": "2026-03-11T09:00:00Z",
  "sha256": "9f2c…", "prev_sha256": "9f2c…", "note": "análisis sobre copia; original intacto" }
```

Para soportar Documentation/Reproducibility (Req 16.4), cada `record.json` de evidencia incluye además el **comando** ejecutado, la **hora UTC**, la **herramienta y su versión** y el **resultado**, y un campo `volatility_rank` (1–7, RFC 3227) que fija su posición en el Orden_Volatilidad de la fase Collect (Req 5.6, 16.1).

Invariantes del modelo forense:
- `collect` registra el hash de verificación (Req 5.3).
- En la fase Collect, el orden de recolección respeta el `volatility_rank` de lo más volátil (1) a lo menos volátil (7), RFC 3227 (Req 5.6, 16.1).
- Operaciones de análisis conservan `sha256` del original idéntico (`prev == actual`) y operan sobre copia (Req 5.5, 16.2).
- Cada eslabón `seq > 0` referencia el eslabón anterior (`prev_sha256`/`link`) (Req 5.4, 16.3).
- Evidencia de un Contenedor_Objetivo: recolección automatizada antes de que el contenedor efímero desaparezca (Req 5.9, 16.8).
- El reporte forense (Req 5.10) renderiza hallazgos + `record.json` + `chain_of_custody.jsonl` + IOCs/TTPs.

### Registro de incidente — `incidents/<incident-id>/incident.json`

El Incident Responder mantiene un **registro de incidente** por cada incidente gestionado, que captura la fase NIST actual, los IOCs (con su formato y mapeo a MITRE ATT&CK / Cyber Kill Chain), las acciones de contención clasificadas corto/largo plazo, los escalamientos y los enlaces a la evidencia preservada por DF (Req 7.7, 7.8, 7.9, 18.2, 18.5, 18.9, 18.10).

```json
// agent_ethack_dfir/engagements/<id>/incidents/inc-0001/incident.json
{
  "incident_id": "inc-0001",
  "engagement_id": "dvwa-lab-ulsa",
  "opened_at_utc": "2026-03-10T13:31:00Z",
  "nist_phase": "Containment, Eradication & Recovery",   // fase NIST actual  Req 18.2
  "phase_history": [                                      // carácter cíclico/iterativo  Req 18.5, 18.7
    { "phase": "Preparation",            "entered_utc": "2026-02-01T00:00:00Z" },
    { "phase": "Detection & Analysis",   "entered_utc": "2026-03-10T13:31:00Z" },
    { "phase": "Containment, Eradication & Recovery", "entered_utc": "2026-03-10T14:00:00Z" }
  ],
  "detection_source": "blue-team",                        // se nutre del Blue Team  Req 18.4, 18.8
  "timeline": [
    { "ts_utc": "2026-03-10T13:31:00Z", "host": "dvwa-01", "event": "SQLi detectada en DVWA", "source": "waf-log" }
  ],
  "iocs": [                                               // Req 18.9, 18.10
    {
      "ioc_id": "ioc-01",
      "type": "ipv4-addr",
      "value": "203.0.113.50",
      "format": "STIX",                                   // STIX | YARA | OpenIOC  Req 18.9
      "kill_chain_stage": "Command and Control",          // Cyber Kill Chain  Req 18.10
      "attack": { "tactic": "Command and Control", "technique": "T1071" }  // MITRE ATT&CK  Req 18.10
    }
  ],
  "containment_actions": [                                // clasificación corto/largo plazo  Req 7.7, 18.5
    { "action": "aislar Contenedor_Objetivo (SG cuarentena + NACL)", "type": "short-term",
      "shutdown": false, "preserves_evidence": true, "ts_utc": "2026-03-10T14:00:00Z" },
    { "action": "rotar credenciales y aplicar parche", "type": "long-term",
      "shutdown": false, "preserves_evidence": false, "ts_utc": "2026-03-11T10:00:00Z" }
  ],
  "escalations": [                                        // movimiento lateral  Req 7.9, 18.5
    { "reason": "AssumeRole hacia otra cuenta", "to": "cloud-ops", "ts_utc": "2026-03-10T15:00:00Z" }
  ],
  "evidence_refs": ["mem-dvwa-01-0001"],                  // notificación a DF  Req 7.4, 18.8
  "csf_subcategories": ["RS.AN", "RS.MI", "RC.RP"],       // alineación CSF  Req 19.7
  "post_incident": { "report": null, "lessons_learned": [] }  // Req 18.6, 18.7
}
```

Invariantes del registro de incidente:
- `nist_phase` ∈ las cuatro fases de NIST SP 800-61 y `phase_history` registra cada entrada de fase; las lecciones de Post-Incident retroalimentan Preparation (ciclo), lo que verifica la Property 16 (Req 18.2, 18.7).
- Cada acción de `containment_actions` se clasifica como `short-term` o `long-term`; una acción `short-term` **no apaga** el sistema (`shutdown == false`) y **preserva evidencia** (`preserves_evidence == true`) (Req 7.7, 18.5, Property 16).
- Cada IOC declara un `format` ∈ `{STIX, YARA, OpenIOC}` y un mapeo a MITRE ATT&CK y a una etapa de la Cyber Kill Chain (Req 18.9, 18.10).

### Artefactos GRC — `grc/risk_register.json` y `grc/csf_profile.json`

El Responsable_GRC mantiene dos artefactos ligados al engagement: el **Registro_Riesgos** y el **Perfil_CSF** (Req 6.7–6.10, 19.3–19.5).

```json
// agent_ethack_dfir/engagements/<id>/grc/risk_register.json
{
  "engagement_id": "dvwa-lab-ulsa",
  "risk_appetite": { "max_residual_score": 8, "scale": "5x5 (prob x impacto)" },  // Apetito_Riesgo  Req 6.8
  "risks": [
    {
      "risk_id": "r-01",
      "description": "SQLi en DVWA permite exfiltración de datos de clientes",
      "owner": "lider-tecnico",                 // dueño  Req 6.7
      "probability": 4,
      "impact": 4,
      "inherent_score": 16,
      "treatment": "mitigar",                   // mitigar | transferir | aceptar | evitar  Req 6.7
      "residual_probability": 2,
      "residual_impact": 4,
      "residual_score": 8,                      // riesgo residual  Req 6.7
      "within_appetite": true,                  // residual_score <= max_residual_score  Req 6.8 (Property 17)
      "csf_subcategory": "ID.RA",               // método estandarizado GV.RM-06  Req 19.3
      "evidence_refs": ["finding-redteam-07"],  // hallazgo técnico como evidencia  Req 6.10, 19.6
      "source_gap": "poam-03"                   // brecha que originó el riesgo  Req 19.5
    }
  ]
}
```

```json
// agent_ethack_dfir/engagements/<id>/grc/csf_profile.json
{
  "engagement_id": "dvwa-lab-ulsa",
  "target_tier": 3,                             // Tier objetivo 1-4  Req 19.4
  "subcategories": [                            // perfil actual vs objetivo por subcategoría  Req 6.9, 19.4
    { "id": "ID.RA", "current": "partial", "target": "achieved", "gap": true,  "evidence_refs": ["finding-va-02"] },
    { "id": "DE.CM", "current": "achieved", "target": "achieved", "gap": false, "evidence_refs": ["finding-blue-01"] },
    { "id": "RS.AN", "current": "partial", "target": "achieved", "gap": true,  "evidence_refs": ["mem-dvwa-01-0001"] }
  ],
  "poam": [                                     // POA_M: una entrada por subcategoría con brecha  Req 6.9, 19.5
    { "poam_id": "poam-03", "csf_subcategory": "ID.RA", "milestone": "parchar y validar", "risk_id": "r-01" },
    { "poam_id": "poam-04", "csf_subcategory": "RS.AN", "milestone": "automatizar preservación", "risk_id": "r-02" }
  ]
}
```

Invariantes de los artefactos GRC:
- Para cada riesgo, `within_appetite == (residual_score <= risk_appetite.max_residual_score)`, y el Responsable_GRC verifica el riesgo residual dentro del Apetito_Riesgo al registrarlo (Req 6.8, Property 17).
- El conjunto de subcategorías del POA&M es **exactamente** el conjunto de subcategorías con `gap == true` del Perfil_CSF; cada brecha genera además un riesgo en el Registro_Riesgos (Req 6.9, 19.5, Property 17).
- Todo hallazgo técnico (Red/Blue/DF/VA) referenciado queda vinculado a una subcategoría CSF como evidencia (Req 6.10, 19.2, 19.6).

## Organización de carpetas y convenciones de integración

Estructura del proyecto integrado, pensada para que el **Líder Técnico** incorpore los Powers de los 13 alumnos (Req 8, 13.1).

```
ethicalforensic/                         # workspace raíz
├── .kiro/
│   ├── hooks/                           # version v1: autorización simulada + auditoría  Req 10
│   └── specs/ethical-hacking-forensics-agent/
├── agent_ethack_dfir/agents/                              # custom agents (Kiro)
│   ├── orquestador/                     # Agente_Orquestador
│   ├── fases/                           # 5 subagentes de fase
│   └── roles/                           # Red, Blue, DF, GRC, IR
├── powers/                              # Powers base + nuevos de alumnos
│   ├── osint-passive-recon/  footprinting-enumeration/
│   ├── exploitation-metasploit/  vulnerability-assessment/
│   └── <equipo>/<power-de-alumno>/      # plugin.json + skills/ + steering/
├── agent_ethack_dfir/scripts/                             # gate_mcp_sim.py, audit_event.py, …
└── agent_ethack_dfir/engagements/<id>/                    # scope.yaml, state.json, inventory.json, evidence/,
                                         # incidents/<id>/incident.json (IR, Req 18),
                                         # grc/risk_register.json + grc/csf_profile.json (GRC, Req 19)
```

### Convención de integración de Powers (Líder Técnico)

Flujo de aceptación de un entregable (Req 8.2, 8.3, 8.4, 13.2, 13.3):

1. El alumno entrega un Power con `plugin.json` + `skills/` + `steering/` y el bloque `x-ethack` completo.
2. El Líder Técnico valida contra el **modelo de Powers**:
   - esquema de `plugin.json` válido y `x-ethack` presente;
   - `tools` no vacío y `ecCouncilPhase` xor `forensicsStage`;
   - `allowlistValidation.required == true` apuntando al `scope.yaml` del engagement;
   - `executionMode.allowed == {script-kiddie, green-hat, pro}` con default `script-kiddie` (Req 14.1, 14.2);
   - presencia de los **Artefactos_Documentacion** bajo `docs/` (`prompt.md`, `sessions/`, `feedback.md`) (Req 15.1).
3. Si cumple, se copia a `powers/<equipo>/` y se **registra** en `inventory.json` asociándolo a su fase/etapa, su subagente invocador, su responsable y el **estado de documentación** (`docStatus`) (Req 8.2, 13.2, 13.4, 15.5).
4. Al incorporar el Power, el Líder Técnico **calcula `docStatus`**: marca cada artefacto presente/ausente y, si falta alguno, deja `complete: false` con la lista `missing` y **señala los artefactos faltantes** (Req 15.6). La integración procede, pero el Power queda marcado como documentación incompleta hasta que se complete.
5. Cuando todos los entregables de una fase están integrados, el Orquestador **habilita** esa fase (Req 13.3).
6. Si un entregable **no cumple** el modelo o la política ética, el Líder Técnico **rechaza** la integración e indica el incumplimiento (Req 8.4). El Power no se añade al inventario.

```python
# agent_ethack_dfir/scripts/check_power_docs.py  — señala Artefactos_Documentacion faltantes al integrar (Req 15.6)
from pathlib import Path

REQUIRED = ("prompt.md", "sessions", "feedback.md")

def doc_status(power_dir: Path) -> dict:
    docs = power_dir / "docs"
    present = {name: (docs / name).exists() for name in REQUIRED}
    missing = [name for name, ok in present.items() if not ok]
    return {
        "root": str(docs),
        "prompt": present["prompt.md"],
        "sessions": present["sessions"],
        "feedback": present["feedback.md"],
        "complete": not missing,
        "missing": missing,          # artefactos faltantes señalados al integrar  Req 15.6
    }
```

Organización de 13 alumnos por equipo/rol (Req 13.1): Red Team (3) · Blue Team (3) · Digital Forensics (4) · GRC (1) · Incident Responder (1) · Líder Técnico (1). Cada alumno aporta ≥2 Powers con Herramienta_Real (Req 9.6, 3.2, 4.2, 5.2, 6.2, 7.2).

## Política ética y seguridad de laboratorio como controles de diseño

Los Principios_Eticos se materializan como controles concretos del sistema, no como texto aspiracional (Req 11.4).

| Principio | Control de diseño | Dónde | Req |
|---|---|---|---|
| Authorization First | `EH_GRANT_PATH` + Hook_Autorizacion `PreToolUse`; `scope.yaml.status == approved` | hooks, scope.yaml | 10, 11.1 |
| Scope Discipline | Guardia de Allowlist_Objetivos en cada Power (resuelve al Contenedor_Objetivo; host EC2 no-objetivo salvo autorización); `prohibited_actions` | `validate_target.py`, scope.yaml | 9.5, 11.2, 11.4, 11.5 |
| Do No Harm | Forense sobre copias (`hash_pre == hash_post`); PoC limitada en Gaining Access; `prohibited_actions` incluye DoS/exfiltración | Powers forenses/ofensivos | 5.5, 2.4 |
| Confidentiality | Ofuscación de datos sensibles en reportes; evidencia en almacén protegido | reportes, evidence/ | 11.7 |
| Full Disclosure | Hallazgos reportados completos y honestos; fallos de herramienta documentados | reportes, auditoría | 11.6 |
| Legal Compliance | Actividad restringida al Entorno_Laboratorio; todo fuera del lab se trata como producción no autorizada | Orquestador + Powers | 11.3 |

Reglas duras de laboratorio:
- **Nunca producción.** Cualquier objetivo que no esté en la Allowlist_Objetivos se trata como producción no autorizada y el sistema se abstiene (Req 11.3, 11.2).
- **Alcance vigente por engagement.** Mientras un engagement está activo, la actividad se mantiene dentro de `scope.yaml.assets` y `authorized_window` (Req 11.5).
- **Objetivos solo del lab.** La Allowlist enumera exclusivamente los Contenedores_Objetivo (DVWA y servicios vulnerables) desplegados en Docker sobre nodos EC2 Debian de los casos de referencia (Req 12.1, 12.2, 12.5).
- **Contenedor, no host.** Toda prueba de penetración apunta al Contenedor_Objetivo que expone el servicio; el host EC2 anfitrión no es objetivo salvo que `host_is_target: true` lo autorice explícitamente en la Allowlist (Req 11.4, 12.3).

## Error Handling

| Condición | Manejo | Req |
|---|---|---|
| Objetivo fuera de la Allowlist_Objetivos | El Power lanza `OutOfScopeError`, no ejecuta la herramienta, informa alcance autorizado | 11.2 |
| Fase solicitada fuera de orden | El Orquestador registra la solicitud, lista fases previas no completadas, luego decide delegar | 1.5 |
| `EH_GRANT_PATH` ausente o grant no aprobado | Hook simulado emite advertencia didáctica y continúa (no bloquea); registra el motivo | 10.2 |
| Herramienta real falla o devuelve vacío | Se documenta el fallo en el registro/reporte; no se inventan datos (Full Disclosure) | 11.6 |
| Evidencia alterada (`hash_pre != hash_post`) | El Power forense marca la pieza como comprometida y lo registra en la cadena de custodia | 5.5 |
| Entregable no conforme al modelo | Líder Técnico rechaza, no se añade al inventario, se indica el incumplimiento | 8.4 |
| Objetivo ambiguo (0 o >1 parámetros de destino) | La guardia exige destino explícito y único antes de ejecutar | 9.5 |

## Correctness Properties

*Una propiedad es una característica o comportamiento que debe cumplirse en todas las ejecuciones válidas del sistema — una afirmación formal sobre lo que el sistema debe hacer. Las propiedades son el puente entre la especificación legible por humanos y las garantías de corrección verificables por máquina.*

### Property 1: Guardia de alcance de la Allowlist_Objetivos

*Para todo* objetivo y *para toda* Allowlist_Objetivos, un Power ejecuta su Herramienta_Real si y solo si el objetivo normalizado pertenece al conjunto normalizado de la allowlist; cualquier objetivo fuera de la allowlist es rechazado sin ejecutar la herramienta.

**Validates: Requirements 9.5, 11.1, 11.2, 11.3, 11.4**

### Property 2: Secuencia canónica de fases por defecto

*Para toda* fase del ciclo EC-Council, la fase "siguiente" por defecto que ofrece el Agente_Orquestador es exactamente su sucesora en la secuencia Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks, y Covering Tracks no tiene sucesora.

**Validates: Requirements 1.3**

### Property 3: Reporte de fases previas no completadas

*Para toda* fase solicitada F y *para todo* conjunto de fases completadas C, el conjunto de fases previas no completadas que reporta el Orquestador antes de delegar es exactamente las predecesoras de F en la secuencia canónica que no están en C.

**Validates: Requirements 1.5**

### Property 4: Declaración de alcance precede a la herramienta

*Para toda* traza de ejecución de un Subagente_Fase, la declaración explícita de objetivo y alcance ocurre antes de la primera invocación de una Herramienta_Real en esa tarea.

**Validates: Requirements 2.7**

### Property 5: Hash de verificación de evidencia recolectada

*Para toda* evidencia recolectada por un Power de Digital Forensics, el hash registrado en su `record.json` es igual al SHA-256 recomputado sobre el contenido de esa evidencia, y contenidos distintos producen registros de hash distinguibles.

**Validates: Requirements 5.3**

### Property 6: No alteración de la evidencia original

*Para toda* evidencia y *para toda* operación de análisis forense aplicada sobre ella, el SHA-256 de la evidencia original antes de la operación es igual al SHA-256 después de la operación. (Se complementa con la Property 15, que verifica que el análisis se realiza sobre una copia cuyo hash coincide con el del original.)

**Validates: Requirements 5.5**

### Property 7: Encadenamiento de la Cadena_Custodia

*Para toda* secuencia de traspasos/transformaciones de una pieza de evidencia, cada eslabón con `seq > 0` referencia el hash del eslabón anterior, de modo que recorrer la cadena reconstruye sin ambigüedad el orden de custodia desde la recolección.

**Validates: Requirements 5.4, 5.10, 16.3**

### Property 8: Decisión del Hook_Autorizacion

*Para todo* grant y *para todo* evento de herramienta, la evaluación del Hook_Autorizacion resulta "autorizada" si y solo si el grant está aprobado, no caducado, la herramienta está en `allowed_tools` y el objetivo declarado está entre los `targets` de esa herramienta; y el registro de evaluación siempre contiene la herramienta y el objetivo declarados.

**Validates: Requirements 10.1, 10.3**

### Property 9: Round-trip del hash de auditoría

*Para todo* evento de invocación de herramienta, el registro del Hook_Auditoria contiene un SHA-256 que, recomputado sobre el evento serializado, coincide con el almacenado, junto con la herramienta y la marca de tiempo.

**Validates: Requirements 10.4**

### Property 10: Cobertura del inventario de entregables

*Para todo* elemento del conjunto {5 fases EC-Council} ∪ {6 etapas del Flujo_Investigacion}, existe al menos un Power en el inventario cuyo campo `ecCouncilPhase`/`forensicsStage` cubre ese elemento, y todo Power del inventario declara un responsable (equipo/alumno).

**Validates: Requirements 8.3, 13.2, 13.4**

### Property 11: Round-trip de la Allowlist_Objetivos

*Para toda* secuencia de operaciones de alta y baja de nodos, consultar la pertenencia de un nodo tras las operaciones refleja el conjunto esperado; en particular, agregar un nodo y luego retirarlo devuelve la allowlist a su estado previo respecto de ese nodo.

**Validates: Requirements 12.3, 12.4**

### Property 12: Selección, validación y default del Modo_Ejecucion

*Para todo* valor solicitado de `Modo_Ejecucion`, la resolución del modo devuelve `script-kiddie` cuando la entrada es ausente o vacía, devuelve el valor normalizado cuando pertenece a `{script-kiddie, green-hat, pro}`, y rechaza la invocación (sin ejecutar la Herramienta_Real) para cualquier otro valor; el resultado siempre pertenece al conjunto admitido o es un rechazo que indica los valores admitidos.

**Validates: Requirements 14.1, 14.2, 14.7**

### Property 13: Completitud de los Artefactos_Documentacion al integrar

*Para todo* Power y *para todo* subconjunto de artefactos presentes de entre los requeridos `{prompt.md, sessions/, feedback.md}`, el estado de documentación calculado al integrar marca `complete == true` si y solo si están presentes los tres, y su lista `missing` es exactamente el conjunto de artefactos requeridos que no están presentes.

**Validates: Requirements 15.1, 15.6**

### Property 14: Orden_Volatilidad en la fase Collect

*Para toda* investigación forense y *para todo* conjunto de piezas de evidencia recolectadas en la fase Collect, la secuencia de recolección (por `collected_at_utc`) respeta el Orden_Volatilidad RFC 3227: ninguna pieza con `volatility_rank` mayor (menos volátil) se recolecta antes que una pieza con `volatility_rank` menor (más volátil); equivalentemente, la serie de `volatility_rank` en orden de recolección es monótona no decreciente.

**Validates: Requirements 5.6, 16.1**

### Property 15: Evidence Integrity — análisis sobre copia verificada

*Para toda* evidencia y *para toda* operación de análisis forense aplicada sobre ella, el análisis opera sobre una **copia** cuyo SHA-256 es igual al hash registrado del original (`hash(copia) == record.sha256`) y la evidencia original permanece intacta tras la operación. Esta propiedad extiende la Property 6 (no alteración del original): la Property 6 garantiza que el original no cambia (`hash_pre == hash_post`) y la Property 15 añade que todo análisis se realiza sobre una copia verificada por hash; juntas cubren el principio Evidence Integrity de forma transversal. (No se duplica la Property 6; se amplía con la verificación de la copia.)

**Validates: Requirements 5.5, 16.2**

### Property 16: Clasificación de contención y ciclicidad del Proceso_Respuesta_Incidentes

*Para todo* registro de incidente y *para toda* acción de contención que contenga, si la acción está clasificada como `short-term` entonces no apaga el sistema (`shutdown == false`) y preserva la evidencia (`preserves_evidence == true`), mientras que una acción `long-term` puede aplicar cambios persistentes; y *para toda* transición de fase del incidente, la fase destino pertenece a las cuatro fases de NIST SP 800-61 y el grafo de fases admite el retorno de Post-Incident Activity a Preparation (y de Recovery a Detection & Analysis cuando reaparecen IOCs), de modo que el proceso es cíclico e iterativo.

**Validates: Requirements 7.7, 18.2, 18.5, 18.7**

### Property 17: Invariante GRC — riesgo residual dentro del apetito y cobertura del POA&M

*Para todo* Registro_Riesgos y *para todo* Perfil_CSF del engagement, (a) cada riesgo cumple `within_appetite == (residual_score <= risk_appetite.max_residual_score)`, es decir el riesgo residual registrado queda dentro del Apetito_Riesgo; y (b) el conjunto de subcategorías CSF cubiertas por el POA&M es exactamente el conjunto de subcategorías con brecha (`gap == true`) del Perfil_CSF, de modo que toda brecha tiene su entrada de plan de acción y ninguna entrada del POA&M carece de brecha.

**Validates: Requirements 6.8, 6.9, 19.4, 19.5**

## Validación mediante GameDay

El sistema completo se valida funcionalmente mediante un **AWS GameDay** de seguridad con escenarios "de la brecha a la solución" (breach-to-solution) sobre incidentes activos en la nube (Req 17.1). El GameDay es la **prueba de integración end-to-end** del sistema de agentes: un incidente simulado activo recorre, de principio a fin, la orquestación, los roles, la preservación de evidencia y la contención. Es **estrategia de validación funcional, no rúbrica ni criterio de calificación** de los alumnos (Req 17.6).

### Coordinación de roles por el Agente_Orquestador

Ante un escenario de GameDay, el Agente_Orquestador coordina los Subagentes_Rol para investigar el incidente activo (Req 17.2):

1. **Red Team** reproduce o continúa la acción ofensiva acotada al Entorno_Laboratorio (Contenedor_Objetivo), generando registros consumibles (Req 3.4).
2. **Blue Team** detecta la actividad analizando logs y produce hallazgos de detección con su evidencia (Req 4.3, 4.4).
3. **Incident Responder** toma el hallazgo (fase **Detection & Analysis** de NIST SP 800-61), inicia la **contención acotada** (corto plazo: aísla el Contenedor_Objetivo sin apagarlo) y **notifica al Digital Forensics Team** para la recolección (Req 7.3, 7.4, 18.4, 18.8). El GameDay es así el escenario donde el Proceso_Respuesta_Incidentes se ejercita de principio a fin (Req 18.11).
4. **Digital Forensics** ejecuta el Flujo_Investigacion (Detect → … → Report) preservando evidencia (abajo).
5. **GRC** verifica que todo ocurra dentro del alcance autorizado (`scope.yaml`) y bajo los Principios_Eticos, y **vincula los hallazgos a subcategorías CSF** como evidencia para las líneas de defensa (Req 6.1, 6.10, 11.5, 19.6).

El rastreo de IOCs del GameDay (Req 17.4) y el mapeo kill-chain → evidencia AWS (abajo) son la misma base que el Incident Responder usa para crear/usar IOCs y mapear la actividad a MITRE ATT&CK y la Cyber Kill Chain (Req 18.9, 18.10).

El Orquestador identifica en su respuesta cada subagente invocado y el rol que representa (Req 1.6).

### Preservación de evidencia durante el GameDay

Mientras se investiga el incidente, la evidencia se preserva aplicando **Evidence Integrity** y **Chain of Custody** conforme al Requirement 16 (Req 17.3): recolección en Orden_Volatilidad (Property 14), análisis sobre copia verificada por hash con original intacto (Property 15, Property 6), encadenamiento de la cadena de custodia (Property 7) y, para recursos efímeros de contenedor, recolección automatizada antes de que desaparezcan (Req 5.9, 16.8).

### Rastreo de IOCs por análisis de logs (kill-chain → evidencia AWS)

El sistema rastrea los indicadores de compromiso (IOCs) mediante análisis de logs (Req 17.4), usando el mapeo kill-chain → evidencia en AWS de `proceso-digital-forensic.md`:

| Etapa de la kill chain | Evidencia típica en AWS a rastrear |
|---|---|
| Reconnaissance | Ráfagas de `List*`/`Describe*`, `GetCallerIdentity` desde una IP nueva |
| Initial Access | `ConsoleLogin` inusual, uso de access keys desde ubicación desconocida |
| Persistence | `CreateUser`, `CreateAccessKey`, `CreateLoginProfile`, nuevas funciones Lambda |
| Privilege Escalation | `AttachUserPolicy`, `PutUserPolicy`, `UpdateAssumeRolePolicy` |
| Lateral Movement | `AssumeRole` hacia otras cuentas, uso de nuevos servicios |
| Data Exfiltration | `GetObject` masivo en S3 (data events), tráfico saliente grande en VPC Flow Logs |

El análisis se apoya en Athena/CloudTrail sobre `event_history` y en los Powers `dfir-linux`/`network-forensics` para correlacionar logs de host y de red.

### Contención y hardening sin interrumpir servicios

Al responder, el sistema aplica contención y **hardening** de la infraestructura manteniendo disponibles los servicios afectados (Req 17.5): **aislar no es apagar**. La contención usa aislamiento de red (Security Group de cuarentena sin reglas + NACL), aislamiento del Contenedor_Objetivo, protección contra terminación de la instancia y desactivación de credenciales comprometidas, **sin apagar** el host (para preservar la RAM volátil) y **sin dar de baja** el servicio. Esto reconcilia "Do No Harm" y disponibilidad con la necesidad de preservar evidencia.

## Modelo de colaboración y entrega (GitHub fork + Pull Request, validación local)

Este modelo diseña el **Requirement 20**: cómo los 13 alumnos entregan sus Powers y cómo el Líder Técnico los integra en un único agente, usando **forks y Pull Request de GitHub** con una **única compuerta de validación local** (sin integración continua remota). Reutiliza, sin modificarlos, el **modelo estándar de Power** (`plugin.json`/`POWER.md` + `x-ethack` + `skills/` + `steering/` + `docs/`), la **convención de integración del Líder Técnico** (Req 8), la **organización por equipos/roles** (Req 13) y los **Artefactos_Documentacion** (Req 15). Se inspira en el flujo del ejercicio **FlowSync** (fork + `upstream` + rama propia + PR hacia arriba), adaptado a este proyecto.

### Topología de tres niveles (fork + upstream + Pull Request)

La colaboración se organiza en tres niveles. El docente posee el **Repositorio_Base** (upstream autoritativo con la estructura del agente); el Líder Técnico mantiene el **Repositorio_Integracion** como **fork** del Repositorio_Base (es el repo de la clase donde se integra todo); cada alumno mantiene un **Fork_Alumno** creado a partir del Repositorio_Integracion. Los alumnos **no tienen permiso de escritura** sobre el Repositorio_Integracion: contribuyen **solo por Pull_Request** desde su fork hacia él (Req 20.1, 20.2).

```
                 ┌───────────────────────────────────────────────┐
                 │  Repositorio_Base  (DOCENTE, upstream)         │   Req 20.1
                 │  estructura del agente: agent_ethack_dfir/agents/ powers/ …      │
                 └───────────────────────┬───────────────────────┘
          fork del Líder Técnico         │  sync upstream (docente → integración)
                                         ▼                        Req 20.10
                 ┌───────────────────────────────────────────────┐
                 │  Repositorio_Integracion (LÍDER TÉCNICO, fork) │   Req 20.1
                 │  repo de la clase · recibe todos los PR        │
                 │  merge solo tras `make validate` + revisión    │   Req 20.7, 20.8
                 └───▲───────────▲───────────▲───────────▲────────┘
    Pull_Request     │           │           │           │   (sin acceso de escritura directa)  Req 20.2
    hacia arriba     │           │           │           │
                 ┌───┴───┐   ┌───┴───┐   ┌───┴───┐   ┌───┴───┐
                 │Fork_  │   │Fork_  │   │Fork_  │   │Fork_  │     … (un fork por alumno)   Req 20.1
                 │Alumno1│   │Alumno2│   │Alumno3│   │AlumnoN│
                 └───┬───┘   └───────┘   └───────┘   └───────┘
   sync integración  │  (integración → fork)                                             Req 20.10
   → fork            ▼
                 rama propia  power/<equipo>-<iniciales>-<nombre-power>                  Req 20.3
```

Analogía con FlowSync: el Repositorio_Base hace de `upstream`, el Fork_Alumno hace del fork personal, la rama propia es la rama de trabajo del ejercicio, y la contribución viaja "hacia arriba" por PR. La diferencia es el **nivel intermedio** (Repositorio_Integracion) que concentra la integración de la clase.

### Convenciones de ramas y sincronización

**Rama propia (nunca sobre la base).** El alumno trabaja en una rama con el patrón `power/<equipo>-<iniciales>-<nombre-power>` y se abstiene de trabajar sobre la rama base o de partida (`main`/`mainline`) (Req 20.3). Ejemplos: `power/red-team-jrp-scanning-nmap-services`, `power/df-amc-memory-volatility`.

**Sincronización upstream en dos saltos** (Req 20.10):

| Salto | Quién | Qué hace | Comando típico |
|---|---|---|---|
| docente → integración | **Líder Técnico** | incorpora al Repositorio_Integracion las actualizaciones del Repositorio_Base | `git fetch upstream && git merge upstream/main` (o `rebase`) y publica en su fork |
| integración → fork | **Alumno** | sincroniza su Fork_Alumno con el Repositorio_Integracion antes de ramificar/abrir PR | `git fetch upstream && git merge upstream/main` sobre su fork (donde `upstream` = Repositorio_Integracion) |

Para el alumno, `origin` es su Fork_Alumno y `upstream` es el Repositorio_Integracion; para el Líder Técnico, `origin` es el Repositorio_Integracion y `upstream` es el Repositorio_Base. Sincronizar **antes** de ramificar reduce conflictos en el PR (mismo hábito que el `git pull upstream` de FlowSync).

### Aislamiento por carpetas y propiedad (CODEOWNERS)

Para que 13 alumnos trabajen en paralelo sin pisarse, cada Power vive **aislado en su propia carpeta** `powers/<equipo>/<power>/` (Req 20.4), coherente con la organización ya descrita en "Organización de carpetas y convenciones de integración". Un archivo **CODEOWNERS** asigna cada ruta a su alumno/equipo responsable; las **rutas compartidas** (orquestador/subagentes, scripts, engagements) pertenecen al Líder Técnico y al docente, de modo que un PR que las toque requiere su revisión (Req 20.4).

Regla clave anti-conflictos: **`inventory.json` no se edita a mano**. Lo **genera el Catalogador** (`agent_ethack_dfir/scripts/catalog.py`, `build_inventory()`) a partir del árbol `powers/`, recorriendo tanto el layout de un nivel de los Powers base (`powers/<nombre>/`) como el de dos niveles de los alumnos (`powers/<equipo>/<power>/`) (Req 20.9). Así, el inventario —archivo compartido y de alta colisión— deja de ser fuente de conflictos de merge: cada alumno solo añade ficheros bajo su carpeta y el inventario se recalcula de forma determinista en cada `make validate`/`make catalog` (ver "Inventario de entregables" y "Catalogador" en la Validacion_Local).

Ejemplo breve de `CODEOWNERS` (en la raíz del Repositorio_Integracion):

```
# Rutas compartidas: orquestador, subagentes, scripts y engagements → Líder Técnico + docente
/agents/orquestador/      @lider-tecnico @docente
/agents/                  @lider-tecnico @docente
/scripts/                 @lider-tecnico @docente
/engagements/             @lider-tecnico @docente
# inventory.json es GENERADO por el Catalogador; no se edita a mano (Req 20.9)
/engagements/*/inventory.json  @lider-tecnico @docente

# Carpetas de Power por equipo/alumno (propiedad del responsable)
/powers/red-team/scanning-nmap-services/     @alumno-jrp
/powers/df/memory-volatility/                @alumno-amc
/powers/blue-team/                           @equipo-blue
# … una entrada por Power/alumno; la última coincidencia gana en CODEOWNERS
```

### Contrato del Pull_Request (qué debe traer)

Un Pull_Request de entrega de un Power **debe** incluir, dentro de `powers/<equipo>/<power>/` (Req 20.5, reutiliza Req 8 y Req 15):

- **El Power**: `plugin.json` **o** `POWER.md` con el bloque de contrato **`x-ethack`** completo (fase/etapa, `tools` no vacío, `allowlistValidation`, `executionMode`, `documentation`).
- **`skills/`** y **`steering/`** del Power.
- **Artefactos_Documentacion** bajo `docs/` (Req 15): `docs/prompt.md`, `docs/sessions/` y `docs/feedback.md`.

El PR **no** incluye ediciones manuales de `inventory.json` ni de rutas compartidas salvo que el cambio lo exija y lo apruebe un CODEOWNER (Req 20.9, 20.4).

Plantilla breve de descripción/checklist de PR (equivalente adaptado al `prompts.md` + checklist de FlowSync). Se sugiere versionarla en `.github/pull_request_template.md` del Repositorio_Integracion:

```markdown
## Entrega de Power — <equipo>/<nombre-power>
- Alumno / iniciales: <nombre> (<iniciales>)
- Rol / equipo: <red-team|blue-team|df|grc|ir>
- Rama: power/<equipo>-<iniciales>-<nombre-power>
- Fase EC-Council o etapa del Flujo_Investigacion que cubre: <…>
- Herramienta(s) real(es) envuelta(s): <nmap|volatility|…>

## Checklist (marcar todo antes de pedir revisión)
- [ ] Power en `powers/<equipo>/<power>/` (carpeta propia, aislada)   # Req 20.4
- [ ] `plugin.json` o `POWER.md` con `x-ethack` completo              # Req 20.5 / Req 9
- [ ] `skills/` y `steering/` presentes                               # Req 20.5
- [ ] `docs/prompt.md`, `docs/sessions/`, `docs/feedback.md`          # Req 20.5 / Req 15
- [ ] `Modo_Ejecucion` admite {script-kiddie, green-hat, pro}, default script-kiddie  # Req 14
- [ ] Objetivos solo contra Allowlist_Objetivos (sin producción)      # Req 11
- [ ] **`make validate` pasa en local** (salida adjunta)              # Req 20.6, 20.7
- [ ] NO edité `inventory.json` a mano (lo genera el Catalogador)     # Req 20.9
- [ ] Sincronicé mi fork con el Repositorio_Integracion               # Req 20.10
```

### Validacion_Local: única compuerta automatizada (sin CI remota)

La compuerta de calidad es **Validacion_Local + revisión humana del Líder Técnico**; el sistema **no** depende de GitHub Actions ni de ningún servicio de integración continua remoto (Req 20.6, 20.11). Un **único punto de entrada** —`make validate` (o `python agent_ethack_dfir/scripts/validate_all.py`)— **encadena** las comprobaciones **que ya existen en este diseño**, sin lógica nueva de validación:

1. **power_adapter** — normaliza y valida el contrato del Power en **ambos formatos** (`plugin.json` y `POWER.md`): `x-ethack` presente, `tools` no vacío, `ecCouncilPhase` **xor** `forensicsStage`, `allowlistValidation.required == true`, `executionMode.allowed == {script-kiddie, green-hat, pro}` (Req 9.1, 9.2, 14.1).
2. **check_power_docs** — calcula `docStatus` de cada Power y señala Artefactos_Documentacion faltantes (`agent_ethack_dfir/scripts/check_power_docs.py`, Req 15.6).
3. **Guardia de Allowlist_Objetivos** — verifica que los Powers resuelven el objetivo contra `scope.yaml` (contenedor, no host) usando `validate_target.py` (Req 11.2, 11.4).
4. **Catalogador** (`agent_ethack_dfir/scripts/catalog.py`, `build_inventory()`) — **genera/regenera** `inventory.json` desde el árbol `powers/` (no se edita a mano), descubriendo **ambos layouts** (Powers base en `powers/<nombre>/` y Powers de alumnos en `powers/<equipo>/<power>/`). Es el mismo componente reutilizable que crea la `baseline` inicial y el que corre `make catalog`; fuente de las dos verificaciones siguientes (Req 20.9, 8.4, 13.2).
5. **Cobertura de fases/etapas** — confirma ≥1 Power por cada fase EC-Council y por cada etapa del Flujo_Investigacion, contando por igual Powers base y de alumnos. Es un **método del inventario** (`inv.coverage_gaps()`) que el agregador **invoca**; las tareas de test (p. ej. 13.3) solo lo verifican (Req 8.3, 13.3).
6. **Conteo por alumno** — confirma ≥2 Powers con Herramienta_Real por alumno (campo `owner`). Es un **método del inventario** (`inv.count_tooled_by_owner()`) que el agregador **invoca**; las tareas de test (p. ej. 14.2) solo lo verifican (Req 9.6, 3.2, 4.2, 5.2, 6.2, 7.2).

**Protocolo de la compuerta** (Req 20.7, 20.8):
- El **alumno** ejecuta `make validate` **antes** de abrir el PR y adjunta la salida al checklist.
- El **Líder Técnico** ejecuta `make validate` y **revisa** el PR **antes** del merge.
- Si la Validacion_Local **falla** o la revisión no se supera, el Líder Técnico **se abstiene de integrar** e indica el incumplimiento (Req 20.8, coherente con Req 8.4).

**Por qué no hay CI remota.** La compuerta se mantiene **local + revisión humana** deliberadamente: evita la complejidad operativa de configurar y mantener runners/credenciales/secretos de un servicio remoto en un contexto docente, mantiene el ciclo de realimentación en la máquina del alumno (misma donde corre Kiro y el laboratorio), y hace la compuerta **reproducible y auditable** sin dependencias externas. La calidad no se delega a infraestructura remota: es el propio `make validate` más el criterio del Líder Técnico (Req 20.11).

Esqueleto del agregador (llama a los módulos ya diseñados; no reimplementa su lógica):

```python
# agent_ethack_dfir/scripts/validate_all.py — único agregador de la Validacion_Local (Req 20.6)
# Encadena módulos YA definidos en el diseño; si alguno falla, la compuerta falla.
import sys
from pathlib import Path

from power_adapter import load_power_contract          # plugin.json | POWER.md + x-ethack (Req 9.1, 9.2)
from check_power_docs import doc_status                # Artefactos_Documentacion (Req 15.6)
from validate_target import scope_endpoints            # guardia Allowlist_Objetivos (Req 11.2, 11.4)
from catalog import build_inventory, discover_powers   # Catalogador reutilizable (Req 20.9, 8.3, 9.6)

def run(root: Path, scope_path: Path, inventory_out: Path) -> int:
    errors: list[str] = []

    # 1) power_adapter + 2) check_power_docs + 3) guardia de allowlist, por Power
    # discover_powers (del Catalogador) descubre AMBOS layouts: Powers base en
    # powers/<nombre>/ (un nivel) y Powers de alumnos en powers/<equipo>/<power>/
    # (dos niveles), detectando carpetas con plugin.json o POWER.md.
    powers = discover_powers(root / "powers")
    assets = load_scope_assets(scope_path)             # lee scope.yaml#assets
    for p in powers:
        c = load_power_contract(p)                     # (1) valida ambos formatos y x-ethack
        errors += c.errors
        ds = doc_status(p)                             # (2) docStatus
        if not ds["complete"]:
            errors.append(f"{p}: docs faltantes {ds['missing']}")
        if not scope_endpoints(assets):                # (3) allowlist resoluble (contenedor, no host)
            errors.append(f"{p}: Allowlist_Objetivos vacía/!resoluble en {scope_path}")

    # 4) Catalogador: build_inventory recorre AMBOS layouts y (re)genera el inventario
    #    desde powers/ (NO edición manual). Es el mismo build_inventory() de make catalog.
    inv = build_inventory(root / "powers", assets)
    inventory_out.write_text(inv.to_json(), encoding="utf-8")

    # 5) cobertura de fases/etapas — método del inventario (no lógica del agregador ni del test)
    missing_cov = inv.coverage_gaps()                  # 5 fases EC-Council ∪ 6 etapas; base + alumnos
    if missing_cov:
        errors.append(f"cobertura incompleta: {missing_cov}")

    # 6) conteo >=2 Powers con Herramienta_Real por alumno — método del inventario
    for owner, cnt in inv.count_tooled_by_owner().items():
        if cnt < 2:
            errors.append(f"alumno {owner}: {cnt} Powers con herramienta (<2)")

    if errors:
        print("VALIDACION_LOCAL: FALLÓ", *errors, sep="\n - ", file=sys.stderr)
        return 1
    print("VALIDACION_LOCAL: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(run(Path("."), Path("agent_ethack_dfir/engagements/dvwa-lab-ulsa/scope.yaml"),
                         Path("agent_ethack_dfir/engagements/dvwa-lab-ulsa/inventory.json")))
```

Makefile mínimo (único punto de entrada; el alumno y el Líder Técnico corren lo mismo):

```makefile
# Makefile — compuerta local (Req 20.6, 20.7, 20.11). Sin CI remota.
PY ?= python3
SCOPE ?= agent_ethack_dfir/engagements/dvwa-lab-ulsa/scope.yaml

.PHONY: validate catalog
validate:            ## compuerta única: encadena las comprobaciones del diseño
	$(PY) agent_ethack_dfir/scripts/validate_all.py

catalog:             ## regenera inventory.json desde powers/ (Catalogador, Req 20.9)
	$(PY) agent_ethack_dfir/scripts/catalog.py --powers powers --scope $(SCOPE)
```

### Trazabilidad y relación con otros requisitos

El modelo de colaboración **envuelve** y reutiliza requisitos previos sin duplicar su lógica: la **integración y el rechazo** del Líder Técnico (Req 8.2–8.4) son la **revisión humana** de esta compuerta; la **organización por equipos/roles y el inventario** (Req 13.1, 13.2, 13.4) se materializan en las carpetas `powers/<equipo>/` y en el `inventory.json` **generado** por el Catalogador; y los **Artefactos_Documentacion** (Req 15.1, 15.5, 15.6) son parte obligatoria del contrato de PR y de `check_power_docs`. El resultado cubre **Validates: Requirements 20.1–20.11**.

## Testing Strategy

Enfoque dual: **pruebas de propiedad** (universales, ≥100 iteraciones) para la lógica que varía con la entrada, y **pruebas de ejemplo / verificación estructural** para configuración, integración y cobertura.

### Pruebas de propiedad (property-based)

Implementan las Properties 1–17. Cada test referencia su propiedad con la etiqueta **Feature: ethical-hacking-forensics-agent, Property {N}: {texto}** y corre ≥100 iteraciones. Lenguaje sugerido: Python con Hypothesis (coherente con los scripts del starter).

- Property 1 y 11: generadores de objetivos (host/IP/URL con variantes de normalización) y de allowlists.
- Property 2 y 3: generadores de fase actual / solicitada y subconjuntos de fases completadas.
- Property 5, 6, 7, 9: generadores de blobs de evidencia y secuencias de traspasos; verificación de hashes y encadenamiento.
- Property 8: generadores de grants (aprobado/caducado/parcial) y eventos de herramienta.
- Property 10: generadores de inventarios parciales y completos.
- Property 12: generadores de strings arbitrarios (incluidos None/vacíos, variantes de mayúsculas/espacios y los tres valores válidos) sobre `resolve_mode`; verifica default, aceptación normalizada y rechazo con `InvalidModeError`.
- Property 13: generadores de subconjuntos de `{prompt.md, sessions/, feedback.md}` sobre `doc_status`; verifica `complete` y que `missing` es exactamente el complemento de los presentes.
- Property 14: generadores de conjuntos de evidencia con `volatility_rank` y tiempos de recolección; verifica que la serie de `volatility_rank` en orden de recolección es monótona no decreciente (Orden_Volatilidad RFC 3227).
- Property 15: generadores de evidencia original + copia; verifica `hash(copia) == record.sha256` y que el original permanece intacto tras la operación de análisis (complementa la Property 6).
- Property 16: generadores de registros de incidente con acciones de contención etiquetadas `short-term`/`long-term` y secuencias de transiciones de fase NIST; verifica que toda acción `short-term` cumple `shutdown == false` y `preserves_evidence == true`, y que el grafo de fases admite el retorno Post-Incident → Preparation y Recovery → Detection & Analysis (ciclicidad/iteración).
- Property 17: generadores de Registro_Riesgos (probabilidad, impacto, residual, apetito) y de Perfil_CSF (subcategorías con `current`/`target`/`gap` y POA&M); verifica `within_appetite == (residual_score <= max_residual_score)` para todo riesgo y que el conjunto de subcategorías del POA&M es exactamente el de subcategorías con `gap == true`.
- Property 1 (host vs contenedor): los generadores de objetivos incluyen endpoints de Contenedor_Objetivo y de host EC2 anfitrión; verifica que el host subyacente queda fuera de alcance salvo `host_is_target: true` (Req 11.4).

### Verificación estructural y de integración (no PBT)

- **Cobertura de fases/etapas (Req 8.3, 13.3):** check que **verifica** el método de cobertura del inventario (`inv.coverage_gaps()`, producido por el Catalogador sobre ambos layouts: Powers base + alumnos) y confirma ≥1 Power por cada fase EC-Council y por cada etapa forense; falla indicando los huecos. La lógica de cobertura vive en el inventario/Catalogador y la invoca el agregador de la Validacion_Local; este check solo la verifica, no la implementa. Es el criterio operativo del Líder Técnico y la validación directa de la estrategia de pruebas pedida (cada fase y etapa forense con al menos un Power integrado).
- **Esquema de Powers (Req 9.1, 9.2):** validación de `plugin.json`/`x-ethack` de cada Power (herramientas no vacías, fase xor etapa, allowlist requerida) — casos de ejemplo y edge cases.
- **Conteo de entregables por integrante (Req 3.2, 4.2, 5.2, 6.2, 7.2, 9.6):** check que **verifica** el método de conteo del inventario (`inv.count_tooled_by_owner()`, sobre el campo `owner`) y confirma ≥2 Powers con Herramienta_Real por alumno. Igual que la cobertura, el conteo es un método del inventario/Catalogador que invoca el agregador; este check (p. ej. tarea 14.2) solo lo verifica, no lo implementa.
- **Hook no bloqueante (Req 10.2):** prueba de ejemplo — evento sin grant que cubra el objetivo produce advertencia y `exit 0` (no aborta).
- **Formato de hooks (Req 10.5):** validación de que `.kiro/hooks/*.json` declara `version: v1` y triggers válidos.
- **Flujos cruzados (Req 3.4, 4.3, 7.3, 7.4):** pruebas de integración con 1–3 ejemplos — una acción ofensiva genera registro → Blue Team detecta → IR contiene y notifica → DF recolecta.
- **GameDay como prueba de integración de alto nivel (Req 17):** escenario breach-to-solution end-to-end que ejercita la coordinación de roles por el Orquestador (Req 17.2), la preservación de evidencia (Req 17.3, apoyada en las Properties 14, 15, 6 y 7), el rastreo de IOCs por análisis de logs con el mapeo kill-chain → evidencia AWS (Req 17.4) y la contención/hardening sin interrumpir servicios ni apagar hosts (Req 17.5). Es validación funcional, no rúbrica (Req 17.6); se verifica por ejemplo/escenario, no por PBT.
- **Forense de contenedores (Req 5.9, 16.8):** prueba de ejemplo — ante evidencia en un Contenedor_Objetivo efímero, el procedimiento automatizado produce snapshot + hash + copia antes de la desaparición del contenedor.
- **Comportamiento por modo (Req 14.3, 14.4, 14.5):** pruebas de ejemplo — `green-hat` incluye explicación en la salida; `pro` puede emitir scripts propios acotados al lab; `script-kiddie` solo comandos predefinidos. Cualitativo, no PBT.
- **Registro del modo en auditoría (Req 14.6):** ejemplo — un evento con `Modo_Ejecucion` produce un record con campo `mode` correspondiente (o `script-kiddie` por defecto).
- **Asociación de Artefactos_Documentacion (Req 15.5):** verificación estructural — `docs/` reside dentro del árbol del Power y `owner` consta en `inventory.json`.
- **Fases del Proceso_Respuesta_Incidentes (Req 18.1, 18.2, 18.3, 18.4, 18.6):** verificación estructural/ejemplo — el Incident Responder reconoce `incident-handling-nist` como base; `incident.json` recorre las cuatro fases; Preparation mantiene documentación/contactos/herramientas; Detection & Analysis fija contexto y timeline; Post-Incident produce reporte + lecciones. La ciclicidad/iteración se cubre por PBT (Property 16).
- **Formatos de IOC y mapeo a marcos (Req 18.9, 18.10):** verificación estructural — cada IOC de `incident.json` declara `format` ∈ `{STIX, YARA, OpenIOC}` y un mapeo a táctica/técnica de MITRE ATT&CK y a una etapa de la Cyber Kill Chain.
- **Coordinación cruzada del IR (Req 18.8, 18.11):** prueba de integración (1–3 ejemplos) — Detection & Analysis se nutre del Blue Team y Containment notifica al DF para preservar evidencia; el flujo Red → Blue → IR → DF es ejercitable dentro del GameDay (Req 17).
- **Escalamiento por movimiento lateral (Req 7.9, 18.5):** prueba de ejemplo — ante un indicio de movimiento lateral, se agrega una entrada a `escalations` del registro de incidente.
- **Cadena de trazabilidad GRC (Req 19.2, 6.6):** verificación estructural — cada requisito se mapea a subcategoría CSF → control → evidencia; `grc-nist-csf` reconocido como base (Req 19.1).
- **Hallazgos técnicos como evidencia CSF (Req 6.10, 19.6):** verificación estructural — los hallazgos de Red/Blue/DF/VA referencian una subcategoría CSF y se aportan a la segunda y tercera línea del Modelo_Tres_Lineas.
- **Alineación RS/RC ↔ NIST SP 800-61 (Req 19.7):** verificación estructural — la tabla de alineación mantiene una terminología única entre el Power GRC y el Power de incident handling; `csf_subcategories` de `incident.json` usa IDs RS.*/RC.* coherentes con la fase NIST.
- **Tier objetivo del Perfil_CSF (Req 19.4):** verificación estructural — `csf_profile.json` declara `target_tier` ∈ {1,2,3,4}.
- **Modelo de colaboración GitHub (Req 20):** se valida de forma **estructural y por el propio `make validate`**, no por PBT. Verificación estructural — topología de tres niveles (Repositorio_Base/Integracion/Fork_Alumno) y contribución solo por PR sin escritura directa (Req 20.1, 20.2); rama propia `power/<equipo>-<iniciales>-<nombre-power>` y no trabajar sobre la base (Req 20.3); aislamiento por carpeta `powers/<equipo>/<power>/` y `CODEOWNERS` que asigna cada ruta a su responsable y las rutas compartidas al Líder Técnico/docente (Req 20.4); contrato del PR con Power + `skills/` + `steering/` + `docs/` (Req 20.5, reutiliza Req 8 y Req 15); `inventory.json` **generado** por el Catalogador y no editable a mano (Req 20.9); sincronización upstream en dos saltos (Req 20.10). La compuerta misma se valida por **ejemplo de ejecución**: `make validate` (o `agent_ethack_dfir/scripts/validate_all.py`) encadena power_adapter, check_power_docs, guardia de Allowlist_Objetivos, generación de `inventory.json`, cobertura de fases/etapas y conteo ≥2 Powers con herramienta por alumno, devolviendo OK/!OK (Req 20.6); un PR que no pasa `make validate` o la revisión no se integra (Req 20.7, 20.8), y la compuerta es local + revisión humana, sin GitHub Actions ni CI remota (Req 20.11).

### Balance de pruebas

Las pruebas unitarias cubren ejemplos concretos, puntos de integración y condiciones de error (objetivo fuera de alcance, grant ausente, evidencia alterada). Las pruebas de propiedad cubren la cobertura universal de entradas, incluidos los invariantes del Proceso_Respuesta_Incidentes (clasificación de contención y ciclicidad, Property 16) y del GRC con NIST CSF 2.0 (riesgo residual dentro del apetito y cobertura del POA&M, Property 17). No se escriben pruebas de propiedad para configuración, organización de carpetas, composición del laboratorio, enumeración de fases/formatos ni principios cualitativos (Confidentiality/Full Disclosure como comportamiento), que se validan por inspección, ejemplo o checks de configuración. De los siete Principios_Forenses, Evidence Integrity (Properties 6, 15), Chain of Custody (Property 7) y el Orden_Volatilidad (Property 14) se cubren con PBT; los demás —Minimization, Objectivity, Documentation/Reproducibility y Legal Admissibility (Req 16.4–16.7)— se validan por **verificación estructural/ejemplo** (presencia de campos comando/UTC/herramienta/versión/resultado en `record.json`, almacenamiento de escritura única, registro de evidencia contraria a la hipótesis). El **modelo de colaboración y entrega** (Req 20) tampoco se cubre con PBT: se valida de forma **estructural** (topología, ramas, CODEOWNERS, contrato de PR, inventario generado) y por el **propio `make validate`** —la única compuerta automatizada— más la revisión humana del Líder Técnico, deliberadamente sin CI remota.
