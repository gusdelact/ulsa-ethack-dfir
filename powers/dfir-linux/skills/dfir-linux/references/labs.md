# Laboratorios: enfoque metodológico

Esta guía da el escenario, el acceso y el **método** de cada laboratorio. **No** da respuestas: el valor está en que el alumno recolecte, razone y documente. Falta la sección 8 de ambos cursos (probablemente el Skills Assessment) en los PDFs disponibles.

## Acceso

| Curso | Credenciales del laboratorio |
|---|---|
| Digital Forensics on Linux | `root` / `123456` (VNC, puerto 5903) |
| Continuación | `analyst` / `123` |

En la continuación, varios logs están copiados en `/home/analyst/` (`auth.log`, `audit.log`). Analiza esas copias; no hace falta tocar `/var/log`.

## Reglas para todos los laboratorios

1. Abre una bitácora del caso en `evidencia/<lab>/bitacora.md` con hora UTC de cada comando.
2. Antes de abrir una imagen o un log copiado, calcula su SHA-256.
3. Responde cada pregunta con la **evidencia** que la sostiene (comando + línea de salida), no solo el valor.
4. Si una pregunta menciona una técnica de MITRE ATT&CK, anota también cómo la detectaste.

## Linux — Live Response 2 (sección 3)

Preguntas sobre: qué proceso lee un log de nginx, qué proceso escucha en un puerto, qué comando usó un usuario para borrar logs (MITRE T1070.002) y si lo logró.

Método:
1. `lsof <ruta_del_log>` para el proceso que lee el archivo.
2. `ss -tulpn` o `netstat -tulpn` (o `lsof -i :<puerto>`) para el proceso en escucha.
3. Historial del usuario (`/home/<usuario>/.bash_history`) para el comando de borrado.
4. Para el éxito: ¿tenía permisos sobre el log? ¿usó `sudo` y aparece en `auth.log`? ¿el log sigue intacto (tamaño, `stat`, contenido)?

## Linux — File System Forensics (sección 5)

Preguntas sobre: hash MD5 de una imagen en `/root/images/` y hash de un archivo dentro de la imagen montada.

Método:
1. `md5sum` (y `sha256sum` para tu bitácora) de la imagen.
2. Monta en solo lectura: `mount -o ro,loop <imagen> /mnt/image`.
3. Localiza el archivo dentro del montaje y calcula su hash.
4. Desmonta al terminar y verifica que el hash de la imagen no cambió.

## Linux — Configuration Files (sección 6)

Preguntas sobre: script que cron ejecuta al reiniciar y cuántos grupos pueden ejecutar todos los comandos en `sudoers`.

Método:
1. Busca `@reboot` en `/etc/crontab`, `/etc/cron.d/` y los crontabs de usuario.
2. En `/etc/sudoers` y `/etc/sudoers.d/`, cuenta las líneas de grupo (`%nombre`) con `ALL` como comandos; ignora comentarios.

## Linux — System Files (sección 7)

Preguntas sobre: IP a la que un script de arranque envía ICMP, qué usuario además de root entra con llave SSH, qué script en `/var/www/html` pueden ejecutar "otros", qué inicio de sesión dispara un GET a un C2 y qué archivo `.php` hay en el directorio web.

Método:
1. Lee el script de arranque encontrado en cron.
2. Recorre `~/.ssh/authorized_keys` de todos los usuarios.
3. `find /var/www/html -type f -perm -o=x` y `find /var/www/html -name '*.php'`.
4. Busca `curl`/`wget` en los `.bashrc` y `.profile` de todos los usuarios.

## Continuación — Log File Analysis (sección 2)

Preguntas sobre `/home/analyst/auth.log`: qué usuario entró por SSH sin contraseña, qué usuario y qué IP tienen más intentos fallidos.

Método: `grep "Accepted" ` para el método de autenticación (`publickey` frente a `password`); para los fallos, cuenta con `grep "Failed password" | ... | sort | uniq -c | sort -rn` (ver `references/logs.md`).

## Continuación — Log File Analysis 2 (sección 3)

Preguntas sobre `/home/analyst/audit.log`: quién no pudo ejecutar un comando por permisos y qué comando, qué AUID y qué UID corresponden a la ejecución de `whoami`, y qué proceso creó un webshell.

Método:
1. `ausearch -if audit.log -i -sv no` para eventos fallidos; mira `exit=-13` (EACCES) o `-1` (EPERM), y `comm`/`exe`.
2. `ausearch -if audit.log -i -x whoami` o `-c whoami`; distingue `auid` (quién inició sesión) de `uid` (identidad del proceso).
3. `ausearch -if audit.log -i -f <ruta_del_archivo>`; lee `comm`/`exe` del SYSCALL con el mismo número de evento.

## Continuación — Log File Analysis 3 (sección 4)

Pregunta sobre qué comando lee `/var/log/btmp`. Repasa la tabla de `wtmp`/`btmp` en `references/logs.md`.

## Continuación — Evidence Acquisition with Commands (secciones 5–6)

Preguntas sobre: versión del kernel, fecha de modificación de un script en `/var/www/html`, qué usuario entró por SSH desde la IP que aparece en ese script, y qué archivos bajo `/home` tienen SUID y SGID.

Método:
1. `uname -r`.
2. `stat <script>` (campo `Modify`) y `cat` del script para obtener la IP.
3. `grep <IP> /home/analyst/auth.log`.
4. `find /home -perm -4000` y `find /home -perm -2000`.
