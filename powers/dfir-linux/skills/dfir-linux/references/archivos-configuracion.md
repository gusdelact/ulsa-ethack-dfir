# Archivos de configuración (Linux, sección 6)

Los archivos de `/etc` muestran cuentas, grupos, privilegios y tareas programadas. Un atacante los modifica para crear accesos, escalar privilegios o persistir.

## `/etc/passwd`

Cuentas de usuario: nombre, UID, GID, directorio personal y shell.

```
username:x:user_id:group_id:real_name:user_home_directory:user_shell
```

| Campo | Significado |
|---|---|
| `username` | Nombre de inicio de sesión. |
| `x` | Marca de que el hash está en `/etc/shadow`. |
| `user_id` (UID) | Identificador único; `0` es root. |
| `group_id` (GID) | Grupo principal. |
| `real_name` | Descripción opcional. |
| `user_home_directory` | Directorio personal. |
| `user_shell` | Shell de inicio de sesión. |

Qué buscar:
- Cuentas nuevas o que no corresponden al inventario (MITRE T1136.001, *Create Local Account*).
- Cualquier cuenta distinta de root con **UID 0**.
- Cuentas de servicio con shell interactivo (`/bin/bash` en lugar de `/usr/sbin/nologin`).

```bash
awk -F: '$3 == 0 {print $1}' /etc/passwd          # cuentas con UID 0
awk -F: '$7 !~ /(nologin|false)$/ {print $1, $7}' /etc/passwd
```

## `/etc/shadow`

Hashes de contraseña y estado de las cuentas. Solo lo lee root.

```
username:password_hash:time:minimum:maximum:warning:inactivity:expiration_date
```

| Campo | Significado |
|---|---|
| `password_hash` | Hash de la contraseña (`$6$` = SHA-512, `$y$` = yescrypt). `!` o `*` = cuenta bloqueada o sin contraseña. |
| `time` | Días desde el 1 de enero de 1970 del último cambio. |
| `minimum` / `maximum` | Días mínimos y máximos entre cambios. |
| `warning` | Días de aviso antes de expirar. |
| `inactivity` | Días tras la expiración antes de inactivar la cuenta. |
| `expiration_date` | Fecha de expiración (días desde 1970). |

Qué buscar: cambios de contraseña recientes que coinciden con el incidente, hashes alterados para persistir, cuentas desbloqueadas que deberían estar bloqueadas y contraseñas débiles.

```bash
date -d "1970-01-01 +19500 days"   # convierte el campo "time" a fecha
```

## `/etc/group`

Grupos y sus miembros.

```
group_name:x:group_id:group_members
```

Qué buscar: usuarios agregados a grupos privilegiados (`sudo`, `wheel`, `adm`, `docker`, `lxd`, `disk`).

```bash
grep -E '^(sudo|wheel|adm|docker|lxd|disk|root):' /etc/group
```

## `/etc/sudoers`

Define qué usuarios o grupos ejecutan comandos como root con `sudo`. Revisa también `/etc/sudoers.d/`.

Qué buscar (MITRE T1548.003, *Sudo and Sudo Caching*):
- Entradas `ALL=(ALL) ALL` o `ALL=(ALL:ALL) ALL` nuevas o inesperadas. Los grupos aparecen con `%` (por ejemplo, `%admin`).
- `NOPASSWD`, que permite `sudo` sin contraseña.
- Comandos permitidos que dan shell (editores, `find`, `tar`, intérpretes).

```bash
grep -vE '^\s*(#|$)' /etc/sudoers /etc/sudoers.d/* 2>/dev/null
```

## `/etc/crontab`

Tareas programadas del sistema. Los atacantes las usan para mantener acceso o repetir acciones (MITRE T1053.003, *Cron*).

```
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# minuto hora día_mes mes día_semana usuario comando
17 *  * * *  root  cd / && run-parts --report /etc/cron.hourly
@reboot      root  /scripts/ejemplo.sh
```

| Campo | Rango |
|---|---|
| minuto | 0–59 |
| hora | 0–23 |
| día del mes | 1–31 |
| mes | 1–12 o Jan–Dec |
| día de la semana | 0–6 (domingo = 0 o 7) o Sun–Sat |
| usuario | Usuario con el que corre (solo en `/etc/crontab` y `/etc/cron.d/`) |
| comando | Comando o script |

`@reboot` ejecuta el comando en cada arranque, un mecanismo de persistencia habitual. Revisa además `/etc/cron.d/`, `/etc/cron.{hourly,daily,weekly,monthly}/` y los crontabs de usuario en `/var/spool/cron/crontabs/` (Debian) o `/var/spool/cron/` (Red Hat).

```bash
cat /etc/crontab; ls -la /etc/cron.d/ /var/spool/cron/crontabs/ 2>/dev/null
for u in $(cut -d: -f1 /etc/passwd); do crontab -l -u "$u" 2>/dev/null | sed "s/^/$u: /"; done
```

Lee el contenido de cada script que aparezca en cron: el hallazgo suele estar en el script, no en la línea de cron.
