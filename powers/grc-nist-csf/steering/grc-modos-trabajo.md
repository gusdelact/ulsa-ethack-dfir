# Modos de trabajo y reglas comunes

> **Dos ejes.** Este power combina el **objetivo de la sesión** (Estudio / Evaluación / Cumplimiento,
> abajo) con el **perfil de ejecución** del parámetro `Modo_Ejecucion` (`script-kiddie` | `green-hat`
> | `pro`, default `script-kiddie`). El objetivo define *qué entregable* se produce; el perfil define
> *cuánta autonomía y profundidad* tiene la guía. Son compatibles: se elige uno de cada eje.

## Perfil de ejecución (`Modo_Ejecucion`)

El frontmatter declara `x-ethack.executionMode.param = "Modo_Ejecucion"` con
`allowed: ["script-kiddie", "green-hat", "pro"]` y `default: "script-kiddie"`. Como grc-nist-csf es
un power de gobierno (marco CSF 2.0, no Kali), los perfiles expresan la profundidad de la guía:

| `Modo_Ejecucion` | Perfil | Comportamiento del agente | Objetivo donde encaja mejor |
|---|---|---|---|
| `script-kiddie` *(default)* | Entrada | Rellena los entregables con las plantillas y los entrega con explicación mínima. | Evaluación / Cumplimiento (rápido) |
| `green-hat` | Aprendiz | Explica cada decisión CSF/riesgo antes de escribirla y pide al alumno justificarla. | **Estudio** (equivalente natural) y Evaluación guiada |
| `pro` | Profesional/experto | No entrega artefactos hechos: guía al alumno a diseñar su propia metodología y exige justificación ética/legal (R5, R10, R11). | Evaluación / Cumplimiento (entregable) |

**Equivalencia:** el modo **Estudio** es trabajo de perfil `green-hat`; **Evaluación** y
**Cumplimiento** pueden correr en cualquiera de los tres perfiles. Si el prompt no trae
`Modo_Ejecucion`, se asume `script-kiddie`. Subir la exigencia (script-kiddie → green-hat → pro) lo
pide cualquiera; bajarla, solo el instructor. El perfil usado se anota en la bitácora del caso.

## Objetivo de la sesión

El power funciona con tres objetivos. Todos usan el mismo conocimiento y las mismas reglas
obligatorias (R1–R13 del `POWER.md`); cambia el objetivo y dónde se detiene el agente.

| | **Estudio** | **Evaluación** | **Cumplimiento** |
|---|---|---|---|
| Para qué | Aprender GRC y CSF 2.0 | Evaluar una organización contra CSF 2.0 | Demostrar el cumplimiento de una obligación |
| Quién decide | El alumno responde; el agente pregunta, corrige y explica | El alumno (como analista GRC) decide; el agente propone, documenta y hace cumplir las reglas | Igual que Evaluación |
| Paradas | Antes de dar cada respuesta | Al cambiar de paso y ante cualquier regla | Al terminar el inventario de requisitos, la matriz y el gap analysis |
| Salida | `grc/estudio/bitacora-estudio.md` (opcional) | `grc/casos/<ORG>-<AAAA>/` | `grc/casos/<ORG>-<AAAA>/cumplimiento/` |
| Guías clave | `grc-autoevaluacion.md` + guía del tema | `grc-03` → `grc-05` → `grc-04` → `grc-07` | `grc-06-cumplimiento.md` |

Se puede cambiar de modo en cualquier momento; el agente lo anota en la bitácora.

---

## Modo Estudio

### Flujo

1. Preguntar qué tema quiere repasar: fundamentos, Core, Govern, perfiles y Tiers, riesgo (incluye
   ALE), cumplimiento, monitoreo, o "todo, en orden".
2. Para cada tema:
   1. **Situación:** el agente plantea una situación corta del caso Inlanefreight y pregunta *¿qué
      harías?* Espera la respuesta.
   2. **Corrección:** compara con la guía del tema, señala lo que faltó y explica el porqué.
   3. **Preguntas:** 3 a 5 preguntas de `grc-autoevaluacion.md`, **una a la vez**. No revela la
      respuesta hasta que el alumno conteste.
   4. **Cierre:** qué acertó y qué debe repasar.
3. Al final: lista de temas débiles y la guía que conviene releer.

### Reglas del modo Estudio

- No dar la respuesta antes de que el alumno conteste, salvo que lo pida ("dime la respuesta").
- Si la respuesta es parcialmente correcta, decir qué parte sí y cuál no.
- Al citar una subcategoría, mostrar su texto oficial desde `core/csf-2.0-core.csv` y luego
  explicarla en español.

---

## Modo Evaluación

### Preguntas de alcance (antes de cualquier otra cosa)

El agente pregunta y espera respuesta. Sin esto no se abre el caso.

1. **Organización** y unidad o sistemas en alcance. ¿Es de laboratorio?
2. **Misión** y servicios críticos (qué no puede dejar de funcionar).
3. **Obligaciones** aplicables (ley, contratos, normas, políticas internas).
4. **Apetito de riesgo**, si existe; si no, el agente propone uno para que el alumno lo valide.
5. **Insumos** disponibles: reportes de OSINT, footprinting, VA, pentest, incidentes, inventarios.
6. **Tier objetivo** y horizonte del plan (p. ej., 12 meses).
7. **Destinatario** del reporte (dirección, auditoría, equipo técnico).

Con las respuestas, el agente escribe `00-alcance.md` usando las palabras del usuario.

### Carpeta del caso

ID sugerido: `<ORG>-<AAAA>`. El agente crea la carpeta con las plantillas de `grc-plantillas.md`:

```
grc/casos/INLANEFREIGHT-2026/
├── 00-alcance.md
├── 01-apetito-riesgo.md
├── 02-escalas.md
├── 03-inventario-activos.csv
├── 04-registro-riesgos.csv
├── 05-perfil-csf.csv
├── 06-matriz-cumplimiento.csv     # solo si hay modo Cumplimiento
├── 07-gap-analysis.md
├── 08-poam.csv
├── 09-aceptacion-riesgo-<ID>.md   # una por cada riesgo aceptado
├── 10-politica-<tema>.md          # opcional
├── 11-reporte-ejecutivo.md
├── bitacora.md
└── insumos/                       # copias o rutas de los reportes de otros powers
```

### Pasos

| # | Paso | Guía | Producto |
|---|---|---|---|
| 1 | Alcance y contexto | `grc-03-govern.md` (GV.OC) | `00-alcance.md` |
| 2 | Apetito, escalas y método | `grc-03-govern.md` (GV.RM), `grc-05-riesgo.md` | `01`, `02` |
| 3 | Inventario de activos | `grc-05-riesgo.md` | `03` |
| 4 | Registro de riesgos | `grc-05-riesgo.md`, `grc-integracion-powers.md` | `04` |
| 5 | Perfil actual y objetivo | `grc-04-perfiles-tiers.md` | `05` |
| 6 | Gap analysis y POA&M | `grc-04-perfiles-tiers.md`, `grc-05-riesgo.md` | `07`, `08`, `09` |
| 7 | Reporte ejecutivo | `grc-07-monitoreo-mejora.md` | `11` |

En cada cambio de paso el agente revisa los criterios de avance del `POWER.md`, los anota en
`bitacora.md` y pregunta si se continúa.

---

## Modo Cumplimiento

### Preguntas de alcance

1. ¿Qué organización y qué datos personales trata (clientes, empleados, proveedores)?
2. ¿En qué sistemas viven esos datos?
3. ¿Quién es el responsable de los datos y quién el responsable de seguridad?
4. ¿Qué evidencia hay disponible (políticas, configuraciones, reportes técnicos)?

### Pasos

1. Inventario de requisitos (por defecto, los requisitos didácticos del deber de seguridad de la
   LFPDPPP de `grc-06-cumplimiento.md`). **Parada.**
2. Matriz de cumplimiento: requisito → subcategoría CSF → salvaguarda CIS IG1 → evidencia →
   diseño → efectividad. **Parada.**
3. Gap analysis: requisitos que no cumplen y su riesgo asociado. **Parada.**
4. Las brechas pasan al registro de riesgos y al POA&M del caso.

---

## Paradas obligatorias (todos los modos)

El agente se detiene y pide decisión cuando:

- Un paso viola una regla R1–R13.
- Falta un dato de alcance.
- Se va a aceptar un riesgo (R5).
- Se va a citar un requisito legal o un ID de CIS sin verificar (R10, R13).
- Un insumo trae credenciales o datos personales (R11).
