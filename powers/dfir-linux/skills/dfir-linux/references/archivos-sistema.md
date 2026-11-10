# Archivos de sistema (Linux, sección 7)

## `~/.ssh/authorized_keys`

Contiene las llaves públicas autorizadas para entrar por SSH a esa cuenta sin contraseña. Quien tenga la llave privada correspondiente entra directamente.

```
<tipo_llave> <valor_llave> <comentario>
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... usuario@equipo
```

| Campo | Significado |
|---|---|
| `tipo_llave` | `ssh-rsa`, `ssh-dss`, `ecdsa-sha2-nistp256`, `ssh-ed25519`. |
| `valor_llave` | Llave pública en base64. |
| `comentario` | Opcional; suele ser el correo o el equipo del dueño. |

Qué buscar (MITRE T1098.004, *SSH Authorized Keys*):
- Llaves desconocidas o agregadas en la ventana del incidente.
- Llaves en cuentas que no deberían tener acceso remoto.
- Algoritmos débiles u obsoletos (`ssh-dss`, RSA corto).
- Opciones al inicio de la línea, como `command="..."`, que ejecutan algo al conectar.

```bash
for h in /root /home/*; do [ -f "$h/.ssh/authorized_keys" ] && { echo "== $h"; stat -c '%y %n' "$h/.ssh/authorized_keys"; cat "$h/.ssh/authorized_keys"; }; done
```

En `auth.log`, una línea `Accepted publickey for <usuario>` confirma que se usó una llave.

## `.bashrc`

Se ejecuta en cada sesión interactiva de bash. Muestra personalizaciones (aliases, funciones, variables) y puede contener comandos maliciosos que corren en cada inicio de sesión (MITRE T1546.004, *Unix Shell Configuration Modification*). Por ejemplo, un `curl` o `wget` a un servidor de C2.

```bash
cat ~/.bashrc
ls -la ~/.bashrc                       # fecha de modificación
for h in /root /home/*; do echo "== $h"; grep -nE 'curl|wget|nc |bash -i|/dev/tcp|base64|python|alias ' "$h/.bashrc" 2>/dev/null; done
```

Compara el `.bashrc` entre cuentas para encontrar diferencias. Revisa también `.bash_profile`, `.profile`, `/etc/profile`, `/etc/profile.d/` y `/etc/bash.bashrc`.

## systemd y servicios

systemd es el sistema de inicio y gestor de servicios de las distribuciones modernas. Los servicios se definen en archivos `.service`. Un servicio malicioso que arranca en cada reinicio es persistencia (MITRE T1543.002, *Systemd Service*).

| Comando | Uso |
|---|---|
| `systemctl status` | Estado de todos los servicios y unidades. |
| `systemctl list-units --type=service` | Servicios en ejecución. |
| `systemctl list-unit-files --state=enabled` | Servicios que arrancan automáticamente. |
| `systemctl list-timers --all` | Timers de systemd (alternativa a cron). |
| `systemctl cat <servicio>` | Contenido de la unidad, incluido `ExecStart`. |
| `journalctl -u <servicio>` | Logs de un servicio. |

Las unidades creadas por un administrador o un atacante suelen estar en `/etc/systemd/system/`; las de paquetes, en `/lib/systemd/system/` o `/usr/lib/systemd/system/`.

```bash
ls -lt /etc/systemd/system/ | head
find /etc/systemd/system /lib/systemd/system -name '*.service' -newer /etc/hostname
```

## `/tmp` y `/var/tmp`

Tienen permisos de escritura amplios, por eso los atacantes suben ahí herramientas, scripts y malware. `/dev/shm` cumple el mismo papel y vive en RAM.

```bash
ls -lart /tmp /var/tmp /dev/shm          # ordenado por fecha
find /tmp -name '*.php'                   # extensiones típicas: .php, .py, .sh
find /var/tmp -name '*.sh'
grep -R "cadena_sospechosa" /tmp
grep -R "192.168.1.1" /var/tmp
find /tmp -mtime -2                       # modificados en los últimos 2 días
find /var/tmp -atime -2                   # accedidos en los últimos 2 días
find /tmp -size +10M                      # archivos grandes (datos recolectados para exfiltrar)
find /tmp -type f -perm -o=w              # escribibles por cualquiera
find / -xdev -name '.*' -path '*/tmp/*'   # archivos ocultos
```

Los mismos comandos aplican al directorio web (`/var/www/html`), donde suelen aparecer webshells (`.php`) y scripts ejecutables por "otros":

```bash
find /var/www/html -type f -perm -o=x
find /var/www/html -name '*.php' -newer /var/www/html/index.html
```
