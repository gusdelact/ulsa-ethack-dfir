# Network Forensics: tráfico TLS/SSL

> Guía de steering del power **network-forensics**, derivada de *TLS/SSL Analysis Techniques* (HTB, sección 7). Detalle en `references/tls-ssl.md`.
>
> **Encuadre:** solo se descifra tráfico propio o autorizado. Las claves de sesión y lo que revelan (credenciales, datos) son evidencia sensible.

## Flujo

```
1. Sin descifrar  → versiones, cipher suites, SNI, certificados, alertas, patrones de tiempo y volumen
2. ¿Hay claves?   → archivo SSLKEYLOGFILE del cliente o (solo en pruebas) llave privada del servidor
3. Descifrar      → Wireshark: Preferences → Protocols → TLS → (Pre)-Master-Secret log filename
4. Analizar       → el tráfico descifrado se analiza como en nf-analisis-trafico.md
5. Registrar      → hash del archivo de claves; enmascarar credenciales en el reporte
```

## 1. Sin descifrar

```bash
tshark -r c.pcap -Y "tls.handshake.type==1" -T fields -e ip.src -e ip.dst -e tls.handshake.extensions_server_name | sort | uniq -c | sort -rn
tshark -r c.pcap -Y "tls.handshake.type==2" -T fields -e ip.src -e tls.handshake.version -e tls.handshake.ciphersuite | sort | uniq -c
tshark -r c.pcap -Y "tls.alert_message" -T fields -e frame.time -e ip.src -e ip.dst
```

| Señal | Interpretación |
|---|---|
| SSLv3, TLS 1.0 o 1.1 | Sistema obsoleto o mal configurado; posible vulnerabilidad. |
| Cipher suite débil | Configuración insegura. |
| SNI desconocido o aleatorio | Posible infraestructura de C2. |
| Conexiones a intervalos regulares | Beaconing. |
| Aumento de volumen cifrado hacia afuera | Posible exfiltración. |
| Handshakes fallidos frecuentes | Interrupción o actividad maliciosa. |

## 2–3. Descifrar

Con el archivo de claves:

```bash
sha256sum ssl.log >> /mnt/evidencia/caso01/hashes.sha256
tshark -r c.pcap -o tls.keylog_file:ssl.log -qz io,phs        # nuevos protocolos visibles tras descifrar
tshark -r c.pcap -o tls.keylog_file:ssl.log -Y "http.request" -T fields -e http.host -e http.request.uri
tshark -r c.pcap -o tls.keylog_file:ssl.log -Y "ftp" -T fields -e frame.time_relative -e ftp.request.command -e ftp.request.arg -e ftp.response.arg
```

Para generar claves en una prueba propia: `export SSLKEYLOGFILE=~/sslkeylog.log` y abre el navegador o cliente desde esa terminal antes de generar el tráfico.

## Límites

- Sin claves, el contenido de TLS 1.3 y de cifrados con forward secrecy no se puede descifrar, ni siquiera con la llave privada del servidor.
- DNS normal viaja en claro, aunque el resto esté cifrado: úsalo para saber qué dominios se resolvieron.

## Preguntas de control

- ¿El uso de las claves estaba autorizado?
- ¿El archivo de claves tiene hash y acceso restringido?
- ¿Enmascaraste credenciales en el reporte?
- ¿Qué concluiste sin descifrar y qué solo después de descifrar?
