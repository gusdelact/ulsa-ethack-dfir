# Live response en Linux (Linux, secciones 1–3)

**Live response** es la recolección de información forense en un host Linux encendido después de un incidente. Se enfoca en los **datos volátiles**: los que se pierden al cortar la energía (RAM, registros de CPU, conexiones de red, procesos). Reflejan el estado del sistema en el momento del incidente, por eso se revisan en cuanto se detecta.

## Hora del sistema

La hora y la zona horaria son la base de la línea de tiempo. Anótalas antes que nada y compáralas con una fuente confiable para medir el desfase del reloj.

```bash
date                 # hora del sistema
date -u              # hora en UTC
timedatectl          # zona horaria y estado de sincronización NTP
```

## Usuarios conectados

| Comando | Qué muestra |
|---|---|
| `who` | Usuarios conectados, terminal (TTY) y hora de inicio de sesión. |
| `w` | Lo mismo, más el comando que ejecuta cada usuario y el tiempo inactivo. |
| `last` | Historial de inicios y cierres de sesión y reinicios (lee `/var/log/wtmp`). |

## Procesos en ejecución

| Comando | Uso forense |
|---|---|
| `ps` | Solo los procesos de la terminal actual (PID, TTY, TIME, CMD). Información limitada. |
| `ps aux` | Todos los procesos: USER, PID, %CPU, %MEM, VSZ, RSS, TTY, STAT, START, TIME, COMMAND. |
| `ps -ef --forest` | Árbol de procesos padre e hijo; útil para ver qué proceso lanzó a cuál. |
| `top` / `htop` | Monitoreo en tiempo real. Un proceso con CPU muy alta puede ser ransomware cifrando o un minero. |

## Archivos abiertos (`lsof`)

`lsof` lista los archivos abiertos y el proceso que los usa (nombre, PID, usuario, tipo, dispositivo, ruta).

```bash
lsof /ruta/archivo_o_directorio   # quién tiene abierto un archivo (p. ej. /var/log/nginx/access.log)
lsof -p <PID>                      # archivos abiertos por un proceso
lsof -u <usuario>                  # archivos abiertos por un usuario
lsof -i                            # sockets de red abiertos con su proceso
lsof -i :9090                      # quién usa el puerto 9090
lsof +L1                           # archivos borrados que un proceso aún mantiene abiertos
```

`lsof +L1` es importante: un binario o log borrado sigue accesible en `/proc/<PID>/fd/` mientras el proceso viva, y se puede copiar como evidencia.

## Conexiones de red

`netstat` muestra conexiones activas, puertos en escucha y el programa dueño de cada socket. En distribuciones modernas `ss` lo reemplaza con los mismos parámetros.

| Parámetro | Significado |
|---|---|
| `-a` | Sockets en escucha y no en escucha. |
| `-l` | Solo en escucha. |
| `-t` / `-u` | TCP / UDP. |
| `-4` / `-6` | Solo IPv4 / IPv6. |
| `-n` | Direcciones numéricas, sin resolver nombres (más rápido y no genera tráfico DNS). |
| `-p` | PID y nombre del programa (requiere root). |

```bash
netstat -at          # todas las conexiones TCP
netstat -lt          # puertos TCP en escucha
ss -tulpn            # TCP y UDP en escucha, numérico, con proceso
ss -tanp state established
```

## Interfaces de red

```bash
ip addr        # o ifconfig
ip route
ip neigh       # tabla ARP
```

Una interfaz nueva o inesperada puede indicar un túnel (por ejemplo, para DNS tunneling).

## Historial de comandos

`~/.bash_history` guarda los comandos de cada usuario. Revísalo para todos los usuarios, no solo el actual.

```bash
history                          # historial de la sesión actual
cat /home/<usuario>/.bash_history
cat /root/.bash_history
```

Limitaciones: el historial se escribe al cerrar la sesión, el usuario puede desactivarlo (`unset HISTFILE`) o borrarlo, y no tiene timestamps salvo que `HISTTIMEFORMAT` esté configurado. Un historial vacío o recién truncado es en sí un hallazgo (posible MITRE T1070.003, *Clear Command History*).

## Memoria RAM

La RAM contiene aplicaciones abiertas, actividad del usuario, conexiones, claves y malware que solo vive en memoria. En Linux se vuelca con **LiME** (Linux Memory Extractor), un módulo del kernel, o con **AVML**, un binario estático. El volcado se analiza con **Volatility** (ver steering `dfl-memoria.md`).

```bash
# LiME: el módulo debe estar compilado para el kernel exacto del sistema (uname -r)
sudo insmod lime-$(uname -r).ko "path=/mnt/evidencia/caso01-mem.lime format=lime"

# AVML
sudo ./avml /mnt/evidencia/caso01-mem.lime
```

Escribe el volcado en un medio externo o por red, nunca en el disco del sistema investigado.
