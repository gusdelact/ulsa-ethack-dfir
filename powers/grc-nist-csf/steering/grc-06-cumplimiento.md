# Cumplimiento: una ley y un catálogo

Subcategoría de entrada: **GV.OC-03**, *"Legal, regulatory, and contractual requirements regarding
cybersecurity - including privacy and civil liberties obligations - are understood and managed"*.

Para que el ciclo completo se entienda, este power usa un alcance simple:

| Pieza | Qué se usa |
|---|---|
| **Obligación** | LFPDPPP (México), **solo el deber de seguridad** de los datos personales. |
| **Puente** | Subcategorías de **NIST CSF 2.0** (verificadas en `core/csf-2.0-core.csv`). |
| **Catálogo de controles** | **CIS Controls v8.1, Grupo de Implementación 1 (IG1)**: 56 salvaguardas de "higiene cibernética esencial". |

```
Requisito LFPDPPP ─► Subcategoría CSF 2.0 ─► Salvaguarda CIS IG1 ─► Evidencia ─► ¿Cumple? ─► Brecha ─► Riesgo
```

Extensiones fuera de la primera versión: ISO/IEC 27001:2022 (Anexo A), PCI DSS v4.0.1, CIS IG2/IG3.

## 1. Ciclo de cumplimiento

1. **Inventariar obligaciones** con su fuente.
2. **Mapear** cada requisito a subcategorías CSF y a controles.
3. **Evaluar el diseño:** ¿el control existe y, si funciona, cubriría el requisito?
4. **Evaluar la efectividad operativa:** ¿funciona en la práctica, en todo el alcance y en el periodo?
5. **Recolectar evidencia** (R6).
6. **Gap analysis** y acciones en el POA&M.
7. **Reportar** y repetir (al menos una vez al año o ante cambios en la ley).

| Diseño | Efectividad | Resultado |
|---|---|---|
| OK | OK | **Cumple** |
| OK | NOK | **Cumple parcialmente**: el control existe pero falla o no cubre todo el alcance |
| NOK | — | **No cumple**: el control no existe o no cubre el requisito |
| Sin evidencia | Sin evidencia | **No demostrado**: se trata como brecha hasta tener evidencia |

## 2. La obligación: deber de seguridad de la LFPDPPP

La **Ley Federal de Protección de Datos Personales en Posesión de los Particulares** regula a las
empresas y personas que tratan datos personales. Se publicó una nueva ley en el Diario Oficial de la
Federación (DOF) el **20 de marzo de 2025**.

> **R10.** Los requisitos de abajo son una **redacción didáctica** del deber de seguridad, no una
> transcripción de la ley. No se cita un artículo hasta verificarlo en el texto vigente del DOF y en
> su reglamento. Todos llevan la marca *a validar con legal*.

| ID | Requisito (redacción didáctica) | Origen |
|---|---|---|
| **L1** | Establecer y mantener medidas de seguridad **administrativas, técnicas y físicas** que protejan los datos personales contra daño, pérdida, alteración, destrucción, o uso, acceso o tratamiento no autorizado. | Deber de seguridad de la LFPDPPP. |
| **L2** | Mantener un **inventario** de los datos personales y de los sistemas donde se tratan. | Acción que la normativa mexicana ha pedido para cumplir el deber de seguridad; verificar si sigue en el reglamento vigente. |
| **L3** | Realizar un **análisis de riesgos** de los datos personales. | Igual que L2. |
| **L4** | Limitar el acceso a los datos personales al **personal autorizado** y guardar **confidencialidad**. | Deberes de seguridad y confidencialidad. |
| **L5** | **Capacitar** al personal que trata datos personales. | Igual que L2. |
| **L6** | Registrar y **monitorear** el acceso a los sistemas con datos personales para detectar vulneraciones. | Medida técnica derivada de L1 (didáctica). |
| **L7** | Contar con **respaldos** y capacidad de **recuperación** de los datos. | Medida técnica derivada de L1 (didáctica). |
| **L8** | **Informar a los titulares** las vulneraciones de seguridad que afecten de forma significativa sus derechos. | Obligación de notificación de vulneraciones; verificar plazos y contenido en la ley vigente. |

## 3. Mapeo requisito → CSF 2.0 → CIS IG1

Los IDs de CSF se verificaron en `core/csf-2.0-core.csv`. Los IDs de CIS llevan la marca
`(verificar CIS v8.1)` hasta compararlos con la publicación oficial de CIS (R13).

| Req. | Subcategorías CSF 2.0 | Salvaguardas CIS v8.1 IG1 `(verificar CIS v8.1)` |
|---|---|---|
| L1 | GV.PO-01, PR.DS-01, PR.DS-02 | 3.1 Proceso de gestión de datos · 4.1 Proceso de configuración segura |
| L2 | ID.AM-07, ID.AM-02, ID.AM-01 | 3.2 Inventario de datos · 1.1 Inventario de activos · 2.1 Inventario de software |
| L3 | ID.RA-01, ID.RA-04, ID.RA-05, GV.RM-06 | 7.1 Proceso de gestión de vulnerabilidades · 7.2 Proceso de remediación |
| L4 | PR.AA-01, PR.AA-03, PR.AA-05 | 3.3 Listas de control de acceso a datos · 4.7 Gestionar cuentas por defecto · 5.1 Inventario de cuentas · 5.2 Contraseñas únicas · 5.3 Deshabilitar cuentas inactivas · 6.1 / 6.2 Alta y baja de accesos · 6.5 MFA para acceso administrativo |
| L5 | PR.AT-01, PR.AT-02 | 14.1 Programa de concientización |
| L6 | PR.PS-04, DE.CM-09 | 8.1 Proceso de gestión de logs · 8.2 Recolectar logs de auditoría |
| L7 | PR.DS-11, RC.RP-03 | 11.1 Proceso de recuperación de datos · 11.2 Respaldos automatizados · 11.3 Proteger datos de recuperación |
| L8 | RS.MA-01, RS.CO-02, RS.CO-03 | 17.1 Personal designado para incidentes · 17.2 Contactos para reportar · 17.3 Proceso para reportar incidentes |

Por qué funciona como ejercicio: los alumnos ven que **un requisito legal genérico** ("medidas de
seguridad") se vuelve **resultados verificables** (CSF) y luego **acciones concretas** (CIS).

## 4. Evidencia típica por requisito

| Req. | Evidencia de diseño | Evidencia de efectividad |
|---|---|---|
| L1 | Política de seguridad y de datos personales aprobada y fechada | Reportes de configuración segura, resultados de VA sin hallazgos críticos abiertos |
| L2 | Inventario de datos y sistemas con dueño | Muestra: un sistema real con datos personales aparece en el inventario |
| L3 | Metodología de riesgo (escalas, apetito) | Registro de riesgos actualizado en el periodo |
| L4 | Procedimiento de alta/baja de accesos, estándar de contraseñas | Lista de cuentas revisada; prueba de que no hay cuentas por defecto ni compartidas; MFA activo |
| L5 | Programa de capacitación | Lista de asistencia y evaluación del periodo |
| L6 | Estándar de logging | Muestra de logs de acceso a la base de datos con retención suficiente |
| L7 | Procedimiento de respaldo | Prueba de restauración documentada y fechada |
| L8 | Plan de respuesta a incidentes con paso de notificación | Simulacro o caso real con registro de la decisión de notificar |

Los reportes técnicos de los otros powers (VA, footprinting) son evidencia de **efectividad**,
normalmente en contra: si el VA encontró credenciales triviales en la base de clientes, L4 no es
efectivo aunque exista la política.

## 5. Matriz de cumplimiento (`06-matriz-cumplimiento.csv`)

Columnas: `req_id, requisito, fuente, subcategorias_csf, salvaguardas_cis, control_en_org, evidencia,
fecha_evidencia, diseño, efectividad, resultado, responsable, riesgo_id, accion_poam, notas`.

Regla R2: una fila sin `subcategorias_csf`, `control_en_org`, `evidencia` o `responsable` tiene
`resultado = No demostrado`.

## 6. Gap analysis de cumplimiento

Por cada requisito con resultado distinto de **Cumple**:

1. Qué falta (diseño o efectividad).
2. Riesgo asociado en el registro (si no existe, crearlo).
3. Acción en el POA&M con responsable y fecha.
4. Si se decide no corregir: aceptación formal (R5) con visto bueno de legal.

## 7. Errores comunes

- Copiar artículos de la ley sin verificar la versión vigente (R10).
- Dar por cumplido un requisito porque "existe la política" (falta efectividad).
- Mapear un requisito a una subcategoría que no existe o es de la v1.1 (R1).
- Confundir el catálogo de controles con el marco: CIS dice *cómo*, CSF dice *qué resultado* (R8).
