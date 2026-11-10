# OSINT: Leaks (archivos, filtraciones internas y breaches)

> Steering del power **osint-passive-recon**. Cubre la categoría **Leaks**: tipos de filtración,
> Archives, Internal Leaks (metadatos) y Breaches.

## Tipos de leak

Un leak divulga información que no estaba destinada al público:

- **Accidental** (*information disclosure*): descuido, p. ej. credenciales comentadas en código.
- **Intencional**: un whistleblower o atacante expone datos a propósito.
- **Forzado**: extorsión o malware ("paga o publicamos"). Aquí entra DFIR.

Se buscan en tres campos: **Archives**, **Internal Leaks** y **Breaches**.

## Archives

### Wayback Machine

`wayback_snapshots` consulta el índice CDX de web.archive.org. No toca al objetivo.

```text
wayback_snapshots(url="<dominio>", match="domain", limit=50)            # todo el dominio y subdominios
wayback_snapshots(url="<dominio>/robots.txt", match="exact")            # carpetas que querían ocultar
wayback_snapshots(url="<dominio>/wp-content/", match="prefix", limit=100)
wayback_snapshots(url="<dominio>", match="host", from="2019", to="2021") # comparar épocas
```

- `robots.txt` histórico revela carpetas que el sitio no quería indexar.
- Contenido eliminado: páginas de equipo, correos antiguos, documentos retirados.
- Comparar capturas de distintos años muestra cambios de tecnología o de proveedores.
- **No usar "Save Page Now"**: hace que Internet Archive visite al objetivo. El power no lo expone.
- Abrir un snapshot (`web.archive.org/web/<ts>/<url>`) es pasivo: lo sirve el archivo, no el
  objetivo. Lo hace el humano en su Resource Browser.

### Pastebin

`search_paste(query="<dominio o empresa>")` busca en volcados de Pastebin indexados por psbdmp.ws.
Como alternativa manual, el dork `site:pastebin.com "<dominio>"`.

> Si aparece una credencial o un dato personal en un paste, se documenta **la existencia** (URL,
> fecha, tipo de dato) con el valor **ofuscado**. Nunca se prueba la credencial.

## Internal Leaks: metadatos

Casi todo archivo (PDF, DOCX, imágenes) guarda metadatos al editarse: aplicación y versión, SO,
autor, empresa, fechas e incluso coordenadas GPS.

**Flujo con el power:**

1. El humano encuentra el documento público (dork `filetype:pdf site:<dominio>` o Wayback).
2. Lo descarga con `wget` o `curl` (no con el navegador, que puede alterar el archivo) dentro del
   workspace:

   ```bash
   mkdir -p evidencia/osint/archivos
   wget "https://<url-publica>/informe.pdf" -O evidencia/osint/archivos/informe.pdf
   shasum -a 256 evidencia/osint/archivos/informe.pdf >> evidencia/osint/archivos/SHA256SUMS
   ```

3. El agente lo analiza: `osint-toolbox::exiftool_metadata(file_path="<ruta absoluta>")`.

| Campo | Qué sugiere |
|---|---|
| `Author`, `Last Modified By` | Nombres de usuario y formato de cuentas |
| `Creator Tool`, `Producer` | Software y versión (p. ej. "Acrobat PDFMaker 10.1 for Word") |
| `Company` | Nombre interno de la organización o tenant |
| `Create Date`, `Modify Date` | Antigüedad del documento y del software |
| GPS (imágenes) | Ubicación donde se tomó la foto |

- `exiftool_metadata` lee **archivos locales**: pasa solo rutas dentro de la carpeta de evidencia
  del lab, nunca rutas personales del equipo.
- Otras fuentes de leaks internos: calendarios públicos, código en GitHub/GitLab con secretos
  olvidados (`search_github`).

## Breaches

Documentación de filtraciones ya existentes (p. ej. Collection #1-5: ~773 M de correos únicos y
~1 160 M de combinaciones correo+contraseña).

| Fuente | En este power |
|---|---|
| HaveIBeenPwned | **Apagado** (`search_breach` requiere llave). Consulta manual solo con correos propios o del lab |
| Listas de contraseñas filtradas | **Fuera de alcance**: descargar o usar credenciales filtradas no es OSINT pasivo |
| CVE Details, Exploit-DB, NVD | Consulta manual para relacionar una versión inferida con CVEs **posibles** |

- **0-day:** vulnerabilidad pública sin parche. **N-day:** el parche existe pero el objetivo no lo
  aplicó.
- Un breach que menciona al dominio es un hallazgo de **exposición**: indica la fuente y la fecha,
  no los datos.

## Preguntas de autoevaluación (sin respuestas)

- A partir de un documento público, ¿qué información adicional revelan sus metadatos (autor,
  software, rutas, GPS)? (Internal Leaks).
