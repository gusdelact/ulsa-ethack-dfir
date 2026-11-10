# Caso de referencia: Inlanefreight

Caso resuelto que el agente usa como ejemplo en el modo Estudio y como referencia de calidad en los
modos Evaluación y Cumplimiento.

> **Encuadre.** Inlanefreight es una empresa **ficticia** de HTB Academy usada en el curso. Los
> hallazgos técnicos son **hechos** tomados del reporte del laboratorio de footprinting
> (`reporte-enumeracion-lab.md`, en la raíz del workspace del curso, objetivo `inlanefreight.htb`).
> El contexto de negocio, los dueños, las cifras y el estado de gobierno son **supuestos didácticos**
> (R7) y se marcan como tales.

## 1. Alcance y contexto (GV.OC)

| Campo | Valor | Tipo |
|---|---|---|
| Organización | Inlanefreight (laboratorio) | Hecho |
| Sistemas en alcance | Host `inlanefreight.htb` con FTP, SMTP, DNS, POP3/IMAP, SMB, MySQL, TFTP | Hecho (footprinting) |
| Misión | Servicios de logística y transporte de carga para clientes empresariales | Supuesto |
| Servicio crítico | Portal de clientes (`app`) y su base de datos `customers` | Supuesto, apoyado en hallazgos |
| Datos personales | Contactos de clientes en la base `customers` | Hecho (la base existe); el detalle de campos no se copia (R11) |
| Obligaciones | LFPDPPP, deber de seguridad (L1–L8) | Supuesto (empresa mexicana) |
| Tier actual | Gobierno: 1 · Gestión: 1 | Inferencia: no hay evidencia de política, inventario ni dueños |
| Tier objetivo (12 meses) | Gobierno: 2 · Gestión: 2 | Decisión propuesta (R9) |

## 2. Apetito (GV.RM-02, propuesto)

| Tema | Apetito | Tolerancia |
|---|---|---|
| Datos personales | Bajo | 0 cuentas por defecto, de prueba o compartidas en sistemas con datos personales |
| Exposición | Bajo | 0 servicios con acceso anónimo; 0 servicios sin dueño |
| Cumplimiento | Muy bajo | 0 requisitos L1–L8 sin plan de acción aprobado |

## 3. Inventario (extracto)

| ID | Activo | Datos personales | Criticidad | Dueño (supuesto) |
|---|---|---|---|---|
| A-01 | Base de datos MySQL `customers` | Sí | Alta | Gerente de Operaciones |
| A-02 | Servidor de correo (`mail1`, SMTP/IMAP/POP3) | Sí (correos) | Alta | Gerente de TI |
| A-03 | Recursos compartidos FTP / SMB / TFTP | Posible (notas internas, carpeta `Clients/`) | Media | Gerente de TI |
| A-04 | DNS interno (BIND) | No | Media | Gerente de TI |
| A-05 | Aplicación `app` | Sí | Alta | Gerente de Operaciones |

## 4. Registro de riesgos

Fuente: `reporte-enumeracion-lab.md`, número de hallazgo entre paréntesis.

| ID | Escenario | Fuente | P | I | Inherente | Nivel | Tratamiento |
|---|---|---|---|---|---|---|---|
| R-01 | Un atacante usa credenciales triviales de una cuenta de prueba, documentadas en notas internas y reutilizadas, para leer la base `customers`, exponiendo datos personales de clientes y obligando a notificar a los titulares. | #5, #1, #3 | 5 | 4 | 20 | Crítico | Mitigar |
| R-02 | Un atacante entra al buzón de correo con la misma credencial reutilizada y lo usa para phishing interno o para leer información de clientes. | #6 | 5 | 3 | 15 | Crítico | Mitigar |
| R-03 | Cualquier persona en la red lee notas internas y archivos de clientes mediante FTP anónimo, sesión nula de SMB y TFTP sin autenticación, obteniendo credenciales y datos internos. | #1, #3, #7 | 5 | 3 | 15 | Crítico | Mitigar |
| R-04 | Un atacante obtiene la zona DNS interna completa por transferencia de zona abierta y conoce hosts y rangos internos, acelerando ataques posteriores. | #2 | 5 | 2 | 10 | Alto | Mitigar |
| R-05 | Un atacante confirma usuarios válidos con SMTP VRFY y los usa para ataques de contraseña y phishing dirigido. | #4 | 4 | 2 | 8 | Medio | Mitigar |
| R-06 | Una vulneración no se detecta a tiempo porque no hay evidencia de logs de acceso ni de su revisión, y la empresa no puede decidir si debe notificar. | Supuesto (sin evidencia de logging) | 3 | 4 | 12 | Alto | Mitigar |

**Nota didáctica (R3):** el reporte técnico clasificó el AXFR (#2) como **Crítico** por severidad.
En el registro queda como riesgo **Alto**: la transferencia por sí sola no expone datos personales;
su impacto es facilitar otros ataques. En cambio, la cuenta de prueba en la base de clientes (#5)
es Crítica por severidad **y** por impacto al negocio.

### ALE de R-01 (cifras ficticias)

Desarrollado en `grc-05-riesgo.md`, sección 3: ALE antes ≈ **1,000,000 MXN/año**; ALE después ≈
**100,000 MXN/año**; costo del control ≈ 150,000 MXN/año; **valor del control ≈ 750,000 MXN/año**.

## 5. Perfil actual y objetivo (extracto)

| Subcategoría | Estado actual | Evidencia | Prioridad | Riesgos |
|---|---|---|---|---|
| GV.OC-03 | No | No hay lista de obligaciones legales | Alta | R-01 |
| GV.RM-02 | No | No hay apetito definido (se propuso uno) | Alta | todos |
| GV.RR-02 | No | Servicios sin dueño conocido | Alta | R-03, R-04 |
| GV.PO-01 | Sin evidencia | No se entregó política | Alta | todos |
| ID.AM-02 | Parcial | Solo el inventario producido por el footprinting | Alta | R-03 |
| ID.AM-07 | No | No hay inventario de datos personales | Alta | R-01 |
| ID.RA-01 | Parcial | Footprinting del curso; sin proceso periódico | Media | todos |
| PR.AA-01 | No | Cuenta de prueba con credencial trivial reutilizada (#5, #6) | Alta | R-01, R-02 |
| PR.AA-05 | No | Acceso anónimo a FTP, SMB y TFTP (#1, #3, #7) | Alta | R-03 |
| PR.PS-01 | No | AXFR abierto, VRFY habilitado, anónimos habilitados (#2, #4) | Alta | R-03, R-04, R-05 |
| PR.PS-04 | Sin evidencia | No se entregaron logs | Alta | R-06 |
| RS.CO-02 | Sin evidencia | No hay plan de notificación | Media | R-06 |

Los textos oficiales están en `core/csf-2.0-core.csv`; en el entregable real van en la columna
`texto_oficial`.

## 6. Matriz de cumplimiento (LFPDPPP, deber de seguridad)

| Req. | Diseño | Efectividad | Resultado | Motivo |
|---|---|---|---|---|
| L1 Medidas de seguridad | Sin evidencia | NOK | **No cumple** | Configuraciones inseguras demostradas (#1–#7) |
| L2 Inventario de datos | NOK | — | **No cumple** | No existe inventario de datos personales |
| L3 Análisis de riesgos | NOK | — | **No cumple** | No había análisis previo (este caso es el primero) |
| L4 Acceso solo autorizado | Sin evidencia | NOK | **No cumple** | Credencial trivial y accesos anónimos (#1, #3, #5, #6, #7) |
| L5 Capacitación | Sin evidencia | Sin evidencia | **No demostrado** | Credenciales en notas internas sugieren falta de capacitación (inferencia) |
| L6 Logs y monitoreo | Sin evidencia | Sin evidencia | **No demostrado** | R-06 |
| L7 Respaldos | Sin evidencia | Sin evidencia | **No demostrado** | No se entregó evidencia |
| L8 Notificación de vulneraciones | Sin evidencia | Sin evidencia | **No demostrado** | No hay plan de respuesta documentado |

Todos los requisitos llevan la marca *a validar con legal* (R10).

## 7. POA&M (extracto)

| ID | Acción | Responsable | Plazo | Riesgos | Residual esperado |
|---|---|---|---|---|---|
| P-01 | Eliminar la cuenta de prueba; cambiar contraseñas de cuentas con acceso a `customers` y correo; prohibir reutilización; MFA en accesos administrativos (CIS 4.7, 5.2, 6.5 `(verificar CIS v8.1)`) | Gerente de TI | 7 días | R-01, R-02 | R-01: 2×4 = 8 Medio · R-02: 2×3 = 6 Medio |
| P-02 | Deshabilitar FTP anónimo, sesión nula de SMB y TFTP; retirar notas con credenciales | Gerente de TI | 7 días | R-03 | 1×3 = 3 Bajo |
| P-03 | Restringir AXFR a secundarios autorizados con TSIG; deshabilitar VRFY/EXPN | Gerente de TI | 30 días | R-04, R-05 | R-04: 1×2 = 2 · R-05: 2×2 = 4 |
| P-04 | Restringir MySQL a la red de la aplicación | Gerente de TI | 30 días | R-01 | contribuye a R-01 |
| P-05 | Activar y retener logs de acceso a base de datos y correo; revisión semanal | Gerente de TI | 60 días | R-06 | 2×4 = 8 Medio |
| P-06 | Aprobar apetito, política de seguridad y RACI; nombrar dueños de servicios | Dirección | 60 días | todos | habilita Tier 2 de gobierno |
| P-07 | Inventario de datos personales y de sistemas | Operaciones + TI | 90 días | R-01 | cierra L2 |
| P-08 | Plan de respuesta con paso de notificación a titulares; simulacro | Seguridad + Legal | 120 días | R-06 | cierra L8 |
| P-09 | Capacitación de personal que trata datos personales | RR. HH. | 120 días | R-01, R-02 | cierra L5 |

## 8. Reporte ejecutivo (resumen)

> Inlanefreight tiene hoy prácticas de seguridad sin formalizar (Tier 1). Una prueba del laboratorio
> demostró que la base de datos de clientes se puede leer con una contraseña trivial publicada en
> notas internas, y que varios servicios permiten acceso anónimo. Esto expone datos personales y
> deja a la empresa sin poder demostrar el deber de seguridad de la LFPDPPP. Las acciones P-01 y P-02
> cuestan poco y bajan los tres riesgos críticos a niveles medios o bajos en una semana. Se solicita
> a la dirección aprobar el apetito de riesgo propuesto, nombrar dueños de los servicios y aprobar el
> plan de 120 días para alcanzar Tier 2.
