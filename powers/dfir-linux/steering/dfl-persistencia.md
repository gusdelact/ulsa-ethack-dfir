# DFIR en Linux: persistencia y escalada de privilegios

> Guía de steering del power **dfir-linux**, derivada de *Linux Configuration Files*, *Linux System Files* y *Linux Evidence Acquisition with Commands - 2* (HTB). Detalle en `references/archivos-configuracion.md` y `references/archivos-sistema.md`.
>
> **Encuadre:** solo en hosts propios o autorizados. Si analizas en vivo, no ejecutes los scripts que encuentres: léelos.

## Mecanismos y dónde buscarlos

| Mecanismo | MITRE ATT&CK | Ubicación | Comando |
|---|---|---|---|
| Cron | T1053.003 | `/etc/crontab`, `/etc/cron.d/`, `/etc/cron.*/`, `/var/spool/cron/` | `cat`, `crontab -l -u <u>` |
| Servicio systemd | T1543.002 | `/etc/systemd/system/`, `/lib/systemd/system/` | `systemctl list-unit-files --state=enabled` |
| Timer systemd | T1053.006 | Igual que servicios | `systemctl list-timers --all` |
| Llave SSH | T1098.004 | `~/.ssh/authorized_keys` | `cat`, `stat` |
| Configuración del shell | T1546.004 | `~/.bashrc`, `~/.profile`, `/etc/profile.d/`, `/etc/bash.bashrc` | `grep` de comandos de red |
| Cuenta local nueva | T1136.001 | `/etc/passwd`, `/etc/shadow` | `awk`, comparar con inventario |
| Cuenta con UID 0 | T1078.003 | `/etc/passwd` | `awk -F: '$3==0'` |
| Grupo privilegiado | T1098 | `/etc/group` | `grep sudo\|wheel\|docker` |
| `sudo` sin contraseña | T1548.003 | `/etc/sudoers`, `/etc/sudoers.d/` | `grep NOPASSWD` |
| Binario SUID/SGID | T1548.001 | Cualquier ruta, sobre todo `/home`, `/tmp` | `find / -perm -4000`, `-2000` |
| Webshell | T1505.003 | `/var/www/html` | `find -name '*.php' -newer` |
| Módulo del kernel | T1547.006 | `/lib/modules/`, `lsmod` | `lsmod`, `dmesg` |

## Flujo

1. **Ventana de tiempo:** fija el inicio probable del incidente (primer acceso en `auth.log`).
2. **Barrido por fecha:** archivos de configuración cambiados después de esa hora.
   ```bash
   find /etc /root /home /var/spool/cron /var/www -xdev -newermt "<inicio>" -type f -ls 2>/dev/null
   ```
3. **Barrido por mecanismo:** recorre la tabla anterior. En una imagen montada, antepón la ruta del montaje (`/mnt/image/etc/crontab`).
4. **Lee el contenido:** cada script, unidad o línea que encuentres. El indicador suele ser lo que hace: `curl`/`wget` a una IP, `bash -i >& /dev/tcp/...`, `nc -e`, `base64 -d | bash`, `ping` periódico a una IP.
5. **Relaciona:** ¿el archivo se modificó en la ventana? ¿qué usuario estaba conectado? ¿aparece en `audit.log` o en el historial?
6. **Documenta** cada hallazgo con ruta, contenido relevante, `stat` y técnica ATT&CK.

## Comandos útiles

```bash
# cron de todos los usuarios
for u in $(cut -d: -f1 /etc/passwd); do crontab -l -u "$u" 2>/dev/null | sed "s/^/$u: /"; done
grep -R "@reboot" /etc/crontab /etc/cron.d /var/spool/cron 2>/dev/null

# servicios y timers creados localmente
ls -lt /etc/systemd/system/*.service 2>/dev/null
systemctl list-timers --all

# llaves SSH de todos los usuarios
for h in /root /home/*; do f="$h/.ssh/authorized_keys"; [ -f "$f" ] && { stat -c '%y %n' "$f"; cat "$f"; }; done

# comandos de red en archivos de inicio del shell
grep -nE 'curl|wget|nc |ncat|/dev/tcp|bash -i|base64' /root/.bashrc /home/*/.bashrc /home/*/.profile /etc/profile.d/* 2>/dev/null

# cuentas y privilegios
awk -F: '$3==0 {print "UID0:", $1}' /etc/passwd
grep -vE '^\s*(#|$)' /etc/sudoers /etc/sudoers.d/* 2>/dev/null
grep -E '^(sudo|wheel|adm|docker|lxd|disk):' /etc/group

# SUID/SGID fuera de rutas estándar
find / -xdev \( -perm -4000 -o -perm -2000 \) -type f 2>/dev/null | grep -vE '^/(usr/)?(s?bin|lib)'

# archivos ejecutables por "otros" en el directorio web
find /var/www/html -type f -perm -o=x
```

## Errores frecuentes

- Revisar solo el crontab de root y no los de usuario ni `/etc/cron.d/`.
- Revisar `.bashrc` del usuario actual y no el de todas las cuentas.
- Ver una línea de cron que llama a un script y no leer el script.
- Confundir un SUID legítimo del sistema (`/usr/bin/passwd`, `/usr/bin/sudo`) con uno malicioso. Compara con un sistema limpio de la misma versión.

## Preguntas de control

- ¿Recorriste todos los mecanismos de la tabla?
- ¿Cada hallazgo tiene `stat`, contenido y técnica ATT&CK?
- ¿Relacionaste cada mecanismo con el usuario y la hora en que se creó?
