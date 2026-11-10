# OSINT: referencia de herramientas MCP, guardrails y errores comunes

> Steering del power **osint-passive-recon** (transversal). Detalla los argumentos de cada
> herramienta, qué está apagado y por qué, cómo verificar los servidores sin LLM y cómo resolver
> los fallos frecuentes.

## Servidor `openosint` (`openosint==2.36.1`)

En modo pasivo (sin `--allow-active`) el servidor no lista las herramientas que tocan al objetivo
(`search_email`, `search_username`, `search_domain`, `search_phone`, `scrape_url`). De las que
quedan, `mcp.json` oculta las que piden llave, un extra o un agente propio.

| Herramienta | Argumentos | A quién consulta | Nota |
|---|---|---|---|
| `search_rdap` | `domain` | Servidor RDAP del TLD (bootstrap IANA) | Algunos ccTLD (p. ej. `.mx`) no tienen RDAP: usar `search_whois` |
| `search_whois` | `domain` | Servidor WHOIS del registro | |
| `search_dns` | `domain` | Resolver del sistema | A/AAAA/MX/NS/TXT/SOA + alertas SPF/DMARC; DKIM solo en modo activo |
| `search_ip` | `ip` | ipinfo.io | ASN, organización, hostname, ubicación; sin token tiene cuota |
| `generate_dorks` | `target` | Nada (local) | 12 plantillas de Google; las abre el humano |
| `search_github` | `query` | API de GitHub | 60 peticiones/hora por IP sin token |
| `search_paste` | `query` | psbdmp.ws | Volcados de Pastebin indexados |

**Ocultas en `mcp.json`:** `search_breach`, `search_shodan`, `search_virustotal`, `search_censys`,
`search_ip2location`, `search_abuseipdb`, `search_dorks_live` y `search_footprint` (piden llave;
`search_dorks_live` además ejecuta los dorks de forma automatizada); `graph_export`,
`graph_neighbors`, `graph_review_candidates` (piden un extra o una base local vacía);
`investigate_multi` (lanza un agente propio con LLM); `search_gdelt_geo` (descarga horas de
noticias en la primera llamada).

## Servidor `osint-toolbox` (`osint-toolbox-mcp@1.1.0`)

Las CLIs externas apuntan a `/nonexistent/disabled` en `env`, así el servidor no las detecta aunque
el equipo las tenga instaladas (p. ej. Kali). Quedan sus herramientas integradas:

| Herramienta | Argumentos | A quién consulta | Nota |
|---|---|---|---|
| `crtsh_certificate_search` | `domain`, `include_expired` (def. `true`) | crt.sh | Hostnames y correos en certificados; crt.sh falla a menudo con HTTP 502 |
| `wayback_snapshots` | `url`, `match` (`exact`/`prefix`/`host`/`domain`), `limit` (1–1000, def. 50), `from`, `to` | CDX de web.archive.org | Más recientes primero |
| `whois_lookup` | `query` (dominio, IP, CIDR o `AS<n>`) | rdap.org o WHOIS | Cross-check de `search_rdap`; además sirve para IPs y ASN |
| `dns_lookup` | `name` (dominio, o IP para PTR), `types` | DoH de Cloudflare/Google | Cross-check independiente de `search_dns`; incluye CAA |
| `exiftool_metadata` | `file_path` (ruta absoluta) | Nada (archivo local) | Solo aparece si ExifTool está instalado; usar solo rutas de `evidencia/` |

**Oculta:** `osint_toolbox_status` (sugiere `--install`; nunca aprobar instalaciones en un ejercicio).

## Tres capas de guardrail

| Capa | Mecanismo | Qué evita |
|---|---|---|
| Servidor | OpenOSINT en modo pasivo: las herramientas activas no se listan y `call_tool` las rechaza | Que el agente vea herramientas que tocan al objetivo |
| Entorno | Variables `OSINT_*=/nonexistent/disabled` del toolbox | Sherlock, Maigret, dnsrecon (AXFR), SpiderFoot, theHarvester, etc. |
| Host | `disabledTools` de Kiro y aprobación manual (sin `autoApprove`) | Herramientas inútiles sin llave y llamadas no revisadas |

Las anotaciones MCP (`readOnlyHint: true`) las declara el propio servidor: "solo lectura" no
significa "pasivo", así que no sirven para imponer el alcance.

## Verificar los servidores sin LLM

```bash
# Calentar caché (primer arranque lento de OpenOSINT)
uvx --python 3.12 --from openosint==2.36.1 openosint-mcp --help

# Toolbox con las mismas variables del power: solo deben quedar "ok" las integradas (y ExifTool)
D=/nonexistent/disabled
env OSINT_SHERLOCK=$D OSINT_MAIGRET=$D OSINT_HOLEHE=$D OSINT_GHUNT=$D OSINT_THEHARVESTER=$D \
    OSINT_SUBFINDER=$D OSINT_DNSTWIST=$D OSINT_DNSRECON=$D OSINT_PHONEINFOGA=$D \
    OSINT_SPIDERFOOT_DIR=$D OSINT_BLACKBIRD_DIR=$D uvx osint-toolbox-mcp@1.1.0 --check

# Opcional (Node 22.19+): listar y llamar herramientas con el MCP Inspector
npx -y @modelcontextprotocol/inspector --cli uvx --python 3.12 --from openosint==2.36.1 openosint-mcp -- --method tools/list
npx -y @modelcontextprotocol/inspector --cli uvx --python 3.12 --from openosint==2.36.1 openosint-mcp -- \
  --method tools/call --tool-name search_rdap --tool-arg domain=example.com
```

El Inspector no aplica `disabledTools` (es una función de Kiro), así que muestra más herramientas
que las que ve el agente. Esa diferencia demuestra el filtro del host.

## Errores comunes y soluciones

### `crt.sh answered HTTP 502`
**Causa:** el servicio público de crt.sh está sobrecargado; ocurre con frecuencia.
**Solución:** reintentar 1–2 veces con unos minutos de diferencia. Si sigue fallando, registrarlo
como pendiente en el informe. Nunca inventar subdominios.

### `No RDAP server found for TLD '.xx' in the IANA bootstrap registry`
**Causa:** no todos los ccTLD tienen RDAP delegado (p. ej. `.mx`).
**Solución:** `openosint::search_whois(domain=...)` o `osint-toolbox::whois_lookup(query=...)`.

### `Unknown tool_id "...::whois_lookup"` / "herramienta diferida no cargada"
**Causa:** no es una caída de red ni un problema del servidor. El host (Kiro) dejó esa herramienta
en su **catálogo diferido**: existe y está conectada, pero hay que **cargarla** antes de poder
llamarla. `whois_lookup` y `dns_lookup` del toolbox no requieren ningún binario externo, así que si
aparecen como "no disponibles" casi siempre es esto, no una ausencia real.
**Solución:** cargar la herramienta por su id exacto y volver a intentar la llamada. **No** marcarla
como pendiente sin antes cargarla: eso confunde una herramienta disponible con una fuente caída.
**Si no aparece ni en el catálogo diferido**, revisa `disabledTools` en `.kiro/settings/mcp.json` del
workspace y en `~/.kiro/settings/mcp.json`: un servidor con el mismo nombre configurado ahí pisa la
configuración del power. En ese caso es una decisión de configuración, no un fallo, y se documenta así.
**Distinguir del caso real:** una herramienta diferida se resuelve cargándola (el dato sí es
obtenible); crt.sh (HTTP 502) y `search_paste` (no resuelve `psbdmp.ws`) son **caídas de red** que sí
se documentan como pendientes. Antes de escribir "pendiente", clasifica cuál de los dos casos es.

### El agente usa la búsqueda web integrada del host
**Causa:** Kiro tiene herramientas web propias que el modelo puede preferir.
**Solución:** pedir "usa solo las herramientas MCP de openosint y osint-toolbox" en el prompt o en
un steering del workspace, o usar un agente sin herramientas web.

### Primer arranque de OpenOSINT muy lento o con timeout
**Causa:** ~20 dependencias directas que `uvx` descarga la primera vez.
**Solución:** calentar la caché antes de la sesión (comando de arriba).

### Kiro no encuentra `uvx`
**Causa:** las apps gráficas a veces arrancan con un PATH reducido.
**Solución:** poner en `command` la ruta absoluta que devuelve `which uvx`.

### `search_dns` no informa sobre DKIM
**Causa:** sondear selectores DKIM es enumeración activa; OpenOSINT solo lo hace con
`--allow-active`.
**Solución:** dejar DKIM como "fuera de alcance pasivo" en el informe.

### `search_github` devuelve error de límite
**Causa:** 60 peticiones/hora por IP sin token; en un aula todos comparten IP.
**Solución:** usarla con moderación y documentar el límite como pendiente.

### `exiftool_metadata` no aparece
**Causa:** ExifTool no está instalado o no está en el PATH del proceso.
**Solución:** instalarlo (`brew install exiftool` / `sudo apt install exiftool`) y reconectar el
servidor desde el panel MCP.

### Sin salida de herramienta, el agente "completa" con su memoria
**Causa:** el modelo rellena huecos con conocimiento previo.
**Solución:** exigir en el prompt que cada hallazgo cite la herramienta y los argumentos; revisar el
informe contra los archivos de `evidencia/osint/.../herramientas/`.
