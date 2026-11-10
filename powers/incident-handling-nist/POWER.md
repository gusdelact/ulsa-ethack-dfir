---
name: "incident-handling-nist"
displayName: "Incident Handling NIST"
description: "Guía para estudiar y conducir el manejo de incidentes de seguridad con el ciclo NIST SP 800-61 (preparación, detección y análisis, contención/erradicación/recuperación, post-incidente), apoyado en Cyber Kill Chain y MITRE ATT&CK. Trae reglas obligatorias de preservación de evidencia y contención coordinada, playbooks por tipo de incidente, plantillas de bitácora, línea de tiempo, cadena de custodia y reporte final, y un modo de estudio con autoevaluación. No necesita servidores MCP."
keywords: ["incident-handling", "incident-response", "nist-800-61", "cyber-kill-chain", "mitre-attack", "dfir"]
author: "Gustavo De la Cruz Tovar"
x-ethack:
  kind: "response"
  ecCouncilPhase: null
  forensicsStage: null
  track: "IR"
  team: "incident-responder"
  owner: "Gustavo De la Cruz Tovar"
  tools: ["NIST SP 800-61", "MITRE ATT&CK", "Cyber Kill Chain", "playbooks"]
  allowlistValidation:
    required: true
    source: "engagements/${ENGAGEMENT_ID}/scope.yaml#assets"
    targetParams: ["target", "host", "hostname", "domain", "url"]
  executionMode:
    param: "Modo_Ejecucion"
    allowed: ["script-kiddie", "green-hat", "pro"]
    default: "script-kiddie"
  documentation:
    root: "powers/incident-handling-nist/docs"
    required: ["prompt.md", "sessions/", "feedback.md"]
---

# Incident Handling NIST

## Al activar este power (obligatorio, en este orden)

1. **Objetivo de la sesión.** Si el prompt no lo indica, el agente lo pregunta **antes que nada** y
   espera la respuesta:
   > ¿Qué quieres hacer en esta sesión?
   > - **Estudio:** repasamos el curso fase por fase; te hago preguntas antes de darte la respuesta.
   > - **Respuesta:** manejamos un incidente (de laboratorio o simulado) y voy llevando la bitácora, la línea de tiempo y el reporte en archivos.
2. **Perfil de ejecución (`Modo_Ejecucion`).** Lee el parámetro `Modo_Ejecucion` del frontmatter
   (`x-ethack.executionMode`, valores `script-kiddie` | `green-hat` | `pro`, default
   `script-kiddie`). En este power de proceso el perfil expresa **la profundidad y la autonomía de la
   guía** (ver "Modos de ejecución (perfil del hacker)" abajo). Si el prompt no lo indica, se pregunta
   junto con el objetivo; si no se define, se usa `script-kiddie`.
3. **Cargar `ih-modos-trabajo.md`** (reglas comunes, detalle de cada objetivo y equivalencia con los
   perfiles).
4. **Modo Estudio:** cargar `ih-autoevaluacion.md` y la guía de la fase que el alumno elija.
   **Modo Respuesta:** hacer las preguntas de alcance de `ih-modos-trabajo.md`, crear la carpeta del
   caso con `ih-plantillas.md` y cargar `ih-02-deteccion-triage.md`.
5. Cargar las demás guías **solo cuando la fase lo requiera**.

## Overview

Este power empaqueta el conocimiento del módulo **"Incident Handling Process"** de **Hack The Box
Academy** y lo convierte en un flujo que el agente puede seguir y hacer cumplir:

- Las **4 etapas de NIST SP 800-61** con checklists y criterios para pasar de una a otra.
- **Cyber Kill Chain** y **MITRE ATT&CK** para ubicar al atacante y mapear hallazgos.
- **Reglas obligatorias** (ver abajo) que el agente revisa antes de cada acción.
- **Playbooks** por tipo de incidente: phishing, ransomware, credenciales comprometidas, insider,
  aplicación expuesta a Internet y cadena de suministro.
- **Plantillas** de alcance, bitácora, línea de tiempo, IOCs, cadena de custodia, comunicación y
  reporte final.
- El caso **Insight Nexus** del curso, resuelto, como ejemplo de referencia.

Para operar con TheHive, Wazuh y VirusTotal en el laboratorio, combínalo con el power
**`incident-response-lab`**.

> **Encuadre:** el modo Respuesta es para laboratorios autorizados, ejercicios simulados o
> incidentes de una organización que te asignó formalmente. El power no da autorización por sí mismo.

Creado para el curso de **Ingeniería Cibernética (ULSA)** con asistencia de Kiro, sobre el módulo
[Incident Handling Process](https://academy.hackthebox.com/module/details/148) de HTB Academy.

## Reglas obligatorias

El agente revisa estas reglas antes de proponer o ejecutar cualquier paso. Si un paso viola una,
**se detiene, explica cuál y por qué, y pide una decisión explícita**.

| # | Regla | Origen en el curso |
|---|---|---|
| R1 | **No saltarse fases ni dejarlas a medias.** No se erradica sin haber contenido *todos* los sistemas identificados. | Sección 3: "10 máquinas, no contener solo 5" |
| R2 | **La contención es coordinada y simultánea.** Contener por partes alerta al atacante. | Sección 8 |
| R3 | **Preservar evidencia primero.** Interactuar lo mínimo; no apagar un equipo sin decidir antes si se captura la RAM. | Sección 7 |
| R4 | **No exponer credenciales privilegiadas.** Usar WinRM o logons tipo 3; nunca PsExec con credenciales explícitas ni RDP con cuentas de dominio a equipos comprometidos. | Sección 7 |
| R5 | **Canales fuera de banda.** Documentación y comunicación del incidente fuera de la infraestructura de la organización; asumir que el atacante lee el correo. | Sección 4 |
| R6 | **Need-to-know.** La información del incidente solo va a quien la necesita; la comunicación externa la hace la persona designada junto con legal. | Sección 6 |
| R7 | **Cadena de custodia** para toda evidencia recolectada (quién, qué, cuándo, dónde, hash). | Sección 7 |
| R8 | **Si aparecen IOCs durante la recuperación, se vuelve a investigación.** | Sección 8 |
| R9 | **Escalar** cuando el impacto es alto, hay muchos sistemas o afecta a otra área. Que el sistema sea de otro departamento no es motivo para no escalar. | Secciones 6 y 7 |
| R10 | **Verificar cada ID de MITRE ATT&CK** en attack.mitre.org antes de ponerlo en un reporte; marcar como `(por verificar)` los que no se comprobaron. | Errores de mapeo detectados en el curso |
| R11 | **Hechos, inferencias e hipótesis separados.** Toda afirmación en el reporte cita su fuente (log, Event ID, archivo, hash). | Sección 6 (timeline con *data source*) |
| R12 | **Acciones de alto impacto con autorización.** Apagar, aislar o reconstruir sistemas de producción se comunica al negocio y se aprueba antes. | Sección 8 |

## Cómo está organizado el conocimiento (steering/)

| Guía | Contenido |
|---|---|
| `ih-modos-trabajo.md` | **Léela primero.** Modos Estudio y Respuesta, preguntas de alcance, estructura de la carpeta del caso, paradas. |
| `ih-01-preparacion.md` | Prerrequisitos, documentación, jump bag, medidas de protección (DMARC, hardening, red, MFA, purple team). |
| `ih-02-deteccion-triage.md` | Fuentes y niveles de detección, investigación inicial, severidad y alcance, priorización, escalamiento, comunicación. |
| `ih-03-investigacion.md` | Ciclo IOC → pistas → recolección, formatos de IOC, live response vs apagado, orden de volatilidad, credenciales, cadena de custodia, IA. |
| `ih-04-contencion-erradicacion-recuperacion.md` | Contención de corto y largo plazo, erradicación, recuperación por fases, monitoreo y criterios de cierre. |
| `ih-05-post-incidente.md` | Reunión de lecciones aprendidas, preguntas del reporte final, métricas, mejoras. |
| `ih-mapeo-killchain-mitre.md` | Kill Chain, ATT&CK (tácticas, técnicas, sub-técnicas), pirámide del dolor, tabla de técnicas frecuentes, regla de verificación. |
| `ih-playbooks.md` | Playbooks por tipo de incidente con pasos por fase. |
| `ih-plantillas.md` | Plantillas listas para copiar a la carpeta del caso. |
| `ih-caso-insight-nexus.md` | Caso del curso con timeline, evidencia, respuesta y lecciones. |
| `ih-autoevaluacion.md` | Banco de preguntas por fase con respuestas y criterios para el modo Estudio. |

## Flujo general

```
Preparación ─► Detección y análisis ─► Contención ─► Erradicación ─► Recuperación ─► Post-incidente
     ▲                 ▲    │                                              │                │
     │                 │    └── nueva evidencia: vuelve a investigar ◄─────┘ (IOCs, R8)     │
     └─────────────────┴──────────────────── lecciones aprendidas ◄─────────────────────────┘
```

Criterios para avanzar de fase (el agente los revisa y los anota en la bitácora):

| De → a | Se avanza cuando |
|---|---|
| Detección → Contención | Se conoce el tipo de incidente, el vector de entrada (o la mejor hipótesis), la lista de sistemas afectados y el impacto en el negocio. |
| Contención → Erradicación | Todos los sistemas identificados están contenidos al mismo tiempo y la evidencia está preservada. |
| Erradicación → Recuperación | La causa raíz está eliminada (malware, persistencia, cuentas creadas por el atacante, vulnerabilidad) en todos los sistemas. |
| Recuperación → Post-incidente | Los sistemas están en producción, verificados por el negocio y con un periodo de monitoreo intensivo sin IOCs. |

## Modos de ejecución (perfil del hacker)

Este power tiene **dos ejes** que conviven:

- **Objetivo de la sesión** (qué se produce): Estudio o Respuesta.
- **Perfil de ejecución** (cuánta autonomía y profundidad), fijado por el parámetro
  **`Modo_Ejecucion`** del frontmatter (`x-ethack.executionMode`:
  `allowed: ["script-kiddie", "green-hat", "pro"]`, `default: "script-kiddie"`).

Como es un power de **proceso** (ciclo NIST SP 800-61, no herramientas de Kali), los **tres**
perfiles expresan la profundidad y la autonomía de la guía de manejo de incidentes:

| `Modo_Ejecucion` | Perfil | Qué hace el agente en incident-handling-nist |
|---|---|---|
| `script-kiddie` *(default)* | Nivel de entrada | Ejecuta el triage, llena la bitácora/timeline y propone el siguiente paso o el playbook con explicación mínima. "Respuesta exprés": avanzar rápido. |
| `green-hat` | Aprendiz | Antes de cada paso explica por qué (orden de volatilidad, por qué contención simultánea, qué prueba cada IOC) y **pide al handler que razone** la decisión. Es el espíritu del modo **Estudio** aplicado a un incidente real. |
| `pro` | Profesional/experto (White/Black Hat) | No entrega el playbook/caso hecho: guía al handler a **diseñar su propio plan de respuesta, sus reglas de detección y su mapeo ATT&CK**, discute arquitectura y límites, y exige la **justificación ética y legal** (cadena de custodia, autorización, need-to-know, canales fuera de banda: R3–R7, R12). |

**Equivalencia con los modos existentes:** el modo **Estudio** es, por naturaleza, trabajo de perfil
`green-hat`; el modo **Respuesta** puede ejecutarse en cualquiera de los tres perfiles (desde
`script-kiddie`, que avanza el caso rápido, hasta `pro`, que exige que el handler diseñe y defienda
cada decisión). Así los tres perfiles del `Modo_Ejecucion` quedan cubiertos. Detalle en
`ih-modos-trabajo.md`.

**Prompts de arranque por perfil:**

- **script-kiddie:** *Activa incident-handling-nist en modo Respuesta con `Modo_Ejecucion=script-kiddie`. Haz el triage de esta alerta y dime el siguiente paso.*
- **green-hat:** *Activa incident-handling-nist con `Modo_Ejecucion=green-hat`. Antes de cada paso explícame por qué y pídeme razonar la decisión.*
- **pro:** *Activa incident-handling-nist con `Modo_Ejecucion=pro`. Guíame para diseñar yo el plan de contención y el mapeo ATT&CK, y pídeme la justificación legal.*

## Prompts de arranque

- **Estudio:** *Activa el power incident-handling-nist en modo Estudio. Quiero repasar la fase de detección y análisis.*
- **Respuesta:** *Activa el power incident-handling-nist en modo Respuesta. Tengo una alerta de Mimikatz en SQLServer01 del laboratorio de HTB.*
- **Reporte:** *Con el power incident-handling-nist, genera el reporte final del caso en `incidentes/IR-2025-001/`.*

## Best Practices

- Abrir la bitácora desde el primer minuto: hora, acción, resultado y responsable.
- Registrar la zona horaria en todos los timestamps (preferir UTC).
- Ordenar la línea de tiempo por hora del evento, no por hora del hallazgo.
- Preferir detecciones por comportamiento (TTPs) sobre IPs y hashes al proponer reglas.
- No cerrar un caso solo porque se borró el artefacto visible (p. ej. `checkme.txt`); buscar la persistencia.

## Troubleshooting

| Situación | Qué hace el agente |
|---|---|
| El usuario pide erradicar con sistemas aún sin contener | Cita R1/R2, lista los sistemas pendientes y pide decisión. |
| El usuario pide apagar un equipo comprometido | Cita R3, pregunta si ya se capturó la RAM y si el negocio lo aprobó (R12). |
| Un ID de MITRE no coincide con la descripción | Aplica R10: lo marca `(por verificar)` y sugiere el ID probable con la URL de attack.mitre.org. |
| Faltan datos para la investigación inicial | Lista los campos faltantes de la plantilla de alcance y no avanza de fase. |
| El usuario no indica el modo | Pregunta el modo antes de hacer cualquier otra cosa. |

## Configuration

**No requiere configuración.** Es un power de conocimiento: no tiene `mcp.json` ni API keys.
