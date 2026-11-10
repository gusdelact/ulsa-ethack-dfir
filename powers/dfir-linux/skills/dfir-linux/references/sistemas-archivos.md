# Sistemas de archivos y forense del sistema de archivos (Linux, secciones 4–5)

## Sistemas de archivos de Linux

| Sistema | Características | Implicación forense |
|---|---|---|
| **EXT2** | Simple, sin journaling. | Recuperación y análisis más difíciles. |
| **EXT3** | EXT2 con journaling. | El journal ayuda a rastrear cambios. Hay herramientas específicas como `ext3grep`. |
| **EXT4** | Sucesor de EXT3, archivos y discos grandes, más rápido. | Más capacidades de recuperación y análisis; guarda fecha de creación (`crtime`). |
| **XFS** | Diseñado para sistemas y archivos muy grandes. | Útil para grandes volúmenes de datos. |
| **Btrfs** | Snapshots, respaldo e integridad de datos. | Los snapshots permiten ver estados anteriores. |
| **ReiserFS** | Optimizado para muchos archivos pequeños. | En desuso. |

```bash
df -hT     # discos montados, tipo de sistema de archivos y uso
lsblk -f   # dispositivos de bloque, particiones y sistemas de archivos
```

## Imagen forense

El análisis empieza adquiriendo una imagen bit a bit del disco o partición. Así se preserva el original y se analiza sin modificarlo.

### `dd`

```bash
dd if=<origen> of=<destino> bs=<tamaño_bloque> status=progress
sudo dd if=/dev/sdb1 of=/ruta/disk_image.img bs=4M status=progress
```

| Parámetro | Significado |
|---|---|
| `if=` | Archivo de entrada: el origen (p. ej. una partición). |
| `of=` | Archivo de salida: donde se escribe la imagen. |
| `bs=` | Tamaño de bloque; `4M` suele acelerar la copia. |
| `status=progress` | Muestra el avance en tiempo real. |

Agrega `conv=noerror,sync` si el disco tiene sectores dañados: continúa ante errores y rellena con ceros para mantener los offsets.

### `dc3dd`

Versión de `dd` para forense: indicador de progreso, cálculo de hash durante la copia y escritura a varios destinos a la vez.

```bash
sudo dc3dd if=/dev/sdb1 of=/mnt/evidencia/caso01-sdb1.dd hash=sha256 log=/mnt/evidencia/caso01-sdb1.log
```

## Hashes

Un hash es una cadena calculada a partir de los datos: el mínimo cambio produce un valor completamente distinto. Si el hash de la imagen coincide con el del original, los datos no cambiaron.

| Algoritmo | Tamaño | Uso |
|---|---|---|
| MD5 | 128 bits | Rápido, pero con colisiones conocidas. Solo como complemento. |
| SHA-1 | 160 bits | Mejor que MD5, ya superado. |
| **SHA-256** | 256 bits | **El preferido hoy en forense.** |

```bash
md5sum disk_image.img
sha1sum disk_image.img
sha256sum disk_image.img
sha256sum /dev/sdb1          # hash del original para comparar
```

## Montar una imagen

Monta siempre en **solo lectura**.

```bash
sudo mkdir -p /mnt/image
sudo mount -o ro,loop /tmp/sda1.img /mnt/image
```

En EXT3/EXT4, `ro` por sí solo puede reproducir el journal y escribir en la imagen. Usa también `noload` y evita ejecutar binarios de la imagen:

```bash
sudo mount -o ro,loop,noload,noexec,nodev /ruta/imagen.dd /mnt/image
```

Si la imagen es de un disco completo (con tabla de particiones), busca el offset de la partición con `mmls imagen.dd` o `fdisk -l imagen.dd` y monta con `offset=<sector_inicio * 512>`.

## Recuperar archivos borrados

Al borrar un archivo, Linux no borra los datos de inmediato: marca el espacio como libre. Los datos pueden recuperarse mientras no se sobrescriban.

1. **Imagen:** trabaja siempre sobre una imagen (`dd`, `dc3dd`), no sobre el disco original.
2. **Herramienta:** The Sleuth Kit (TSK), TestDisk, PhotoRec, Foremost o herramientas específicas como `ext3grep`.
3. **Análisis:** la herramienta revisa las tablas del sistema de archivos y las marcas de asignación.
4. **Recuperación:** los archivos encontrados se restauran en una ubicación segura, distinta de la imagen.

### `ext3grep` (EXT3)

```bash
apt install ext3grep
dd if=/dev/sdb1 of=/root/forensic.dd status=progress bs=8k
ext3grep --dump-name forensic.dd     # lista los nombres de archivo en la imagen
ext3grep --restore-all forensic.dd   # restaura todo en ./RESTORED_FILES/
```

### The Sleuth Kit (cualquier EXT, XFS parcial)

```bash
fsstat imagen.dd                    # información del sistema de archivos
fls -r -d imagen.dd                 # entradas borradas, recursivo
icat imagen.dd <inodo> > recuperado # extrae el contenido de un inodo
fls -r -m / imagen.dd > body.txt    # bodyfile para línea de tiempo
mactime -b body.txt -d > timeline.csv
```

### Carving (sin metadatos)

```bash
foremost -i imagen.dd -o /mnt/evidencia/carving
photorec imagen.dd                  # interactivo
```
