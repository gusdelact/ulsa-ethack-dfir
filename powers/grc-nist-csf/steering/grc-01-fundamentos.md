# Fundamentos de GRC

Guía de referencia del power. En modo Estudio, el agente la usa para explicar y para corregir las
preguntas de la sección "Fundamentos" de `grc-autoevaluacion.md`.

## 1. Definición

**GRC (Governance, Risk & Compliance)** es la forma integrada en que una organización dirige su
operación, maneja la incertidumbre y demuestra que cumple sus obligaciones. OCEG lo define como el
conjunto integrado de capacidades que permiten a una organización **alcanzar sus objetivos de forma
confiable, atender la incertidumbre y actuar con integridad** ("Principled Performance").

Los tres componentes dependen entre sí:

| Componente | Pregunta que responde | Quién lo encabeza | Productos típicos |
|---|---|---|---|
| **Governance** (gobierno) | ¿Hacia dónde vamos, quién decide y cómo rendimos cuentas? | Consejo, dirección general, comité de riesgos | Estrategia, apetito de riesgo, políticas, roles (RACI), indicadores |
| **Risk** (gestión de riesgos) | ¿Qué puede impedir los objetivos y qué hacemos al respecto? | Dueños de riesgo, CISO, área de riesgos | Registro de riesgos, matriz de calor, plan de tratamiento |
| **Compliance** (cumplimiento) | ¿Cumplimos leyes, contratos, normas y nuestras propias políticas? ¿Lo podemos demostrar? | Cumplimiento, legal, auditoría | Matriz de requisitos, evidencia, gap analysis, reportes de auditoría |

Sin gobierno no hay quién acepte un riesgo. Sin gestión de riesgos el cumplimiento se vuelve una
lista de casillas sin prioridad. Sin cumplimiento no hay evidencia de que los controles funcionan.

> **Cumplir no es estar seguro.** Una organización puede pasar una auditoría y aun así ser
> vulnerable. El cumplimiento fija un piso mínimo; el riesgo define hasta dónde subir.

## 2. Gobierno (Governance)

El gobierno de ciberseguridad traduce los objetivos del negocio en dirección para la seguridad.

- **Contexto organizacional:** misión, partes interesadas, servicios críticos, dependencias y
  obligaciones legales.
- **Apetito y tolerancia al riesgo:**
  - *Apetito*: cuánto riesgo, en términos generales, está dispuesta a asumir la organización para
    lograr sus objetivos (p. ej., "riesgo bajo en datos de clientes").
  - *Tolerancia*: la desviación aceptable medible (p. ej., "máximo 4 h de indisponibilidad del
    portal al mes").
- **Roles y responsabilidades:** quién es dueño de cada riesgo, activo y control. Una matriz RACI
  (Responsible, Accountable, Consulted, Informed) evita huecos y duplicidades.
- **Jerarquía documental:**

| Nivel | Qué es | Obligatorio | Ejemplo |
|---|---|---|---|
| Política | Intención y dirección de la dirección | Sí | "Todo acceso remoto usa MFA." |
| Estándar | Requisito medible que concreta la política | Sí | "MFA con FIDO2 o TOTP; SMS no permitido." |
| Procedimiento | Pasos para cumplir el estándar | Sí | "Alta de MFA en el IdP: paso 1, 2, 3." |
| Guía (guideline) | Recomendación | No | "Se sugiere usar llave física para administradores." |

- **Supervisión (oversight):** revisión periódica de la estrategia, métricas (KPIs y KRIs) y
  resultados de auditoría para ajustar el rumbo.

## 3. Gestión de riesgos (Risk Management)

### 3.1 Conceptos

| Término | Definición breve |
|---|---|
| **Activo** | Algo con valor para la organización: datos, sistemas, personas, procesos, reputación. |
| **Amenaza** | Circunstancia o actor con potencial de causar daño (ransomware, insider, error humano, inundación). |
| **Vulnerabilidad** | Debilidad que una amenaza puede explotar (CVE sin parchar, contraseña débil, falta de proceso). |
| **Riesgo** | Posibilidad de que una amenaza explote una vulnerabilidad y cause impacto. Se expresa como **probabilidad × impacto**. |
| **Riesgo inherente** | Riesgo antes de aplicar controles. |
| **Control** | Medida que modifica el riesgo (reduce probabilidad o impacto). |
| **Riesgo residual** | Riesgo que queda después de los controles. Debe quedar dentro del apetito. |
| **Dueño del riesgo** | Persona con autoridad para decidir el tratamiento y responder por él. |

> **CVSS no es riesgo.** CVSS mide la severidad técnica de una vulnerabilidad. El riesgo agrega el
> valor del activo, la exposición, la probabilidad real de explotación (p. ej., EPSS o el catálogo
> KEV de CISA) y el impacto al negocio. Un CVSS 9.8 en un equipo aislado sin datos puede ser menor
> riesgo que un CVSS 6.5 en el portal de pagos.

### 3.2 Ciclo de gestión de riesgos

Basado en NIST SP 800-30 Rev. 1 (preparar, conducir, comunicar, mantener) e ISO 31000:

```
 Establecer contexto ─► Identificar ─► Analizar ─► Evaluar ─► Tratar ─► Monitorear y revisar
        ▲                                                                      │
        └──────────────────────── comunicación y consulta ◄────────────────────┘
```

1. **Contexto:** alcance, criterios de riesgo, escalas de probabilidad e impacto, apetito.
2. **Identificación:** escenarios "amenaza → vulnerabilidad → activo → impacto".
3. **Análisis:** cualitativo (matriz 5×5), semicuantitativo (puntajes) o cuantitativo (FAIR, ALE =
   SLE × ARO).
4. **Evaluación:** comparar contra el apetito y priorizar.
5. **Tratamiento:** una de cuatro respuestas.
6. **Monitoreo:** KRIs, revisión periódica del registro, disparadores (incidentes, cambios).

### 3.3 Matriz cualitativa 5×5 (ejemplo)

| Probabilidad \ Impacto | 1 Insignificante | 2 Menor | 3 Moderado | 4 Mayor | 5 Catastrófico |
|---|---|---|---|---|---|
| **5 Casi seguro** | 5 Medio | 10 Alto | 15 Crítico | 20 Crítico | 25 Crítico |
| **4 Probable** | 4 Bajo | 8 Medio | 12 Alto | 16 Crítico | 20 Crítico |
| **3 Posible** | 3 Bajo | 6 Medio | 9 Medio | 12 Alto | 15 Crítico |
| **2 Improbable** | 2 Bajo | 4 Bajo | 6 Medio | 8 Medio | 10 Alto |
| **1 Raro** | 1 Bajo | 2 Bajo | 3 Bajo | 4 Bajo | 5 Medio |

Los cortes (Bajo/Medio/Alto/Crítico) los define el gobierno según su apetito; no son universales.

### 3.4 Opciones de tratamiento

| Respuesta | Qué significa | Ejemplo |
|---|---|---|
| **Mitigar** | Aplicar controles para reducir probabilidad o impacto | Parchar, segmentar, MFA |
| **Transferir** | Compartir el impacto con un tercero | Ciberseguro, contrato con SLA y penalizaciones |
| **Aceptar** | Asumirlo de forma documentada y firmada por el dueño | Sistema legado sin parche, con fecha de revisión |
| **Evitar** | Eliminar la actividad que genera el riesgo | Dar de baja un servicio expuesto que no se usa |

CSF 2.0 también reconoce el **riesgo positivo** (oportunidades) en GV.RM-07.

## 4. Cumplimiento (Compliance)

### 4.1 Tipos de obligación

| Tipo | Origen | Ejemplos |
|---|---|---|
| Regulatoria | Ley o autoridad | LFPDPPP (México), GDPR, HIPAA, regulación financiera |
| Contractual | Contratos con clientes, socios, marcas | PCI DSS (marcas de tarjetas), cláusulas de seguridad, SLAs |
| Voluntaria / certificable | Decisión de la organización | ISO/IEC 27001, SOC 2, alineación con NIST CSF |
| Interna | Políticas propias | Política de contraseñas, de respaldos, de uso aceptable |

### 4.2 Ciclo de cumplimiento

1. **Inventariar obligaciones** (matriz de requisitos con fuente, artículo o cláusula).
2. **Mapear** cada requisito a controles (un control puede cubrir varios requisitos: "evaluar una
   vez, cumplir muchas").
3. **Evaluar** el estado del control: diseño (¿existe y es adecuado?) y efectividad operativa
   (¿funciona en la práctica durante el periodo?).
4. **Recolectar evidencia**: configuraciones, logs, tickets, actas, capturas con fecha.
5. **Gap analysis y plan de acción** (en NIST se usa el término POA&M: *Plan of Action and
   Milestones*).
6. **Reportar y auditar**; repetir.

### 4.3 Evidencia de calidad

Una buena evidencia es **pertinente** (prueba el control), **fechada**, **completa** (cubre el
periodo y la población), **verificable** (alguien más la puede reproducir) y **trazable** (se sabe
de qué sistema salió y quién la obtuvo).

## 5. Controles

| Clasificación por función | Ejemplo |
|---|---|
| Preventivo | MFA, firewall, segregación de funciones |
| Detectivo | SIEM, GuardDuty, revisión de logs, auditoría |
| Correctivo | Restauración de respaldos, parche, playbook de respuesta |
| Disuasivo | Avisos legales, política de sanciones |
| Compensatorio | Monitoreo reforzado cuando no se puede parchar |

| Clasificación por naturaleza | Ejemplo |
|---|---|
| Administrativo (gerencial) | Políticas, capacitación, evaluación de proveedores |
| Técnico (lógico) | Cifrado, control de acceso, EDR |
| Físico | Acceso a centro de datos, CCTV |

## 6. Modelo de las tres líneas (IIA, 2020)

| Rol | Quién | Qué hace |
|---|---|---|
| **Órgano de gobierno** | Consejo / comité | Rinde cuentas a las partes interesadas, fija apetito, supervisa. |
| **Primera línea** | Operación, TI, dueños de procesos | Gestiona el riesgo día a día y opera los controles. |
| **Segunda línea** | Riesgos, cumplimiento, seguridad (CISO) | Define marcos, asesora, monitorea y cuestiona a la primera línea. |
| **Tercera línea** | Auditoría interna | Aseguramiento independiente al órgano de gobierno. |
| Externos | Auditores externos, reguladores | Aseguramiento adicional. |

El pentest y el VA del curso aportan evidencia técnica a la segunda y tercera línea.

## 7. Marcos y regulaciones de referencia

| Marco / norma | Tipo | Para qué sirve en GRC |
|---|---|---|
| **NIST CSF 2.0** | Marco de resultados (voluntario) | **Eje del power.** Lenguaje común para gobierno, riesgo y cumplimiento. |
| NIST SP 800-30 Rev. 1 | Guía | Metodología de evaluación de riesgos. |
| NIST SP 800-37 Rev. 2 (RMF) | Marco | Ciclo de autorización y monitoreo de sistemas (sector federal EE. UU.). |
| NIST SP 800-53 Rev. 5 | Catálogo de controles | Controles detallados; NIST publica su mapeo a CSF 2.0. |
| NIST IR 8286 | Guía | Integrar riesgo de ciberseguridad con riesgo empresarial (ERM). |
| ISO/IEC 27001:2022 | Norma certificable | SGSI; Anexo A con 93 controles en 4 temas (organizacionales, personas, físicos, tecnológicos). |
| ISO/IEC 27005:2022 | Guía | Gestión de riesgos de seguridad de la información. |
| ISO 31000:2018 | Guía | Principios generales de gestión de riesgos. |
| CIS Controls v8 / v8.1 | Catálogo priorizado | 18 controles con grupos de implementación IG1–IG3; buen punto de partida práctico. |
| COBIT 2019 | Marco de gobierno de TI | Gobierno y gestión de TI empresarial. |
| PCI DSS v4.0.1 | Estándar contractual | Organizaciones que procesan tarjetas de pago. |
| SOC 2 (AICPA) | Reporte de atestiguamiento | Proveedores de servicio que demuestran controles a clientes. |
| **LFPDPPP (México)** | Ley | Protección de datos personales en posesión de particulares. Se publicó una nueva ley en el DOF el 20 de marzo de 2025; **verificar la versión vigente y su reglamento antes de citarla.** |

> Los requisitos legales se documentan como insumo, pero su interpretación final corresponde al
> área legal. El power no da asesoría jurídica.

## 8. GRC en la nube (AWS)

El **modelo de responsabilidad compartida** define qué controles opera AWS ("seguridad *de* la
nube") y cuáles opera el cliente ("seguridad *en* la nube"). Herramientas útiles como evidencia:

| Servicio | Aporte a GRC |
|---|---|
| AWS Organizations + SCPs | Gobierno preventivo (guardrails) a nivel de cuentas. |
| AWS Config + conformance packs | Evaluación continua de configuraciones contra reglas (existe un paquete de buenas prácticas para NIST CSF). |
| AWS Security Hub | Puntaje contra estándares (AWS FSBP, CIS AWS Foundations, NIST SP 800-53 Rev. 5, PCI DSS). |
| AWS Audit Manager | Recolección automática de evidencia por marco. Verificar qué versión de NIST CSF trae disponible. |
| AWS CloudTrail | Evidencia de actividad y trazabilidad (visto en el módulo de CloudTrail del curso). |
| Amazon GuardDuty | Control detectivo (visto en el módulo de GuardDuty del curso). |
| AWS Artifact | Reportes de cumplimiento de AWS (SOC, ISO, PCI) para la parte que opera AWS. |

## 9. Errores comunes

- Tratar el marco como checklist y "cumplir" sin priorizar por riesgo.
- Registros de riesgo sin dueño, sin fecha de revisión o con riesgos genéricos ("hackeo").
- Confundir severidad técnica (CVSS) con riesgo de negocio.
- Aceptar riesgos de forma verbal, sin firma ni vencimiento.
- Evidencia sin fecha o que no cubre el periodo auditado.
- Políticas que nadie lee ni se revisan.
- Medir solo actividad (número de parches) y no resultados (tiempo de exposición de activos críticos).

## 10. Siguiente guía

- Para el marco: `grc-02-csf-core.md`.
- Para el detalle de riesgo y ALE: `grc-05-riesgo.md`.
- Para el detalle de cumplimiento: `grc-06-cumplimiento.md`.
- Para AWS: `grc-aws-evidencia.md`.
