# OSINT: modos de trabajo

> Steering del power **osint-passive-recon**. Define los tres modos de trabajo, qué guía carga cada
> uno, dónde se detiene el agente y las reglas que valen en **todos** los modos. Léelo al inicio de
> la sesión, junto con `osint-metodologia-flujo.md`.

## Los tres modos

| | **Rápido** | **Guiado** | **Spec** |
|---|---|---|---|
| Para qué | Demo del instructor, práctica individual, repetir una corrida | Laboratorio en clase: aprender el flujo fase por fase | Proyecto o entregable: planear antes de ver datos |
| Guía que carga | `osint-metodologia-flujo.md` | `osint-compuertas-aprendizaje.md` | `osint-spec-investigacion.md` + `osint-spec-plantilla.md` |
| Quién decide qué consultar | El agente, siguiendo el flujo por fases | El alumno, en cada fase | El alumno, en el `design.md`, antes de ejecutar |
| Dónde se detiene el agente | Solo en las paradas comunes (abajo) | Antes y después de **cada fase** (compuertas G1–GF) | Al escribir cada documento del Spec, y antes y después de **cada tarea** |
| Aprobación por herramienta | No (salvo que el host lo pida) | No | No |
| Explicación | Una línea por fase: qué pregunta responde y por qué es pasiva | El alumno da Observe/Orient/Decide; el agente valida | El alumno escribe requirements y design; el agente pregunta y cuestiona |
| Hooks | Ninguno | Ninguno | `osint-task-pre.json` y `osint-task-post.json` (`PreTaskExec`/`PostTaskExec`) |
| Entregables | `00-alcance.md`, `herramientas/`, `informe.md` | Lo mismo + `bitacora-decisiones.md` | Lo mismo + el Spec en `.kiro/specs/osint-<objetivo>/` |
| Duración aproximada | Minutos | Una sesión de clase | Varias sesiones |

Los tres modos usan las mismas herramientas, la misma frontera pasiva y la misma estructura de
evidencia. Solo cambia **quién piensa en cada paso** y **dónde se detiene el agente**.

## Equivalencia con el parámetro `Modo_Ejecucion` (perfil del hacker)

El frontmatter de `POWER.md` declara `x-ethack.executionMode.param = "Modo_Ejecucion"` con
`allowed: ["script-kiddie", "green-hat", "pro"]` y `default: "script-kiddie"`. **Los tres modos de
este power son esos tres perfiles**; Rápido/Guiado/Spec son sus nombres operativos. La equivalencia
es exacta y define qué hace distinto el agente según el `Modo_Ejecucion` recibido:

| `Modo_Ejecucion` | Modo operativo | Perfil del alcance | Comportamiento del agente |
|---|---|---|---|
| `script-kiddie` *(default)* | **Rápido** | Nivel de entrada | Recorre el flujo listo y entrega los hallazgos con explicación mínima. |
| `green-hat` | **Guiado** | Aprendiz | Explica cada fase antes/después y pide al alumno razonar la salida. |
| `pro` | **Spec** | Profesional/experto (White/Black Hat) | No ejecuta por el alumno: lo guía a diseñar la investigación, discute método y límites y exige justificar alcance y frontera pasiva (ética/legalidad). |

Así, cuando el prompt trae `Modo_Ejecucion=green-hat`, el agente trabaja en modo Guiado; con
`Modo_Ejecucion=pro`, en modo Spec; sin valor, en `script-kiddie` (Rápido), el default. El resto de
esta guía usa los nombres operativos, que son intercambiables con los del parámetro.

## Reglas comunes a los tres modos (no se levantan en ninguno)

1. **Fase 0.** El agente pregunta objetivo, quién autoriza y propósito, y espera la respuesta. No se
   autodeclara autorizado (ver Fase 0 en `osint-metodologia-flujo.md`).
2. **La autorización no se hereda.** Si aparece otro dominio u organización, el agente se detiene y
   pide una Fase 0 nueva. Nunca escribe "asumo el mismo alcance".
3. **Frontera pasiva.** Nada de AXFR, fuerza bruta, escaneos, abrir buckets, verificar correos ni
   sondear DKIM.
4. **Regla de detención.** Ante un bucket o servicio expuesto: documentar y detenerse.
5. **Evidencia cruda.** Un archivo literal por llamada en `herramientas/`. La interpretación va solo
   en `informe.md`.
6. **Nunca borrar evidencia.** Cada corrida en su carpeta (`<objetivo>-<fecha>[-runN]`).
7. **Lectura correcta de los datos.** Las reglas de `osint-infraestructura-dominio.md` (SPF + DMARC
   + MX, NS de RDAP frente a NS de la zona, certificados comodín) aplican aunque nadie las pregunte.

El modo Rápido tiene **pocas paradas**, no **menos reglas**.

## Paradas del modo Rápido

En modo Rápido el agente ejecuta el flujo de `osint-metodologia-flujo.md` de corrido y solo se
detiene en:

- la Fase 0 (antes de la primera herramienta);
- un objetivo nuevo (otro dominio u organización);
- un bucket o servicio expuesto;
- una técnica que no sea pasiva;
- el final, para entregar el informe.

Antes de cada fase escribe **una línea**: qué pregunta responde y por qué sus consultas son pasivas.
No escribe tarjetas por herramienta.

## Cómo se elige el modo

- El humano lo dice al empezar (ver prompts abajo).
- Si no lo dice, el agente lo **pregunta antes que nada**, antes de la Fase 0, con una frase de
  cada uno (texto en "Al activar este power" de `POWER.md`). No elige por su cuenta.
- Con el modo elegido, carga su guía y luego hace la Fase 0.
- El modo queda escrito en `00-alcance.md` (campo `Modo:`).

## Cambiar de modo a mitad de sesión

- **A un modo con más paradas** (Rápido → Guiado → Spec): lo puede pedir cualquiera. El agente
  continúa desde la fase siguiente con las nuevas paradas.
- **A un modo con menos paradas** (Spec o Guiado → Rápido): solo el **instructor**. Si un alumno lo
  pide ("hazlo rápido", "sáltate las preguntas"), el agente responde que esa decisión es del
  instructor y mantiene el modo.
- Todo cambio se anota en `00-alcance.md` con la hora UTC y quién lo pidió.

## Prompts de arranque

**Rápido:**

> Activa el power osint-passive-recon en modo Rápido. Objetivo: <dominio>. Te confirmo el alcance
> cuando me lo preguntes.

**Guiado:**

> Activa el power osint-passive-recon en modo Guiado y carga `osint-compuertas-aprendizaje.md`.
> Objetivo: <dominio>. Detente en cada fase y pregúntame antes de ejecutar.

**Spec:**

> Activa el power osint-passive-recon en modo Spec y carga `osint-spec-investigacion.md`. Quiero
> crear el Spec de investigación OSINT para <dominio>. Hazme las preguntas; no escribas tú las
> respuestas.

## Sugerencia de progresión en el curso

1. **Rápido** (instructor, en proyector): mostrar el flujo completo y un informe de referencia.
2. **Guiado** (alumnos, primer laboratorio): aprender qué pregunta responde cada fase.
3. **Spec** (alumnos, entregable): planear la investigación antes de ver datos y defender la
   comparación entre hipótesis y hallazgos.
