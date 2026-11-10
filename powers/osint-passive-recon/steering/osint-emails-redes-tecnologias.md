# OSINT: correos, redes mixtas y tecnologías

> Steering del power **osint-passive-recon**. Cubre tres subcategorías de **Infrastructure**: Email
> Addresses, Compounded Networks y Technologies in Use.

## Email Addresses

Lo que interesa es el **formato** (`nombre.apellido@dominio`, `inicialapellido@dominio`, alias por
rol como `soporte@`) y los **dominios alternativos** o abreviados de la empresa.

| Técnica | En este power |
|---|---|
| theHarvester (múltiples fuentes) | **Apagado** (la CLI apunta a `/nonexistent/disabled`) |
| Hunter.io, RocketReach | Fuera del power (cuenta o llave) |
| Emailrep.io (spoofable, SPF/DMARC) | Fuera del power; SPF/DMARC salen de `search_dns` |
| h8mail, HaveIBeenPwned | **Apagados** (`search_breach` requiere llave de HIBP) |
| Correos en certificados TLS | `crtsh_certificate_search` |
| Correos en commits públicos | `search_github` |
| Correos antiguos en la web | `wayback_snapshots(url="<dominio>/contact", match="prefix")` |
| Dorks | Propuestos: `intext:"@<dominio>"`, `intext:"@<dominio>" inurl:linkedin.com` |

> **Correos y personas reales:** no se verifica si un correo existe (eso contacta al servidor de
> correo) ni se buscan sus contraseñas. En el lab solo se documentan correos de identidades
> sintéticas. Un correo suplantable (SPF/DMARC débil) es un **indicador** de riesgo de phishing.

## Compounded Networks

Facebook, Instagram, X/Twitter: plataformas donde se mezcla lo personal y lo profesional. La gente
comparte opiniones (y a veces información sensible) porque se siente lejos de la empresa.

- Buscar por **hashtags** y combinar términos (`"<empresa>" Java "interfaz web"`).
- Revisar grupos, comentarios e imágenes. Las quejas de empleados son buenos indicadores de
  procesos rotos.
- En este power: `generate_dorks` produce las plantillas de X/Twitter, Facebook e Instagram; las
  abre el humano. No hay scraping de redes sociales.

## Technologies in Use

El stack tecnológico permite ajustar escenarios de ingeniería social y priorizar qué revisar en la
fase activa.

| Fuente | Herramienta | Qué revela |
|---|---|---|
| Rutas históricas | `wayback_snapshots(url=..., match="domain", limit=100)` | `wp-content/`, `wp-includes/`, `/administrator/` (Joomla), `/sites/default/` (Drupal), nombres de temas y plugins, `?ver=` con versiones |
| Registros TXT | `search_dns` | SaaS en uso (Atlassian, Google, Microsoft, Mailgun...) |
| Certificados | `crtsh_certificate_search` | Subdominios por producto (`jira.`, `vpn.`, `owa.`, `gitlab.`) |
| ASN / proveedor | `search_ip` | Hosting, CDN o WAF delante (Cloudflare, Akamai) |
| Código público | `search_github` | Lenguajes, frameworks, archivos de configuración |
| BuiltWith, Wappalyzer | Fuera del power (web, abierta por el humano) | CMS, plugins, analítica |
| Shodan | **Apagado** (requiere llave) | Banners y puertos ya indexados |

- Una **versión** inferida de una ruta archivada es una **hipótesis con fecha** (la del snapshot),
  no el estado actual. Indica siempre la fecha del snapshot.
- Una versión antigua no es una vulnerabilidad confirmada: se relaciona con CVEs públicas como
  **posible** riesgo, a validar en una fase autorizada.

## Preguntas de autoevaluación (sin respuestas)

- Formato de correo de la empresa y un correo de un directivo (Email Addresses).
- CMS y su versión, nombre del tema y WAF delante del sitio (Technologies in Use).
