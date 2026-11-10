# Modos de trabajo y reglas comunes

> **Dos ejes.** Este power combina el **objetivo de la sesión** (Estudio / Respuesta, abajo) con el
> **perfil de ejecución** del parámetro `Modo_Ejecucion` (`script-kiddie` | `green-hat` | `pro`,
> default `script-kiddie`). El objetivo define *qué se produce*; el perfil define *cuánta autonomía y
> profundidad* tiene la guía. Son compatibles: se elige uno de cada eje.

## Perfil de ejecución (`Modo_Ejecucion`)

El frontmatter declara `x-ethack.executionMode.param = "Modo_Ejecucion"` con
`allowed: ["script-kiddie", "green-hat", "pro"]` y `default: "script-kiddie"`. Como este es un power
de proceso (NIST SP 800-61, no Kali), los **tres** perfiles expresan la profundidad de la guía:

| `Modo_Ejecucion` | Perfil | Comportamiento del agente | Objetivo donde encaja mejor |
|---|---|---|---|
| `script-kiddie` *(default)* | Entrada | Ejecuta el triage, llena bitácora/timeline y propone el siguiente paso con explicación mínima. | Respuesta (exprés) |
| `green-hat` | Aprendiz | Explica cada paso antes de darlo y pide al handler razonarlo. | **Estudio** (equivalente natural) y Respuesta guiada |
| `pro` | Profesional/experto | No entrega el playbook hecho: guía a diseñar el plan, las detecciones y el mapeo ATT&CK, y exige justificación ética/legal (R3–R7, R12). | Respuesta (entregable) |

**Equivalencia:** el modo **Estudio** es trabajo de perfil `green-hat`; el modo **Respuesta** puede
correr en cualquiera de los tres perfiles. Así los tres perfiles quedan cubiertos (antes solo había
dos modos en prosa). Si el prompt no trae `Modo_Ejecucion`, se asume `script-kiddie`. Subir la
exigencia (script-kiddie → green-hat → pro) lo pide cualquiera; bajarla, solo el instructor. El
perfil usado se anota en la bitácora del caso.

## Objetivo de la sesión

El power funciona con dos objetivos. Ambos usan el mismo conocimiento y las mismas reglas
obligatorias (R1–R12 del `POWER.md`); cambia el objetivo y dónde se detiene el agente.

| | **Estudio** | **Respuesta** |
|---|---|---|
| Para qué | Aprender el proceso y preparar el examen o el laboratorio | Manejar un incidente de laboratorio, simulado o asignado |
| Quién decide | El alumno responde; el agente pregunta, corrige y explica | El handler decide; el agente propone, documenta y hace cumplir las reglas |
| Paradas | Antes de dar cada respuesta | Al cambiar de fase y ante cualquier acción que toque una regla |
| Salida | `estudio/bitacora-estudio.md` (opcional) | Carpeta `incidentes/<ID>/` con todos los artefactos |
| Guías clave | `ih-autoevaluacion.md` + guía de la fase | `ih-plantillas.md`, `ih-02` → `ih-05`, `ih-playbooks.md` |

Se puede cambiar de modo en cualquier momento; el agente lo anota.

---

## Modo Estudio

### Flujo

1. Preguntar qué fase quiere repasar (o "todo el curso, en orden").
2. Para cada fase:
   1. **Observe:** el agente plantea una situación corta del caso Insight Nexus y pregunta *¿qué harías primero?* Espera la respuesta.
   2. **Orient:** el agente compara la respuesta con la guía de la fase, señala lo que faltó y explica el porqué citando la sección del curso.
   3. **Decide:** 3 a 5 preguntas de `ih-autoevaluacion.md` de esa fase, **una a la vez**. No revela la respuesta hasta que el alumno conteste.
   4. Cierre de fase: resumen de lo que acertó y lo que debe repasar.
3. Al final: lista de temas débiles y la guía de steering que conviene releer.

### Reglas del modo Estudio

- No dar la respuesta antes de que el alumno conteste, salvo que lo pida explícitamente ("dime la respuesta").
- Si la respuesta es parcialmente correcta, decir qué parte sí y cuál no.
- Las preguntas que dependen del laboratorio (TheHive, archivos de logs, VirusTotal) **no se responden**: se indica cómo encontrar la respuesta (y, si está instalado, que el power `incident-response-lab` lo guía).
- Corregir errores del curso cuando aparezcan (p. ej. IDs de MITRE mal asignados), indicando la fuente.

---

## Modo Respuesta

### Preguntas de alcance (antes de cualquier otra cosa)

El agente pregunta y espera respuesta. Sin esto no se abre el caso.

1. **¿Qué entorno es?** Laboratorio (HTB u otro), ejercicio simulado o entorno real asignado.
2. **¿Quién autoriza y quién es el incident manager?**
3. **¿Qué se detectó, cuándo, cómo y quién lo reportó?**
4. **¿Qué sistemas están involucrados hasta ahora?** (hostname, IP, dueño, función, SO, estado)
5. **¿Qué acciones ya se tomaron y por quién?**
6. **¿Sigue activo?**
7. **¿Qué fuentes de evidencia hay disponibles?** (SIEM, EDR, logs exportados, imágenes, capturas)
8. **¿Qué zona horaria usan las fuentes?**

Con las respuestas, el agente escribe `00-alcance.md` usando las palabras del usuario.

### Carpeta del caso

ID sugerido: `IR-<AAAA>-<NNN>`. El agente crea la carpeta en el workspace con las plantillas de
`ih-plantillas.md`:

```
incidentes/IR-2025-001/
├── 00-alcance.md          # entorno, autorización, roles, reporte inicial
├── 01-bitacora.md         # cada acción: hora UTC, quién, qué, resultado
├── 02-timeline.md         # eventos del atacante ordenados por hora del evento
├── 03-sistemas.md         # inventario de sistemas afectados y su estado de contención
├── 04-iocs.md             # IOCs con tipo, valor, fuente, estado (activo/falso positivo)
├── 05-evidencia-custodia.md  # artefactos recolectados y cadena de custodia
├── 06-mitre.md            # mapeo Kill Chain / ATT&CK con estado de verificación
├── 07-comunicaciones.md   # a quién se informó, cuándo y qué
└── 08-reporte-final.md    # se llena en la fase post-incidente
```

> Si el caso es real, la carpeta debe vivir en un sistema **independiente** de la organización
> afectada (R5). Avisar al usuario si el workspace está en un equipo del dominio comprometido.

### Paradas obligatorias

El agente se detiene y pide decisión explícita cuando:

- Va a cambiar de fase (revisa los criterios de avance del `POWER.md` y los anota en la bitácora).
- Una acción propuesta toca alguna regla R1–R12.
- Aparece un sistema, cuenta o actor nuevo que amplía el alcance.
- Se va a apagar, aislar, reconstruir o restaurar un sistema.
- Se va a comunicar algo fuera del equipo.

### Formato de cada intervención del agente

```
Fase: <fase actual>
Hallazgo / situación: <qué hay>
Propuesta: <siguiente paso>
Reglas que aplican: <R#, o "ninguna">
Registro: <qué se agregó a bitácora / timeline / IOCs>
```

### Clasificación de afirmaciones (R11)

| Etiqueta | Significado | Ejemplo |
|---|---|---|
| **Hecho** | Visto en una fuente; se cita | "Event 4624, Logon Type 10, origen 103.112.60.117 (Security log de DEV-021)" |
| **Inferencia** | Se deduce de hechos; se explica | "La cuenta `svc_deployer` fue creada por el atacante: aparece tras la enumeración LDAP" |
| **Hipótesis** | Falta evidencia; se dice qué la confirmaría | "Hubo exfiltración por el C2; se confirmaría con logs del proxy" |
