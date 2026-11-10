# Autopsy en Linux (continuación, sección 7)

Autopsy es una plataforma de análisis forense de código abierto. Es la interfaz gráfica de **The Sleuth Kit (TSK)** y examina datos de computadoras, teléfonos y medios de almacenamiento.

## Capacidades

| Función | Uso |
|---|---|
| Varios sistemas de archivos | FAT, NTFS, HFS+, EXT. |
| Línea de tiempo | Visualiza cuándo ocurrieron los eventos. |
| Búsqueda por palabra clave | Texto en todo el conjunto de datos; consultas predefinidas para IP, tarjetas, fechas, SSN. |
| Historial del navegador | Navegación del usuario. |
| Correo | Recupera y analiza correos. |
| EXIF | Metadatos de fotos (fecha, ubicación). |
| Módulos | Extensiones de la comunidad. |

Aplicaciones: investigación de delitos informáticos, revisión de brechas (origen, datos afectados, cómo ocurrió), recuperación de datos, análisis de malware, amenazas internas y examen de evidencia para procesos legales.

## Flujo de trabajo

### 1. Instalar e iniciar

```bash
apt install autopsy
autopsy
# abrir http://localhost:9999/autopsy en el navegador
```

La versión de los repositorios de Linux es la 2.x (interfaz web sobre TSK). La 4.x es una aplicación de escritorio distinta.

### 2. Crear el caso

**New Case**: nombre del caso, nombre del analista, número de caso y directorio donde se guarda. Después, los datos del host.

### 3. Agregar la fuente de datos

La fuente puede ser una partición, una imagen de disco o una imagen de memoria. La imagen se obtiene antes, por ejemplo:

```bash
dd if=/dev/sdb1 of=/root/image.iso status=progress bs=8k
```

**Add Image**: ruta de la imagen, tipo (disco o partición), método de importación (enlace simbólico, copia o mover) y sistema de volúmenes.

### 4. Verificar el hash

Agrega el hash de la imagen (Autopsy 2.x usa MD5) para comprobar su integridad y que es la imagen correcta. Continúa solo si coincide. Registra también el SHA-256 en tu bitácora.

```bash
md5sum /root/image.iso
sha256sum /root/image.iso
```

### 5. Analizar (**ANALYZE**)

| Menú | Qué permite |
|---|---|
| **File Analysis** | Jerarquía de archivos, contenido, metadatos y actividad asociada; archivos borrados. |
| **Keyword Search** | Busca palabras o expresiones en toda la imagen (p. ej. `mimikatz`, una IP, un usuario). Muestra ubicación, texto y contexto. |
| **File Type** | Clasifica por tipo (imágenes, documentos, ejecutables). Usa **Sort Files by Type**. Detecta archivos cuya extensión no coincide con su firma. |
| **Image Details** | Detalles de la imagen; acceso a EXIF. |
| **Meta Data** | Timestamps (creación, modificación, acceso), dueño, permisos, inodos; espacio asignado y libre. |
| **Data Unit** | Datos crudos en hexadecimal o ASCII; útil para borrados y datos ocultos. |

### 6. Reportar

Exporta los hallazgos como reporte. Es un anexo del reporte forense, no el reporte en sí.

### 7. Cerrar el caso

Guarda los hallazgos y cierra el caso.

## Comandos de TSK equivalentes

Autopsy usa TSK por debajo. Para trabajar en terminal o automatizar:

```bash
mmls imagen.dd                 # tabla de particiones
fsstat -o <offset> imagen.dd   # info del sistema de archivos
fls -r -o <offset> imagen.dd   # listado recursivo (borrados marcados con *)
istat -o <offset> imagen.dd <inodo>
icat -o <offset> imagen.dd <inodo> > archivo
```
