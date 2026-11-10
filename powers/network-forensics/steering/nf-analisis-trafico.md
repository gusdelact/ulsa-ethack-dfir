# Network Forensics: análisis de tráfico por hipótesis

> Guía de steering del power **network-forensics**, derivada de *Network Traffic Analysis* (HTB, sección 4). Detalle en `references/analisis-trafico.md`.
>
> **Encuadre:** analiza copias de pcaps con su hash verificado.

## 1. Panorama primero

```bash
capinfos captura.pcap
tshark -r captura.pcap -qz io,phs
tshark -r captura.pcap -qz conv,ip
tshark -r captura.pcap -qz conv,tcp
tshark -r captura.pcap -qz endpoints,ip
```

En Wireshark: **Statistics → Protocol Hierarchy, Conversations, Endpoints, IO Graphs**.

Anota: protocolos inesperados, conversaciones asimétricas, hosts internos con muchos destinos externos, picos en el tiempo.

## 2. Recetario por hipótesis

| Hipótesis | Filtro de visualización | Qué confirma | ATT&CK |
|---|---|---|---|
| Escaneo de puertos | `tcp.flags.syn==1 && tcp.flags.ack==0` | Un origen, muchos puertos o destinos en poco tiempo | T1046 |
| C2 por HTTP | `http.request` y `http.host` | Peticiones periódicas, User-Agent raro, URIs codificadas | T1071.001 |
| C2 por DNS | `dns` · `dns.qry.name contains "..."` | Muchas consultas, subdominios largos o aleatorios | T1071.004 |
| Túnel por DNS | `dns.qry.name.len > 50` | Datos codificados en subdominios | T1572 |
| Protocolo en puerto no estándar | `tcp.port == 443 && !tls` | Contenido que no es TLS en el 443 (p. ej. SSH) | T1571 |
| Búsqueda de cadenas | `frame contains "curl"` | Herramientas o comandos en claro | — |
| Acceso remoto | `vnc` · `ssh` · `tcp.port == 5900` | Sesiones de escritorio remoto o SSH inesperadas | T1021 |
| Exfiltración | `ip.src == <interno> && tcp.len > 1000` | Volumen alto hacia el exterior | T1048 |
| Exfiltración por correo | `smtp` · `imap` | Adjuntos o volumen fuera de lo normal | T1048.003 |
| Dispositivo no autorizado | `(!(eth.src contains 98:CA:33) and arp) && !(eth.dst == ff:ff:ff:ff:ff:ff)` | MAC de un fabricante que no debería estar | — |
| ARP spoofing | `arp.duplicate-address-detected` · `arp.opcode == 2` | Una IP con dos MAC, respuestas ARP sin petición | T1557.002 |
| Errores TCP | `tcp.analysis.flags && !tcp.analysis.window_update` | Retransmisiones, resets masivos | — |

## 3. Profundizar

1. **Follow TCP/UDP Stream** sobre el flujo sospechoso: lee los datos y comandos enviados.
2. Si el contenido está codificado, decodifícalo (base64, hex) y documenta cómo.
3. **File → Export Objects** (HTTP, SMB, FTP-DATA, TFTP) o NetworkMiner para extraer archivos; calcula el hash de cada uno.
4. Si el flujo está cifrado, pasa a `nf-tls.md`.

## 4. Contadores útiles con tshark

```bash
# destinos más contactados por un host
tshark -r c.pcap -Y "ip.src==10.1.23.101" -T fields -e ip.dst | sort | uniq -c | sort -rn | head
# dominios consultados
tshark -r c.pcap -Y "dns.flags.response==0" -T fields -e dns.qry.name | sort | uniq -c | sort -rn | head
# puertos destino de un escaneo
tshark -r c.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e ip.src -e ip.dst -e tcp.dstport | sort -u
# contenido de un stream en ASCII
tshark -r c.pcap -qz follow,tcp,ascii,5
```

## 5. Registrar el hallazgo

Por cada hallazgo: filtro usado, número de paquetes o stream, IPs y puertos, hora UTC de inicio y fin, bytes, interpretación (marcada como inferencia) y técnica ATT&CK.

## Preguntas de control

- ¿Partiste del panorama antes de filtrar?
- ¿Cada hipótesis tiene una evidencia que la confirma o la descarta?
- ¿Los archivos extraídos tienen hash?
- ¿Comparaste contra el tráfico normal de la red?
