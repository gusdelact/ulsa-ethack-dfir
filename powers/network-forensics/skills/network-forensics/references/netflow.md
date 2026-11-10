# Forense basado en NetFlow (sección 6)

NetFlow es un protocolo de Cisco que recolecta estadísticas de tráfico de routers y switches. Registra todos los **flujos** de la red. Un flujo es la secuencia de paquetes entre una IP y puerto de origen y una IP y puerto de destino con un protocolo.

## Datos de un flujo

- IP de origen y de destino.
- Puerto de origen y de destino (solo TCP y UDP).
- Protocolo IP.
- Interfaz y versión de IP.
- Hora de inicio y fin, duración, bytes y paquetes transferidos, estado del flujo.

NetFlow **no guarda contenido**. Indica qué host investigar; el detalle viene del pcap o del endpoint.

## Qué permite detectar

- Aumentos anormales de volumen.
- Fugas de datos.
- Acceso a sistemas privados.
- IPs nuevas en la red.
- Sistemas accedidos por primera vez.

En el curso, el NetFlow lo produce **Suricata** y se ve en un dashboard. Puede analizarse con herramientas automáticas o manualmente.

## Usos

### Detección de anomalías y perfil de tráfico

NetFlow permite definir el tráfico **normal** de una red; lo que se desvía es sospechoso.

| Anomalía | Ejemplo del curso |
|---|---|
| Protocolo y puerto | Pico de paquetes sobre el umbral a las 19:00. Al filtrar DNS, el aumento es de DNS. El host con más consultas DNS (172.16.8.92) se pasa a examen detallado. |
| Horario | Tráfico alto al final de la jornada, dominado por SMTP. Un host infectado podría estar enviando spam. Se pasa a forense del endpoint. |

### Respuesta a incidentes

| Actividad | Objetivo |
|---|---|
| Análisis de flujos | Saber cuándo y dónde empezó el incidente. Ejemplo: SSH sobre el puerto 443 (técnica para evadir controles); hay que examinar el proceso en el endpoint. |
| Evaluación de impacto | Alcance de sistemas y datos afectados. |
| Vector de ataque | Origen y métodos usados. |

### Comportamiento

| Aspecto | Qué buscar |
|---|---|
| Uso de aplicaciones | Puertos y protocolos de cada aplicación; cuándo y con qué frecuencia se usan. |
| Tráfico inesperado | No coincide con el uso estándar: compartición de archivos fuera de horario, puertos no estándar, protocolos prohibidos (en el curso, FTP prohibido por política). |
| Anomalías dentro de la aplicación | Transferencias grandes en una aplicación que normalmente mueve poco. |
| Actividad de usuarios | Patrones por hora, día o semana; acceso a recursos; accesos a horas o desde lugares inesperados. |

### Amenazas internas

- Acceso a recursos fuera de horario o en días festivos.
- Transferencias grandes o que violan la política de datos.
- Patrones de acceso anómalos a sistemas con información sensible.

## NetFlow de Suricata en terminal

Suricata escribe los flujos en `eve.json` con `event_type` `flow` (o `netflow`, según la configuración).

```bash
# flujos con más bytes hacia el servidor (posible subida/exfiltración)
jq -r 'select(.event_type=="flow") | [.src_ip, .dest_ip, .dest_port, .proto, .flow.bytes_toserver, .flow.bytes_toclient] | @tsv' eve.json | sort -t$'\t' -k5 -nr | head

# hosts con más consultas DNS
jq -r 'select(.event_type=="flow" and .dest_port==53) | .src_ip' eve.json | sort | uniq -c | sort -rn | head

# protocolo de aplicación en puerto no estándar (p. ej. SSH en 443)
jq -r 'select(.event_type=="flow" and .app_proto=="ssh" and .dest_port!=22) | [.src_ip,.dest_ip,.dest_port] | @tsv' eve.json
```

## Equivalente en AWS: VPC Flow Logs

Registran por interfaz: cuenta, ENI, IP y puerto de origen y destino, protocolo, paquetes, bytes, inicio, fin y acción (ACCEPT/REJECT). Se consultan con CloudWatch Logs Insights o con Athena si se envían a S3.

```sql
-- Athena: destinos externos con más bytes desde una IP interna
SELECT dstaddr, dstport, SUM(bytes) AS total_bytes
FROM vpc_flow_logs
WHERE srcaddr = '10.0.1.25' AND action = 'ACCEPT'
GROUP BY dstaddr, dstport
ORDER BY total_bytes DESC
LIMIT 20;
```

Los nombres de columna dependen de cómo se creó la tabla en Athena; revísalos antes de consultar.
