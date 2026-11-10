# Perfiles y Tiers

## 1. Perfiles organizacionales

Un perfil describe la postura de la organización en términos de resultados del Core.

- **Perfil actual (Current Profile):** qué resultados se logran hoy y en qué medida.
- **Perfil objetivo (Target Profile):** qué resultados se quieren lograr, priorizados por riesgo,
  requisitos y objetivos.
- **Perfil comunitario (Community Profile):** línea base publicada para un sector o caso de uso
  (p. ej., manufactura, sector financiero, ransomware) que sirve como punto de partida del perfil
  objetivo.

### Los cinco pasos para crear y usar un perfil

| Paso | Actividad | Producto |
|---|---|---|
| 1. Alcance | Definir qué cubre el perfil (toda la organización, una unidad, un sistema, un tipo de amenaza). | Declaración de alcance |
| 2. Recolectar información | Políticas, apetito de riesgo, inventarios, requisitos legales, resultados de evaluaciones (VA, pentest, auditorías). | Insumos documentados |
| 3. Crear el perfil | Por cada subcategoría en alcance: estado actual con evidencia, y objetivo con prioridad. | Perfil actual y objetivo |
| 4. Analizar brechas y crear plan de acción | Comparar actual vs objetivo; priorizar por riesgo, costo y beneficio. | Gap analysis y POA&M |
| 5. Implementar y actualizar | Ejecutar el plan, monitorear y repetir. | Perfil actualizado |

## 2. Cómo llenar el perfil (`05-perfil-csf.csv`)

### Selección de subcategorías

No se evalúan las 106 de golpe. Para un primer perfil del curso:

1. Todas las de **GV.OC**, **GV.RM-02**, **GV.RM-06**, **GV.RR-02** y **GV.PO-01** (gobierno mínimo).
2. Las de **ID.AM** y **ID.RA** (saber qué hay y qué riesgos tiene).
3. Las ligadas a los riesgos del registro (cada riesgo apunta a una o más subcategorías).
4. Las que exige la matriz de cumplimiento (si hay modo Cumplimiento).

### Escala de estado actual

| Estado | Significado | Requisito de evidencia |
|---|---|---|
| **No** | El resultado no se logra. | Evidencia de ausencia o hallazgo técnico que lo contradice. |
| **Parcial** | Se logra en parte (algunos sistemas, sin documentar, sin revisión). | Evidencia de lo que sí existe y de lo que falta. |
| **Sí** | Se logra en todo el alcance y hay evidencia. | Evidencia fechada que cubre el alcance (R6). |
| **Sin evidencia** | Se declara que existe, pero no hay cómo comprobarlo. | Se anota quién lo declaró y cuándo. |

### Prioridad objetivo

| Prioridad | Cuándo |
|---|---|
| **Alta** | La subcategoría reduce un riesgo Alto o Crítico del registro, o la exige una obligación legal. |
| **Media** | Reduce un riesgo Medio o es base para otras subcategorías de prioridad alta. |
| **Baja** | Mejora deseable sin riesgo asociado relevante en el horizonte del plan. |

La prioridad siempre se justifica con el ID del riesgo o del requisito (columna `justificacion`).

### Del perfil al gap analysis

Brecha = subcategoría con prioridad Alta o Media cuyo estado actual no es **Sí**. Cada brecha se
liga a riesgos del registro y genera una o más acciones en el POA&M.

## 3. Tiers (niveles)

Los Tiers caracterizan el **rigor** de las prácticas de *gobierno* y de *gestión* del riesgo de
ciberseguridad. No son un modelo de madurez obligatorio ni una calificación: la organización elige
el Tier objetivo según su riesgo y recursos.

| Tier | Nombre | Gobierno del riesgo | Gestión del riesgo |
|---|---|---|---|
| 1 | **Partial** (Parcial) | Estrategia ad hoc, sin priorización formal por riesgo. | Conciencia limitada; sin procesos repetibles; poca coordinación con terceros. |
| 2 | **Risk Informed** (Informado por riesgos) | Prácticas aprobadas por la dirección, pero no establecidas como política en toda la organización. | Hay conciencia del riesgo, pero no hay un enfoque organizacional consistente. |
| 3 | **Repeatable** (Repetible) | Prácticas aprobadas formalmente y expresadas como política; se actualizan regularmente. | Enfoque organizacional consistente; el personal tiene conocimientos y roles definidos. |
| 4 | **Adaptive** (Adaptativo) | El riesgo de ciberseguridad forma parte de la cultura y de las decisiones financieras y de negocio. | Se adapta con base en lecciones aprendidas e indicadores predictivos; mejora continua. |


### Cómo elegir el Tier actual y el objetivo

- Se evalúa por separado **gobierno** y **gestión** del riesgo; la organización puede estar en
  Tier 1 en uno y Tier 2 en otro.
- El Tier actual se justifica con evidencia (R6): ¿hay política aprobada? ¿se aplica igual en toda
  la organización? ¿se actualiza? ¿se usan lecciones aprendidas?
- El objetivo se elige por riesgo y recursos (R9). Para una empresa pequeña con datos personales de
  clientes, pasar de Tier 1 a Tier 2 en 12 meses ya es una meta seria; Tier 3 en un segundo ciclo.

| Pregunta de diagnóstico | Si la respuesta es "no", el Tier probable es |
|---|---|
| ¿Existe al menos una evaluación de riesgos documentada? | 1 |
| ¿La dirección aprobó las prácticas de riesgo? | 1 |
| ¿Las prácticas están en una política vigente aplicada a toda la organización? | 2 |
| ¿El personal conoce sus roles y las prácticas se repiten igual cada vez? | 2 |
| ¿Las prácticas se ajustan con lecciones aprendidas e indicadores? | 3 |
