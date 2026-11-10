# OSINT: metodología y flujo de trabajo

> Guía de steering del power **osint-passive-recon**. Es el punto de partida: explica los
> principios de OSINT, la frontera legal pasivo/activo y el flujo por fases con las herramientas MCP
> del power. Las demás guías `osint-*.md` desarrollan cada categoría de información.
>
> **Encuadre:** solo se investigan objetivos autorizados (dominio de laboratorio, dominio propio o
> permiso por escrito). OSINT es **solo pasivo**: se consulta a terceros, nunca al objetivo.

## Qué es OSINT

OSINT es encontrar información **públicamente disponible** sobre una empresa o personas para
identificar eventos, dependencias internas y externas y conexiones. La palabra clave es
**Intelligence**: no basta con juntar datos sueltos, hay que **relacionarlos** hasta formar patrones
y perfiles del objetivo.

- Elegir herramientas es apenas **~10 %** del trabajo. Ninguna reemplaza el análisis manual: cada
  una depende de unas fuentes concretas y por eso está limitada.
- Definición operativa: información de fuentes públicas, obtenible por cualquiera sin
  restricciones, de forma legal y éticamente aceptable.

### La frontera legal (crítica)

OSINT usa fuentes públicas accesibles **sin registro ni autenticación** y **sin interactuar** con el
objetivo. Cualquier enumeración activa ya **no es OSINT** y puede violar el contrato o ser delito.

| Actividad | ¿OSINT? | En este power |
|---|---|---|
| Ver la web pública, "About Us", vacantes | Sí | La abre el humano en su navegador |
| Buscar empleados en redes sociales | Sí | `generate_dorks` arma la búsqueda; la abre el humano |
| Revisar logs de Certificate Transparency | Sí | `crtsh_certificate_search` |
| Archivos históricos (Wayback, Pastebin) | Sí | `wayback_snapshots`, `search_paste` |
| Terceros que **ya** recopilaron info del objetivo | Sí | RDAP/WHOIS, DNS público, `search_ip` |
| Metadatos de archivos **ya publicados** | Sí | `exiftool_metadata` sobre una copia local |
| Brute-forcing de subdominios o directorios | **No** | Fuera de alcance |
| Transferencia de zona (AXFR) | **No** | Fuera de alcance (`dnsrecon` apagado) |
| Terceros que **escanean por encargo** al objetivo | **No** | Fuera de alcance |
| Listar o abrir un bucket/servicio encontrado | **No** | Se documenta y se detiene |

> Ejemplo: encontrar un bucket S3 abierto **adivinando nombres** ya es una violación de contrato
> aunque nunca se abra. La regla mental es: no es "mirar sin tocar", es **"entender sin tocar"**.

## Metodología

OSINT se apoya en dos conceptos que dependen uno del otro:

- **Core Elements**, lo que buscamos: nombres y versiones de software, servidores, usuarios,
  hashes, URLs, contraseñas.
- **Information Resources**, de dónde lo sacamos: home page, archivos, redes sociales, buscadores,
  plataformas de desarrollo, fuentes de leaks.

Este power organiza la información en **tres grandes categorías**, cada una desarrollada en su guía
de steering:

| Company Information | Infrastructure | Leaks |
|---|---|---|
| Organization | Domain Information | Archives |
| Locations | Public Domain Records | Internal Leaks |
| Staff | Domain Structure | Breaches |
| Contact Information | Cloud Storage | |
| Business Records | Email Addresses | |
| Services | Third Parties | |
| Social Networks | Technologies in Use | |
| | Compounded Networks | |

### Principios

1. Trabajar en **ciclos**, de lo **general a lo detallado**. Cada dato nuevo abre otro ciclo (un
   subdominio nuevo de crt.sh se vuelve a pasar por DNS y Wayback).
2. **No hay orden fijo** de recursos. Es un flujo estructurado, no una receta paso a paso.
3. **Se adaptan los recursos a la metodología, no la metodología a los recursos.** Primero decides
   qué categoría investigas; después eliges la herramienta.

### Dos navegadores (trabajo del humano)

- **Research Browser**: solo para buscar. Historial limpio al empezar y exportado al final con
  *History Master* (timestamp, título, URL, query). Aquí se abren los dorks que genera el agente.
- **Resource Browser**: guarda lo encontrado con *SingleFile* (un `.html` autocontenido por
  página), que sirve de evidencia y de búsqueda offline.

```bash
csvtojson < history.csv | jq .                     # historial exportado -> JSON legible
cat *.html | html2text | grep "Nombre Apellido"     # buscar en las páginas guardadas
```

## Investigación de negocio: preguntas guía

- **Company Information:** ¿cuántos empleados?, ¿qué servicios ofrece?, ¿posición en el mercado?,
  ¿situación financiera?, ¿ubicaciones?, ¿seguridad física?, ¿reputación?
- **Staff:** ¿qué puestos y departamentos existen?, ¿de qué es responsable cada uno?, ¿qué
  dependencias tienen?
- **Infrastructure:** ¿cómo está montada la IT?, ¿quiénes son los admins?, ¿qué tecnologías usan?,
  ¿cuántos dominios?, ¿ASN y netblocks?, ¿certificados?, ¿terceros?, ¿servidores públicos?, ¿emails?

## Flujo recomendado por fases (OODA en cada paso)

Cada llamada a herramienta es un **Act**: antes decide la consulta que resuelve tu duda con menos
exposición; después vuelve a **Observe**, lee la salida cruda y separa hechos de inferencias.

| Fase | Pregunta | Herramienta MCP | Guía |
|---|---|---|---|
| 0. Alcance | ¿Qué objetivo está autorizado y para qué? | (ninguna; se declara por escrito) | este documento |
| 1. Registro | ¿Quién registró el dominio, cuándo, con quién? | `search_rdap` → `search_whois` / `whois_lookup` | `osint-infraestructura-dominio.md` |
| 2. DNS | ¿Qué registros publica? ¿SPF/DMARC? | `search_dns` + `dns_lookup` (cross-check) | `osint-infraestructura-dominio.md` |
| 3. Netblock / ASN | ¿Dónde está alojado? | `search_ip`, `whois_lookup(query=<ip>)` | `osint-infraestructura-dominio.md` |
| 4. Subdominios | ¿Qué nombres aparecen en certificados? | `crtsh_certificate_search` | `osint-infraestructura-dominio.md` |
| 5. Huella histórica | ¿Qué existió y ya no se ve? | `wayback_snapshots` | `osint-leaks.md` |
| 6. Empresa y personas | ¿Qué publican la empresa y su personal? | `generate_dorks`, `search_github` | `osint-company-information.md` |
| 7. Cloud y terceros | ¿Qué proveedores aparecen en DNS/TXT? | (inferencia sobre fases 2–5) | `osint-cloud-terceros.md` |
| 8. Leaks | ¿Hay volcados o documentos con metadatos? | `search_paste`, `exiftool_metadata` | `osint-leaks.md` |
| 9. Intelligence | ¿Cómo se conectan los hallazgos? | (análisis) | `osint-intelligence-reporte.md` |

Los subdominios nuevos de la fase 4 o 5 vuelven a la fase 2 (nuevo ciclo). Cada salida se guarda,
**una por llamada y sin editar**, en `evidencia/osint/<objetivo>-<fecha>/herramientas/` (ver
`osint-intelligence-reporte.md`).

### Modos de trabajo

Este flujo se recorre en uno de tres modos (detalle en `osint-modos-trabajo.md`):

- **Rápido:** el agente recorre la tabla de corrido y explica cada fase en una línea.
- **Guiado:** el alumno razona antes y después de cada fase (`osint-compuertas-aprendizaje.md`).
- **Spec:** el alumno planea la investigación en un Spec de Kiro antes de ejecutar
  (`osint-spec-investigacion.md`).

Si el humano no indica el modo, el agente lo pregunta **antes que nada**, antes incluso de la Fase 0
(ver "Al activar este power" en `POWER.md`). En ningún modo hay tarjetas ni aprobaciones por
herramienta.

### Evidencia: nunca borrar

Cada corrida va en su propia carpeta (`evidencia/osint/<objetivo>-<fecha>[-runN]/`). El agente **no
borra, mueve ni sobrescribe** evidencia de corridas anteriores, aunque cambie la convención de
nombres. Si una corrida vieja no cumple el formato nuevo, se deja como está y se anota en el informe.

### Fase 0: la autorización la declara el humano, no el agente

Con el modo ya elegido, y antes de la primera llamada a herramienta, el agente **pregunta y espera
respuesta** a:

1. ¿Cuál es el objetivo exacto (dominio u organización)?
2. ¿Quién autoriza la investigación y con qué base (laboratorio del curso, dominio propio, permiso
   por escrito)?
3. ¿Cuál es el propósito y hay restricciones adicionales del docente?

Reglas:

- El agente **no se autodeclara autorizado** ni deduce la autorización de que un dominio "es
  conocido", "aparece en un curso" o "parece de laboratorio". Aunque el dominio aparezca en material
  didáctico, eso no autoriza a investigar la infraestructura real que hay detrás.
- `00-alcance.md` se escribe con las **palabras del humano** (quién autoriza y por qué) y la fecha.
  Si el humano no responde o la respuesta es ambigua, no se ejecuta ninguna herramienta.
- Si durante la investigación aparece un dominio u organización **distinto** del autorizado (un
  tercero, otro dominio de la empresa), el agente se detiene y pregunta antes de consultarlo.
- **La autorización no se hereda.** Un objetivo nuevo requiere su propia Fase 0 respondida por el
  humano. El agente **no** escribe "asumo el mismo alcance" ni arranca hasta recibir la respuesta. Un
  proveedor real (registrador, servicio de privacidad, hosting) casi nunca está autorizado: el
  agente debe advertirlo al preguntar.

## Mapa de guías de steering de este power

| Guía | Categorías que cubre | Cuándo usarla |
|---|---|---|
| `osint-metodologia-flujo.md` | Principios y flujo | Punto de partida: principios, frontera legal y flujo. |
| `osint-company-information.md` | Organization, Locations, Staff, Contact Information, Business Records, Services, Social Networks | Empresa y personas. |
| `osint-infraestructura-dominio.md` | Domain Information, Public Domain Records, Domain Structure | Registro del dominio, DNS, ASN/netblocks, subdominios. |
| `osint-cloud-terceros.md` | Cloud Storage, Third Parties | Almacenamiento cloud y proveedores externos. |
| `osint-emails-redes-tecnologias.md` | Email Addresses, Compounded Networks, Technologies in Use | Formato de email, redes mixtas, stack tecnológico. |
| `osint-leaks.md` | Archives, Internal Leaks, Breaches | Archivos históricos, metadatos, breaches. |
| `osint-intelligence-reporte.md` | Intelligence (Origin → Impact → State) | Análisis final, evidencia e informe. |
| `osint-herramientas-mcp.md` | (transversal) | Referencia de herramientas, guardrails y errores comunes. |
| `osint-modos-trabajo.md` | (didáctica) | Los tres modos (Rápido, Guiado, Spec), sus paradas y las reglas comunes. |
| `osint-spec-investigacion.md` | (didáctica, modo Spec) | Construir con el alumno el Spec de Kiro de la investigación y ejecutarlo por tareas. |
| `osint-spec-plantilla.md` | (didáctica) | Plantilla de `requirements.md`, `design.md` y `tasks.md`. |
| `osint-compuertas-aprendizaje.md` | (didáctica) | Preguntas Observe/Orient/Decide por fase; las usan los hooks de tarea. |
