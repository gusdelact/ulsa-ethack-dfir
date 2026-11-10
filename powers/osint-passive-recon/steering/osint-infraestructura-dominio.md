# OSINT: dominio, registros públicos y estructura

> Steering del power **osint-passive-recon**. Cubre la categoría **Infrastructure** en su parte de
> dominio: Domain Information, Public Domain Records y Domain Structure. Es la parte mejor cubierta
> por las herramientas MCP del power.

## Domain Information

De lo general a lo detallado, en tres categorías: **registros públicos**, **terceros** y
**dominios** (SLD + TLD). El código público (GitHub, GitLab) puede filtrar IPs, hostnames,
configuraciones o credenciales: `search_github(query="<dominio>")`.

> **Terceros** (hosting, CDN, cloud): aparecen en los registros, pero probar sus sistemas requiere
> permiso explícito del proveedor. Ver `osint-cloud-terceros.md`.

## Public Domain Records

Cuatro componentes a obtener: **1) netblocks/CIDR, 2) ASN, 3) servidores DNS, 4) servidores de
correo**.

| Comando típico | Equivalente MCP en este power | Qué responde |
|---|---|---|
| `whois <dominio>` / ICANN lookup | `search_rdap(domain=...)`; si el TLD no tiene RDAP, `search_whois(domain=...)` o `whois_lookup(query=...)` | Registrador, fechas, NS, Registry Domain ID |
| `host www.<dominio>` | `search_dns(domain="www.<dominio>")` o `dns_lookup(name="www.<dominio>", types=["A","AAAA"])` | IP del servidor web |
| `whois <ip>` | `whois_lookup(query="<ip>")` | Rango/CIDR, organización, OriginAS |
| ASN y proveedor | `search_ip(ip="<ip>")` (ipinfo.io) | ASN, organización, hostname, ubicación |
| `whois AS<n>` | `whois_lookup(query="AS<n>")` | Titular del sistema autónomo |
| `dig any <dominio>` | `search_dns(domain=...)` + `dns_lookup(name=..., types=["A","AAAA","MX","NS","TXT","SOA","CAA"])` | Registros publicados y alertas SPF/DMARC |
| PTR (DNS inverso) | `dns_lookup(name="<ip>")` | Nombre inverso de la IP |
| MXToolbox (open relay) | **Fuera de alcance**: probar un relay es contacto activo | — |

### Cómo leer los registros DNS

| Registro | Qué revela |
|---|---|
| **A / AAAA** | IP del (sub)dominio. Pasarla por `search_ip` y `whois_lookup` para el netblock. |
| **MX** | Servidores de correo. Si es Google o Microsoft, el correo está en un tercero. |
| **NS** | Proveedor DNS/hosting. **Contrástalo con los NS de RDAP** (ver "NS del registro frente a NS de la zona"). |
| **TXT** | Claves de verificación de terceros (Atlassian, Google, MS=, Mailgun...) y SPF/DMARC. **Muy valioso.** |
| **SOA** | Contacto administrativo (el primer `.` del rname es `@`) y, a veces, otros dominios relacionados. |
| **CAA** | Qué autoridades de certificación están autorizadas. |

**Pistas de infraestructura en TXT:** Atlassian (Confluence/Jira), Google (Workspace, posibles
GDrive compartidos), Microsoft `MS=` (Office 365, OneDrive, Azure storage), Mailgun (APIs de
correo), LogMeIn (acceso remoto). En SPF aparecen a veces **IPs internas** (`ip4:10.x.x.x`):
anótalas.

**SPF / DMARC.** `search_dns` señala SPF ausente o permisivo (`+all`, `?all`) y DMARC ausente o con
`p=none`. Son **indicadores de exposición**, no vulnerabilidades confirmadas. DKIM no se revisa:
sondear selectores es activo.

> **No repitas la alerta de la herramienta sin interpretarla.** El aviso "No SPF record found —
> anyone can spoof email" de `search_dns` es genérico: solo mira SPF. La protección contra
> suplantación la decide **DMARC**, que pasa si SPF **o** DKIM pasan y están alineados con el dominio
> del `From:`. Interpreta SPF y DMARC **juntos** con esta tabla:

| SPF | DMARC | Lectura correcta |
|---|---|---|
| Ausente o permisivo | Ausente o `p=none` | Suplantación posible: los receptores no tienen política que aplicar. **Indicador alto.** |
| Ausente | `p=quarantine` / `p=reject` | Todo correo con `From: @dominio` falla DMARC (sin SPF y, salvo evidencia de DKIM, sin firma) → los receptores que aplican DMARC lo mandan a spam o lo rechazan. La suplantación queda **mitigada**; el efecto secundario es que **el correo legítimo del dominio tampoco pasaría**. Típico de un dominio que **no envía correo** ("parked"). |
| Estricto (`-all`) | `p=reject` | Postura fuerte. Lo que quede es fuera del alcance de OSINT (DKIM, receptores que no aplican DMARC). |
| Cualquiera | `pct<100` | La política solo se aplica a ese porcentaje: anótalo. |

Además, cruza con **MX**: un MX que no resuelve (NXDOMAIN) significa que el dominio no recibe correo
(y que los `rua`/`ruf` de DMARC hacia ese dominio no llegan). Sin MX funcional, SPF ausente y DMARC
`p=reject`, la conclusión coherente es "dominio que no usa correo", no "dominio suplantable".

### NS del registro frente a NS de la zona

Hay **dos fuentes de nameservers** y no siempre coinciden:

| Fuente | Herramienta | Qué es |
|---|---|---|
| **Delegación** (registro del TLD) | `search_rdap` / `search_whois` → "Name servers" | Los NS que el registro publica para el dominio. **Son los autoritativos**: a ellos van los resolvers. |
| **Registros NS dentro de la zona** | `search_dns` / `dns_lookup` → NS | Lo que la zona dice de sí misma. Lo sirven los NS delegados. |
| **SOA** | `search_dns` / `dns_lookup` → SOA | El `mname` suele ser el primario del proveedor que sirve la zona hoy. |

Reglas de lectura:

1. **Si RDAP y la zona coinciden**, la delegación es coherente.
2. **Si no coinciden**, manda la **delegación de RDAP**. Si el SOA coincide con los NS de RDAP (p. ej.
   ambos en `awsdns-*` = Route 53), ese proveedor es el **actual**. Los NS de la zona que no aparecen
   en RDAP son una **inconsistencia de configuración** ("lame" o sobrantes), no el proveedor real.
3. **No llames "residual" o "histórico" al dato que coincide con el registro.** "Histórico" solo se
   usa con evidencia fechada (un snapshot, un certificado antiguo).
4. Escribe la conclusión como **inferencia** y cita ambas salidas (RDAP y DNS).

Ejemplo: RDAP lista `ns-161.awsdns-20.com` y otros tres de Route 53; la zona publica NS
`ns1.<dominio>` y `ns2.<dominio>`; el SOA es `ns-161.awsdns-20.com`. Lectura: la zona la sirve
**Route 53** (hecho: RDAP + SOA); los NS internos `ns1`/`ns2` no están delegados (inferencia:
registros NS sobrantes o de una configuración anterior, sin fecha que lo confirme).

## Domain Structure

Técnicas de descubrimiento de subdominios. **Solo las cuatro primeras son pasivas**:

| # | Técnica | ¿Pasiva? | En este power |
|---|---|---|---|
| 1 | Certificate Transparency | ✅ | `crtsh_certificate_search(domain=..., include_expired=true)` |
| 2 | Forward DNS datasets (Rapid7 Sonar) | ✅ | Fuera del power (dataset de >30 GB) |
| 3 | Web search | ✅ | `generate_dorks` + dork propuesto `site:*.<dominio> -site:www.<dominio>` |
| 4 | Disclosure / leak | ✅ | `wayback_snapshots(url=..., match="domain")`, `search_paste` |
| 5 | Subdomain brute-forcing | ❌ | **Prohibido** |
| 6 | Zone transfer (AXFR) | ❌ | **Prohibido** (`dnsrecon` apagado) |

### Ciclo de subdominios

```text
crtsh_certificate_search(domain)  ─┐
wayback_snapshots(match="domain") ─┼─▶ lista de nombres únicos
                                   │
                                   ▼
        para cada nombre: search_dns / dns_lookup ─▶ IP
                                   │
                                   ▼
        solo IPs del propio objetivo: search_ip + whois_lookup ─▶ ASN / netblock / proveedor
```

- **Filtrar terceros:** un subdominio que resuelve a un CDN o SaaS no es infraestructura propia.
- **vHosts:** dos o más subdominios en la misma IP sugieren hosting virtual.
- **Nombres que ya no resuelven** (solo en Wayback o en certificados viejos) son huella histórica:
  documéntalos como tal, no como activos vivos.
- **Un subdominio ausente de crt.sh no prueba que no tenga TLS.** Antes de concluir nada, revisa la
  salida cruda de `crtsh_certificate_search`:
  1. ¿Hay un **comodín** `*.<dominio>`? Si lo hay, cubre `blog.`, `support.`, etc. sin nombrarlos.
  2. ¿El número de certificados es muy superior al de hostnames? Muchos certificados con pocos
     nombres suelen ser **renovaciones** (p. ej. Let's Encrypt cada 90 días) del mismo par de nombres.
  3. ¿Hay certificados de **otro dominio** (un SAN compartido o el del proveedor) que cubran el host?
  Solo si descartas los tres, la lectura "probablemente sin certificado público propio" es una
  **hipótesis**, no un hecho. Ver la web en `http://` en Wayback no prueba que hoy no haya HTTPS.
- Shodan, VirusTotal, Censys, SecurityTrails y C99 son otras fuentes de subdominios conocidas, pero
  en este power están apagadas o fuera de alcance porque piden llave.

## Documentar

Tabla de infraestructura: nombre → IP → ASN/organización → proveedor → fuente (herramienta +
argumentos) → estado (vivo / histórico / tercero). Guardar cada salida cruda en
`evidencia/osint/` (ver `osint-intelligence-reporte.md`).

## Preguntas de autoevaluación (sin respuestas)

- ¿Cuántos nameservers tiene el dominio?, FQDN del servidor de correo, Registry Domain ID,
  registrador y contenido del TXT (Public Domain Records).
- Versión del servidor web, proveedor de hosting, ASN, SO del servidor y número de recursos JS
  (Domain Structure / Technologies in Use). Algunas requieren fuentes con llave (p. ej. Shodan) o la
  web en vivo: indica cuáles **no** puedes responder con las herramientas del power.
