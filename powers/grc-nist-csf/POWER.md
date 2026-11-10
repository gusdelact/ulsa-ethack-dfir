---
name: "grc-nist-csf"
displayName: "GRC con NIST CSF 2.0"
description: "Guía para estudiar y conducir Governance, Risk & Compliance con NIST Cybersecurity Framework 2.0: función Govern, perfiles actual y objetivo, Tiers, evaluación y tratamiento de riesgos (SP 800-30, matriz 5×5 y ALE), cumplimiento simple (deber de seguridad de la LFPDPPP mapeado a CSF 2.0 y a CIS Controls v8.1 IG1), gap analysis, POA&M y reporte ejecutivo. Convierte hallazgos de OSINT, VA, pentest e incidentes en riesgos de negocio. Incluye una copia exportada del Core oficial, reglas obligatorias de trazabilidad y evidencia, plantillas, el caso Inlanefreight resuelto y un modo de estudio con autoevaluación; no necesita servidores MCP."
keywords: ["grc", "governance", "risk-management", "compliance", "nist-csf", "csf-2.0", "risk-register", "gap-analysis"]
author: "Gustavo De la Cruz Tovar"
x-ethack:
  kind: "governance"
  ecCouncilPhase: null
  forensicsStage: null
  track: "GRC"
  team: "grc"
  owner: "Gustavo De la Cruz Tovar"
  tools: ["NIST CSF 2.0", "risk-register", "gap-analysis", "POA&M"]
  allowlistValidation:
    required: true
    source: "engagements/${ENGAGEMENT_ID}/scope.yaml#assets"
    targetParams: ["target", "host", "hostname", "domain", "url"]
  executionMode:
    param: "Modo_Ejecucion"
    allowed: ["script-kiddie", "green-hat", "pro"]
    default: "script-kiddie"
  documentation:
    root: "powers/grc-nist-csf/docs"
    required: ["prompt.md", "sessions/", "feedback.md"]
---

# GRC con NIST CSF 2.0

## Al activar este power (obligatorio, en este orden)

1. **Objetivo de la sesión.** Si el prompt no lo indica, el agente lo pregunta **antes que nada** y
   espera la respuesta:
   > ¿Qué quieres hacer en esta sesión?
   > - **Estudio:** repasamos GRC y CSF 2.0 tema por tema; te hago preguntas antes de darte la respuesta.
   > - **Evaluación:** evaluamos una organización (Inlanefreight u otra de laboratorio) contra CSF 2.0 y voy generando los entregables en archivos.
   > - **Cumplimiento:** mapeamos el deber de seguridad de la LFPDPPP a CSF 2.0 y a CIS Controls IG1, y armamos la matriz de cumplimiento.
2. **Perfil de ejecución (`Modo_Ejecucion`).** Lee el parámetro `Modo_Ejecucion` del frontmatter
   (`x-ethack.executionMode`, valores `script-kiddie` | `green-hat` | `pro`, default
   `script-kiddie`). En un power de gobierno el perfil expresa **la profundidad y la autonomía de la
   guía**, no comandos de Kali (ver "Modos de ejecución (perfil del hacker)" abajo). Si el prompt no
   lo indica, el agente lo pregunta junto con el objetivo; si no se define, usa `script-kiddie`.
3. **Cargar `grc-modos-trabajo.md`** (reglas comunes, detalle de cada objetivo y equivalencia con los
   perfiles).
4. **Modo Estudio:** cargar `grc-autoevaluacion.md` y la guía del tema que el alumno elija.
   **Modo Evaluación:** hacer las preguntas de alcance, crear la carpeta del caso con
   `grc-plantillas.md` y cargar `grc-05-riesgo.md`.
   **Modo Cumplimiento:** hacer las preguntas de alcance y cargar `grc-06-cumplimiento.md`.
5. Cargar las demás guías **solo cuando el paso lo requiera**.
6. Antes de escribir cualquier ID de CSF en un entregable, **consultar `core/csf-2.0-core.csv`** (R1).

## Overview

Este power enseña y conduce **Governance, Risk & Compliance (GRC)** con **NIST CSF 2.0** como eje:

- **Fundamentos de GRC:** gobierno, gestión de riesgos, cumplimiento, controles, modelo de las tres líneas.
- **CSF 2.0 completo:** 6 funciones, 22 categorías y 106 subcategorías, con la función **Govern** a detalle.
- **Perfiles actual y objetivo**, los 5 pasos para crearlos y los **Tiers** 1–4.
- **Riesgo:** ciclo SP 800-30, escalas, matriz 5×5 y **ALE** (SLE × ARO) como introducción cuantitativa.
- **Cumplimiento simple:** *una ley y un catálogo*. Deber de seguridad de la **LFPDPPP** →
  subcategorías CSF 2.0 → salvaguardas **CIS Controls v8.1 IG1** → evidencia.
- **Integración** con los hallazgos de los demás powers del curso (OSINT, footprinting, VA,
  Metasploit, incident handling, DFIR).
- **Copia exportada del Core oficial** en `core/` para validar IDs sin Internet.
- **Caso Inlanefreight** resuelto, construido con los hallazgos del laboratorio de footprinting.

> **Encuadre:** el power es educativo. No da asesoría legal, no certifica cumplimiento y no modifica
> sistemas. Los casos usan organizaciones de laboratorio.

Creado para el curso de **Ingeniería Cibernética (ULSA)** con asistencia de Kiro. Fuente principal:
NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0* (26 de febrero de 2024),
<https://doi.org/10.6028/NIST.CSWP.29>.

## Reglas obligatorias

El agente revisa estas reglas antes de cada entregable. Si un paso viola una, **se detiene, explica
cuál y por qué, y pide una decisión explícita**.

| # | Regla |
|---|---|
| R1 | **Verificar cada ID de CSF 2.0** contra `core/csf-2.0-core.csv`. Un ID que no aparece ahí no se usa; si aparece en `core/withdrawn-v1.1.csv` es de la v1.1 y se sustituye por el de 2.0. Nunca se inventan IDs. |
| R2 | **Trazabilidad completa:** cada requisito tiene subcategoría, control, evidencia y responsable. Una fila sin alguno de esos campos queda como brecha. |
| R3 | **Severidad técnica ≠ riesgo.** CVSS, EPSS o KEV son insumos; el nivel de riesgo sale de probabilidad × impacto al negocio con la escala acordada. |
| R4 | **Todo riesgo tiene dueño** con autoridad para decidir su tratamiento. Sin dueño, no se cierra. |
| R5 | **Aceptar un riesgo requiere registro formal:** justificación, dueño, firma (nombre y fecha) y fecha de revisión o vencimiento. |
| R6 | **Evidencia verificable:** fecha, fuente, periodo cubierto y quién la obtuvo. Lo que no tiene evidencia se registra como *declarado, sin evidencia*. |
| R7 | **Hechos, inferencias y supuestos separados** en perfiles y reportes. |
| R8 | **CSF describe resultados, no controles.** Los controles se citan del catálogo correspondiente (CIS, ISO, SP 800-53). |
| R9 | **Los Tiers no son una calificación.** El Tier objetivo se justifica por riesgo y recursos; no se asume Tier 4. |
| R10 | **Sin asesoría legal.** Los requisitos legales se redactan en lenguaje sencillo, con la marca *a validar con legal*; no se cita un artículo sin haberlo verificado en el texto vigente publicado en el DOF. |
| R11 | **Confidencialidad:** solo organizaciones de laboratorio o datos anonimizados; no se copian credenciales ni datos personales a los entregables (se describen, no se transcriben). |
| R12 | **Solo lectura.** El power no modifica sistemas ni recursos en la nube; las correcciones van al POA&M para el responsable. |
| R13 | **IDs de CIS verificados.** Los IDs de salvaguardas CIS se marcan `(verificar CIS v8.1)` hasta que se comparen con la publicación oficial de CIS. |

## Cómo está organizado el conocimiento (steering/)

| Guía | Contenido |
|---|---|
| `grc-modos-trabajo.md` | **Léela primero.** Modos Estudio, Evaluación y Cumplimiento; preguntas de alcance; carpeta del caso; paradas. |
| `grc-01-fundamentos.md` | Qué es GRC; gobierno, riesgo y cumplimiento; controles; tres líneas; marcos de referencia. |
| `grc-02-csf-core.md` | CSF 2.0: componentes, 6 funciones, 22 categorías, cómo leer y usar el Core y la copia de `core/`. |
| `grc-03-govern.md` | GV.OC, GV.RM, GV.RR, GV.PO, GV.OV y GV.SC con ejemplos y entregables de gobierno. |
| `grc-04-perfiles-tiers.md` | Perfil actual y objetivo, los 5 pasos, escala de estado, Tiers 1–4. |
| `grc-05-riesgo.md` | Ciclo SP 800-30, escalas, matriz 5×5, ALE, tratamiento, riesgo residual, KRIs. |
| `grc-06-cumplimiento.md` | Ciclo de cumplimiento, LFPDPPP (deber de seguridad), CIS IG1, matriz de cumplimiento, evidencia, gap analysis. |
| `grc-07-monitoreo-mejora.md` | GV.OV e ID.IM, métricas, revisión periódica, auditoría, reporte ejecutivo. |
| `grc-integracion-powers.md` | Cómo convertir salidas de OSINT, footprinting, VA, Metasploit, IH y DFIR en riesgos y brechas CSF. |
| `grc-aws-evidencia.md` | Responsabilidad compartida y servicios de AWS como fuente de evidencia (solo lectura). |
| `grc-plantillas.md` | Plantillas para copiar a la carpeta del caso. |
| `grc-caso-inlanefreight.md` | Caso resuelto de referencia. |
| `grc-autoevaluacion.md` | Banco de preguntas por tema con respuestas y criterios. |

| Archivo de `core/` | Contenido |
|---|---|
| `csf-2.0-core-cprt.json` | Exportación oficial del CPRT de NIST, sin modificar. |
| `csf-2.0-core.csv` | 106 subcategorías vigentes: función, categoría, texto oficial (inglés) y ejemplos de implementación. |
| `csf-2.0-core.md` | Mismo contenido en Markdown, agrupado por función y categoría. |
| `withdrawn-v1.1.csv` | 91 elementos de la v1.1 retirados y a dónde se movieron. |
| `build_core.py` | Regenera CSV y Markdown desde el JSON (`python3 build_core.py` dentro de `core/`). |

## Flujo general (modo Evaluación)

```
 Alcance y contexto (GV.OC) ─► Apetito y método de riesgo (GV.RM) ─► Inventario (ID.AM)
                                                                         │
 Reporte ejecutivo ◄─ POA&M ◄─ Gap analysis ◄─ Perfil objetivo ◄─ Perfil actual + registro de riesgos (ID.RA)
        │                                                                 ▲
        └──────────── monitoreo y mejora (GV.OV, ID.IM) ──────────────────┘
```

Criterios para avanzar (el agente los revisa y los anota en `bitacora.md`):

| De → a | Se avanza cuando |
|---|---|
| Alcance → Riesgo | Hay alcance escrito, servicios críticos, obligaciones listadas y destinatario del reporte. |
| Riesgo → Perfil actual | Hay escalas de probabilidad e impacto, apetito (aprobado o propuesto) e inventario de activos críticos con dueño. |
| Perfil actual → Perfil objetivo | Cada subcategoría en alcance tiene estado y evidencia (o la marca *sin evidencia*). |
| Perfil objetivo → Gap analysis | Cada subcategoría objetivo tiene prioridad justificada por riesgo o requisito. |
| Gap analysis → POA&M | Cada brecha está ligada a uno o más riesgos del registro. |
| POA&M → Reporte | Cada acción tiene responsable, fecha, costo estimado (orden de magnitud) y riesgo residual esperado. |

## Modos de ejecución (perfil del hacker)

Este power tiene **dos ejes** que se combinan y conviven sin contradicción:

- **Objetivo de la sesión** (qué entregable se produce): Estudio, Evaluación o Cumplimiento.
- **Perfil de ejecución** (cuánta autonomía y profundidad), fijado por el parámetro
  **`Modo_Ejecucion`** del frontmatter (`x-ethack.executionMode`:
  `allowed: ["script-kiddie", "green-hat", "pro"]`, `default: "script-kiddie"`).

Como es un power de **gobierno** (usa el marco CSF 2.0, no herramientas de Kali), los tres perfiles
expresan **la profundidad y la autonomía de la guía GRC**, no la ejecución de comandos:

| `Modo_Ejecucion` | Perfil | Qué hace el agente en grc-nist-csf |
|---|---|---|
| `script-kiddie` *(default)* | Nivel de entrada | Rellena los entregables (perfil CSF, registro de riesgos, matriz de cumplimiento, POA&M) con las plantillas y los entrega con explicación mínima. "GRC de copiar y pegar": terminar rápido. |
| `green-hat` | Aprendiz | Antes de escribir cada fila, explica la decisión (por qué esa subcategoría, cómo se calcula el riesgo probabilidad × impacto, qué evidencia hace falta) y **pide al alumno que la justifique**. Es el espíritu del modo **Estudio** aplicado a un caso real. |
| `pro` | Profesional/experto (White/Black Hat) | No entrega artefactos hechos: guía al analista a **diseñar su propia metodología** (escalas, apetito, perfil objetivo, criterios de aceptación), discute límites del marco (CSF describe resultados, no controles; los Tiers no son calificación) y exige la **justificación ética y legal** del tratamiento de riesgo y del cumplimiento (R5, R10, R11). |

**Equivalencia con los modos existentes:** el modo **Estudio** es, por naturaleza, trabajo de perfil
`green-hat` (aprender razonando); **Evaluación** y **Cumplimiento** pueden ejecutarse en cualquiera
de los tres perfiles (desde `script-kiddie`, que llena los entregables, hasta `pro`, que exige que el
alumno diseñe y defienda el método). Tabla completa en `grc-modos-trabajo.md`.

**Prompts de arranque por perfil:**

- **script-kiddie:** *Activa grc-nist-csf en modo Evaluación con `Modo_Ejecucion=script-kiddie`. Llena el registro de riesgos de Inlanefreight.*
- **green-hat:** *Activa grc-nist-csf con `Modo_Ejecucion=green-hat`. Antes de cada fila explícame la decisión y pídeme justificarla.*
- **pro:** *Activa grc-nist-csf con `Modo_Ejecucion=pro`. Guíame para diseñar yo las escalas y el perfil objetivo y pídeme la justificación de cada aceptación de riesgo.*

## Prompts de arranque

- **Estudio:** *Activa el power grc-nist-csf en modo Estudio. Quiero repasar la función Govern.*
- **Evaluación:** *Activa el power grc-nist-csf en modo Evaluación para Inlanefreight; usa como insumo `reporte-enumeracion-lab.md`.*
- **Cumplimiento:** *Con el power grc-nist-csf, arma la matriz de cumplimiento de Inlanefreight para el deber de seguridad de la LFPDPPP usando CIS Controls IG1.*
- **Reporte:** *Genera el reporte ejecutivo del caso `grc/casos/INLANEFREIGHT-2026/`.*

## Best Practices

- Empezar por el negocio (misión y servicios críticos), no por los controles.
- Escribir escenarios de riesgo completos: *amenaza → vulnerabilidad → activo → impacto*.
- Un control puede cubrir varios requisitos: evaluar una vez, reportar a varios marcos.
- Priorizar pocas subcategorías bien evaluadas sobre muchas evaluadas a medias.
- Fechar todo: evidencia, revisiones, aceptaciones de riesgo.
- Hablarle a la dirección en impacto al negocio y dinero (ALE), no en CVEs.

## Troubleshooting

| Situación | Qué hace el agente |
|---|---|
| El usuario no indica el modo | Pregunta el modo antes de hacer cualquier otra cosa. |
| Se quiere "calificar" a la organización con un Tier sin evidencia | Cita R6 y R9; pide la evidencia o marca la evaluación como *declarada*. |
| Un hallazgo CVSS 9.8 se quiere registrar como riesgo crítico directo | Cita R3; pide valor del activo y exposición antes de calcular. |
| Se quiere aceptar un riesgo "por ahora" | Cita R5; usa la plantilla de aceptación con firma y vencimiento. |
| Una subcategoría no aparece en `core/csf-2.0-core.csv` | Cita R1; revisa `core/withdrawn-v1.1.csv` y propone el equivalente en 2.0. |
| Se pide interpretar o citar un artículo de ley | Cita R10; documenta el requisito en lenguaje sencillo y lo marca *a validar con legal*. |
| Se pide corregir una configuración para cerrar una brecha | Cita R12; registra la acción en el POA&M para el responsable. |
| Un reporte de otro power trae credenciales o datos personales | Cita R11; los describe ("credenciales débiles reutilizadas") sin copiarlos. |

## Configuration

**No requiere configuración.** Es un power de conocimiento: no tiene `mcp.json` ni API keys. La copia
del Core en `core/` permite trabajar sin Internet. Para actualizarla, descargar de nuevo el JSON del
CPRT y ejecutar `build_core.py`:

```bash
curl -sSL -o core/csf-2.0-core-cprt.json \
  'https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/csf_2_0_0/export/json?element=all'
cd core && python3 build_core.py
```
