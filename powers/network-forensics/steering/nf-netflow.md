# Network Forensics: análisis de flujos (NetFlow y VPC Flow Logs)

> Guía de steering del power **network-forensics**, derivada de *NetFlow-Based Network Forensics* (HTB, sección 6). Detalle en `references/netflow.md`.
>
> **Encuadre:** flujos de redes propias o autorizadas.

## Para qué sirven los flujos

Los flujos no tienen contenido, pero cubren más tiempo y más red que un pcap. Responden **quién habló con quién, cuándo y cuánto**, y señalan el host que hay que examinar después.

## Flujo de análisis

```
1. Línea base     → tráfico normal por hora, protocolo, host y aplicación
2. Anomalías      → volumen, horario, protocolo/puerto, IP nueva, primer acceso
3. Acotar         → host, ventana de tiempo, destino
4. Impacto        → qué sistemas y datos se tocaron
5. Vector         → origen y método
6. Derivar        → pcap del periodo (si existe) y forense del endpoint
```

## Tipos de anomalía y qué hacer

| Anomalía | Ejemplo | Siguiente paso |
|---|---|---|
| Pico de volumen | Paquetes sobre el umbral a una hora | Filtra por protocolo para ver qué creció; identifica el host con más tráfico. |
| Horario | SMTP alto al final de la jornada | Origen y destino del SMTP; posible host enviando spam. |
| Puerto/protocolo | SSH sobre el 443 | Identificar el proceso en el endpoint. |
| Política | FTP prohibido en uso | Host y usuario; forense del endpoint. |
| Fuera de horario | Acceso a recursos sensibles de madrugada | Usuario, recurso y volumen. |
| Transferencia grande | Bytes hacia afuera muy por encima de lo normal | Destino, duración, protocolo; posible exfiltración. |
| IP nueva o primer acceso | Host que nunca había contactado un servidor | Relación con el incidente. |

## Consultas de ejemplo

Suricata (`eve.json`):

```bash
jq -r 'select(.event_type=="flow") | [.flow.start, .src_ip, .dest_ip, .dest_port, .app_proto, .flow.bytes_toserver] | @tsv' eve.json | sort -t$'\t' -k6 -nr | head
jq -r 'select(.event_type=="flow" and .dest_port==53) | .src_ip' eve.json | sort | uniq -c | sort -rn | head
```

AWS VPC Flow Logs en CloudWatch Logs Insights:

```
fields @timestamp, srcAddr, dstAddr, dstPort, bytes
| filter srcAddr = "10.0.1.25" and action = "ACCEPT"
| stats sum(bytes) as total by dstAddr, dstPort
| sort total desc
| limit 20
```

Rechazos (posible escaneo desde afuera):

```
fields srcAddr, dstPort
| filter action = "REJECT"
| stats count(*) as intentos by srcAddr
| sort intentos desc
| limit 20
```

## Preservación

Exporta los flujos del periodo del incidente a `evidencia/<caso>/flujos/` con su hash; la retención de la herramienta puede borrarlos.

## Preguntas de control

- ¿Contra qué línea base comparas cada anomalía?
- ¿Acotaste host, ventana y destino?
- ¿Exportaste y aseguraste los flujos del periodo?
- ¿Qué host pasa al endpoint y con qué datos?
