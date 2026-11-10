# Integración con los demás powers del curso

El power GRC **no repite** el trabajo técnico. Pide la ruta del reporte de otro power, lo lee y lo
convierte en filas del inventario, del registro de riesgos, del perfil y de la matriz de
cumplimiento.

## 1. Qué aporta cada power

| Power | Salida que se consume | Destino en GRC | Subcategorías CSF |
|---|---|---|---|
| `osint-passive-recon` | Exposición pública, subdominios, correos, fugas, terceros | Inventario (activos expuestos, proveedores), escenarios de riesgo | ID.AM-02, ID.AM-04, ID.RA-02, ID.RA-03, GV.SC-04 |
| `footprinting-enumeration` | Servicios, versiones, configuraciones inseguras | Inventario, escenarios, evidencia de efectividad (en contra) | ID.AM-02, ID.RA-01, PR.PS-01, PR.AA-01, PR.IR-01 |
| `vulnerability-assessment` | Hallazgos con CVSS, validación de falsos positivos | Probabilidad e impacto por activo (R3), evidencia para L3 | ID.RA-01, ID.RA-04, ID.RA-05, PR.PS-02 |
| `exploitation-metasploit` | Explotación demostrada | Probabilidad 5 en el escenario; mejora | ID.RA-04, ID.IM-02 |
| `incident-handling-nist` | Reporte final, lecciones aprendidas, timeline | Riesgos materializados, actualización de políticas, evidencia para L8 | RS.MA-01, RS.CO-02, ID.IM-04, GV.PO-02 |
| `dfir-linux`, `network-forensics` | Causa raíz, evidencia, controles detectivos que faltaron | Brechas de detección y registro | RS.AN-03, PR.PS-04, DE.CM-01, DE.CM-09 |

## 2. Procedimiento de conversión

Para cada hallazgo del reporte técnico:

1. **¿Qué activo?** Si no está en `03-inventario-activos.csv`, agregarlo (y preguntar el dueño).
2. **¿Es un riesgo nuevo o agrava uno existente?** Agrupar hallazgos que llevan al mismo impacto en
   un solo escenario (p. ej., FTP anónimo + SMB nulo exponen notas internas → un escenario de fuga
   de información interna).
3. **Probabilidad:** usar exposición, explotación demostrada, EPSS/KEV; no solo CVSS (R3).
4. **Impacto:** según el activo y los datos que contiene, con la escala de `02-escalas.md`.
5. **Subcategorías CSF** que el hallazgo demuestra que **no** se cumplen → estado *No* o *Parcial*
   en el perfil.
6. **Requisito de cumplimiento** afectado (L1–L8) → efectividad *NOK* en la matriz.
7. **Fuente** en la columna `fuente` del registro: power, archivo y número de hallazgo.

## 3. Tabla de traducción rápida

| Hallazgo técnico típico | Escenario de riesgo | Subcategorías CSF | Req. |
|---|---|---|---|
| Credenciales débiles o reutilizadas | Acceso no autorizado a datos | PR.AA-01, PR.AA-03 | L4 |
| Login anónimo (FTP, SMB, TFTP) | Fuga de información interna | PR.AA-05, PR.PS-01 | L1, L4 |
| Transferencia de zona DNS abierta | Reconocimiento acelerado de la red interna | PR.PS-01, PR.IR-01 | L1 |
| Enumeración de usuarios (SMTP VRFY) | Ataques de contraseña y phishing dirigidos | PR.PS-01 | L1 |
| Servicio de base de datos accesible desde fuera de la red de aplicación | Acceso directo a datos | PR.IR-01, ID.AM-03 | L1, L4 |
| Software sin soporte o sin parches | Explotación de vulnerabilidades conocidas | PR.PS-02, ID.RA-01 | L1, L3 |
| Sin logs de acceso o sin revisión | Vulneración no detectada | PR.PS-04, DE.CM-09 | L6 |
| Sin respaldos probados | Pérdida de datos tras ransomware | PR.DS-11, RC.RP-03 | L7 |
| Incidente sin decisión documentada de notificar | Incumplimiento de notificación | RS.CO-02 | L8 |

## 4. Reglas al consumir reportes

- No copiar credenciales, flags ni datos personales a los entregables (R11).
- Citar la fuente exacta (archivo y número de hallazgo) para mantener la trazabilidad (R2, R7).
- Si el reporte técnico no dice algo (p. ej., el valor del activo), preguntarlo; no inventarlo.
