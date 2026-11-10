# OSINT: almacenamiento cloud y terceros

> Steering del power **osint-passive-recon**. Cubre dos subcategorías de **Infrastructure**: Cloud
> Storage y Third Parties.

> **Regla de detención:** si encuentras un bucket, blob o servicio expuesto, **lo documentas y te
> detienes**. Listarlo, abrirlo o descargar su contenido ya es interacción y queda fuera de alcance.
> Adivinar nombres de buckets (brute-forcing) también está prohibido.

## Cloud Storage

| Proveedor | Almacenamiento | Patrón de URL a reconocer |
|---|---|---|
| AWS | S3 bucket | `<bucket>.s3.amazonaws.com`, `s3-<region>.amazonaws.com/<bucket>`, `s3-website-*` |
| Azure | Blob | `<cuenta>.blob.core.windows.net/<contenedor>` |
| GCP | Cloud Storage | `storage.googleapis.com/<bucket>`, `googleapis.com/storage/v1/b/<bucket>` |
| DigitalOcean | Spaces | `<bucket>.<region>.digitaloceanspaces.com` |

La gran mayoría de las exposiciones cloud son **misconfiguraciones** (ACLs, bucket policies, IAM,
bloqueo de acceso público), no fallos del proveedor.

### Descubrimiento pasivo con el power

| Fuente | Herramienta | Qué buscar |
|---|---|---|
| Registros DNS | `search_dns`, `dns_lookup` | CNAME o A apuntando a `amazonaws.com`, `windows.net`, `googleapis.com` |
| Certificados | `crtsh_certificate_search` | Subdominios tipo `assets.`, `cdn.`, `static.`, `files.` |
| Huella histórica | `wayback_snapshots(match="domain")` | URLs de imágenes, JS o PDFs servidas desde storage |
| Código público | `search_github(query="<empresa> s3")` | Nombres de buckets o claves en repos |
| Buscadores | Dorks propuestos: `site:s3.amazonaws.com "<empresa>"`, `site:blob.core.windows.net "<empresa>"` | Documentos indexados |
| GrayHatWarfare | Fuera del power (web, abierta por el humano) | Buckets ya indexados por terceros |

- Cualquiera puede crear un bucket con el nombre de la empresa: **verifica la pertenencia** (el
  nombre aparece en DNS del objetivo, en su web o en su código) antes de atribuirlo.
- Las empresas usan **abreviaturas** de su nombre en IT. Anótalas como hipótesis; no las pruebes.
- Riesgo crítico si aparece: **claves SSH privadas o credenciales** en un archivo público. Se
  documenta la ubicación y se avisa al docente; no se descarga ni se usa.

## Third Parties

Identificar proveedores externos (hosting, CDN, SaaS, correo) es trabajo manual a partir de NS, MX,
TXT, ASN y las tecnologías detectadas.

- `search_ip` devuelve la organización del ASN: si es AWS, Azure, Cloudflare o un hosting conocido,
  la IP pertenece a un tercero.
- Si el ASN pertenece al propio objetivo, probablemente es **self-hosted**.
- Para probar sistemas de un tercero hace falta su autorización (formularios de pentest de AWS,
  Azure, GCP, DigitalOcean) o que el cliente la consiga. En OSINT solo se **identifican**.
- Dorks propuestos para documentos en servicios de terceros: `site:docs.google.com "<empresa>"`,
  `site:storage.googleapis.com "<empresa>"`, `site:amazonaws.com "<empresa>"`.

## Documentar

Tabla de terceros: proveedor → servicio (DNS, correo, hosting, CDN, storage) → evidencia (registro
o salida + herramienta) → implicación (p. ej. "correo en Microsoft 365: posible OneDrive/SharePoint
compartidos"). Los recursos cloud expuestos van con su URL, fecha, cómo se encontraron y la nota
"no verificado: requiere autorización".

## Preguntas de autoevaluación (sin respuestas)

- Nombre del bucket de almacenamiento usado por la empresa (Cloud Storage).
- Proveedor cloud principal en el que se apoya la empresa (Third Parties).
