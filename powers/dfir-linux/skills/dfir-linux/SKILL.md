---
name: dfir-linux
description: Conocimiento de los cursos Digital Forensics on Linux y su continuación de HTB Academy (14 secciones) para investigar un incidente en un host Linux autorizado. Cubre live response y datos volátiles, sistemas de archivos, imagen forense con dd/dc3dd y hashes, montaje de solo lectura, recuperación de borrados, archivos de configuración y de sistema, persistencia, análisis de logs (syslog, auth.log/secure, audit.log, boot.log, dmesg, faillog, wtmp/btmp), adquisición con comandos, Autopsy y memoria con LiME y Volatility 3, más el equivalente en AWS con snapshots EBS. Sigue el proceso Detect, Isolate, Collect, Preserve, Analyze, Report. Use when el usuario pida responder a un incidente en Linux, recolectar datos volátiles, crear, verificar o montar una imagen, revisar auth.log, audit.log o wtmp, buscar persistencia, recuperar archivos borrados, analizar un volcado de memoria de Linux o construir la línea de tiempo de un incidente en un laboratorio autorizado.
---

# DFIR en Linux

Este skill entrega el conocimiento de los cursos **Digital Forensics on Linux** (secciones 1–7) y su **continuación** (secciones 1–7) de HTB Academy. Sirve para investigar un incidente en un host Linux: recolectar la evidencia sin alterarla, analizarla y reportar lo que pasó.

> **Regla de encuadre (crítica):** solo se analiza evidencia de sistemas propios o con autorización por escrito (por ejemplo, las máquinas del laboratorio de HTB). Este material es didáctico y no concede autorización por sí mismo. Windows está **fuera de alcance**: si la investigación llega a un host Windows, indícalo y no lo analices.

## Principios que no se negocian

1. **Integridad:** nunca trabajes sobre el original. Calcula el SHA-256 al adquirir y verifícalo antes de cada análisis. Analiza copias o montajes de solo lectura.
2. **Orden de volatilidad:** primero lo que desaparece antes (memoria, procesos, conexiones), después el disco y al final los logs remotos.
3. **No escribir en el sistema sospechoso:** la salida de cada comando va a un medio externo o a la carpeta de evidencia del caso, nunca al disco que investigas.
4. **Bitácora:** cada acción se anota con hora UTC, comando, herramienta y resultado. Otro analista debe poder repetirla (Reproducibility).
5. **Objetividad:** separa **hechos** (la línea X de `auth.log` dice Y) de **inferencias** (el atacante entró por SSH). Registra también lo que contradice tu hipótesis.
6. **Minimización:** recolecta lo necesario para responder las preguntas del caso.

> **Regla de persistencia de evidencia (obligatoria):** la evidencia se guarda en el workspace del proyecto, en `evidencia/<caso>/`. No la dejes solo en `/tmp` o `/var/tmp`: se borra. Si una herramienta escribe primero en `/tmp`, copia el resultado a `evidencia/<caso>/` y calcula su hash.

## Proceso (detalle en steering `dfl-metodologia-flujo.md`)

```
1. Detect   → confirmar el incidente, abrir el caso, identificar host y fuentes de evidencia
2. Isolate  → aislar de la red sin apagar (apagar borra la RAM)
3. Collect  → memoria (LiME/AVML) → datos volátiles (ps, lsof, ss) → imagen del disco (dd/dc3dd)
4. Preserve → SHA-256 de cada evidencia, cadena de custodia, almacenamiento de solo lectura
5. Analyze  → logs, persistencia, sistema de archivos, memoria, línea de tiempo
6. Report   → línea de tiempo, IOCs, técnicas MITRE ATT&CK, causa raíz, recomendaciones
```

El proceso viene de la presentación *Ethical Hacking & Digital Forensics* (La Salle 2026) y está documentado en `digitalforensic/proceso-digital-forensic.md`.

## Cómo está organizado el conocimiento (references/)

Carga solo el archivo que necesites (divulgación progresiva).

| Reference | Secciones HTB | Contenido |
|---|---|---|
| `references/live-response.md` | Linux 1–3 | Datos volátiles: procesos, hora, usuarios, archivos abiertos, red, historial, RAM. |
| `references/sistemas-archivos.md` | Linux 4–5 | EXT2/3/4, XFS, Btrfs; `dd`, `dc3dd`, hashes, montaje de solo lectura, recuperación de borrados. |
| `references/archivos-configuracion.md` | Linux 6 | `/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/sudoers`, `/etc/crontab`. |
| `references/archivos-sistema.md` | Linux 7 | `authorized_keys`, `.bashrc`, systemd, `/tmp` y `/var/tmp`. |
| `references/logs.md` | Continuación 2–4 | `syslog`/`messages`, `auth.log`/`secure`, `audit.log`, `boot.log`, `dmesg`, `faillog`, `wtmp`/`btmp`. |
| `references/comandos-adquisicion.md` | Continuación 5–6 | `uname`, `tcpdump`, `ngrep`, `strings`, `stat`, `find`, `grep`. |
| `references/autopsy-linux.md` | Continuación 7 | Caso, fuente de datos, verificación de hash, menús de análisis, reporte. |
| `references/labs.md` | Todas | Escenario, credenciales y método de cada laboratorio, sin respuestas. |

## Guías de steering

| Steering | Cuándo cargarla |
|---|---|
| `dfl-metodologia-flujo.md` | Al iniciar un caso o cuando no sepas en qué fase estás. |
| `dfl-live-response.md` | El host sigue encendido y hay que recolectar datos volátiles. |
| `dfl-imagen-hash.md` | Crear, verificar o montar una imagen; recuperar borrados; snapshots EBS. |
| `dfl-persistencia.md` | Buscar cómo se mantiene el atacante en el sistema. |
| `dfl-logs.md` | Responder preguntas de acceso, privilegios o borrado de rastros con los logs. |
| `dfl-memoria.md` | Analizar un volcado de RAM de Linux con Volatility 3. |
| `dfl-autopsy.md` | Revisar una imagen con Autopsy. |
| `dfl-reporte.md` | Construir la línea de tiempo, mapear a MITRE ATT&CK y redactar el reporte. |

## Dónde mirar según la pregunta

| Pregunta del caso | Primera fuente | Reference |
|---|---|---|
| ¿Quién entró y desde dónde? | `auth.log`/`secure`, `wtmp` (`last`), `who`/`w` | `logs.md`, `live-response.md` |
| ¿Hubo fuerza bruta? | `Failed password` en `auth.log`, `btmp` (`lastb`), `faillog` | `logs.md` |
| ¿Qué comandos se ejecutaron? | `~/.bash_history`, `audit.log` (EXECVE, USER_CMD), `linux.bash` en memoria | `logs.md`, `live-response.md` |
| ¿Quién escaló privilegios? | `sudo` en `auth.log`, `audit.log` (auid frente a euid), `/etc/sudoers`, SUID/SGID | `logs.md`, `archivos-configuracion.md` |
| ¿Cómo persiste? | `crontab`, servicios systemd, `authorized_keys`, `.bashrc` | `archivos-configuracion.md`, `archivos-sistema.md` |
| ¿Qué proceso tiene un puerto o un archivo? | `ss -tulpn`, `lsof -i`, `lsof <archivo>` | `live-response.md` |
| ¿Qué cambió y cuándo? | `stat`, `find -mtime`, línea de tiempo con `fls`/`mactime` | `comandos-adquisicion.md`, `sistemas-archivos.md` |
| ¿Se borraron logs o archivos? | Huecos en logs, historial (`rm`, `> /var/log/...`), recuperación con TSK | `logs.md`, `sistemas-archivos.md` |
| ¿Hay herramientas del atacante? | `/tmp`, `/var/tmp`, `/dev/shm`, archivos web (`/var/www/html`) | `archivos-sistema.md` |

## Equivalente en AWS

En una instancia EC2 no hay acceso físico al disco. La imagen forense se reemplaza por un **snapshot EBS**: se crea un volumen a partir del snapshot, se adjunta a una instancia forense aislada y se monta en solo lectura. El volcado de memoria se hace dentro de la instancia con LiME o AVML antes de detenerla. Detalle en `dfl-imagen-hash.md`.

## Preguntas didácticas (úsalas en cada hallazgo)

- ¿Qué **observaste** y qué solo **inferiste**?
- ¿Qué **evidencia** (archivo, línea, hash) sostiene el hallazgo?
- ¿La acción que tomaste modificó la evidencia? ¿Lo dejaste anotado?
- ¿En qué zona horaria están los timestamps? ¿Los convertiste a UTC?
- ¿Qué técnica de MITRE ATT&CK corresponde al hallazgo?
- ¿Otro analista llegaría al mismo resultado con tu bitácora?

## Relación con otros powers

- `network-forensics`: analiza capturas de tráfico (pcap) y NetFlow. Cuando el análisis de red identifica un host Linux sospechoso, el caso pasa a este power. Si aquí encuentras una captura o un IOC de red, carga `network-forensics`.
- `footprinting-enumeration`, `vulnerability-assessment`, `exploitation-metasploit`: muestran el lado del atacante. Este power investiga los rastros que dejan esas fases.

## Referencias

- HTB Academy: *Digital Forensics on Linux* (PDFs en `digitalforensic/htb_dfir_linux/`) y su continuación (`digitalforensic/htb_dfir_linux_advanced/`). Falta la sección 8 de ambos cursos.
- Metodología de memoria: adaptada de *Memory Forensics* (HTB, `digitalforensic/htb/`), basada en SANS.
- Proceso general: `digitalforensic/proceso-digital-forensic.md`.
