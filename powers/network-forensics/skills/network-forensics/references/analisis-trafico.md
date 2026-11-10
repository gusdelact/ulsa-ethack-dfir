# Análisis de tráfico (sección 4)

El **análisis de tráfico de red** (NTA) recolecta, examina y analiza los datos que fluyen por la red para detectar brechas, ataques y comportamiento anómalo. No tiene un estándar establecido: hay que entender **por qué** se analiza y dirigir el análisis en consecuencia.

## Qué se puede detectar

| Actividad | Señal en el tráfico |
|---|---|
| Acceso no autorizado | Intentos exitosos y fallidos contra recursos de la red. |
| Propagación de malware | Comunicación por puertos específicos, intentos de exfiltración. |
| Amenazas internas | Exfiltración u otra actividad maliciosa desde dentro. |
| DoS/DDoS | Volumen de tráfico anormal hacia un recurso. |
| ARP spoofing | Anomalías en el protocolo ARP y aumento de su frecuencia. |

## Aspectos del análisis

| Aspecto | Descripción |
|---|---|
| Filtrado | Excluir lo irrelevante para acelerar el análisis. |
| Análisis de protocolos | Examen detallado de TCP, UDP, HTTP, DNS, etc. |
| Análisis de sesiones | Inicio, fin, duración y volumen de cada sesión. |
| Análisis de comportamiento | Definir el patrón normal y tratar las desviaciones como anomalías (tráfico alto de noche, protocolos inusuales). |
| Revisión post-incidente | Origen del incidente, sistemas afectados e impacto. |

## Panorama: Statistics de Wireshark

### Protocol Hierarchy

Muestra qué porcentaje de paquetes usa cada protocolo. Ejemplo de lectura del curso:

| Protocolo | Lectura |
|---|---|
| Ethernet + IPv4 | Tráfico de una LAN estándar. |
| UDP (pocos paquetes) | Probablemente DNS. |
| DNS | Puede revelar resolución de dominios de C2. |
| TCP (mayoría) | La mayor parte del tráfico es orientado a conexión. |
| VNC (pocos paquetes) | Escritorio remoto: posible acceso no autorizado. Revisar. |
| TLS | Tráfico cifrado: puede ocultar malware o transferencia de datos sensibles. Revisar. |
| HTTP (poco) | Poca web en claro. |
| Data | Contenido no asociado a ningún protocolo conocido: revisar. |

### Conversations

| Columna | Qué indica |
|---|---|
| Address A / Address B | Las dos partes de la comunicación (interna frente a externa). |
| Packets / Bytes | Volumen. Asimetría fuerte (mucho en un sentido) indica descarga o posible fuga. |
| Rel Start / Duration | Inicio y duración. Larga y voluminosa: flujo normal o transferencia/sesión maliciosa. |
| Bits/s A→B, B→A | Tasa por sentido. A→B alta hacia el exterior: posible subida o exfiltración. |

Un host interno que habla con muchos servicios externos puede indicar C2, descarga de malware u otra actividad inusual.

Equivalente en terminal:

```bash
tshark -r captura.pcap -qz io,phs         # jerarquía de protocolos
tshark -r captura.pcap -qz conv,tcp       # conversaciones TCP
tshark -r captura.pcap -qz conv,ip
tshark -r captura.pcap -qz endpoints,ip
capinfos captura.pcap                     # número de paquetes, duración
```

## Escenario: malware y C2

1. Revisa Protocol Hierarchy y Conversations.
2. Filtra por IPs, puertos o protocolos asociados a malware:
   ```
   ip.addr == 140.223.29.110 or (tcp.dstport == 5500 and vnc)
   ```
3. Busca comunicación con C2 por IRC, HTTP u otros protocolos, y firmas conocidas (características del payload, puertos, IPs).
4. Busca cadenas en el contenido (no funciona si el tráfico está cifrado):
   ```
   frame contains "curl"
   ```
5. Revisa DNS; el malware suele resolver dominios de C2:
   ```
   dns
   dns and dns.qry.name == "testmyids.com"
   ```
6. **Follow TCP Stream / UDP Stream** (Analyze → Follow) para leer el flujo completo y los comandos enviados.

## Escenario: amenaza interna

1. Protocol Hierarchy: protocolos que violan la política (en el ejemplo del curso, mucho DCE/RPC y Microsoft Network Logon que hay que justificar).
2. Tráfico en puertos no estándar o con protocolos inesperados.
3. Actividad fuera de horario o en días festivos.
4. SMTP, IMAP u otros protocolos de mensajería usados para sacar datos.
5. Conexiones inesperadas de direcciones internas a externas, sobre todo de alto ancho de banda.
6. Consultas DNS sospechosas o repetidas de usuarios internos.
7. Dispositivos no registrados. Ejemplo: si la red solo tiene equipos Apple (prefijo MAC `98:CA:33`), lista los que no lo son, excluyendo broadcast:
   ```
   (!(eth.src contains 98:CA:33) and arp) && !(eth.dst == ff:ff:ff:ff:ff:ff)
   ```

## Escenario: transferencia anómala de datos

1. Statistics → Protocol Hierarchy para el panorama.
2. Filtra transferencias grandes:
   ```
   ip.src == 192.168.0.1 && tcp.len > 1000
   ```
3. Protocolos viejos o inseguros poco usados en la red.
4. Statistics → Conversations y Endpoints para ver quién envía o recibe volúmenes anormales.
5. Compara con el patrón normal: picos, horas inusuales, puertos inesperados.
6. Statistics → **IO Graphs** para ver tendencias en el tiempo.

## Escenario: escaneo de puertos

```
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

```bash
tshark -r portscan.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e ip.src | sort | uniq -c | sort -rn
tshark -r portscan.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e ip.dst | sort | uniq -c
tshark -r portscan.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e tcp.dstport | sort -u | wc -l
```

Un origen que envía SYN a muchos puertos de un destino en poco tiempo es un escaneo (MITRE T1046).

## Extraer datos transmitidos

- **Follow TCP Stream** con "Show data as: ASCII" o "Raw" para el texto enviado por un puerto.
- Si el contenido está codificado (base64, hex), decodifícalo y documenta el método.
- **File → Export Objects** (HTTP, SMB, FTP-DATA, TFTP) para extraer archivos; NetworkMiner hace lo mismo de forma automática. Calcula el hash de cada archivo extraído.
