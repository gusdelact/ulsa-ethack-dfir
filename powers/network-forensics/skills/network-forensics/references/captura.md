# Captura de tráfico (sección 3)

Capturar es copiar los paquetes que pasan por la red: contenido, encabezados, direcciones, protocolo y timestamps. Es la base de todo el análisis posterior.

## Dónde capturar

- **Un solo host:** se ejecuta Wireshark o tcpdump en ese host.
- **Toda una red:** el tráfico se envía al equipo de captura mediante un **puerto SPAN** (port mirroring) del switch.
- **AWS:** VPC Traffic Mirroring copia el tráfico de una interfaz (ENI) a un destino de análisis.

## Dos cuestiones a cuidar

| Cuestión | Por qué importa |
|---|---|
| **Filtrado** | Reglas adecuadas eliminan tráfico irrelevante, ahorran espacio y simplifican el análisis. |
| **Timestamps** | La hora de cada paquete permite analizar los eventos en orden cronológico. |

## Filtros de captura frente a filtros de visualización

La sintaxis es distinta; no los confundas.

| | Filtro de captura | Filtro de visualización |
|---|---|---|
| Cuándo actúa | Al capturar: lo que no coincide no se guarda | Al mostrar: el pcap completo sigue ahí |
| Sintaxis | **BPF** (Berkeley Packet Filter), más simple | Sintaxis propia de Wireshark, más rica |
| Dónde | tcpdump y Wireshark (Capture Options) | Wireshark y `tshark -Y` |

### Ejemplos de filtros de captura (BPF)

| Objetivo | Filtro |
|---|---|
| Por IP | `host 192.168.1.1` |
| Por puerto | `port 80` |
| Por protocolo | `tcp` |
| Combinado | `src host 192.168.1.1 and dst port 80` |

### Ejemplos de filtros de visualización (Wireshark)

| Objetivo | Filtro |
|---|---|
| IP de origen | `ip.src == 192.168.1.1` |
| IP de destino | `ip.dst == 192.168.1.1` |
| Cualquier sentido | `ip.addr == 192.168.1.1` |
| Puertos TCP/UDP | `tcp.port == 80 \|\| udp.port == 53` |
| Protocolo | `dns` |
| MAC de origen | `eth.src == 00:11:22:33:44:55` |
| Protocolo y puerto | `tcp.port == 443 && http` |
| Host HTTP | `http.host == "www.example.com"` |
| Inicio de conexión (SYN sin ACK) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| Un flujo TCP | `tcp.stream eq 5` |
| Errores o anomalías TCP | `tcp.analysis.flags && !tcp.analysis.window_update` |
| Combinado | `ip.src == 192.168.1.1 && tcp.dstport == 80` |

## Wireshark

```bash
sudo apt install wireshark
```

1. Abre Wireshark, elige la interfaz y, si aplica, escribe el filtro de captura.
2. Inicia la captura; los paquetes aparecen en pantalla.
3. Detén con el botón rojo (**Stop**) y guarda con **Save this Capture File** (`.pcapng`).
4. Para capturas largas, en **Capture → Options** divide la salida en varios archivos por número de paquetes, tamaño o tiempo. Así los archivos son manejables para analizar y transportar.

## tcpdump

```bash
apt install tcpdump      # Debian
yum install tcpdump      # RHEL
sudo tcpdump             # requiere root
```

| Parámetro | Uso |
|---|---|
| `-i <interfaz>` | Interfaz de captura (`-i any` para todas). |
| `-w <archivo>` | Guarda en pcap para abrirlo después en Wireshark. |
| `-r <archivo>` | Lee un pcap. |
| `-n` | No resuelve nombres (más rápido y no genera tráfico DNS). |
| `-C <MB>` / `-W <n>` | Rota archivos por tamaño y conserva `n`. |
| `-G <seg>` | Rota por tiempo (usa formato de fecha en el nombre). |

```bash
sudo tcpdump -i ens33 -w testpcap.pcap            # detener con Ctrl+C
tcpdump -i eth0 src 192.168.1.1                   # IP de origen
tcpdump -i eth0 dst 192.168.1.1                   # IP de destino
tcpdump -i eth0 port 80                           # puerto
tcpdump -i eth0 src 192.168.1.1 and dst 10.0.0.1  # entre dos IPs
tcpdump -i eth0 'tcp'                             # protocolo
tcpdump -i eth0 net 192.168.1.0/24                # red
tcpdump -i eth0 ether host 00:1A:2B:3C:4D:5E      # MAC
tcpdump -i eth0 'tcp[tcpflags] & (tcp-syn) != 0'  # paquetes con SYN
tcpdump -i eth0 udp port 53                       # DNS
sudo tcpdump -i eth0 -n -C 100 -W 20 -w /mnt/evidencia/caso01/cap.pcap   # rotación: 20 archivos de 100 MB
```

## Al cerrar una captura

```bash
sha256sum /mnt/evidencia/caso01/*.pcap* > /mnt/evidencia/caso01/pcap.sha256
capinfos /mnt/evidencia/caso01/cap.pcap      # inicio, fin, paquetes, tamaño
```

Anota en la bitácora: interfaz, filtro de captura, hora de inicio y fin (UTC), host de captura y hash.
