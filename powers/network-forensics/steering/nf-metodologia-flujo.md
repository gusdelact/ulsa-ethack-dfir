# Network Forensics: metodología y flujo

> Guía de steering del power **network-forensics**. Aplica el proceso de seis fases de la presentación *Ethical Hacking & Digital Forensics* (La Salle 2026), documentado en `digitalforensic/proceso-digital-forensic.md`, al tráfico de red con el material del curso de HTB.
>
> **Encuadre:** solo redes propias o con autorización por escrito. Windows está fuera de alcance como endpoint a investigar.

## Las seis fases en red

| Fase | En red | Guía |
|---|---|---|
| 1. Detect | Alerta de IDS, pico en NetFlow, aviso del SIEM. Definir preguntas y segmento. | Esta guía |
| 2. Isolate | Contener el host o segmento manteniendo un punto de captura. | Esta guía |
| 3. Collect | pcap (tcpdump/Wireshark, SPAN), NetFlow, alertas de IDS; en AWS Traffic Mirroring y VPC Flow Logs. | `nf-captura.md` |
| 4. Preserve | SHA-256 del pcap y de cada exporte, cadena de custodia. | `nf-captura.md` |
| 5. Analyze | Panorama → hipótesis → filtros → flujos → firmas → TLS. | `nf-analisis-trafico.md`, `nf-netflow.md`, `nf-snort.md`, `nf-tls.md` |
| 6. Report | Línea de tiempo, IOCs de red, ATT&CK, derivación al endpoint. | `nf-reporte.md` |

El curso describe el proceso en cuatro principios: recolección, investigación, análisis y reporte.

## Fase 1 — Detect

1. ¿Qué disparó la alerta? (firma de IDS, umbral de NetFlow, reporte de usuario).
2. Abre el caso en `evidencia/<caso>/` con `bitacora.md`, `custodia.md`, `pcap/`, `flujos/`, `ids/` y `hallazgos.md`.
3. Escribe las preguntas: ¿qué host?, ¿con quién se comunicó?, ¿cuándo empezó?, ¿qué datos salieron?, ¿por qué protocolo?
4. Identifica qué evidencia de red existe y su retención: ¿hay pcap continuo o solo flujos? ¿cuánto tiempo guardan los flow logs?

## Fase 2 — Isolate

- Aislar el host no debe cortar la visibilidad: mantén el SPAN o el Traffic Mirroring si necesitas observar al atacante.
- Bloquea IPs o dominios de C2 en el firewall o DNS solo cuando el caso lo decida; bloquear avisa al atacante.
- Anota la hora de cada acción.

## Fase 5 — Orden de análisis

```
1. Integridad    → sha256sum del pcap; capinfos (inicio, fin, paquetes)
2. Panorama      → Protocol Hierarchy, Conversations, Endpoints, IO Graphs
3. Hipótesis     → ¿C2? ¿exfiltración? ¿escaneo? ¿intruso interno? ¿spoofing?
4. Filtros       → display filters para cada hipótesis (nf-analisis-trafico.md)
5. Flujos        → Follow TCP/UDP Stream; Export Objects
6. Firmas        → Snort sobre el pcap para contrastar (nf-snort.md)
7. Cifrado       → SNI, versiones, descifrado con claves si las hay (nf-tls.md)
8. Correlación   → con NetFlow, logs DNS y del endpoint
```

## Ciclo de razonamiento por hallazgo

| Paso | Pregunta |
|---|---|
| Observar | ¿Qué paquetes o flujos exactos lo muestran? (número de paquete, stream, flujo) |
| Orientar | ¿Es normal en esta red? ¿Contra qué línea base lo comparas? |
| Decidir | ¿Qué filtro o herramienta confirma o descarta la hipótesis? |
| Actuar | Aplícalo, guarda el resultado y vuelve a observar. |

## Cuándo pasar al endpoint

El análisis de red identifica **qué** host y **cuándo**; el **por qué** está en el host. Deriva a `dfir-linux` cuando:
- Un host interno se comunica con un C2 o una IP maliciosa.
- Hay exfiltración desde un host.
- Un protocolo aparece en un puerto que no le corresponde (SSH en 443): hay que identificar el proceso.
- Un host envía tráfico prohibido por política (FTP, spam por SMTP).

Entrega: IP, MAC, rango de tiempo en UTC, IPs y puertos remotos, y el pcap con su hash.

## Preguntas de control antes de cerrar

- ¿Cada pcap y exporte tiene hash y entrada en la cadena de custodia?
- ¿Documentaste el filtro de captura y lo que pudo quedar fuera?
- ¿Cada hallazgo cita paquetes, streams o flujos concretos?
- ¿Definiste los hosts que pasan a forense del endpoint?
