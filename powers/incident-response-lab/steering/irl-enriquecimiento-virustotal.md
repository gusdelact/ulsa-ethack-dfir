# Enriquecimiento con VirusTotal

Antes de consultar: aplicar R-LAB3 (el indicador se revela a VirusTotal) y R-LAB4 (cuota). Agrupar
los indicadores y consultar cada uno **una sola vez**; guardar el resultado en `04-iocs.md`.

## IP

1. `get_ip_report` con `ip`. Mirar:
   - Detecciones (malicious / suspicious / harmless).
   - AS, ASN y país.
   - **WHOIS:** el servidor muestra solo líneas que empiezan con `Organization:`, `OrgName:`, `Country:`, `City:`, `Address:`, `RegDate:`, `NetName:`, `NetType:`, `Comment:`. Si el registro regional usa otro formato (p. ej. minúsculas) y falta un dato, revisarlo en la pestaña **Details → Whois Lookup** de la web de VirusTotal.
   - Relaciones incluidas en el reporte.
2. Para pivotear, `get_ip_relationship` con `relationship`:

| Relación | Responde |
|---|---|
| `referrer_files` | Archivos que contienen o refieren esta IP (en la web: *Files Referring*) |
| `communicating_files` | Archivos que se conectaron a esta IP en sandbox |
| `downloaded_files` | Archivos descargados desde esta IP |
| `resolutions` | Dominios que resolvieron a esta IP |
| `urls` | URLs alojadas en esta IP |
| `historical_whois` | Cambios de registro |

## Dominio

`get_domain_report` (opcional `relationships: ["resolutions","subdomains"]`) y
`get_domain_relationship` (`subdomains`, `resolutions`, `communicating_files`, `referrer_files`,
`historical_whois`, …).

## Hash

1. `get_file_report` con `hash` (MD5, SHA-1 o SHA-256): detecciones, nombres conocidos, tipo, firma, primera vez visto.
2. `get_file_behaviour_summary`: procesos, archivos, registro y red observados en sandbox.
3. `get_file_relationship`: `contacted_ips`, `contacted_domains`, `contacted_urls`, `dropped_files`, `execution_parents`.

## URL

`get_url_report` **envía la URL a escanear** si no está en caché. No usar con URLs internas o con
tokens en la query string. Preferir `search_vt` con la URL si solo se quiere saber si existe.

## Cómo interpretar

| Resultado | Lectura |
|---|---|
| Muchas detecciones | Indicador conocido como malicioso: **hecho** que VT lo reporta; inferencia que es malicioso en nuestro caso. |
| 0 detecciones | **No** prueba que sea benigno; puede ser infraestructura nueva o dedicada al objetivo. |
| IP de nube o CDN | Puede ser compartida; bloquearla puede afectar servicios legítimos. |
| Archivos relacionados con nombres de herramientas | Pista de qué malware usa la infraestructura. |

## Registro

En `04-iocs.md`, columna *Contexto*: `VT <fecha>: <det>/<total>, AS<n> <org>, <país/ciudad>`.
En el caso: comentario con la plantilla de `irl-triage-thehive.md` (paso 7).
