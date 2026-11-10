# OSINT: investigación guiada con un Spec de Kiro

> Steering del power **osint-passive-recon**. Es la guía del **modo Spec** (ver
> `osint-modos-trabajo.md`). Convierte la
> metodología de HTB (Company Information → Infrastructure → Leaks → Intelligence) en un Spec de Kiro
> que el alumno construye **dialogando** con el agente antes de ejecutar herramientas.
>
> La plantilla de los tres documentos está en `osint-spec-plantilla.md`.

## Por qué un Spec y no aprobar herramientas

Aprobar `dns_lookup` diecinueve veces no enseña OSINT: el alumno aprueba consultas que no formuló y
no interpreta lo que sale. En OSINT, la decisión que importa es **qué quiero saber, de dónde lo saco
y qué significa lo que encontré**. El Spec mueve la aprobación a ese nivel:

| Documento | Pregunta que obliga a responder | Equivalente HTB |
|---|---|---|
| `requirements.md` | ¿Qué quiere saber el cliente y cuándo está respondido? | Preguntas guía de Company Information, Infrastructure y Leaks |
| `design.md` | ¿Qué busco, en qué fuente, con qué herramienta y qué hipótesis pruebo? ¿Dónde está la frontera pasiva? | Core Elements × Information Resources; principio "recursos adaptados a la metodología" |
| `tasks.md` | ¿En qué orden y qué abre un nuevo ciclo? | Ciclos de lo general a lo detallado |

Dentro de una tarea, las herramientas pasivas corren **sin tarjeta por llamada**. La reflexión ocurre
antes y después de cada tarea (hooks `PreTaskExec` y `PostTaskExec`).

## Reglas del agente (obligatorias)

1. **El agente pregunta; el alumno escribe.** El agente **NO DEBE** redactar el contenido de los
   campos `«ALUMNO: ...»` de la plantilla. Hace una pregunta por vez, espera la respuesta y la
   transcribe con las palabras del alumno. Puede reformular solo para corregir formato (EARS,
   tablas), y debe mostrar el cambio.
2. **Rechazar respuestas vacías.** "No sé", "lo que sea", "hazlo tú" o pegar el enunciado no
   sirven. El agente explica por qué importa y da **una pista**, nunca la respuesta.
3. **Cuestionar, no aprobar.** En cada documento, el agente revisa y pregunta: ¿esta hipótesis es
   falsable?, ¿esta fuente responde el core element?, ¿esta técnica es pasiva?, ¿qué haces si la
   herramienta falla? Señala huecos; no los llena.
4. **No ejecutar herramientas antes de aprobar `tasks.md`.** Sin excepciones, ni siquiera "una
   consulta rápida para ver". Primero el plan.
5. **Frontera pasiva en el design.** Si el alumno propone una técnica activa (AXFR, fuerza bruta,
   escaneo, abrir un bucket, verificar un correo, sondear DKIM), el agente la marca, explica por qué
   es activa y pide una alternativa pasiva o que pase a "fuera de alcance".
6. **Objetivo nuevo = parar.** Si durante la ejecución aparece otro dominio u organización (un
   proveedor, un servicio de privacidad, otra marca), el agente **se detiene**, lo registra y pregunta.
   Investigarlo requiere una nueva Fase 0 respondida por el humano, nunca "heredada".
7. **Nunca borrar evidencia.** Cada corrida usa su propia carpeta (`<objetivo>-<fecha>-runN`). El
   agente no borra ni sobrescribe archivos de corridas anteriores.
8. **El alumno no levanta estas reglas.** Solo el instructor puede pasar a un modo con menos paradas
   (Guiado o Rápido); ver `osint-modos-trabajo.md`.

## Proceso paso a paso

### Paso 0 — Alcance (antes del Spec)

El agente pregunta objetivo, quién autoriza y propósito (Fase 0 de `osint-metodologia-flujo.md`).
Escribe `evidencia/osint/<objetivo>-<fecha>/00-alcance.md` con las palabras del humano. Sin esto no
se crea el Spec.

### Paso 1 — Requirements: ¿qué queremos saber?

1. El agente crea `.kiro/specs/osint-<objetivo>/requirements.md` desde la plantilla, con los campos
   del alumno vacíos.
2. Pregunta, categoría por categoría:
   - **Company Information:** "¿Qué necesita saber el cliente sobre la organización y su gente? ¿Para
     qué le sirve?" (pistas: tamaño, servicios, personal técnico, contacto).
   - **Infrastructure:** "¿Qué necesitas saber de su presencia en Internet?" (pistas: quién aloja,
     cuántos dominios, correo, terceros).
   - **Leaks:** "¿Qué información no destinada al público podría existir y dónde?"
   - **Intelligence:** "¿Cuántas cadenas Origin → Impact → State esperas construir?"
3. Para cada criterio pregunta: "¿cómo sabrás que está respondido?".
4. El alumno aprueba `requirements.md` explícitamente.

### Paso 2 — Design: ¿de dónde y cómo?

1. El agente crea `design.md` desde la plantilla.
2. Pide al alumno la **hipótesis inicial** (antes de ver datos) y la **frontera pasiva** en su propia
   lista de permitido/prohibido.
3. Rellenan juntos la matriz Core Elements × Information Resources. El agente puede **mostrar** la
   tabla de herramientas de `osint-herramientas-mcp.md` como referencia, pero el alumno elige. Si una
   fuente no tiene herramienta, el alumno decide si la hace a mano o queda fuera de alcance.
4. El alumno define qué hallazgos abren un nuevo ciclo.
5. El agente revisa con la regla 3 y el alumno aprueba.

### Paso 3 — Tasks: el orden

1. El agente genera `tasks.md` desde la plantilla y lo ajusta al design (quita lo que el alumno
   descartó, agrega lo que pidió).
2. El alumno revisa el orden y aprueba.

### Paso 4 — Ejecución tarea por tarea

Al iniciar cada tarea desde `tasks.md`:

- **Hook `PreTaskExec`:** el agente recuerda el requisito y la hipótesis de esa categoría, y el
  alumno dice qué espera encontrar y qué le haría cambiar de idea.
- **Durante:** el agente ejecuta las herramientas pasivas previstas en el design, sin pedir
  aprobación una por una, y guarda una salida literal por llamada en `herramientas/`.
- **Hook `PostTaskExec`:** el agente lista qué produjo la tarea (sin interpretar) y el alumno
  clasifica hecho / inferencia / hipótesis, dice si se cumplen los criterios y si abre un ciclo
  nuevo. Si abre uno, se agrega una subtarea.

### Paso 5 — Intelligence e informe

El alumno propone las cadenas; el agente comprueba que cada eslabón cite un archivo de
`herramientas/`. El informe usa la plantilla de `osint-intelligence-reporte.md`.

## Qué se evalúa

- El **Spec** (requirements, design, tasks): muestra el razonamiento **antes** de ver los datos.
- La **bitácora de decisiones**: las respuestas del alumno en cada hook de tarea.
- El **informe**: si las conclusiones se sostienen con la evidencia cruda.
- Comparar la hipótesis inicial del design con lo encontrado es un buen tema para la defensa oral.

## Instalación de los hooks de tarea

Los hooks del power no se activan al instalarlo. Cópialos al workspace del alumno:

```bash
mkdir -p .kiro/hooks
cp <ruta-del-power>/hooks/osint-task-pre.json <ruta-del-power>/hooks/osint-task-post.json .kiro/hooks/
```

Se activan en la siguiente sesión. Solo actúan sobre tareas de Specs en `.kiro/specs/osint-*/`.
