# Network Forensics: reporte

> Guía de steering del power **network-forensics**. Cierra el proceso (fase Report). El curso pide un reporte completo e imparcial, porque puede usarse en un proceso legal.

## 1. Línea de tiempo de red (UTC)

| Hora (UTC) | Fuente | Evidencia | Evento | ATT&CK |
|---|---|---|---|---|
| 10:00:05 | pcap | paquetes 1–2.400 | 203.0.113.5 envía SYN a 1.000 puertos de 10.0.0.5 | T1046 |
| 10:07:40 | pcap | stream 17 | Sesión SSH exitosa desde 203.0.113.5 | T1021.004 |
| 10:20:11 | Snort | SID 2014726 | Descarga de ejecutable por HTTP a 10.0.0.5 | T1105 |
| 10:25:00–10:40:00 | NetFlow | flujos 8812–8830 | 10.0.0.5 envía 450 MB a 198.51.100.7:443 | T1048 |

## 2. IOCs de red

Lista exportable: IPs, dominios (y SNI), URLs, User-Agents, puertos no estándar, SIDs de Snort disparados, JA3 si lo calculaste, hashes de archivos extraídos.

## 3. Técnicas frecuentes en red (MITRE ATT&CK)

| Técnica | ID |
|---|---|
| Network Service Discovery (escaneo) | T1046 |
| Application Layer Protocol: Web / DNS | T1071.001 / T1071.004 |
| Non-Standard Port | T1571 |
| Protocol Tunneling | T1572 |
| Ingress Tool Transfer | T1105 |
| Exfiltration Over Alternative Protocol | T1048 |
| Remote Services (SSH, VNC) | T1021.004 / T1021.005 |
| ARP Cache Poisoning | T1557.002 |
| Brute Force | T1110 |

## 4. Estructura del reporte

1. **Resumen ejecutivo** en lenguaje no técnico.
2. **Alcance y preguntas del caso.**
3. **Metodología:** puntos de captura, filtros, herramientas y versiones (Wireshark, tcpdump, Snort y sus reglas, Suricata).
4. **Inventario de evidencia:** pcaps, flujos, alertas, claves TLS; con SHA-256 y cadena de custodia.
5. **Línea de tiempo.**
6. **Hallazgos:** cada uno con filtro, paquetes o streams, y su interpretación marcada como inferencia cuando corresponda.
7. **IOCs y técnicas ATT&CK.**
8. **Hosts derivados a forense del endpoint**, con IP, MAC, ventana de tiempo y motivo.
9. **Recomendaciones:** bloqueos, segmentación, monitoreo (flow logs con retención adecuada, IDS con reglas actualizadas), cifrado y políticas de protocolos.
10. **Limitaciones:** tráfico no capturado, cifrado sin claves, retención de flujos.
11. **Anexos:** salidas de tshark, alertas de Snort, capturas de pantalla, bitácora.

## Preguntas de control

- ¿Cada hallazgo es reproducible con el filtro y el pcap indicados?
- ¿Las credenciales encontradas están enmascaradas?
- ¿Quedó claro qué host sigue en forense del endpoint?
- ¿Las limitaciones están declaradas?
