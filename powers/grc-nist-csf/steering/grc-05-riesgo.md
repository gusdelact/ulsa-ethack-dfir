# Evaluación y tratamiento de riesgos

Subcategorías CSF 2.0 que cubre esta guía: **GV.RM-02** (apetito), **GV.RM-06** (método
estandarizado), **ID.AM-05** (priorizar activos), **ID.RA-01** a **ID.RA-07** (vulnerabilidades,
amenazas, impacto y probabilidad, riesgo inherente, respuesta, excepciones).

Metodología base: **NIST SP 800-30 Rev. 1**, *Guide for Conducting Risk Assessments*
(preparar → conducir → comunicar → mantener).

## 1. Preparar (contexto y método)

Antes de calificar un solo riesgo deben existir (criterio de avance del `POWER.md`):

1. **Alcance** (`00-alcance.md`).
2. **Apetito y tolerancia** (`01-apetito-riesgo.md`, ver `grc-03-govern.md`).
3. **Escalas** (`02-escalas.md`): las mismas para todos los riesgos (GV.RM-06).
4. **Inventario de activos críticos con dueño** (`03-inventario-activos.csv`).

### Escala de probabilidad (ejemplo del curso)

| Valor | Nivel | Criterio |
|---|---|---|
| 1 | Raro | No se conoce explotación; requiere acceso interno y habilidades avanzadas. |
| 2 | Improbable | Explotación posible pero con condiciones poco comunes. |
| 3 | Posible | Explotación pública conocida; requiere algún acceso o paso previo. |
| 4 | Probable | Expuesto a Internet o a la red interna, explotación sencilla y documentada. |
| 5 | Casi seguro | Expuesto, sin autenticación o con credenciales triviales; ya demostrado en una prueba o incidente. |

Insumos para la probabilidad (R3): exposición (Internet / interna), si un pentest lo explotó,
EPSS (probabilidad de explotación en 30 días, FIRST), si está en el catálogo KEV de CISA, y el
vector y complejidad de CVSS.

### Escala de impacto (ejemplo del curso)

| Valor | Nivel | Datos personales | Operación | Financiero (MXN, ejemplo) | Legal / reputación |
|---|---|---|---|---|---|
| 1 | Insignificante | Ninguno | < 1 h | < 50 mil | Ninguno |
| 2 | Menor | Datos internos no sensibles | 1–8 h | 50–500 mil | Queja aislada |
| 3 | Moderado | Datos personales de pocos titulares | 8–24 h | 0.5–2 M | Aviso a titulares, nota local |
| 4 | Mayor | Datos personales de muchos clientes | 1–3 días | 2–10 M | Procedimiento de la autoridad, prensa nacional |
| 5 | Catastrófico | Datos personales sensibles o financieros masivos | > 3 días | > 10 M | Sanción, pérdida de clientes clave |

El impacto se califica con el **peor criterio aplicable** de la fila. Las cifras son ejemplo; cada
organización define las suyas según su tamaño.

### Matriz 5×5 y niveles

`Riesgo = Probabilidad × Impacto` (1 a 25).

| Puntaje | Nivel | Respuesta esperada (ejemplo de apetito) |
|---|---|---|
| 1–4 | **Bajo** | Aceptable; se monitorea. |
| 5–9 | **Medio** | Tratar en el plan anual; el dueño puede aceptar con justificación. |
| 10–14 | **Alto** | Tratar en ≤ 90 días; aceptación solo por la dirección. |
| 15–25 | **Crítico** | Tratar de inmediato (≤ 30 días); no se acepta sin controles compensatorios. |

## 2. Conducir la evaluación

### 2.1 Identificar escenarios (ID.RA-01, ID.RA-03)

Un riesgo bien escrito tiene cuatro partes:

> **Amenaza** (quién o qué) **explota** una **vulnerabilidad** (debilidad) **en** un **activo**
> **causando** un **impacto** (al negocio).

| Mal escrito | Bien escrito |
|---|---|
| "Hackeo de la base de datos" | Un atacante externo usa credenciales débiles reutilizadas (`robin`) para leer la base `customers` en MySQL, exponiendo datos personales de clientes y obligando a notificar a los titulares. |
| "DNS inseguro" | Un atacante obtiene la zona interna completa mediante transferencia de zona abierta, conociendo hosts y rangos internos y acelerando ataques posteriores. |

Fuentes de escenarios: reportes de los otros powers (ver `grc-integracion-powers.md`), incidentes
previos, inteligencia de amenazas (ID.RA-02) y entrevistas con dueños de procesos.

### 2.2 Analizar (ID.RA-04, ID.RA-05)

Por cada escenario:

1. Probabilidad (1–5) con justificación.
2. Impacto (1–5) con justificación.
3. **Riesgo inherente** = P × I, considerando solo los controles que hoy funcionan con evidencia.
4. Controles existentes y su efectividad (con evidencia, R6).

### 2.3 Tratar (ID.RA-06)

| Respuesta | Cuándo | Qué se registra |
|---|---|---|
| **Mitigar** | El costo del control es razonable frente al riesgo | Acción en el POA&M, responsable, fecha, riesgo residual esperado |
| **Transferir** | Impacto financiero alto y probabilidad baja | Seguro o contrato; recordar que la responsabilidad legal no se transfiere |
| **Aceptar** | Riesgo dentro del apetito, o costo del control mayor que el beneficio | Plantilla `09-aceptacion-riesgo-<ID>.md` con firma y vencimiento (R5) |
| **Evitar** | La actividad no aporta valor suficiente | Decisión de la dirección y fecha de baja del servicio |

**Riesgo residual** = P × I esperados *después* del tratamiento. Debe quedar dentro del apetito o
contar con aceptación formal.

### 2.4 Excepciones (ID.RA-07)

Una excepción (p. ej., "este servidor no puede parcharse hasta mayo") es un riesgo aceptado
temporalmente: se registra igual que una aceptación (R5), con controles compensatorios y fecha de
vencimiento.

## 3. Introducción cuantitativa: ALE

La matriz cualitativa prioriza; el **ALE** traduce el riesgo a dinero para hablar con la dirección
y comparar el costo de un control contra el beneficio.

| Término | Fórmula / definición |
|---|---|
| **AV** (Asset Value) | Valor del activo en dinero (reposición, ingresos que genera, costo de una brecha). |
| **EF** (Exposure Factor) | Porcentaje del valor que se pierde si el escenario ocurre (0 a 1). |
| **SLE** (Single Loss Expectancy) | Pérdida por evento: **SLE = AV × EF**. |
| **ARO** (Annualized Rate of Occurrence) | Veces que se espera que ocurra en un año (0.1 = una vez cada 10 años). |
| **ALE** (Annualized Loss Expectancy) | Pérdida esperada por año: **ALE = SLE × ARO**. |
| **Valor del control** | **ALE antes − ALE después − costo anual del control**. Si es positivo, el control se justifica económicamente. |
| **ROSI** (opcional) | (ALE antes − ALE después − costo) / costo. |

### Ejemplo (caso Inlanefreight, cifras ficticias)

Escenario R-01: acceso no autorizado a la base `customers` por credenciales débiles.

| Dato | Valor | Justificación |
|---|---|---|
| AV | 4,000,000 MXN | Costo estimado de una brecha de datos de clientes: notificación, atención, forense, pérdida de clientes. |
| EF | 0.5 | Se expondría la base completa, pero no todos los costos se materializan. |
| SLE | 4,000,000 × 0.5 = **2,000,000 MXN** | |
| ARO antes | 0.5 | Credenciales triviales, servicio accesible; se espera un evento cada 2 años. |
| ALE antes | 2,000,000 × 0.5 = **1,000,000 MXN/año** | |
| Control | Eliminar cuentas de prueba, contraseñas robustas, MFA en accesos administrativos, restringir 3306 a la red de aplicación | |
| Costo anual del control | 150,000 MXN | Horas de TI y licencia de MFA. |
| ARO después | 0.05 | Un evento cada 20 años. |
| ALE después | 2,000,000 × 0.05 = **100,000 MXN/año** | |
| Valor del control | 1,000,000 − 100,000 − 150,000 = **750,000 MXN/año** | Se justifica. |

### Límites del ALE (explicarlos siempre)

- Los valores de ARO y EF son estimaciones; un rango (mínimo, más probable, máximo) es más honesto
  que un número único.
- No captura bien eventos raros y catastróficos.
- Sirve para **comparar opciones**, no para predecir la pérdida exacta.
- Metodologías más completas (p. ej., FAIR) quedan fuera del alcance de este power.

## 4. Comunicar y mantener

- El registro de riesgos se revisa al menos **trimestralmente** y siempre que haya un incidente, un
  cambio relevante o un nuevo reporte técnico.
- **KRIs** (Key Risk Indicators) ligados a la tolerancia, por ejemplo:

| KRI | Umbral (ejemplo) | Tolerancia relacionada |
|---|---|---|
| Servicios expuestos a Internet sin dueño | 0 | Exposición a Internet |
| Cuentas por defecto o compartidas en sistemas con datos personales | 0 | Datos personales |
| Vulnerabilidades críticas en activos críticos abiertas > 30 días | 0 | Datos personales / disponibilidad |
| Riesgos aceptados vencidos sin revisión | 0 | Gobierno |

## 5. Columnas del registro de riesgos

Ver plantilla `04-registro-riesgos.csv` en `grc-plantillas.md`. Columnas obligatorias:
`id, escenario, fuente, activo, dueño, P, I, inherente, nivel, controles_existentes, tratamiento,
acción_poam, P_res, I_res, residual, subcategorias_csf, fecha_revision, estado`.
