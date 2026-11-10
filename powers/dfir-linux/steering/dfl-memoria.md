# DFIR en Linux: memoria con LiME y Volatility 3

> Guía de steering del power **dfir-linux**. La adquisición viene de *Linux Live Response - 2* (HTB, que menciona LiME y Volatility). La metodología de análisis está adaptada a Linux de la metodología de 6 pasos de *Memory Forensics* (HTB, basada en SANS), cuyo curso original es de Windows.
>
> **Encuadre:** solo en hosts propios o autorizados. El volcado puede contener contraseñas y datos personales; trátalo como evidencia sensible.

## 1. Adquisición

| Herramienta | Tipo | Requisito |
|---|---|---|
| **LiME** | Módulo del kernel | Compilado para el kernel exacto (`uname -r`). |
| **AVML** | Binario estático | Ninguno especial; práctico en la nube. |

```bash
# LiME
sudo insmod lime-$(uname -r).ko "path=/mnt/evidencia/caso01/memoria/mem.lime format=lime"

# AVML
sudo ./avml /mnt/evidencia/caso01/memoria/mem.lime

sha256sum /mnt/evidencia/caso01/memoria/mem.lime
```

Anota en la bitácora la hora, la versión del kernel (`uname -a`) y la distribución (`/etc/os-release`): los necesitarás para los símbolos.

## 2. Símbolos para Volatility 3

Volatility 3 necesita una **tabla de símbolos (ISF)** que corresponda exactamente al kernel del volcado. Sin ella, los plugins `linux.*` fallan.

1. Identifica el kernel del volcado: `vol -f mem.lime banners.Banners`.
2. Busca un ISF ya generado para ese kernel en repositorios públicos de símbolos, o genéralo con `dwarf2json` a partir del `vmlinux` con símbolos de depuración (paquete `linux-image-<versión>-dbgsym` o equivalente):
   ```bash
   ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-<versión> > <versión>.json
   ```
3. Copia el `.json` (o `.json.xz`) a `volatility3/symbols/linux/`.

## 3. Metodología de 6 pasos adaptada a Linux

| Paso | Objetivo | Plugins |
|---|---|---|
| 1. Procesos | Listar todos y compararlos con los legítimos; revisar padre e hijo. | `linux.pslist`, `linux.pstree`, `linux.psaux` |
| 2. Detalle del proceso | Línea de comandos, comandos de bash, bibliotecas y regiones mapeadas. | `linux.psaux`, `linux.bash`, `linux.proc.Maps`, `linux.lsof` |
| 3. Red | Sockets abiertos, IPs remotas y proceso dueño. | `linux.sockstat` |
| 4. Código inyectado | Regiones anónimas con permisos de ejecución. | `linux.malfind` |
| 5. Rootkits | Módulos ocultos y llamadas al sistema interceptadas. | `linux.lsmod`, `linux.check_modules`, `linux.check_syscall` |
| 6. Extracción | Volcar procesos o regiones sospechosas para análisis posterior. | `linux.proc.Maps --pid <PID> --dump`, `linux.elfs --pid <PID> --dump` |

```bash
vol -f mem.lime linux.pslist
vol -f mem.lime linux.pstree
vol -f mem.lime linux.psaux
vol -f mem.lime linux.bash
vol -f mem.lime linux.sockstat
vol -f mem.lime linux.malfind
vol -f mem.lime linux.lsmod
vol -f mem.lime linux.check_modules
vol -f mem.lime linux.check_syscall
vol -f mem.lime -o /mnt/evidencia/caso01/memoria/dump linux.proc.Maps --pid <PID> --dump
```

Los nombres de plugins cambian entre versiones de Volatility 3. Comprueba los disponibles con `vol -h` y anota la versión usada en la bitácora.

## Qué buscar

| Señal | Ejemplo |
|---|---|
| Proceso sin padre esperado | Un `bash` o `sh` hijo de `apache2`, `nginx` o `php-fpm` (webshell). |
| Nombre que imita al sistema | `[kworker]` que no es hijo de `kthreadd` (PID 2). |
| Binario en ruta temporal | Procesos desde `/tmp`, `/dev/shm`, `/var/tmp`. |
| Comandos en memoria | `linux.bash` muestra comandos aunque el `.bash_history` se haya borrado. |
| Conexión a IP externa | Socket ESTABLISHED de un proceso que no debería usar red. |
| Región RWX anónima | Hallazgo de `linux.malfind` en un proceso legítimo. |
| Módulo oculto | Aparece en `check_modules` pero no en `lsmod`. |
| Syscall interceptada | `check_syscall` muestra un manejador fuera del kernel. |

## Correlación

Contrasta la memoria con el live response: un proceso o socket en memoria que no apareció en `ps` o `ss` indica ocultamiento. Contrasta `linux.bash` con `.bash_history` para detectar borrado del historial.

## Preguntas de control

- ¿El volcado tiene hash y entrada en la cadena de custodia?
- ¿Los símbolos corresponden exactamente al kernel del volcado?
- ¿Anotaste la versión de Volatility y los plugins usados?
- ¿Cada hallazgo de memoria está relacionado con otra fuente (logs, disco, red)?
