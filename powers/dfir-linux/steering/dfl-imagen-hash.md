# DFIR en Linux: imagen, hash, montaje y recuperación

> Guía de steering del power **dfir-linux**, derivada de *Linux File Systems* y *Linux File System Forensics* (HTB, secciones 4–5). Detalle en `references/sistemas-archivos.md`.
>
> **Encuadre:** la imagen se toma de discos propios o autorizados. El original no se monta en escritura ni se analiza directamente.

## Flujo

```
1. Identificar el dispositivo   → lsblk -f, df -hT, fdisk -l
2. Hash del original            → sha256sum /dev/sdX (si es posible)
3. Imagen                       → dc3dd (hash integrado) o dd
4. Hash de la imagen            → debe coincidir con el original
5. Cadena de custodia           → custodia.md
6. Copia de trabajo             → se analiza la copia, la imagen maestra queda intacta
7. Montaje de solo lectura      → ro,loop,noload,noexec,nodev
8. Análisis y recuperación      → TSK, ext3grep, foremost, PhotoRec, Autopsy
```

## Paso 3: crear la imagen

Preferido, con hash durante la copia:

```bash
sudo dc3dd if=/dev/sdb1 of=/mnt/evidencia/caso01/disco/sdb1.dd hash=sha256 log=/mnt/evidencia/caso01/disco/sdb1.log
```

Con `dd`:

```bash
sudo dd if=/dev/sdb1 of=/mnt/evidencia/caso01/disco/sdb1.dd bs=4M conv=noerror,sync status=progress
sha256sum /dev/sdb1 /mnt/evidencia/caso01/disco/sdb1.dd
```

Si el sistema está en uso, copiar el disco en vivo produce una imagen inconsistente. Documéntalo o, si el caso lo permite, toma la imagen con el sistema apagado desde un medio de arranque forense, después de haber recolectado la memoria.

## Paso 5: registro de cadena de custodia

| Campo | Ejemplo |
|---|---|
| ID de evidencia | CASO01-EV002 |
| Descripción | Imagen de `/dev/sdb1` del host `web01` |
| Herramienta y versión | dc3dd 7.2 |
| SHA-256 | `…` |
| Fecha y hora (UTC) | 2026-11-05 18:42:10 |
| Entregó / Recibió | Analista A / Analista B |
| Propósito | Análisis de sistema de archivos |
| Ubicación | `evidencia/caso01/disco/` |

## Paso 7: montar

```bash
sudo mkdir -p /mnt/image
sudo mount -o ro,loop,noload,noexec,nodev /mnt/evidencia/caso01/disco/sdb1.dd /mnt/image
```

- `noload` evita que EXT3/EXT4 reproduzca el journal y escriba en la imagen.
- `noexec` y `nodev` evitan ejecutar binarios o usar dispositivos de la imagen.
- Imagen de disco completo: `mmls imagen.dd`, y monta con `offset=$((sector_inicio * 512))`.

Al terminar: `umount /mnt/image` y vuelve a calcular el SHA-256 de la imagen para demostrar que no cambió.

## Paso 8: recuperar archivos borrados

| Situación | Herramienta |
|---|---|
| EXT3 con nombres aún en el journal | `ext3grep --dump-name` y `--restore-all` |
| Cualquier sistema soportado por TSK, con inodo disponible | `fls -r -d` + `icat` |
| Sin metadatos, solo contenido | `foremost`, `photorec` (carving por firma) |
| Revisión gráfica | Autopsy (`dfl-autopsy.md`) |

Restaura siempre en un directorio distinto de la imagen y calcula el hash de cada archivo recuperado.

## Línea de tiempo del sistema de archivos

```bash
fls -r -m / /mnt/evidencia/caso01/disco/sdb1.dd > body.txt
mactime -b body.txt -d -z UTC 2026-11-01..2026-11-06 > timeline.csv
```

Columnas MACB: **M**odificación, **A**cceso, **C**ambio de metadatos, **B**irth (creación). Filtra la ventana del incidente y busca ráfagas de cambios.

## Equivalente en AWS: snapshot EBS

1. Antes de detener la instancia, vuelca la memoria (AVML) a un bucket o volumen de evidencia.
2. Crea el snapshot, etiquetado con el caso:
   ```bash
   aws ec2 create-snapshot --volume-id vol-0123456789abcdef0 \
     --description "Caso01 - web01 root" \
     --tag-specifications 'ResourceType=snapshot,Tags=[{Key=CaseId,Value=Caso01}]'
   ```
3. Crea un volumen desde el snapshot en la misma zona que la instancia forense y adjúntalo:
   ```bash
   aws ec2 create-volume --snapshot-id snap-0abc... --availability-zone us-east-1a \
     --tag-specifications 'ResourceType=volume,Tags=[{Key=CaseId,Value=Caso01}]'
   aws ec2 attach-volume --volume-id vol-0def... --instance-id i-0forense... --device /dev/sdf
   ```
4. En la instancia forense (aislada, sin acceso a Internet), el volumen suele aparecer como `/dev/nvme1n1` en instancias Nitro. Calcula su hash y móntalo con `ro,noload,noexec,nodev`.
5. Guarda la evidencia en un bucket S3 con Object Lock y versionado.

## Preguntas de control

- ¿El hash de la imagen coincide con el del original? ¿Y después del análisis?
- ¿Montaste siempre en solo lectura con `noload`?
- ¿Los archivos recuperados están fuera de la imagen y con hash?
- ¿La cadena de custodia tiene una entrada por cada traspaso?
