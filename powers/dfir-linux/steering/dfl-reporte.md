# DFIR en Linux: línea de tiempo y reporte

> Guía de steering del power **dfir-linux**. Cierra el proceso (fase Report) según `digitalforensic/proceso-digital-forensic.md`. El reporte debe ser completo e imparcial porque puede usarse en un proceso legal.

## 1. Línea de tiempo unificada

Une todas las fuentes en una tabla en **UTC**, ordenada por hora.

| Hora (UTC) | Fuente | Evidencia | Evento | Técnica ATT&CK |
|---|---|---|---|---|
| 2026-11-05 10:02:11 | `auth.log` | línea 1234 | 300 `Failed password` para `root` desde 203.0.113.5 | T1110.001 |
| 2026-11-05 10:07:40 | `auth.log` | línea 1540 | `Accepted password for admin from 203.0.113.5` | T1078 |
| 2026-11-05 10:09:02 | `audit.log` | evento 1650 | `admin` ejecuta `sudo` (euid=0) | T1548.003 |
| 2026-11-05 10:11:30 | `stat` / `mactime` | `/etc/crontab` | Línea `@reboot` agregada | T1053.003 |
| 2026-11-05 10:15:05 | `.bash_history` | `admin` | `> /var/log/syslog` | T1070.002 |

Herramientas: `mactime` (TSK) para el sistema de archivos; `ausearch -i` para auditd; los logs con su hora convertida. Para unir muchas fuentes, Plaso (`log2timeline.py` y `psort.py`) genera una línea de tiempo combinada.

## 2. Técnicas frecuentes en Linux (MITRE ATT&CK)

| Técnica | ID | Evidencia típica |
|---|---|---|
| Brute Force | T1110 | `Failed password` masivos, `btmp` |
| Valid Accounts | T1078 | `Accepted` desde IP desconocida |
| Create Local Account | T1136.001 | `useradd` en `auth.log`, entrada nueva en `/etc/passwd` |
| SSH Authorized Keys | T1098.004 | Llave nueva en `authorized_keys`, `Accepted publickey` |
| Cron | T1053.003 | `@reboot` o línea nueva en cron |
| Systemd Service | T1543.002 | Unidad nueva en `/etc/systemd/system/` |
| Unix Shell Configuration Modification | T1546.004 | `curl`/`wget` en `.bashrc` |
| Setuid and Setgid | T1548.001 | Binario SUID nuevo |
| Sudo and Sudo Caching | T1548.003 | `NOPASSWD`, `sudo` en `auth.log` |
| Web Shell | T1505.003 | `.php` en `/var/www`, creado por el proceso web |
| Clear Linux or Mac System Logs | T1070.002 | Logs vacíos, huecos, comandos de borrado |
| Clear Command History | T1070.003 | `.bash_history` vacío, `history -c` |
| Timestomp | T1070.006 | `Modify` antiguo con `Change` reciente |

## 3. IOCs

Lista separada y exportable: IPs, dominios, usuarios, rutas, nombres de archivo, hashes SHA-256 de binarios y scripts, llaves SSH (huella con `ssh-keygen -lf`).

## 4. Estructura del reporte

1. **Resumen ejecutivo:** qué pasó, impacto y estado actual, en lenguaje no técnico.
2. **Alcance y preguntas del caso.**
3. **Metodología:** fases, herramientas y versiones.
4. **Inventario de evidencia:** ID, descripción, SHA-256, cadena de custodia.
5. **Línea de tiempo** (sección 1).
6. **Hallazgos:** uno por sección, con la evidencia que lo sostiene (archivo, línea, comando y salida), distinguiendo hechos de inferencias.
7. **Técnicas ATT&CK e IOCs.**
8. **Causa raíz:** cómo entró el atacante y qué control falló.
9. **Recomendaciones:** contención pendiente, erradicación (cuentas, llaves, cron, servicios, binarios) y prevención (MFA o solo llaves en SSH, `fail2ban`, auditd con reglas, logs centralizados con retención).
10. **Limitaciones:** evidencia faltante, logs rotados o borrados, memoria no adquirida.
11. **Anexos:** salidas de herramientas, reporte de Autopsy, bitácora.

## Preguntas de control

- ¿Cada hallazgo cita su evidencia y su hash?
- ¿La línea de tiempo está completa en UTC y sin contradicciones?
- ¿Las inferencias están marcadas como tales?
- ¿Las recomendaciones atacan la causa raíz y no solo los síntomas?
- ¿Un lector no técnico entiende el resumen ejecutivo?
