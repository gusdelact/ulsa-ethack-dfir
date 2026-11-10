# Adquisición de evidencia con comandos (continuación, secciones 5–6)

Comandos para obtener información detallada del sistema, examinar posibles intrusiones y construir la línea de tiempo.

## `uname`

Sistema operativo, versión del kernel y arquitectura. Sirve para identificar vulnerabilidades del kernel y para elegir el módulo de LiME o los símbolos de Volatility correctos.

```bash
uname -a     # todo
uname -r     # solo la versión del kernel (p. ej. 6.5.0-28-generic)
cat /etc/os-release
```

## `tcpdump`

Captura tráfico para documentar ataques, comunicaciones maliciosas y su origen. Detalle completo en el power `network-forensics`.

```bash
tcpdump -i ens33 dst host 1.1.1.1
tcpdump -i ens33 -w /mnt/evidencia/caso01.pcap
```

## `ngrep`

Como `tcpdump`, pero filtra por texto o patrones dentro del contenido. Útil para buscar firmas o palabras clave en el tráfico.

```bash
ngrep -W byline -d ens33 dst host 1.1.1.1
ngrep -q -d ens33 -i 'password|user' port 21
```

## `strings`

Extrae cadenas imprimibles de binarios: contraseñas, configuraciones, URLs, IPs, comandos. Útil para entender un binario sospechoso sin ejecutarlo.

```bash
strings -n 6 /tmp/binario_sospechoso | grep -E 'http|/bin/|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
```

## `stat`

Detalles y timestamps de un archivo. Esencial para la línea de tiempo y para verificar integridad.

```bash
stat /usr/sbin/arp
```

| Campo | Significado |
|---|---|
| `File` | Nombre y ruta. |
| `Size` / `Blocks` / `IO Block` | Tamaño en bytes, bloques ocupados y tamaño de bloque de E/S. |
| `Device` | Identificador del dispositivo (hex/decimal). |
| `Inode` | Identificador único del archivo en el sistema de archivos. |
| `Links` | Número de enlaces duros. |
| `Access (permisos)` | Permisos octal y simbólico (p. ej. `0755/-rwxr-xr-x`). |
| `Uid` / `Gid` | Dueño y grupo. |
| `Access` | Último acceso (atime). |
| `Modify` | Última modificación del contenido (mtime). |
| `Change` | Último cambio de metadatos: permisos, dueño, renombre (ctime). |
| `Birth` | Creación (crtime). No todos los sistemas de archivos lo guardan. |

**Detección de timestomping:** `touch -t` o `touch -d` cambia atime y mtime, pero el kernel actualiza **ctime** con la hora real del cambio. Un `Modify` antiguo con un `Change` reciente indica manipulación de fechas (MITRE T1070.006, *Timestomp*). Ten en cuenta también que muchos sistemas montan con `relatime`, así que `Access` no siempre refleja cada lectura.

## `find`

Busca archivos por nombre, fecha, tamaño, permisos y otros atributos.

### SUID y SGID

- **SUID:** el programa corre con los privilegios de su dueño (normalmente root) sin importar quién lo ejecute.
- **SGID:** corre con los privilegios del grupo del archivo.

Un binario SUID/SGID desconocido, sobre todo en `/home`, `/tmp` o `/var/www`, puede ser una puerta trasera para escalar privilegios (MITRE T1548.001, *Setuid and Setgid*).

```bash
find / -perm -4000 2>/dev/null        # SUID
find / -perm -2000 2>/dev/null        # SGID
find /home -perm /6000 -type f -ls 2>/dev/null
```

Compara la lista con la de un sistema limpio de la misma distribución; la mayoría de SUID legítimos están en `/usr/bin` y `/usr/sbin`.

### Por fecha, en la ventana del incidente

```bash
find / -xdev -newermt "2024-07-27 10:00" ! -newermt "2024-07-27 12:00" -type f 2>/dev/null
find /etc -mtime -7
```

## `grep`

Filtra logs e historiales por IP, usuario, evento o comando.

```bash
grep "172.16.8.1" /var/log/auth.log                         # accesos de una IP
grep -E "session opened|session closed" /var/log/auth.log   # inicios y cierres de sesión
grep "rm " /home/<usuario>/.bash_history                    # archivos borrados por un usuario
```

## Encadenar comandos

Un hallazgo suele llevar al siguiente. Ejemplo de razonamiento del laboratorio:
1. `stat` sobre un script sospechoso en `/var/www/html` da la fecha de modificación.
2. El contenido del script (`cat`, `strings`) revela una IP.
3. `grep <IP> auth.log` muestra qué usuario entró por SSH desde esa IP y cuándo.
4. La fecha de entrada se compara con la fecha de modificación del script para ordenar los hechos.
