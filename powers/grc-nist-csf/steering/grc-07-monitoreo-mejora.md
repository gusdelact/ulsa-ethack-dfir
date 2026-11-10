# Monitoreo, mejora y reporte ejecutivo

Subcategorías que cubre: **GV.OV-01**, **GV.OV-02**, **GV.OV-03** (supervisión), **ID.IM-01** a
**ID.IM-04** (mejora), **GV.PO-02** (actualizar políticas).

## 1. Ciclo de mejora continua

```
 Planear (perfil objetivo, POA&M) ─► Hacer (ejecutar acciones) ─► Verificar (KRIs, auditoría, pruebas) ─► Actuar (ajustar estrategia y políticas)
        ▲                                                                                                          │
        └──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Fuente de mejora | Subcategoría | Ejemplo |
|---|---|---|
| Evaluaciones (auditorías, gap analysis) | ID.IM-01 | Gap analysis anual contra el perfil objetivo |
| Pruebas y ejercicios (VA, pentest, simulacros) | ID.IM-02 | Reporte de footprinting o pentest del curso |
| Operación diaria | ID.IM-03 | Tickets recurrentes, errores de cambios |
| Planes de respuesta y continuidad | ID.IM-04 | Lecciones aprendidas del power `incident-handling-nist` |

## 2. Qué se revisa y cada cuándo

| Elemento | Frecuencia mínima | Disparadores adicionales |
|---|---|---|
| Registro de riesgos | Trimestral | Incidente, nuevo reporte técnico, cambio de sistema |
| Perfil actual | Anual | Cambio grande de alcance |
| Políticas (GV.PO-02) | Anual | Cambio de ley, nueva amenaza relevante, incidente |
| Aceptaciones de riesgo | En su fecha de vencimiento | Cambio en el activo o en la amenaza |
| Matriz de cumplimiento | Anual | Reforma de la ley o nuevo contrato |
| POA&M | Mensual | Atraso de una acción de prioridad alta |

## 3. Métricas

Medir **resultados**, no solo actividad.

| Tipo | Ejemplo | Para quién |
|---|---|---|
| KRI (riesgo) | Servicios expuestos sin dueño; cuentas por defecto en sistemas con datos personales | Dirección |
| KPI (desempeño) | % de acciones del POA&M a tiempo; tiempo medio de remediación de críticas | Seguridad y TI |
| Cumplimiento | % de requisitos L1–L8 en estado *Cumple* | Dirección, legal |
| Madurez | Tier actual vs objetivo en gobierno y en gestión | Dirección |

## 4. Auditoría

- La auditoría (tercera línea) prueba **diseño y efectividad** con evidencia del periodo.
- Muestreo: se eligen elementos de la población (cuentas, cambios, respaldos) y se revisa que el
  control funcionó en cada uno.
- Un hallazgo de auditoría entra al registro de riesgos y al POA&M igual que un hallazgo técnico.

## 5. Reporte ejecutivo (`11-reporte-ejecutivo.md`)

Una a dos páginas, en lenguaje de negocio. Estructura:

1. **Resumen** (5 líneas): situación, riesgo principal, decisión que se pide.
2. **Postura:** Tier actual → objetivo (gobierno y gestión), con justificación.
3. **Top 5–10 riesgos:** escenario en una línea, nivel inherente → residual esperado, dueño.
4. **Mapa de calor** (matriz 5×5 con los IDs de los riesgos).
5. **Cumplimiento:** estado de L1–L8 (Cumple / Parcial / No / No demostrado).
6. **Plan:** acciones principales del POA&M, fechas, costo estimado y ALE evitado cuando exista.
7. **Decisiones solicitadas:** aprobar apetito, presupuesto, aceptaciones de riesgo.
8. **Anexos:** rutas a registro, perfil, matriz y evidencia.

Reglas al redactar:

- Sin jerga técnica en el cuerpo; los CVE y comandos van a los anexos.
- Cada afirmación remite a un ID de riesgo, requisito o evidencia (R7).
- No exponer credenciales ni datos personales (R11): "credenciales triviales reutilizadas en la base
  de clientes", no el usuario y la contraseña.
