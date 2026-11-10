# Govern (GV): gobierno del riesgo de ciberseguridad

Govern es la función que convierte la ciberseguridad en una decisión de negocio. Responde quién
decide, con qué criterios y cómo se supervisa. Las demás funciones (ID, PR, DE, RS, RC) ejecutan lo
que Govern define.

Texto oficial de la función: *"The organization's cybersecurity risk management strategy,
expectations, and policy are established, communicated, and monitored."*

Los resúmenes en español de abajo se verificaron contra `core/csf-2.0-core.csv`. En los entregables
se cita el ID con su texto oficial (R1).


### GV.OC: Contexto organizacional
Se entienden las circunstancias (misión, expectativas de partes interesadas, dependencias y
requisitos legales, regulatorios y contractuales) que rodean las decisiones de riesgo.

| ID | Resultado (resumen) |
|---|---|
| GV.OC-01 | La misión de la organización se entiende y orienta la gestión del riesgo de ciberseguridad. |
| GV.OC-02 | Se entienden las partes interesadas internas y externas y sus necesidades y expectativas. |
| GV.OC-03 | Se entienden y gestionan los requisitos legales, regulatorios y contractuales (incluidos privacidad y libertades civiles). **← cumplimiento** |
| GV.OC-04 | Se entienden y comunican los objetivos, capacidades y servicios críticos de los que dependen terceros. |
| GV.OC-05 | Se entienden y comunican los resultados, capacidades y servicios de los que depende la organización. |

### GV.RM: Estrategia de gestión de riesgos
Se establecen y usan las prioridades, restricciones, tolerancias y apetito de riesgo.

| ID | Resultado (resumen) |
|---|---|
| GV.RM-01 | Se establecen y acuerdan los objetivos de gestión de riesgos. |
| GV.RM-02 | Se establecen, comunican y mantienen las declaraciones de apetito y tolerancia al riesgo. |
| GV.RM-03 | La gestión del riesgo de ciberseguridad se integra a los procesos de gestión de riesgo empresarial (ERM). |
| GV.RM-04 | Se establece y comunica la dirección estratégica sobre las opciones de respuesta al riesgo. |
| GV.RM-05 | Se establecen líneas de comunicación sobre riesgos, incluidos los de proveedores y terceros. |
| GV.RM-06 | Se usa un método estandarizado para calcular, documentar, categorizar y priorizar riesgos. |
| GV.RM-07 | Se caracterizan las oportunidades estratégicas (riesgos positivos) y se incluyen en las discusiones. |

### GV.RR: Roles, responsabilidades y autoridades
| ID | Resultado (resumen) |
|---|---|
| GV.RR-01 | La dirección es responsable y rinde cuentas del riesgo de ciberseguridad y fomenta una cultura consciente del riesgo. |
| GV.RR-02 | Se establecen, comunican, entienden y aplican los roles, responsabilidades y autoridades. |
| GV.RR-03 | Se asignan recursos adecuados acordes con la estrategia, los roles y las políticas. |
| GV.RR-04 | La ciberseguridad se incluye en las prácticas de recursos humanos. |

### GV.PO: Política
| ID | Resultado (resumen) |
|---|---|
| GV.PO-01 | Se establece la política de gestión del riesgo de ciberseguridad con base en el contexto, la estrategia y las prioridades; se comunica y se aplica. |
| GV.PO-02 | La política se revisa, actualiza, comunica y aplica ante cambios de requisitos, amenazas, tecnología y misión. |

### GV.OV: Supervisión
| ID | Resultado (resumen) |
|---|---|
| GV.OV-01 | Se revisan los resultados de la estrategia para orientarla y ajustarla. |
| GV.OV-02 | Se revisa y ajusta la estrategia para asegurar que cubre los requisitos y riesgos. |
| GV.OV-03 | Se evalúa y revisa el desempeño de la gestión del riesgo de ciberseguridad para hacer ajustes. |

### GV.SC: Gestión de riesgos de la cadena de suministro
| ID | Resultado (resumen) |
|---|---|
| GV.SC-01 | Existe un programa, estrategia, objetivos, políticas y procesos de riesgo de cadena de suministro, acordados por las partes interesadas. |
| GV.SC-02 | Se establecen y comunican los roles de seguridad para proveedores, clientes y socios. |
| GV.SC-03 | El riesgo de cadena de suministro se integra a la gestión de riesgo de ciberseguridad y empresarial. |
| GV.SC-04 | Los proveedores se conocen y se priorizan por criticidad. |
| GV.SC-05 | Los requisitos de seguridad para la cadena de suministro se establecen e incluyen en contratos. |
| GV.SC-06 | Se planea y hace due diligence antes de iniciar relaciones con proveedores o terceros. |
| GV.SC-07 | Los riesgos de cada proveedor se entienden, registran, priorizan, evalúan, responden y monitorean durante la relación. |
| GV.SC-08 | Los proveedores relevantes se incluyen en la planeación, respuesta y recuperación de incidentes. |
| GV.SC-09 | Las prácticas de seguridad de cadena de suministro se integran a los programas y su desempeño se monitorea en todo el ciclo de vida. |
| GV.SC-10 | Los planes incluyen actividades para cuando termina la relación con el proveedor. |


## Entregables de gobierno que produce el modo Evaluación

| Entregable | Subcategorías que evidencia | Plantilla |
|---|---|---|
| Declaración de alcance y contexto (misión, servicios críticos, partes interesadas, dependencias) | GV.OC-01, GV.OC-02, GV.OC-04, GV.OC-05 | `00-alcance.md` |
| Lista de obligaciones legales, contractuales y normativas | GV.OC-03 | `00-alcance.md`, `06-matriz-cumplimiento.csv` |
| Declaraciones de apetito y tolerancia | GV.RM-02 | `01-apetito-riesgo.md` |
| Escalas y método de cálculo de riesgo | GV.RM-06 | `02-escalas.md` |
| Matriz RACI de riesgo y seguridad | GV.RR-02 | `00-alcance.md` (sección Roles) |
| Política de seguridad | GV.PO-01, GV.PO-02 | `10-politica-<tema>.md` |
| Reporte ejecutivo y revisión periódica | GV.OV-01, GV.OV-02, GV.OV-03 | `11-reporte-ejecutivo.md` |
| Inventario de proveedores críticos | GV.SC-04 (y ID.AM-04) | `03-inventario-activos.csv` (tipo = proveedor) |

## Cómo escribir buenas declaraciones de apetito y tolerancia (GV.RM-02)

- Una declaración por tema que importe al negocio: datos de clientes, disponibilidad del servicio,
  cumplimiento, reputación, proveedores.
- **Apetito** cualitativo y **tolerancia** medible.

| Tema | Apetito | Tolerancia (ejemplo) |
|---|---|---|
| Datos personales de clientes | Bajo | Ningún acceso no autorizado confirmado; 0 credenciales por defecto o compartidas en sistemas con datos personales. |
| Disponibilidad del servicio principal | Moderado | Máximo 8 h de indisponibilidad acumulada al mes. |
| Cumplimiento legal | Muy bajo | 0 requisitos legales sin plan de acción aprobado. |
| Exposición a Internet | Bajo | 0 servicios expuestos sin dueño y sin justificación de negocio. |

Si la organización no tiene apetito definido, el agente propone uno, lo marca como *propuesto* y
pide al alumno que lo valide antes de usarlo para evaluar riesgos.

## Matriz RACI mínima (GV.RR-02)

| Actividad | Dirección | Dueño del proceso | Seguridad (CISO) | TI | Legal | Auditoría |
|---|---|---|---|---|---|---|
| Aprobar apetito de riesgo | **A** | C | R | I | C | I |
| Mantener registro de riesgos | I | C | **A/R** | C | I | I |
| Aceptar un riesgo | **A** (o dueño con autoridad) | R | C | I | C | I |
| Operar controles técnicos | I | C | C | **A/R** | I | I |
| Interpretar requisitos legales | I | C | C | I | **A/R** | I |
| Evaluar efectividad de controles | I | C | C | C | I | **A/R** |

R = Responsible (ejecuta), A = Accountable (rinde cuentas, solo uno), C = Consulted, I = Informed.

## Errores frecuentes en Govern

- Política aprobada que nadie conoce (falla GV.PO-01: "communicated and enforced").
- Apetito de riesgo que no se usa para decidir nada.
- Seguridad como "dueña" de todos los riesgos: el dueño es quien tiene autoridad sobre el proceso de negocio.
- Proveedores críticos sin inventario ni cláusulas de seguridad (GV.SC-04, GV.SC-05).
