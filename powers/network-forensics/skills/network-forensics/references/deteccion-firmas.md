# Detección por firmas (sección 5)

La detección por firmas identifica amenazas conocidas (malware, virus, troyanos) por sus firmas, IPs, URLs o hashes predefinidos. Es rápida para lo conocido, pero **no detecta ataques 0-day**.

## Qué detecta

| Categoría | Ejemplos |
|---|---|
| Ataques de red | Escaneos de puertos, inyección SQL, XSS, detectados por peticiones y patrones. |
| Malware | Comunicación, infecciones y actualizaciones. |
| Ransomware | Patrones de cifrado y de comunicación. |
| Phishing | Estructuras de URL o contenido de correo. |
| Exploits | Explotación directa no cubierta por otras categorías. |

## Herramientas (más adecuadas en sistemas *nix)

| Herramienta | Características |
|---|---|
| **Snort** | NIDS de código abierto con lenguaje de reglas flexible y reglas de la comunidad. |
| **Suricata** | NIDS multihilo; combina firmas y anomalías; eficaz en redes rápidas. |
| **Zeek** | Monitoreo con firmas y anomalías; orientado a threat hunting y forense. |

## Snort

### Instalación y prueba (Ubuntu 22.04)

```bash
apt install snort
snort -V                 # versión
curl testmyids.com       # genera tráfico que debe disparar una alerta de prueba
```

### Analizar un pcap

```bash
snort -r <archivo_pcap> -c <archivo_config>
snort -r /tmp/2024-01-23-infection-traffic.pcap -c /etc/snort/snort.conf
tail -f /var/log/snort/alert.fast        # o snort.alert.fast, según la configuración de salida
```

Para el caso, conviene separar las salidas y dejar el pcap sin modificar:

```bash
mkdir -p /mnt/evidencia/caso01/snort
snort -q -r captura.pcap -c /etc/snort/snort.conf -l /mnt/evidencia/caso01/snort -A fast -k none
```

`-l` fija el directorio de logs, `-A fast` produce alertas de una línea y `-k none` evita descartar paquetes por checksums incorrectos (frecuente en capturas con offloading de la tarjeta de red).

### Leer una alerta

```
12/10-05:32:16.929144 [**] [1:2014726:123] ET POLICY Outdated Flash Version M1 [**]
[Classification: Potential Corporate Privacy Violation] [Priority: 1] {TCP} 172.16.2.139:49186 -> 23.218.156.83:80
```

| Parte | Significado |
|---|---|
| `12/10-05:32:16.929144` | Fecha (mes/día) y hora con microsegundos. Snort no imprime el año. |
| `[1:2014726:123]` | Generator ID : **SID** (ID de la firma) : revisión. |
| `ET POLICY Outdated Flash Version M1` | Descripción; `ET` = Emerging Threats, categoría `POLICY`. |
| `Classification` | Clase de la alerta (p. ej. *Potential Corporate Privacy Violation*, *Detection of a Network Scan*, *access to a potentially vulnerable web application*). |
| `Priority: 1` | Prioridad; 1 es la más alta. |
| `{TCP} 172.16.2.139:49186 -> 23.218.156.83:80` | Protocolo, origen y destino con puertos. |

### Ejemplos de alertas del curso

| Alerta | Interpretación |
|---|---|
| `ATTACK-RESPONSES 403 Forbidden` | El servidor negó un recurso: posibles intentos de acceso no autorizado. |
| `ET CURRENT_EVENTS ... JNLP ... Base64` | Archivos JNLP codificados en base64: método usado para ejecutar applets Java maliciosos. |
| `ET CURRENT_EVENTS Terse alphanumeric executable downloader` | Probable descargador de malware. |
| `ET POLICY Java EXE Download` | Descarga de un EXE en un entorno Java. |
| `ET POLICY Outdated Flash Version` | Versión vieja de Flash con vulnerabilidades. |
| `ET POLICY PE EXE or DLL Windows file download HTTP` | Descarga de ejecutable de Windows por HTTP. |
| `ET POLICY Vulnerable Java Version 1.6.x` | Java 1.6 con vulnerabilidades conocidas. |
| `ET WEB_CLIENT SUSPICIOUS Java Request ...` | Peticiones Java sospechosas asociadas a exploits. |

## Triage de alertas

```bash
# alertas agrupadas por firma
grep -oP '\] \K[^\[]+(?= \[\*\*\])' alert | sort | uniq -c | sort -rn
# alertas de una clase
grep "Detection of a Network Scan" alert
# origen y destino de una firma concreta
grep "SCAN UPnP" alert | grep -oP '\{\w+\} \S+ -> \S+'
```

Ordena por prioridad, agrupa por firma, y verifica cada alerta en el pcap con Wireshark (filtra por las IPs y puertos de la alerta) antes de reportarla como hallazgo: una alerta es una hipótesis, no una confirmación.
