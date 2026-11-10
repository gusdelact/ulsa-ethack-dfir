# DFIR en Linux: análisis de logs por pregunta

> Guía de steering del power **dfir-linux**, derivada de *Linux Log File Analysis* 1–3 (HTB, continuación, secciones 2–4). Detalle de cada log en `references/logs.md`.
>
> **Encuadre:** analiza copias de los logs con su hash, no los originales del sistema sospechoso.

## Antes de empezar

1. Copia los logs a `evidencia/<caso>/logs/` y calcula su SHA-256.
   ```bash
   cp -a /var/log /mnt/evidencia/caso01/logs/varlog
   sha256sum $(find /mnt/evidencia/caso01/logs -type f) > /mnt/evidencia/caso01/logs.sha256
   ```
2. Incluye los rotados (`auth.log.1`, `auth.log.2.gz`). Lee los comprimidos con `zgrep` o `zcat`.
3. Anota la zona horaria del sistema: `syslog` y `auth.log` usan hora local sin año; `audit.log` usa epoch.

## Recetario por pregunta

### ¿Hubo fuerza bruta? ¿Desde dónde?

```bash
grep -c "Failed password" auth.log
grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head
grep "Failed password" auth.log | grep -oP 'for (invalid user )?\K\S+' | sort | uniq -c | sort -rn | head
lastb -Fai -f btmp | head
```

### ¿El ataque tuvo éxito?

```bash
grep "Accepted" auth.log                         # método: password o publickey
grep "<IP_atacante>" auth.log | grep -E "Accepted|session opened"
last -Faiw -f wtmp | grep "<IP_atacante>"
```

Patrón de compromiso: ráfaga de `Failed` y después `Accepted` desde la misma IP.

### ¿Quién entró sin contraseña?

```bash
grep "Accepted publickey" auth.log
```

Después revisa el `authorized_keys` de ese usuario (`dfl-persistencia.md`).

### ¿Quién usó `sudo` y para qué?

```bash
grep "sudo:" auth.log | grep COMMAND
grep "NOT in sudoers" auth.log
ausearch -if audit.log -i -m USER_CMD
```

### ¿Qué comandos se ejecutaron y quién los inició?

```bash
ausearch -if audit.log -i -m EXECVE
ausearch -if audit.log -i -x whoami        # por ejecutable
```

Lee `auid` (quién inició sesión) frente a `uid`/`euid` (con qué identidad corrió). Si `auid=admin` y `euid=root`, el usuario `admin` ejecutó como root.

### ¿Qué falló por falta de permisos?

```bash
ausearch -if audit.log -i -sv no
```

`exit=-13` (EACCES) y `exit=-1` (EPERM) indican permiso denegado; `comm` y `exe` dicen qué intentó ejecutarse.

### ¿Qué proceso creó o modificó un archivo?

```bash
ausearch -if audit.log -i -f /var/www/html/upload/shell.php
```

En el evento, el registro `PATH` con `nametype=CREATE` confirma la creación; `comm`/`exe` del `SYSCALL` con el mismo número de evento dice qué proceso lo hizo (por ejemplo, el servidor web, lo que indica una subida por la aplicación).

### ¿Qué pasó con un servicio?

```bash
grep -E "sshd|nginx|apache2" syslog | grep -E "Started|Stopped|Failed"
journalctl -u ssh --since "2026-11-05 10:00" --until "2026-11-05 12:00"
```

### ¿Se cargó algo raro en el arranque o en el kernel?

```bash
less boot.log
dmesg -T | grep -iE 'module|taint|usb'
```

### ¿Se borraron rastros?

- Huecos de tiempo en `auth.log` o `syslog`.
- Logs de tamaño 0 o con `Modify` reciente (`stat`).
- `rm`, `>`, `truncate`, `shred`, `history -c` en el historial.
- Para el éxito, verifica permisos (¿`sudo`? ¿`Permission denied`?) y el estado real del archivo.

## Convertir timestamps

```bash
date -u -d @1722078602                         # epoch de audit.log a UTC
date -u -d 'TZ="America/Mexico_City" 2024-07-27 10:15:02'   # hora local de syslog a UTC (syslog no guarda el año: agrégalo)
```

## Correlación

Une las fuentes en una tabla ordenada por hora UTC: `auth.log` (acceso), `audit.log` (ejecución), historial (intención), `stat` y `mactime` (archivos). Ver `dfl-reporte.md`.

## Preguntas de control

- ¿Incluiste los logs rotados y comprimidos?
- ¿Convertiste todas las horas a UTC?
- ¿Cada respuesta cita la línea exacta del log?
- ¿Revisaste si faltan periodos (borrado de rastros)?
