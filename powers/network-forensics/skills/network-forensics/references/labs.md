# Laboratorios: enfoque metodológico

Esta guía da el escenario, el acceso y el **método** de cada laboratorio. **No** da respuestas. Falta la sección 8 del curso (probablemente el Skills Assessment) en los PDFs disponibles.

## Acceso

- Credenciales del laboratorio: `root` / `123456` (VNC, puerto 5903).
- Las capturas están en la máquina del laboratorio.

## Reglas para todos los laboratorios

1. Antes de abrir un pcap, calcula su SHA-256 y anótalo en `evidencia/<lab>/bitacora.md`.
2. Trabaja sobre una copia del pcap.
3. Responde cada pregunta con la evidencia: filtro usado, número de paquete o de flujo y valor observado.

## Capturing Network Traffic (sección 3)

Pregunta sobre qué filtro de protocolo se usó para capturar `protocol.pcapng`.

Método: Statistics → Protocol Hierarchy (o `tshark -qz io,phs`). Si la captura se filtró por protocolo, todos los paquetes pertenecen a él. Revisa también Capture File Properties, que a veces registra el filtro de captura.

## Network Traffic Analysis (sección 4)

Preguntas sobre `data-transfer.pcapng` (texto enviado por un puerto y texto "cifrado" enviado por otro) y sobre `portscan.pcap` (número de paquetes, IP que escanea, IP escaneada y cuántos puertos distintos).

Método:
1. Filtra `tcp.port == <puerto>` y usa **Follow TCP Stream**. Si el contenido está codificado, identifica la codificación (base64, hex, ROT) y documenta cómo la decodificaste.
2. `capinfos` para el número de paquetes.
3. Filtro de SYN sin ACK; agrupa por `ip.src`, `ip.dst` y cuenta los `tcp.dstport` distintos (ver `references/analisis-trafico.md`).

## Signature-based Detection (sección 5)

Preguntas sobre `infection-traffic-1.pcap` analizado con Snort (`/etc/snort/snort.conf`): nombre de la alerta de una clase dada, origen y protocolo de una alerta de escaneo UPnP, y destino de una alerta web.

Método:
1. `snort -q -r infection-traffic-1.pcap -c /etc/snort/snort.conf -l <dir> -A fast -k none`.
2. Busca en el archivo de alertas por clase (`Classification`) o por nombre de firma.
3. Lee origen, destino, puerto y protocolo de la línea de la alerta.
4. Confirma en Wireshark con las IPs y puertos de la alerta.

## NetFlow-Based Network Forensics (sección 6)

Pregunta sobre en qué intervalo de 15 minutos hubo un número inusual de peticiones según una gráfica del curso.

Método: compara cada intervalo con la línea de promedio (umbral) y elige el que la supera. Es un ejercicio de lectura de la gráfica.

## TLS/SSL Analysis Techniques (sección 7)

Preguntas sobre `ftp.pcapng` (FTP sobre TLS): usuario y contraseña de acceso a un servidor FTP, momento del mensaje de login exitoso y dominio consultado por DNS. Las claves están en `ssl.log`, en el escritorio.

Método:
1. Configura `ssl.log` en Preferences → Protocols → TLS → (Pre)-Master-Secret log filename (o `tshark -o tls.keylog_file:ssl.log`).
2. Filtra `ftp` y busca los comandos `USER` y `PASS`.
3. Para el tiempo, usa la columna de tiempo relativo (`frame.time_relative`) del paquete con la respuesta de login.
4. El DNS no está cifrado: filtra `dns` y lee la consulta.
5. Trata las credenciales obtenidas como dato sensible en tu reporte (enmascáralas si el reporte se comparte).
