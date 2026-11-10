# CSF 2.0: componentes y Core

Guía de referencia del marco. Para Govern a detalle ver `grc-03-govern.md`; para Perfiles y Tiers,
`grc-04-perfiles-tiers.md`.

## 1. Qué es

El **NIST CSF 2.0** (documento NIST CSWP 29, publicado el 26 de febrero de 2024) es una taxonomía
de **resultados** (*outcomes*) de ciberseguridad de alto nivel. Ayuda a cualquier organización a
entender, evaluar, priorizar y comunicar su gestión del riesgo de ciberseguridad.

Características clave:

- **Voluntario y neutral:** no prescribe tecnologías ni *cómo* lograr cada resultado. Dice *qué*
  lograr; los controles concretos salen de otros catálogos (SP 800-53, ISO 27001, CIS Controls).
- **Para todo tipo de organización:** la versión 1.1 (2018) estaba dirigida a infraestructura
  crítica. La 2.0 amplía el alcance a organizaciones de cualquier tamaño y sector.
- **Nueva función Govern (GV):** pone el gobierno al centro, rodeando a las otras cinco funciones.
- **Más énfasis en la cadena de suministro** (categoría GV.SC).
- **Recursos en línea** que se actualizan por separado del documento: ejemplos de implementación,
  referencias informativas (mapeos), guías rápidas (Quick Start Guides) y perfiles comunitarios.
- Hay traducciones oficiales, incluida al español, en <https://www.nist.gov/cyberframework>.

Tiene tres componentes:

| Componente | Qué es | Para qué sirve en GRC |
|---|---|---|
| **CSF Core** | Jerarquía Funciones → Categorías → Subcategorías | Lenguaje común; base para mapear requisitos y controles. |
| **CSF Organizational Profiles** | Perfil actual y perfil objetivo de la organización | Gap analysis y plan de acción. |
| **CSF Tiers** | Niveles de rigor de las prácticas de gobierno y gestión del riesgo (1 a 4) | Fijar la ambición y comunicarla a la dirección. |

## 2. CSF Core

### 2.1 Las seis funciones

```
                ┌───────────────┐
                │  GOVERN (GV)  │   ← rodea y orienta a las demás
   ┌────────────┴───────────────┴────────────┐
   │ IDENTIFY ─► PROTECT ─► DETECT ─► RESPOND ─► RECOVER │
   │   (ID)       (PR)       (DE)      (RS)       (RC)   │
   └─────────────────────────────────────────┘
```

| Función | Propósito (resumen) |
|---|---|
| **GV Govern** | Se establecen, comunican y supervisan la estrategia, las expectativas y la política de gestión del riesgo de ciberseguridad. |
| **ID Identify** | Se entienden los riesgos actuales de ciberseguridad de la organización. |
| **PR Protect** | Se usan salvaguardas para gestionar esos riesgos. |
| **DE Detect** | Se encuentran y analizan posibles ataques y compromisos. |
| **RS Respond** | Se toman acciones ante un incidente detectado. |
| **RC Recover** | Se restauran los activos y operaciones afectados por un incidente. |

Las funciones no son una secuencia estricta: se trabajan en paralelo y de forma continua. GV, ID,
PR y DE son preventivas o continuas; RS y RC se activan con un incidente.

### 2.2 Las 22 categorías

| Función | Categoría | Nombre (en inglés, como aparece en el Core) |
|---|---|---|
| GV | GV.OC | Organizational Context |
| GV | GV.RM | Risk Management Strategy |
| GV | GV.RR | Roles, Responsibilities, and Authorities |
| GV | GV.PO | Policy |
| GV | GV.OV | Oversight |
| GV | GV.SC | Cybersecurity Supply Chain Risk Management |
| ID | ID.AM | Asset Management |
| ID | ID.RA | Risk Assessment |
| ID | ID.IM | Improvement |
| PR | PR.AA | Identity Management, Authentication, and Access Control |
| PR | PR.AT | Awareness and Training |
| PR | PR.DS | Data Security |
| PR | PR.PS | Platform Security |
| PR | PR.IR | Technology Infrastructure Resilience |
| DE | DE.CM | Continuous Monitoring |
| DE | DE.AE | Adverse Event Analysis |
| RS | RS.MA | Incident Management |
| RS | RS.AN | Incident Analysis |
| RS | RS.CO | Incident Response Reporting and Communication |
| RS | RS.MI | Incident Mitigation |
| RC | RC.RP | Incident Recovery Plan Execution |
| RC | RC.CO | Incident Recovery Communication |

Las categorías se dividen en **106 subcategorías** (p. ej., `GV.RM-02`). Algunos números se
retiraron o se movieron entre versiones, por eso la numeración tiene huecos. **La fuente de verdad
para IDs y textos es el CPRT de NIST** (<https://csrc.nist.gov/projects/cprt>); los textos de este
documento son resúmenes en español. En `core/` (en la raíz del power) hay una copia exportada del Core oficial
con los textos en inglés y los ejemplos de implementación. Contra esa copia se verificaron todos los
IDs de CSF 2.0 citados aquí. ID.GV, PR.IP, PR.PT y DE.DP solo aparecen como categorías retiradas de
la v1.1.

Cambios relevantes respecto a la 1.1: se creó GV (absorbe el antiguo ID.GV y la gestión de riesgo
de proveedores), ID.IM agrupa la mejora continua, PR.PS y PR.IR reemplazan parte de PR.IP/PR.PT, y
DE.DP desaparece como categoría.

## 3. Cómo usar la copia del Core (`core/`)

| Necesito… | Hago… |
|---|---|
| Comprobar que un ID existe (R1) | Buscar el ID en la columna `subcategory` o `category` de `core/csf-2.0-core.csv`. |
| Texto oficial de una subcategoría | Columna `subcategory_text` del CSV, o buscar el ID en `core/csf-2.0-core.md`. |
| Ideas de cómo lograr un resultado | Columna `implementation_examples` (separados por ` \| `). Son ejemplos, no requisitos. |
| Traducir un ID de la v1.1 (p. ej., PR.AC-01, ID.GV-01) | Buscar en `core/withdrawn-v1.1.csv`; la columna `reason` dice a qué ID de 2.0 se movió. |
| Listar todas las subcategorías de una categoría | Filtrar el CSV por la columna `category`. |

Ejemplos de consulta desde la terminal (dentro de la carpeta del power):

```bash
python3 -c "import csv;print([r['subcategory'] for r in csv.DictReader(open('core/csf-2.0-core.csv')) if r['function']=='GV'])"   # IDs de Govern
grep 'GV.RM-02' core/csf-2.0-core.md                     # texto oficial
grep '^PR.AC' core/withdrawn-v1.1.csv                    # a dónde se movió PR.AC (v1.1)
python3 -c "import csv;print(sum(1 for _ in csv.DictReader(open('core/csf-2.0-core.csv'))))"   # 106
```

Al citar una subcategoría en un entregable: **ID + texto oficial en inglés + resumen en español**.

### Cómo leer una subcategoría

`PR.AA-05` → función **PR** (Protect) · categoría **AA** (Identity Management, Authentication, and
Access Control) · subcategoría **05**: *"Access permissions, entitlements, and authorizations are
defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least
privilege and separation of duties"*.

Es un **resultado**: dice qué debe ser cierto, no qué producto instalar (R8). Para evaluarlo se
pregunta: ¿está definido en una política? ¿se gestiona? ¿se aplica? ¿se revisa? ¿incluye mínimo
privilegio y segregación de funciones? Cada "no" es una brecha parcial.

## 4. Recursos en línea

| Recurso | Uso |
|---|---|
| **CSF 2.0 Reference Tool / CPRT** | Explorar y exportar el Core (JSON, Excel); fuente de verdad de IDs. |
| **Implementation Examples** | Ejemplos de acciones concretas por subcategoría. |
| **Informative References** | Mapeos del Core a otros documentos (SP 800-53 Rev. 5, SP 800-171, CIS Controls, ISO/IEC 27001, entre otros). |
| **Quick Start Guides (QSG)** | Guías cortas: pequeñas empresas, perfiles, tiers, ERM, cadena de suministro, referencias informativas. |
| **Community Profiles** | Perfiles base por sector o amenaza. |
| **Concept Paper / FAQ / traducciones** | Material de apoyo, incluida la traducción al español. |

## 5. Cómo usar CSF 2.0 como eje de GRC

```
 Requisito (ley, contrato, norma, política)
        │  se mapea a
        ▼
 Subcategoría CSF (resultado esperado)  ◄── evaluada en el Perfil actual / objetivo
        │  se logra con
        ▼
 Control (SP 800-53, ISO 27001 Anexo A, CIS v8, control de AWS)
        │  se demuestra con
        ▼
 Evidencia (config, log, ticket, acta, reporte)  ──► Auditoría / reporte de cumplimiento
        │  si falta o falla
        ▼
 Brecha ─► Riesgo en el registro (GV.RM-06) ─► Tratamiento ─► POA&M
```

- **Gobierno:** GV.OC, GV.RM, GV.RR, GV.PO y GV.OV dan la estructura (apetito, roles, políticas,
  supervisión). Los Tiers comunican la ambición a la dirección.
- **Riesgo:** ID.RA (evaluación de riesgos) más GV.RM-06 (método estandarizado) más ID.IM (mejora).
- **Cumplimiento:** GV.OC-03 obliga a entender los requisitos; los mapeos (Informative References)
  permiten demostrar que el perfil cubre ISO 27001, PCI DSS u otros. "Evaluar una vez, reportar a
  varios marcos."

## 6. Referencias

- NIST CSWP 29, *The NIST Cybersecurity Framework (CSF) 2.0*: <https://doi.org/10.6028/NIST.CSWP.29>
- Sitio oficial y recursos: <https://www.nist.gov/cyberframework>
- CPRT (Core, ejemplos y mapeos): <https://csrc.nist.gov/projects/cprt>
- NIST SP 800-30 Rev. 1; NIST SP 800-53 Rev. 5; NIST IR 8286; NIST SP 800-61 Rev. 3.
