# Fase 4: Actividad post-incidente

Objetivo: documentar el incidente y mejorar las capacidades con las lecciones aprendidas.

## Reunión de lecciones aprendidas

- Con **todos** los involucrados durante el incidente.
- Pocos días después del cierre, cuando el reporte está terminado.
- Buen momento para **entrenar a los miembros junior** mostrando cómo se manejó el caso.
- Revisar también herramientas, entrenamiento, preparación y estructura del equipo, no solo documentación.

Agenda sugerida:

1. Línea de tiempo resumida (5 min).
2. Qué funcionó.
3. Qué no funcionó o tardó (brechas de detección, de comunicación, de herramientas).
4. Acciones de mejora con responsable y fecha.

## Preguntas que el reporte final debe responder

- [ ] ¿Qué pasó y cuándo?
- [ ] ¿Cómo se desempeñó el equipo respecto a planes, playbooks, políticas y procedimientos?
- [ ] ¿El negocio entregó la información necesaria a tiempo? ¿Qué se puede mejorar?
- [ ] ¿Qué acciones se tomaron para contener y erradicar?
- [ ] ¿Qué medidas preventivas evitarían incidentes similares?
- [ ] ¿Qué herramientas y recursos hacen falta para detectar y analizar incidentes similares?

La plantilla completa está en `ih-plantillas.md` (reporte final). El reporte se escribe en orden
secuencial por fase del atacante (de Initial Access a Impact), como los reportes de Mandiant,
Unit 42 o The DFIR Report.

## Usos del reporte

- **Métricas:** número de incidentes, tiempo por incidente, acciones realizadas. Métricas útiles adicionales: tiempo hasta detectar (desde el primer evento del atacante) y tiempo hasta contener.
- **Referencia** para incidentes futuros similares.
- **Evidencia** en procesos legales y base para estimar costos e impacto.

## Mejoras a revisar

- [ ] ¿Hay que actualizar planes, playbooks, políticas o procedimientos?
- [ ] ¿Qué reglas de detección nuevas se necesitan? (preferir reglas por comportamiento; ver Sigma en el caso Insight Nexus)
- [ ] ¿Qué alertas generaron ruido y deben filtrarse (alert fatigue)?
- [ ] ¿Qué fuentes de log faltaron o tenían retención insuficiente?
- [ ] ¿Qué entrenamiento necesita el equipo?

## Regla de revisión del agente

Antes de dar por terminado el reporte, el agente verifica:

- Toda afirmación cita su fuente (R11).
- Todos los IDs de ATT&CK están verificados o marcados `(por verificar)` (R10).
- La línea de tiempo está ordenada por hora del evento y con zona horaria.
- Las acciones de mejora tienen responsable y fecha.
