# Análisis de logs en Linux (continuación, secciones 2–4)

Los logs registran eventos del sistema, actividad de usuarios, errores e incidentes de seguridad. Sirven para construir la línea de tiempo, detectar intrusiones y entender cambios. Casi toda acción del atacante deja un rastro en alguno de ellos.

## Mapa de logs

| Log | Distribución | Qué registra | Cómo leerlo |
|---|---|---|---|
| `/var/log/syslog` | Debian/Ubuntu | Eventos generales del sistema y servicios. | `grep`, `less` |
| `/var/log/messages` | Red Hat | Equivalente a `syslog`. | `grep`, `less` |
| `/var/log/auth.log` | Debian/Ubuntu | Autenticación: logins, `sudo`, SSH. | `grep` |
| `/var/log/secure` | Red Hat | Equivalente a `auth.log`. | `grep` |
| `/var/log/audit/audit.log` | Con auditd | Llamadas al sistema, comandos, accesos a archivos, SELinux. | `ausearch`, `aureport` |
| `/var/log/boot.log` | Varias | Servicios y drivers en el arranque. | `less` |
| `/var/log/dmesg` | Varias | Mensajes del kernel: hardware, drivers, módulos. | `dmesg`, `less` |
| `/var/log/faillog` | Varias (binario) | Contador de intentos fallidos por usuario. | `faillog -a` |
| `/var/log/wtmp` | Todas (binario) | Logins y logouts exitosos, reinicios, apagados. | `last` |
| `/var/log/btmp` | Todas (binario) | Intentos de login fallidos. | `lastb` |
| journal de systemd | Modernas | Todo lo anterior en formato binario. | `journalctl` |

En una imagen montada, lee los binarios con `-f`: `last -f /mnt/image/var/log/wtmp`, `lastb -f /mnt/image/var/log/btmp`, `journalctl --directory=/mnt/image/var/log/journal`.

## `syslog` y `messages`

Registran eventos con timestamp, cambios de estado de servicios, errores, advertencias, instalaciones de software y cambios de configuración.

Puntos de análisis: inicios y cierres de sesión, mensajes de error de seguridad, advertencias críticas (disco, red), arranque y parada de servicios (SSH, FTP, web), fallos de autorización y cambios del sistema.

```bash
grep -iE 'error|fail|denied' /var/log/syslog
grep -E 'Started|Stopped' /var/log/syslog
grep CRON /var/log/syslog              # ejecuciones de cron
```

## `auth.log` y `secure`

Registran todos los intentos de autenticación, uso de `sudo`, sesiones SSH y otros eventos de autorización. Cada línea incluye timestamp, usuario, IP de origen, resultado y, en `sudo`, el comando.

| Patrón | Significado |
|---|---|
| `Failed password for <u> from <ip>` | Contraseña fallida. Muchos en poco tiempo = fuerza bruta (MITRE T1110). |
| `Failed password for invalid user <u>` | Usuario inexistente: enumeración o diccionario. |
| `Accepted password for <u> from <ip>` | Login exitoso con contraseña. |
| `Accepted publickey for <u> from <ip>` | Login exitoso con llave SSH (no usa contraseña). |
| `session opened for user <u>` / `session closed` | Inicio y fin de sesión. |
| `sudo: <u> : TTY=... ; USER=root ; COMMAND=...` | Comando ejecutado con `sudo`. |
| `<u> : user NOT in sudoers` | Intento de `sudo` sin permiso. |
| `useradd`, `usermod`, `passwd` | Altas o cambios de cuentas. |

```bash
grep "172.16.8.1" /var/log/auth.log                         # actividad de una IP
grep -E "session opened|session closed" /var/log/auth.log   # sesiones
grep "Accepted" /var/log/auth.log                           # logins exitosos y método
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn   # IPs con más fallos
grep "Failed password" /var/log/auth.log | grep -oP 'for (invalid user )?\K\S+' | sort | uniq -c | sort -rn  # usuarios con más fallos
grep "sudo:" /var/log/auth.log | grep COMMAND
```

Busca el patrón clásico de compromiso: muchos `Failed password` desde una IP seguidos de un `Accepted` desde la misma IP.

## `audit.log` (auditd)

Registro detallado de eventos de seguridad: acciones de usuarios, llamadas al sistema, accesos a archivos y violaciones de SELinux. Cada evento tiene timestamp, identificadores de usuario, detalle de la acción y resultado.

### Tipos de registro

| Tipo | Registra |
|---|---|
| `LOGIN` | Inicios y cierres de sesión, exitosos y fallidos. |
| `CWD` | Directorio de trabajo cuando ocurrió el evento. |
| `PATH` | Rutas de archivos y directorios accedidos o modificados. |
| `EXECVE` | Comandos ejecutados y sus argumentos. |
| `SYSCALL` | Llamadas al sistema (operaciones de bajo nivel). |
| `USER_CMD` | Comandos ejecutados con `sudo`. |
| `USER_LOGIN` / `USER_LOGOUT` | Login y logout de usuarios. |
| `USER_AUTH` | Intentos de autenticación y método usado. |

### Lectura de un evento `SYSCALL`

```
type=SYSCALL msg=audit(1722078602.266:1650): arch=c000003e syscall=59 success=yes exit=0 ...
ppid=6143 pid=6229 auid=1001 uid=1001 gid=1001 euid=0 suid=0 fsuid=0 ... tty=pts2 ses=9
comm="sudo" exe="/usr/bin/sudo" subj=unconfined key="priv_esc"
```

| Campo | Significado |
|---|---|
| `msg=audit(1722078602.266:1650)` | Timestamp en epoch y número de evento. Los registros con el mismo número forman un solo evento (SYSCALL + EXECVE + CWD + PATH). |
| `arch=c000003e` | x86_64. |
| `syscall=59` | `execve` en x86_64: ejecución de un programa. |
| `success` / `exit` | Resultado. `exit=0` éxito; `-13` EACCES (permiso denegado); `-2` ENOENT (no existe); `-1` EPERM (operación no permitida); `-5` EIO (error de E/S). |
| `ppid` / `pid` | Proceso padre y proceso. |
| `auid` | **Audit UID: el usuario que inició sesión originalmente.** No cambia con `sudo` o `su`. |
| `uid` / `gid` | Usuario y grupo reales del proceso. |
| `euid` / `suid` / `fsuid` | Efectivos. `euid=0` con `auid` distinto de 0 = el usuario actuó como root. |
| `tty` / `ses` | Terminal y sesión. |
| `comm` / `exe` | Nombre del comando y ruta del binario. |
| `key` | Etiqueta de la regla de auditd que generó el evento (p. ej. `priv_esc`). |

Con `ausearch -i` los valores numéricos se traducen (AUID="admin", EUID="root", SYSCALL=execve).

```bash
date -d @1722078602                                    # convertir epoch
ausearch -if /home/analyst/audit.log -i -m EXECVE      # comandos ejecutados (archivo offline)
ausearch -if audit.log -i -sv no                       # eventos fallidos (success=no)
ausearch -if audit.log -i -k priv_esc                  # por etiqueta de regla
ausearch -if audit.log -i -f /var/www/html/upload/shell.php   # quién tocó un archivo
ausearch -if audit.log -i -ua 1001                     # por auid
aureport -if audit.log -au                             # resumen de autenticaciones
aureport -if audit.log -x --summary                    # ejecutables más usados
```

Para responder "quién ejecutó X": `auid` dice quién inició sesión; `uid`/`euid` dicen con qué identidad corrió el proceso. Para "qué proceso creó un archivo": busca el evento con `PATH` del archivo (`nametype=CREATE`) y lee `comm`/`exe` del `SYSCALL` con el mismo número de evento.

## `boot.log`

Registra servicios iniciados, drivers cargados y mensajes del arranque. Sirve para detectar errores de arranque y servicios o drivers inesperados que indiquen cambios no autorizados.

## `dmesg`

Mensajes del kernel: hardware detectado, drivers y módulos cargados, errores y kernel panics. Un módulo del kernel desconocido puede ser un rootkit. Un dispositivo USB nuevo puede indicar acceso físico. Los timestamps de `dmesg` son relativos al arranque y no siempre están activos; usa `dmesg -T` para aproximarlos a hora real.

```bash
dmesg -T | grep -iE 'usb|module|taint|segfault'
```

## `faillog`

Por usuario: número de intentos fallidos, fecha del último intento y umbral de bloqueo. Contadores altos en cuentas privilegiadas requieren atención. En distribuciones recientes el comando `faillog` puede no existir; usa `faillock --user <u>` o `lastb`.

```bash
faillog -a
```

## `wtmp` y `btmp`

| Archivo | Contenido | Comando |
|---|---|---|
| `/var/log/wtmp` | Logins y logouts exitosos, reinicios y apagados, con usuario, terminal, IP y hora. | `last` |
| `/var/log/btmp` | Logins fallidos con usuario intentado, IP y hora. | `lastb` |

```bash
last -Faiw                 # fechas completas, IP numérica
last reboot                # reinicios
lastb -Fai | head -50      # fallidos (requiere root)
lastlog                    # último login por usuario
```

Busca logins fuera de horario, desde IPs nuevas y cambios frecuentes de usuario.

## Borrado de rastros

Un atacante puede vaciar o borrar logs (MITRE T1070.002, *Clear Linux or Mac System Logs*). Señales:
- Huecos de tiempo en un log que normalmente es continuo.
- Archivos de log de tamaño 0 o con fecha de modificación reciente (`stat`).
- Comandos en el historial como `rm /var/log/...`, `> /var/log/auth.log`, `truncate`, `shred`, `history -c`.
- Para saber si el intento tuvo éxito: revisa si el usuario tenía permisos (¿usó `sudo`? ¿aparece `user NOT in sudoers` o `Permission denied`?) y si el archivo realmente cambió.
