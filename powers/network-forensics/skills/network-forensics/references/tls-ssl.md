# Análisis de TLS/SSL (sección 7)

TLS/SSL cifra las comunicaciones. Analizar este tráfico permite examinar flujos cifrados e identificar amenazas que viajan ocultas.

## Protocolos y cipher suites

| Qué revisar | Por qué |
|---|---|
| **Cipher suite** | Algoritmos débiles o inseguros indican sistemas mal configurados o software obsoleto. |
| **Versión** | SSLv2, SSLv3 y las primeras versiones de TLS tienen vulnerabilidades conocidas. |

En Wireshark, el filtro `tls` muestra solo TLS y la versión aparece en el detalle del paquete. Lo mismo vale para otros protocolos cifrados: en tráfico SSH, el detalle del paquete muestra el método de cifrado negociado.

Filtros útiles:

| Objetivo | Filtro |
|---|---|
| Todo TLS | `tls` |
| ClientHello | `tls.handshake.type == 1` |
| ServerHello | `tls.handshake.type == 2` |
| Nombre del servidor (SNI) | `tls.handshake.extensions_server_name` |
| Versión del handshake | `tls.handshake.version` |
| Alertas TLS (errores) | `tls.alert_message` |
| SSL/TLS antiguo | `tls.record.version < 0x0303` (menor que TLS 1.2) |

El **SNI** viaja en claro en el ClientHello y revela el dominio aunque el contenido esté cifrado.

## Descifrar tráfico

Para descifrar se necesitan las claves de la sesión TLS. Hay dos formas:

### 1. Variable `SSLKEYLOGFILE`

Los navegadores modernos (Chrome, Firefox) y muchas herramientas escriben las claves de sesión en el archivo que indica esta variable. Wireshark lo usa para descifrar.

```bash
export SSLKEYLOGFILE=~/sslkeylog.log     # Linux y macOS
# luego iniciar el navegador o el cliente desde esa terminal
```

Solo sirve para sesiones generadas **después** de definir la variable, en el equipo cliente.

### 2. Llave privada del servidor

Si tienes acceso y privilegios, puedes usar la llave privada del servidor. No se recomienda por seguridad y solo funciona con intercambio de claves RSA (no con cifrados con forward secrecy, que son la norma en TLS 1.2 moderno y obligatorios en TLS 1.3). Úsala solo en entornos de prueba.

### Configurar Wireshark

1. **Edit → Preferences**.
2. **Protocols → TLS**.
3. En **(Pre)-Master-Secret log filename**, indica la ruta del archivo de `SSLKEYLOGFILE`.
4. Recarga la captura: el tráfico descifrado aparece como HTTP, FTP, etc.

Equivalente en terminal:

```bash
tshark -r ftp.pcapng -o tls.keylog_file:ssl.log -Y "ftp"
tshark -r ftp.pcapng -o tls.keylog_file:ssl.log -Y "ftp.request.command == \"USER\" || ftp.request.command == \"PASS\""
tshark -r ftp.pcapng -o tls.keylog_file:ssl.log -Y "ftp.response" -T fields -e frame.time_relative -e ftp.response.arg
tshark -r ftp.pcapng -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort -u
```

El archivo de claves es evidencia sensible: permite leer todo el tráfico de esas sesiones. Guárdalo con hash y acceso restringido.

## Anomalías en tráfico cifrado

Sin descifrar, todavía se puede detectar:

| Señal | Posible causa |
|---|---|
| Patrones de cifrado inesperados | Exfiltración o C2. |
| Volumen de tráfico cifrado inusual, sobre todo aumentos | Actividad sospechosa. |
| Handshakes fallidos o inesperados frecuentes | Interrupción o actividad maliciosa. |
| Conexiones periódicas a intervalos regulares (beaconing) | Implante comunicándose con su C2. |
| SNI con dominios recién registrados o aleatorios | Infraestructura de atacante. |
