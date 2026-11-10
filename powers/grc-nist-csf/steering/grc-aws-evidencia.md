# Evidencia en AWS (solo lectura)

Guía de referencia para cuando el alcance incluye cuentas de AWS. El power **no modifica recursos**
(R12): consulta evidencia con credenciales de solo lectura y registra las correcciones en el POA&M.

## 1. Modelo de responsabilidad compartida

| Lo opera AWS ("seguridad *de* la nube") | Lo opera el cliente ("seguridad *en* la nube") |
|---|---|
| Centros de datos, hardware, red física, hipervisor, servicios administrados por dentro | Identidades e IAM, configuración de servicios, datos y su cifrado, red (VPC, security groups), sistemas operativos en EC2, logging y monitoreo |

Consecuencia para GRC: los reportes de AWS (SOC, ISO, PCI en **AWS Artifact**) cubren la parte de
AWS; la parte del cliente se evalúa con su propia evidencia.

## 2. Servicios como fuente de evidencia

| Servicio | Qué evidencia da | Subcategorías CSF típicas |
|---|---|---|
| **AWS Organizations + SCPs** | Guardrails preventivos aplicados a todas las cuentas | GV.PO-01, PR.AA-05 |
| **AWS Config + conformance packs** | Estado de configuración contra reglas, historial de cambios (existe un paquete de buenas prácticas para NIST CSF) | PR.PS-01, ID.AM-02, ID.RA-07 |
| **AWS Security Hub** | Puntaje contra estándares: AWS FSBP, CIS AWS Foundations, NIST SP 800-53 Rev. 5, PCI DSS | ID.RA-01, PR.PS-01 |
| **AWS Audit Manager** | Recolección automática de evidencia por marco (verificar qué versión de NIST CSF está disponible) | GV.OV-03, ID.IM-01 |
| **AWS CloudTrail** | Registro de actividad de API (quién, qué, cuándo, desde dónde) | PR.PS-04, DE.CM-03, RS.AN-06 |
| **Amazon GuardDuty** | Hallazgos de detección de amenazas | DE.CM-01, DE.AE-02 |
| **IAM Access Analyzer** | Accesos externos y permisos no usados | PR.AA-05 |
| **AWS Backup** | Planes de respaldo y pruebas de restauración | PR.DS-11, RC.RP-03 |

## 3. Comandos de solo lectura (ejemplos)

```bash
aws sts get-caller-identity                                         # confirmar identidad y rol (debe ser de solo lectura)
aws configservice describe-compliance-by-config-rule --output table
aws securityhub get-enabled-standards
aws cloudtrail describe-trails
aws guardduty list-detectors
aws accessanalyzer list-analyzers
```

Antes de ejecutar, el agente confirma con el usuario la cuenta, la región y que las credenciales
son de solo lectura. Si el rol tiene permisos de administración, lo advierte y pide confirmación.

## 4. Cómo registrar la evidencia

Por cada evidencia: comando o consola usada, cuenta y región, fecha y hora UTC, quién la obtuvo,
archivo de salida guardado en `insumos/aws/`. Sin identificadores sensibles innecesarios (R11).
