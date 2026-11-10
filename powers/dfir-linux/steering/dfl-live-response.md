# DFIR en Linux: live response

> Guía de steering del power **dfir-linux**, derivada de *Linux Live Response* 1 y 2 (HTB, secciones 2–3). Detalle de cada comando en `references/live-response.md`.
>
> **Encuadre:** solo en hosts propios o autorizados. Cada comando que ejecutas modifica un poco el sistema; ejecuta lo necesario y anótalo.

## Reglas

1. **Salida fuera del disco sospechoso:** monta un USB o un recurso de red en `/mnt/evidencia`, o envía la salida por red (`| nc <analista> <puerto>`). En el laboratorio, usa `evidencia/<caso>/volatil/`.
2. **Binarios confiables:** si sospechas un rootkit, los `ps`, `ls` o `netstat` del sistema pueden mentir. Usa binarios estáticos desde tu medio externo y compara con lo que muestra `/proc`.
3. **Una salida por archivo**, con la hora y el hash.

## Script de recolección

Plantilla para recolectar en orden de volatilidad. Ajusta `OUT` al medio externo.

```bash
#!/bin/bash
OUT=/mnt/evidencia/caso01/volatil
mkdir -p "$OUT"
run() { local n="$1"; shift; echo "### $(date -u +%FT%TZ) $*" >> "$OUT/bitacora.log"; "$@" > "$OUT/$n.txt" 2>&1; }

run 01-date        date -u
run 02-timedatectl timedatectl
run 03-uname       uname -a
run 04-who         who -a
run 05-w           w
run 06-last        last -Faiw
run 07-ps          ps auxwwf
run 08-pstree      ps -ef --forest
run 09-lsof        lsof -n -P
run 10-lsof-del    lsof -n -P +L1
run 11-ss          ss -tulpna
run 12-netstat     netstat -antup
run 13-ip-addr     ip addr
run 14-ip-route    ip route
run 15-arp         ip neigh
run 16-mounts      mount
run 17-lsmod       lsmod
run 18-services    systemctl list-units --type=service --all
for h in /root /home/*; do [ -f "$h/.bash_history" ] && cp -p "$h/.bash_history" "$OUT/hist_$(basename "$h").txt"; done

sha256sum "$OUT"/* > "$OUT/../volatil.sha256"
```

## Qué buscar en cada salida

| Salida | Señales de compromiso |
|---|---|
| `date` / `timedatectl` | Desfase del reloj o zona horaria distinta de los logs; corrige la línea de tiempo con ello. |
| `who`, `w`, `last` | Sesiones desde IPs desconocidas, a horas inusuales, usuarios que no deberían entrar. |
| `ps` | Procesos con nombres que imitan a los del sistema (`kworkerr`, `[kthreadd]` con PPID distinto de 2), ejecutándose desde `/tmp`, `/dev/shm` o un binario borrado, shells hijas de un servidor web (`www-data` → `bash`), consumo de CPU anómalo. |
| `lsof` | Procesos con archivos borrados abiertos (`(deleted)`), sockets inesperados, lectura de archivos sensibles. |
| `ss` / `netstat` | Puertos en escucha no documentados, conexiones salientes a IPs externas, shells inversas (`bash` o `nc` con conexión ESTABLISHED). |
| `ip` | Interfaces nuevas (túneles), rutas o entradas ARP alteradas. |
| `lsmod` | Módulos del kernel desconocidos (posible rootkit). |
| Historial | Descargas (`wget`, `curl`), cambios de permisos, creación de usuarios, borrado de logs, `history -c`. |

## Verificaciones cruzadas con `/proc`

```bash
ls -l /proc/<PID>/exe          # binario real del proceso; "(deleted)" si se borró
cat /proc/<PID>/cmdline | tr '\0' ' '
ls -l /proc/<PID>/cwd          # directorio de trabajo
cat /proc/<PID>/environ | tr '\0' '\n'
cp /proc/<PID>/exe /mnt/evidencia/caso01/volatil/pid<PID>.bin   # recupera un binario borrado
ls /proc | grep -E '^[0-9]+$' | sort -n > /tmp/proc_pids; ps -e -o pid= | sort -n > /tmp/ps_pids; diff /tmp/proc_pids /tmp/ps_pids   # PIDs ocultos a ps
```

En el último ejemplo los archivos temporales son de trabajo; si el `diff` muestra diferencias, guarda el resultado en la carpeta de evidencia.

## Memoria

Vuelca la RAM antes de los comandos anteriores si tienes la herramienta lista (ver `dfl-memoria.md`). LiME necesita un módulo compilado para el kernel exacto (`uname -r`); AVML es un binario estático y suele ser más simple en la nube.

## Preguntas de control

- ¿Cada salida está fuera del disco sospechoso y con hash?
- ¿Anotaste la hora UTC de cada comando?
- ¿Revisaste el historial de **todos** los usuarios, incluido root?
- ¿Relacionaste cada conexión sospechosa con su proceso y cada proceso con su binario?
