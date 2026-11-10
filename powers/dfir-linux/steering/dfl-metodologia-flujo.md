# DFIR en Linux: metodología y flujo

> Guía de steering del power **dfir-linux**. Aplica el proceso de seis fases de la presentación *Ethical Hacking & Digital Forensics* (La Salle 2026), documentado en `digitalforensic/proceso-digital-forensic.md`, a un host Linux con el material de los cursos de HTB.
>
> **Encuadre:** solo se analiza evidencia de sistemas propios o con autorización por escrito. Windows está fuera de alcance.

## Las seis fases

```
Detect → Isolate → Collect → Preserve → Analyze → Report
   ↑                                                 │
   └──────────── lecciones aprendidas, IOCs ─────────┘
```

| Fase | Objetivo en Linux | Guía |
|---|---|---|
| 1. Detect | Confirmar el incidente, abrir el caso, identificar host, usuarios y fuentes de evidencia. | Esta guía |
| 2. Isolate | Cortar la red del host sin apagarlo. | Esta guía |
| 3. Collect | Memoria → datos volátiles → imagen del disco → logs. | `dfl-live-response.md`, `dfl-imagen-hash.md` |
| 4. Preserve | Hash, cadena de custodia, almacenamiento de solo lectura. | `dfl-imagen-hash.md` |
| 5. Analyze | Logs, persistencia, sistema de archivos, memoria, línea de tiempo. | `dfl-logs.md`, `dfl-persistencia.md`, `dfl-memoria.md`, `dfl-autopsy.md` |
| 6. Report | Línea de tiempo, IOCs, MITRE ATT&CK, causa raíz, recomendaciones. | `dfl-reporte.md` |

Los cursos de HTB resumen el proceso en cuatro etapas (recolección, preservación, análisis y reporte). El modelo de seis fases separa la detección y el aislamiento.

## Fase 1 — Detect

1. Valida la alerta: ¿qué la disparó?, ¿es un falso positivo?
2. Abre el caso en `evidencia/<caso>/`:
   ```
   evidencia/<caso>/
   ├── bitacora.md        # cada acción con hora UTC
   ├── custodia.md        # registro de cadena de custodia
   ├── hashes.sha256      # hash de cada evidencia
   ├── volatil/           # salidas de live response
   ├── memoria/
   ├── disco/
   ├── logs/
   └── hallazgos.md
   ```
3. Escribe las **preguntas del caso** (quién, qué, cuándo, cómo, desde dónde). Guían la minimización: recolectas lo que las responde.
4. Inventaria las fuentes: logs locales, journal, auditd activo o no, logs remotos (SIEM, syslog central), en AWS CloudTrail y VPC Flow Logs.
5. Anota el estado inicial tal como lo encontraste.

## Fase 2 — Isolate

- **No apagues ni reinicies:** se pierde la RAM y los procesos del atacante.
- Desconecta de la red (cable, VLAN de cuarentena o reglas de firewall) manteniendo el acceso del analista.
- En AWS: security group de aislamiento sin reglas, reforzado con una Network ACL (las conexiones ya rastreadas pueden persistir con solo cambiar el security group); protección contra terminación; sacar la instancia del Auto Scaling Group y del balanceador; desactivar las credenciales comprometidas.
- Anota la hora exacta de cada acción de contención.

## Fase 3 — Collect: orden de volatilidad

1. Hora del sistema (`date -u`, `timedatectl`).
2. **Memoria RAM** (LiME o AVML) a un medio externo.
3. Datos volátiles: usuarios, procesos, archivos abiertos, red, historial.
4. **Imagen del disco** (`dd`/`dc3dd`) o snapshot EBS.
5. Logs (copia de `/var/log`, journal, `audit.log`).

Volcar la memoria primero es el estándar porque los comandos de live response también modifican la RAM. Si no hay herramienta de volcado disponible, recolecta los datos volátiles y documenta por qué no se volcó la memoria.

## Fase 4 — Preserve

- SHA-256 de cada archivo de evidencia al crearlo, anotado en `hashes.sha256`.
- Entrada en `custodia.md` por cada evidencia y cada traspaso.
- Copias de trabajo para el análisis; el original no se toca.

## Fase 5 — Analyze

Empieza por las preguntas del caso y elige la fuente con la tabla "Dónde mirar según la pregunta" del `SKILL.md`. Un hallazgo lleva al siguiente: una IP en un script lleva a `auth.log`, un usuario lleva a su historial y su `authorized_keys`, una hora lleva a `find -newermt`.

## Fase 6 — Report

Línea de tiempo en UTC, hallazgos con su evidencia, técnicas de MITRE ATT&CK, IOCs, causa raíz y recomendaciones. Ver `dfl-reporte.md`.

## Ciclo de razonamiento por hallazgo

| Paso | Pregunta |
|---|---|
| Observar | ¿Qué dice exactamente la evidencia? (archivo, línea, campo) |
| Orientar | ¿Qué significa? ¿Con qué otra evidencia se relaciona? |
| Decidir | ¿Qué comando, lo menos invasivo posible, confirma o descarta la hipótesis? |
| Actuar | Ejecútalo, guarda la salida, anótalo en la bitácora y vuelve a observar. |

## Preguntas de control antes de cerrar el caso

- ¿Cada evidencia tiene hash y entrada en la cadena de custodia?
- ¿Trabajaste siempre sobre copias o montajes de solo lectura?
- ¿Todos los timestamps están en UTC o con su zona horaria indicada?
- ¿Cada hallazgo del reporte cita su evidencia?
- ¿Respondiste las preguntas del caso o dejaste anotado por qué no?
