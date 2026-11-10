# Plantillas de la carpeta del caso

El agente copia cada plantilla al archivo correspondiente en `grc/casos/<ORG>-<AAAA>/` y la llena
con lo que diga el usuario y lo que encuentre en los insumos. Fechas en formato `AAAA-MM-DD`.

---

## `00-alcance.md`

```markdown
# <ORG>-<AAAA>: Alcance y contexto

- **Organización:** <nombre> (<laboratorio / simulada / real asignada>)
- **Unidad o sistemas en alcance:** <>
- **Exclusiones:** <>
- **Analista GRC:** <nombre> · **Patrocinador:** <nombre y rol>
- **Destinatario del reporte:** <dirección / auditoría / equipo técnico>
- **Horizonte del plan:** <12 meses>
- **Tier actual (gobierno / gestión):** <por evaluar> · **Tier objetivo:** <>

## Contexto (GV.OC)
- **Misión:** <>
- **Servicios críticos:** <qué no puede dejar de funcionar>
- **Partes interesadas y expectativas:** <clientes, empleados, socios, autoridad>
- **Dependencias (proveedores, nube):** <>

## Obligaciones (GV.OC-03)
| ID | Obligación | Tipo (ley / contrato / norma / interna) | Fuente | Estado de verificación |
|---|---|---|---|---|

## Roles (GV.RR-02)
| Rol | Persona | Responsabilidad |
|---|---|---|

## Insumos
| Insumo | Ruta | Fecha | Power que lo generó |
|---|---|---|---|

## Supuestos
- <cada supuesto marcado como tal (R7)>
```

## `01-apetito-riesgo.md`

```markdown
# Apetito y tolerancia al riesgo (GV.RM-02)

Estado: <propuesto / aprobado por <nombre> el <fecha>>

| Tema | Apetito (muy bajo / bajo / moderado / alto) | Tolerancia medible | KRI |
|---|---|---|---|
| Datos personales | | | |
| Disponibilidad | | | |
| Cumplimiento legal | | | |
| Exposición a Internet | | | |
| Proveedores | | | |
```

## `02-escalas.md`

```markdown
# Escalas y método (GV.RM-06)

## Probabilidad (1–5)
| Valor | Nivel | Criterio |
|---|---|---|

## Impacto (1–5)
| Valor | Nivel | Datos personales | Operación | Financiero | Legal / reputación |
|---|---|---|---|---|---|

## Niveles
| Puntaje P×I | Nivel | Plazo de tratamiento | Quién puede aceptar |
|---|---|---|---|
| 1–4 | Bajo | | |
| 5–9 | Medio | | |
| 10–14 | Alto | | |
| 15–25 | Crítico | | |

## Cuantitativo (opcional): ALE = (AV × EF) × ARO
```

## `03-inventario-activos.csv`

```csv
id,activo,tipo,descripcion,dueño,confidencialidad,integridad,disponibilidad,criticidad,ubicacion,datos_personales,dependencias,fuente
A-01,,servidor|aplicación|base de datos|datos|proveedor|persona,,,,alta|media|baja,alta|media|baja,alta|media|baja,alta|media|baja,,sí|no,,
```

## `04-registro-riesgos.csv`

```csv
id,escenario,fuente,activo,dueño,P,I,inherente,nivel,controles_existentes,tratamiento,accion_poam,P_res,I_res,residual,subcategorias_csf,requisitos,fecha_revision,estado
R-01,"<amenaza> explota <vulnerabilidad> en <activo> causando <impacto>",<power/archivo#hallazgo>,A-01,,,,,,,mitigar|transferir|aceptar|evitar,P-01,,,,,L4,,abierto|en tratamiento|cerrado|aceptado
```

## `05-perfil-csf.csv`

```csv
subcategoria,texto_oficial,estado_actual,evidencia,fecha_evidencia,prioridad_objetivo,estado_objetivo,justificacion,riesgos,brecha
GV.OC-03,"<copiar de core/csf-2.0-core.csv>",No|Parcial|Sí|Sin evidencia,,,Alta|Media|Baja,Sí|Parcial,"R-01; L1",R-01,sí|no
```

## `06-matriz-cumplimiento.csv`

```csv
req_id,requisito,fuente,subcategorias_csf,salvaguardas_cis,control_en_org,evidencia,fecha_evidencia,diseño,efectividad,resultado,responsable,riesgo_id,accion_poam,notas
L1,"<redacción didáctica>","LFPDPPP (DOF 2025-03-20), deber de seguridad; artículo por verificar — a validar con legal","GV.PO-01; PR.DS-01","3.1; 4.1 (verificar CIS v8.1)",,,,OK|NOK|Sin evidencia,OK|NOK|Sin evidencia,Cumple|Parcial|No cumple|No demostrado,,,,
```

## `07-gap-analysis.md`

```markdown
# Gap analysis

| # | Subcategoría / requisito | Estado actual | Objetivo | Qué falta | Riesgos | Prioridad | Acción POA&M |
|---|---|---|---|---|---|---|---|

## Causas comunes
- <p. ej., no hay dueño de los servicios expuestos; no hay estándar de configuración>
```

## `08-poam.csv`

```csv
id,brecha,accion,responsable,inicio,fin,hitos,costo_estimado,estado,riesgos,riesgo_residual_esperado,evidencia_cierre
P-01,,,,AAAA-MM-DD,AAAA-MM-DD,,bajo|medio|alto (o MXN),pendiente|en curso|terminado|atrasado,R-01,,
```

## `09-aceptacion-riesgo-<ID>.md`

```markdown
# Aceptación de riesgo <R-XX>

- **Riesgo:** <escenario>
- **Nivel residual aceptado:** <P × I = n, nivel>
- **Justificación de negocio:** <>
- **Controles compensatorios:** <>
- **Requisitos legales afectados:** <L-x / ninguno> · **Visto bueno de legal:** <sí / no aplica>
- **Dueño del riesgo:** <nombre y cargo>
- **Firma:** <nombre> · **Fecha:** <AAAA-MM-DD>
- **Vencimiento / próxima revisión:** <AAAA-MM-DD>
```

## `10-politica-<tema>.md`

```markdown
# Política de <tema>

- **Versión / fecha / aprobó:** <>
- **Propósito:** <>
- **Alcance:** <personas, sistemas, datos>
- **Declaraciones de política:** <enunciados "debe", medibles y cortos>
- **Roles y responsabilidades:** <>
- **Cumplimiento y excepciones:** <cómo se mide; excepciones vía aceptación de riesgo>
- **Referencias:** <subcategorías CSF y requisitos que atiende>
- **Revisión:** <anual o ante cambios (GV.PO-02)>
```

## `11-reporte-ejecutivo.md`

Estructura en `grc-07-monitoreo-mejora.md`, sección 5.

## `bitacora.md`

```markdown
# Bitácora

| Fecha | Actividad | Decisión / resultado | Responsable |
|---|---|---|---|
```
