---
name: network-forensics
description: Conocimiento del curso Introduction to Network Forensics de HTB Academy (7 secciones) para investigar incidentes a partir del tráfico de red en un entorno autorizado. Cubre principios y herramientas (Wireshark, tcpdump, Snort, NetworkMiner), captura con filtros BPF y filtros de visualización, análisis de tráfico (jerarquía de protocolos, conversaciones, C2, exfiltración, amenazas internas, escaneos, ARP spoofing), NetFlow con Suricata, detección por firmas con Snort y análisis de TLS/SSL con SSLKEYLOGFILE, más los equivalentes en AWS (VPC Flow Logs, Traffic Mirroring). Sigue el proceso Detect, Isolate, Collect, Preserve, Analyze, Report. Use when el usuario pida capturar tráfico, analizar un pcap, escribir filtros de Wireshark o tcpdump, buscar C2, exfiltración o escaneos en el tráfico, revisar NetFlow o flow logs, correr Snort sobre una captura o descifrar y analizar tráfico TLS en un laboratorio autorizado.
---

# Network Forensics

Este skill entrega el conocimiento del curso **Introduction to Network Forensics** de HTB Academy (secciones 1–7). El forense de red detecta, monitorea y analiza incidentes a partir del tráfico y de los registros de red: origen de ataques, DoS/DDoS, amenazas internas y otras actividades maliciosas.

> **Regla de encuadre (crítica):** solo se captura o analiza tráfico de redes propias o con autorización por escrito (por ejemplo, las capturas del laboratorio de HTB). Capturar tráfico de terceros puede violar la ley y la privacidad. Este material es didáctico y no concede autorización por sí mismo. Si el análisis apunta a un host Windows, indica que está fuera de alcance.

## Principios del curso

| Principio | Qué significa |
|---|---|
| **Recolección** | Monitoreo continuo del tráfico para tener datos que analizar después (sniffers, servidores de logs, herramientas de monitoreo). |
| **Investigación** | Determinar tipo de incidente, hora, sistemas afectados y daño potencial. |
| **Análisis** | Examen detallado con herramientas y técnicas de análisis de red. |
| **Reporte** | Reporte completo e imparcial, porque puede usarse en un proceso legal. |

Reglas adicionales del power:
1. **Integridad:** calcula el SHA-256 de cada pcap al cerrar la captura y antes de analizarlo. Analiza copias.
2. **Timestamps:** cada paquete trae su hora; anota la zona horaria y trabaja en UTC.
3. **Filtrado:** filtra para reducir ruido y almacenamiento, pero documenta el filtro usado; lo que no capturaste no se puede analizar después.
4. **Hechos frente a inferencias:** "10.1.23.101 envió 6 MB a 162.125.8.15" es un hecho; "hubo exfiltración" es una inferencia que requiere más evidencia.

> **Regla de persistencia de evidencia (obligatoria):** pcaps, salidas de Snort, exportes de NetFlow y notas se guardan en `evidencia/<caso>/` dentro del workspace, con su hash. Nunca solo en `/tmp`.

## Proceso (detalle en steering `nf-metodologia-flujo.md`)

```
1. Detect   → alerta (IDS, NetFlow, SIEM), preguntas del caso, qué segmento de red
2. Isolate  → contener el host o el segmento sin perder la capacidad de capturar
3. Collect  → pcap (tcpdump/Wireshark, SPAN), NetFlow, logs de IDS; en AWS Traffic Mirroring y VPC Flow Logs
4. Preserve → SHA-256 del pcap, cadena de custodia
5. Analyze  → panorama (jerarquía, conversaciones) → hipótesis → filtros → flujos → firmas → TLS
6. Report   → línea de tiempo, IOCs de red, técnicas ATT&CK; derivar el host a forense del endpoint
```

## Cómo está organizado el conocimiento (references/)

| Reference | Sección HTB | Contenido |
|---|---|---|
| `references/fundamentos-herramientas.md` | 1–2 | Qué es, principios, Wireshark, tcpdump, Snort, NetworkMiner, SIEM, detección de anomalías. |
| `references/captura.md` | 3 | Captura en vivo, SPAN, filtros BPF frente a filtros de visualización, rotación de pcap. |
| `references/analisis-trafico.md` | 4 | Protocol Hierarchy, Conversations, malware y C2, amenazas internas, transferencias anómalas. |
| `references/deteccion-firmas.md` | 5 | Detección por firmas, Snort/Suricata/Zeek, análisis de pcap con Snort, lectura de alertas. |
| `references/netflow.md` | 6 | Flujos, perfil de tráfico, anomalías, respuesta a incidentes, comportamiento, amenazas internas. |
| `references/tls-ssl.md` | 7 | Versiones y cipher suites, descifrado con SSLKEYLOGFILE, anomalías en tráfico cifrado. |
| `references/labs.md` | 3–7 | Escenario, credenciales y método de cada laboratorio, sin respuestas. |

## Guías de steering

| Steering | Cuándo cargarla |
|---|---|
| `nf-metodologia-flujo.md` | Al iniciar un caso de red. |
| `nf-captura.md` | Hay que capturar tráfico. |
| `nf-analisis-trafico.md` | Hay un pcap y una hipótesis (C2, exfiltración, escaneo, intruso interno). |
| `nf-netflow.md` | Hay datos de flujo (NetFlow, Suricata, VPC Flow Logs). |
| `nf-snort.md` | Correr firmas sobre un pcap e interpretar alertas. |
| `nf-tls.md` | El tráfico relevante está cifrado. |
| `nf-reporte.md` | Redactar el reporte y derivar al forense del endpoint. |

## Qué herramienta según la pregunta

| Pregunta | Herramienta | Steering |
|---|---|---|
| ¿Qué protocolos y quién habla con quién? | Wireshark Statistics, `tshark -z io,phs`, `-z conv,tcp` | `nf-analisis-trafico.md` |
| ¿Qué datos se enviaron en una conexión? | Follow TCP/UDP Stream | `nf-analisis-trafico.md` |
| ¿Hay un escaneo de puertos? | Filtro de SYN sin ACK, conteo de puertos destino | `nf-analisis-trafico.md` |
| ¿Hay tráfico conocido como malicioso? | Snort sobre el pcap | `nf-snort.md` |
| ¿Cuándo empezó y qué volumen tuvo? | NetFlow / flow logs, IO Graphs | `nf-netflow.md` |
| ¿Qué hay dentro de HTTPS/FTPS? | Wireshark con SSLKEYLOGFILE | `nf-tls.md` |
| ¿Qué archivos o credenciales viajaron? | NetworkMiner, Export Objects de Wireshark | `nf-analisis-trafico.md` |

## Equivalentes en AWS

| Concepto del curso | En AWS |
|---|---|
| SPAN / port mirroring | **VPC Traffic Mirroring** (copia los paquetes de una ENI a un destino de análisis). |
| NetFlow | **VPC Flow Logs** (metadatos de flujo: IPs, puertos, protocolo, bytes, paquetes, ACCEPT/REJECT; no incluyen contenido). |
| Logs DNS | Route 53 Resolver query logs. |
| IDS por firmas | AWS Network Firewall (reglas compatibles con Suricata), GuardDuty para detecciones administradas. |

## Preguntas didácticas

- ¿Qué **observaste** en el tráfico y qué **inferiste**?
- ¿Con qué filtro se capturó el pcap? ¿Qué pudo quedar fuera?
- ¿El hash del pcap coincide con el registrado?
- ¿Cuál es el tráfico **normal** de esta red? ¿Contra qué comparas la anomalía?
- ¿Qué host debe pasar a forense del endpoint y con qué evidencia?

## Relación con otros powers

- `dfir-linux`: cuando el análisis de red identifica un host Linux sospechoso, el caso continúa allí (procesos, persistencia, logs). El curso lo indica explícitamente al hablar de NetFlow.
- `footprinting-enumeration`: los escaneos de nmap que estudia son los que este power detecta en el tráfico.

## Referencias

- HTB Academy: *Introduction to Network Forensics* (PDFs en `digitalforensic/htb_dfir_networking/`). Falta la sección 8.
- Proceso general: `digitalforensic/proceso-digital-forensic.md`.
