# `powers/digital-forensics/` — Powers de Digital Forensics (alumnos)

Powers **nuevos o extendidos** del equipo Digital Forensics (4 alumnos), en layout de dos niveles `powers/digital-forensics/<power>/`, que cubren el Flujo_Investigacion **Detect → Isolate → Collect → Preserve → Analyze → Report**.

**Cimiento existente** (vive en `powers/<nombre>/`, un nivel; **no recrear**):

- `dfir-linux` — forense de **host** Linux (live response, dd/dc3dd, logs, persistencia, Autopsy).
- `network-forensics` — forense de **red** (Wireshark, tcpdump, Snort, Suricata/NetFlow, TLS).

**Deriva red→host:** `network-forensics` deriva a `dfir-linux` cuando el análisis de tráfico identifica el host sospechoso; la investigación continúa sobre ese host.

Alcance limitado a **Linux y nube (AWS)**; si el host sospechoso es **Windows**, se marca **fuera de alcance** (Req 5.7). Análisis siempre sobre **copia verificada por hash** (`hash_pre == hash_post`); recolección en Orden_Volatilidad (RFC 3227); Cadena_Custodia encadenada por `sha256`.

Regla transversal: ≥2 Powers con Herramienta_Real por alumno (Req 5.2, 9.6).

_Referencias: Req 5.1–5.10, 16.1–16.8, 9.4, 13.1, 5.8._
