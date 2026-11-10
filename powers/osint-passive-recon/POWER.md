---
name: "osint-passive-recon"
displayName: "OSINT Passive Recon"
description: "Curso completo de OSINT pasivo con herramientas MCP sin API keys: Company Information, Infrastructure y Leaks, cerrando con Origin -> Impact -> State bajo metodología OODA. Combina OpenOSINT (RDAP, WHOIS, DNS, dorks, GitHub, pastes, IP) y OSINT Toolbox (crt.sh, Wayback Machine, ExifTool). Incluye guías de steering por categoría, referencia de herramientas, reglas de evidencia y plantilla de informe."
keywords: ["osint", "reconocimiento-pasivo", "footprinting", "whois-rdap", "certificate-transparency", "wayback-machine"]
author: "Gustavo De la Cruz Tovar"
x-ethack:
  kind: "offensive"
  ecCouncilPhase: "Reconnaissance"
  forensicsStage: null
  team: "red-team"
  owner: "Gustavo De la Cruz Tovar"
  tools: ["RDAP", "WHOIS", "DNS", "crt.sh", "Wayback Machine", "ExifTool", "GitHub dorks"]
  allowlistValidation:
    required: true
    source: "engagements/${ENGAGEMENT_ID}/scope.yaml#assets"
    targetParams: ["target", "host", "hostname", "domain", "url"]
  executionMode:
    param: "Modo_Ejecucion"
    allowed: ["script-kiddie", "green-hat", "pro"]
    default: "script-kiddie"
  documentation:
    root: "powers/osint-passive-recon/docs"
    required: ["prompt.md", "sessions/", "feedback.md"]
---

# OSINT Passive Recon

## Al activar este power (obligatorio, en este orden)

1. **Modo de trabajo (perfil del hacker).** Este modo es el parámetro `Modo_Ejecucion` del
   frontmatter (`x-ethack.executionMode`: `allowed: ["script-kiddie", "green-hat", "pro"]`,
   `default: "script-kiddie"`). Los tres modos de este power son esos tres perfiles; **Rápido,
   Guiado y Spec son sus nombres operativos equivalentes** (Rápido = `script-kiddie`,
   Guiado = `green-hat`, Spec = `pro`; ver tabla de equivalencia abajo). Si el prompt no indica el
   modo, el agente lo pregunta **antes que nada** y espera la respuesta. No lo elige por su cuenta; si
   aun así no se define, usa el default `script-kiddie` (Rápido). Lo pregunta así:

   > ¿En qué modo trabajamos?
   > - **script-kiddie (Rápido):** yo recorro el flujo completo y te explico cada fase en una línea. Para demos o práctica individual.
   > - **green-hat (Guiado):** antes y después de cada fase me dices qué buscas y qué significa lo que salió. Para aprender el flujo.
   > - **pro (Spec):** primero planeamos juntos la investigación en un Spec de Kiro (qué quieres saber, de dónde y cómo), diseñas tú el método y justificas el alcance; luego se ejecuta por tareas. Para un entregable.

2. **Cargar la guía del modo:** Rápido → `osint-metodologia-flujo.md`; Guiado →
   `osint-compuertas-aprendizaje.md`; Spec → `osint-spec-investigacion.md`. En todos los modos
   también `osint-modos-trabajo.md` (reglas comunes).
3. **Fase 0:** preguntar objetivo, quién autoriza y propósito, y esperar la respuesta. Escribir
   `00-alcance.md` con las palabras del humano, incluido el campo `Modo:`.
4. **Seguir según el modo.** Ninguna herramienta MCP se ejecuta antes de completar los pasos 1 y 3.

## Overview

Este power entrega un **cuerpo de conocimiento de OSINT pasivo** (metodología, categorías de
información y flujo de trabajo) y dos servidores MCP para practicarlo de forma **100 % pasiva** sobre
un dominio u organización autorizada:

- **OpenOSINT**: RDAP, WHOIS, DNS con alertas SPF/DMARC, información de IP/ASN, generación de
  Google dorks, búsqueda en GitHub y en pastes.
- **OSINT Toolbox**: certificados vía crt.sh (Certificate Transparency), snapshots de Wayback
  Machine, WHOIS/DNS de cross-check y metadatos de archivos locales con ExifTool.

Ninguna herramienta habilitada envía tráfico al objetivo: todas consultan a terceros (registros,
resolvers DNS, crt.sh, web.archive.org, ipinfo.io, GitHub) o trabajan en local.

OSINT **no busca entrar**: busca **entender sin tocar** cuánto puede saber cualquiera sobre la
organización, y dejarlo documentado con evidencia.

> **Regla de encuadre:** solo se investigan objetivos dentro del alcance autorizado (dominio de
> laboratorio como `example.com`, dominio propio o permiso por escrito). Este
> material es didáctico y no concede autorización por sí mismo. Si encuentras un bucket o servicio
> expuesto, **lo documentas y te detienes**.

Creado para el curso de **Hackeo Ético, Ingeniería Cibernética (ULSA)** con asistencia de Kiro.

> **Base didáctica:** este power está construido sobre el módulo **"OSINT: Corporate Recon"** de
> **Hack The Box Academy** ([academy.hackthebox.com/course/preview/osint-corporate-recon](https://academy.hackthebox.com/course/preview/osint-corporate-recon/osint-methodology)).
> Las categorías (Company Information, Infrastructure, Leaks), la metodología de ciclos de lo
> general a lo detallado y el cierre Origin → Impact → State provienen de ese módulo; aquí se
> adaptan a un flujo reproducible con herramientas MCP sin API keys, compuertas de aprendizaje
> anti copy-paste y entrega de evidencia versionable para uso académico.

## Cómo está organizado el conocimiento (steering/)

El conocimiento está repartido en guías de steering que se cargan **bajo demanda** (acción
`readSteering`): lee solo la que necesites según la fase.

| Guía | Categoría | Contenido |
|---|---|---|
| `osint-metodologia-flujo.md` | Metodología | Principios, frontera legal pasivo/activo, dos navegadores, flujo por fases con las herramientas MCP. **Léela primero.** |
| `osint-company-information.md` | Company Information | Organization, Locations, Staff, Contact Information, Business Records, Services, Social Networks. |
| `osint-infraestructura-dominio.md` | Infrastructure (dominio) | Domain Information, Public Domain Records (registro, DNS, ASN, netblocks), Domain Structure (subdominios). |
| `osint-cloud-terceros.md` | Infrastructure (cloud) | Cloud Storage (S3, Blob, GCS) y Third Parties, con la regla de detención. |
| `osint-emails-redes-tecnologias.md` | Infrastructure (email/tech) | Email Addresses, Compounded Networks, Technologies in Use. |
| `osint-leaks.md` | Leaks | Tipos de leak, Archives (Wayback, Pastebin), Internal Leaks (metadatos), Breaches. |
| `osint-intelligence-reporte.md` | Intelligence | Origin → Impact → State, estructura de evidencia y plantilla de informe. |
| `osint-herramientas-mcp.md` | (transversal) | Argumentos de cada herramienta, qué está apagado y por qué, verificación sin LLM, errores comunes. |
| `osint-modos-trabajo.md` | (didáctica) | **Léela al inicio.** Los modos Rápido, Guiado y Spec, sus paradas y las reglas comunes. |
| `osint-spec-investigacion.md` | (didáctica, modo Spec) | Cómo construir con el alumno el Spec de la investigación y ejecutarlo por tareas. |
| `osint-spec-plantilla.md` | (didáctica) | Plantilla de `requirements.md`, `design.md` y `tasks.md` del Spec OSINT. |
| `osint-compuertas-aprendizaje.md` | (didáctica, modo Guiado) | Compuertas Observe/Orient/Decide antes y después de cada fase. |

Cada guía incluye una tabla **técnica → herramienta del power**, que separa lo que cubre el MCP,
lo que hace el humano en su navegador y lo que queda fuera de alcance (activo o con llave).

## Modos de trabajo

El power se usa en uno de tres modos. Todos usan las mismas herramientas, la misma frontera pasiva y
la misma evidencia; cambia **quién piensa en cada paso** y **dónde se detiene el agente**. Detalle en
`osint-modos-trabajo.md`.

Estos tres modos **son** los tres perfiles del parámetro `Modo_Ejecucion` del frontmatter
(`script-kiddie` | `green-hat` | `pro`, default `script-kiddie`). Rápido, Guiado y Spec son los
nombres operativos que este power ya usaba; la equivalencia es exacta, de modo que la declaración del
frontmatter no queda huérfana:

| `Modo_Ejecucion` | Nombre operativo | Qué hace el agente (perfil del hacker) |
|---|---|---|
| `script-kiddie` *(default)* | **Rápido** | Recorre el flujo listo y entrega los hallazgos con explicación mínima (una línea por fase). Nivel de entrada: terminar rápido. |
| `green-hat` | **Guiado** | Antes y después de cada fase explica qué se consulta y por qué, y te pide razonar la salida (compuertas Observe/Orient/Decide). Aprendiz: aprender el flujo en el laboratorio. |
| `pro` | **Spec** | No ejecuta por ti: te guía a **diseñar tú la investigación** en un Spec (requirements/design), discute método y límites y exige justificar el alcance y la frontera pasiva (ética/legalidad, White vs Black). Profesional/experto. |

| | **Rápido** | **Guiado** | **Spec** |
|---|---|---|---|
| Para qué | Demo del instructor, práctica individual | Laboratorio: aprender el flujo fase por fase | Entregable: planear antes de ver datos |
| Guía | `osint-metodologia-flujo.md` | `osint-compuertas-aprendizaje.md` | `osint-spec-investigacion.md` |
| Paradas | Solo alcance, objetivo nuevo, bucket expuesto, técnica activa y final | Antes y después de cada **fase** | Al escribir cada documento del Spec y antes/después de cada **tarea** |
| Quién decide qué consultar | El agente | El alumno, por fase | El alumno, en el `design.md` |
| Hooks | Ninguno | Ninguno | `osint-task-pre.json` y `osint-task-post.json` |
| Entregables extra | — | `bitacora-decisiones.md` | Bitácora + Spec en `.kiro/specs/osint-<objetivo>/` |

En ningún modo hay aprobación ni tarjeta por herramienta. Si el humano no indica el modo, el agente
lo pregunta antes que nada (ver "Al activar este power"). Pasar a un modo con **más** paradas lo puede pedir cualquiera; pasar a uno
con **menos** paradas, solo el instructor.

**Prompts de arranque:**

- **Rápido:** *Activa el power osint-passive-recon en modo Rápido. Objetivo: <dominio>.*
- **Guiado:** *Activa el power osint-passive-recon en modo Guiado y carga
  `osint-compuertas-aprendizaje.md`. Objetivo: <dominio>. Detente en cada fase y pregúntame.*
- **Spec:** *Activa el power osint-passive-recon en modo Spec y carga `osint-spec-investigacion.md`.
  Quiero crear el Spec de investigación OSINT para <dominio>. Hazme las preguntas; no escribas tú las
  respuestas.*

### Modo Spec: documentos y hooks

| Documento del Spec | El alumno decide | Categorías HTB |
|---|---|---|
| `requirements.md` | Qué quiere saber el cliente y cuándo está respondido | Company Information, Infrastructure, Leaks, Intelligence |
| `design.md` | Hipótesis inicial, frontera pasiva, matriz Core Elements × Information Resources, qué abre un ciclo nuevo | Metodología |
| `tasks.md` | Orden de las tareas, una por categoría | Ciclos de lo general a lo detallado |

- **Hook `hooks/osint-task-pre.json`** (`PreTaskExec`): el alumno dice qué espera encontrar y qué le
  haría cambiar de idea.
- **Hook `hooks/osint-task-post.json`** (`PostTaskExec`): el alumno clasifica hecho / inferencia /
  hipótesis, revisa los criterios y decide si abre un ciclo nuevo.

Los hooks solo actúan sobre Specs en `.kiro/specs/osint-*/`, así que no interfieren con los modos
Rápido y Guiado. El power no los activa solo (Kiro solo lee `.kiro/hooks/` del workspace):

```bash
mkdir -p .kiro/hooks
cp powers/osint-passive-recon/hooks/osint-task-pre.json powers/osint-passive-recon/hooks/osint-task-post.json .kiro/hooks/
```

Hay un Spec de ejemplo completo en `.kiro/specs/osint-inlanefreight-ejemplo/` del workspace del curso.

> El hook antiguo por herramienta (`hooks/legacy/osint-gate.json`) queda solo como referencia: pausa
> cada llamada con un texto fijo y no ayuda a entender la investigación.

## Principios de OSINT

- **Intelligence, no recolección.** El valor está en relacionar los datos, no en acumularlos. Elegir
  herramientas es ~10 % del trabajo.
- **Ciclos de lo general a lo detallado.** Cada hallazgo abre otro ciclo (un subdominio nuevo vuelve
  a pasar por DNS y Wayback).
- **Se adaptan los recursos a la metodología**, no al revés.
- **Solo pasivo.** Brute-forcing de subdominios o directorios, AXFR, escaneos, abrir buckets o probar
  credenciales **no son OSINT** y están fuera de alcance.

| Company Information | Infrastructure | Leaks |
|---|---|---|
| Organization, Locations, Staff, Contact Information, Business Records, Services, Social Networks | Domain Information, Public Domain Records, Domain Structure, Cloud Storage, Email Addresses, Third Parties, Compounded Networks, Technologies in Use | Archives, Internal Leaks, Breaches |

Cierre: **Origin → Impact → State**, que conecta cuándo se originó cada hallazgo, qué
impacto tiene y qué estado se observa hoy.

## Metodología cognitiva: OSINT con OODA

**OODA** es un ciclo de toma de decisiones formulado por el coronel **John Boyd** de la Fuerza Aérea
de EE. UU. a partir de su experiencia como piloto de combate. Boyd observó que, en un duelo aéreo,
no ganaba necesariamente el piloto con mejor avión, sino el que **completaba más rápido y con mejor
información** el ciclo **Observe → Orient → Decide → Act**: mirar lo que pasa, interpretarlo con su
experiencia y contexto, decidir una maniobra y ejecutarla, para luego volver a observar el resultado.

El ciclo saltó de la aviación al negocio, al litigio y a la ciberseguridad porque describe cualquier
situación en la que **se decide bajo incertidumbre con información parcial y cambiante**, que es
exactamente el escenario de OSINT: nunca ves "toda" la superficie de una organización, solo señales
indirectas (un registro DNS, un certificado, un snapshot de Wayback), y cada nueva señal cambia lo
que conviene preguntar a continuación.

Aplicado a OSINT pasivo, OODA fuerza tres disciplinas que evitan el "copy-paste de herramientas":

1. **Pensar antes de ejecutar.** Nunca se lanza una consulta "a ver qué sale"; primero se nombra qué
   se quiere reducir de incertidumbre.
2. **Separar hechos de interpretaciones.** La salida cruda es el hecho; "usan Microsoft 365" es
   interpretación. El informe los registra en columnas distintas.
3. **Cerrar el ciclo con evidencia.** Cada "Act" produce un archivo guardado en
   `evidencia/osint/`, no un recuerdo en la conversación.

| Etapa | Pregunta | Qué haces en OSINT |
|---|---|---|
| **Observe** | ¿Qué sé realmente? | Lee la salida cruda de la herramienta. Separa **hechos** (MX apunta a `outlook.com`) de **inferencias** (usan Microsoft 365). |
| **Orient** | ¿Qué significa? | Relaciona el dato con su categoría OSINT (Company / Infrastructure / Leaks) y con hallazgos previos. Formula hipótesis explícitas. |
| **Decide** | ¿Qué conviene y está autorizado? | Elige la **próxima consulta pasiva** que reduzca la incertidumbre más grande. Confirma que no toca al objetivo. |
| **Act** | ¿Qué pasó? | Ejecuta la herramienta MCP, guarda la salida cruda con fecha y argumentos en `evidencia/osint/`, y vuelve a Observe con el resultado. |

Cada ciclo es corto (una pregunta, una herramienta, una salida) y encadena al siguiente: un
subdominio nuevo descubierto en "Act" vuelve a entrar como "Observe" de otro ciclo sobre DNS y
Wayback. Las compuertas de aprendizaje de este power (steering + hook) existen justamente para que
el alumno no se salte Orient y Decide.

### Reglas cognitivas (críticas para el alumno)

1. **Un indicador no es una vulnerabilidad.** DMARC `p=none` o un WordPress antiguo en Wayback son
   exposición a validar en una fase autorizada.
2. **Registra por separado** hechos, inferencias, hipótesis y pendientes.
3. **Toda observación lleva procedencia** (herramienta + argumentos, o URL) y **fecha**. Un snapshot
   de 2019 describe 2019.
4. **Nada sin salida real.** Si una herramienta falla o devuelve vacío, se reporta así; no se rellena
   con conocimiento del modelo.
5. **Las herramientas son limitadas**: crt.sh falla, RDAP no cubre todos los TLD, ipinfo tiene cuota.
   Contrasta con una segunda fuente (`whois_lookup`, `dns_lookup`).
6. **La información de una fase alimenta a otra.** Encadenar es el corazón del método.
7. **Las alertas de una herramienta no son conclusiones.** "No SPF: anyone can spoof" se lee junto
   con DMARC y MX; los NS de la zona se contrastan con los de RDAP; la ausencia en crt.sh se
   contrasta con certificados comodín. Reglas en `osint-infraestructura-dominio.md`.

## Onboarding

### Prerequisitos

- **`uv`** (trae `uvx`) para ejecutar ambos servidores sin clonar repositorios ni usar Docker:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- Opcional: **ExifTool** para `exiftool_metadata` (`brew install exiftool` o `sudo apt install exiftool`).
- Opcional: **Node.js 22.19+** solo para depurar con el MCP Inspector.

### Instalación

Es un **Guided MCP Power**: al instalarlo, Kiro añade los dos servidores de `mcp.json`. No requiere
API keys, tokens ni cuentas.

Calentar la caché antes del primer uso (OpenOSINT trae ~20 dependencias):

```bash
uvx --python 3.12 --from openosint==2.36.1 openosint-mcp --help
uvx osint-toolbox-mcp@1.1.0 --check
```

### Configuración incluida en `mcp.json`

- **`openosint`**: 13 herramientas ocultas con `disabledTools` (las que piden llave, un extra o lanzan
  un agente propio). Modo pasivo por defecto; **nunca** añadir `--allow-active`.
- **`osint-toolbox`**: las CLIs externas (Sherlock, Maigret, Holehe, GHunt, theHarvester, subfinder,
  dnstwist, dnsrecon, PhoneInfoga, SpiderFoot, Blackbird) apuntan a `/nonexistent/disabled` para que
  el servidor no las detecte aunque estén instaladas (p. ej. en Kali). `osint_toolbox_status` oculta.
- **Sin `autoApprove`**: cada llamada se aprueba a mano para mantener trazabilidad.

## Herramientas disponibles (resumen)

| Servidor | Herramienta | Uso principal | Guía |
|---|---|---|---|
| `openosint` | `search_rdap`, `search_whois` | Registro del dominio | `osint-infraestructura-dominio.md` |
| `openosint` | `search_dns` | Registros DNS + alertas SPF/DMARC | `osint-infraestructura-dominio.md` |
| `openosint` | `search_ip` | ASN, organización y proveedor de una IP | `osint-infraestructura-dominio.md` |
| `openosint` | `generate_dorks` | URLs de Google dorks (local; las abre el humano) | `osint-company-information.md` |
| `openosint` | `search_github` | Repos, perfiles y correos de commits | `osint-company-information.md` |
| `openosint` | `search_paste` | Volcados de Pastebin (psbdmp.ws) | `osint-leaks.md` |
| `osint-toolbox` | `crtsh_certificate_search` | Subdominios y correos en certificados | `osint-infraestructura-dominio.md` |
| `osint-toolbox` | `wayback_snapshots` | Huella histórica, rutas, tecnologías retiradas | `osint-leaks.md` |
| `osint-toolbox` | `whois_lookup`, `dns_lookup` | Cross-check; WHOIS de IP/ASN, PTR, CAA | `osint-infraestructura-dominio.md` |
| `osint-toolbox` | `exiftool_metadata` | Metadatos de documentos públicos descargados | `osint-leaks.md` |

Argumentos, límites y lo que está apagado: `osint-herramientas-mcp.md`.

## Flujo de trabajo típico

1. **Modo y alcance:** primero el modo (si no se indicó; ver "Al activar este power"). Después el
   agente **pregunta** objetivo, quién autoriza y propósito, y espera la respuesta. No se autodeclara
   autorizado. Escribe `evidencia/osint/<objetivo>-<fecha>/00-alcance.md` con las
   palabras del humano (ver Fase 0 en `osint-metodologia-flujo.md`).
2. **Registro:** `search_rdap(domain=...)`; si el TLD no tiene RDAP, `search_whois` o `whois_lookup`.
3. **DNS:** `search_dns` sobre la raíz y `www`; cross-check con `dns_lookup`. Revisar SPF/DMARC y TXT.
4. **IP → ASN → proveedor:** `search_ip(ip=...)` y `whois_lookup(query=<ip>)`.
5. **Subdominios:** `crtsh_certificate_search(domain=...)`; si da HTTP 502, reintentar y, si persiste,
   dejarlo como pendiente. Cada subdominio nuevo vuelve al paso 3.
6. **Huella histórica:** `wayback_snapshots(url=..., match="domain", limit=50)` y `robots.txt`.
7. **Empresa y personas:** `generate_dorks(target=...)` (el humano abre las URLs) y `search_github`.
8. **Leaks:** `search_paste`; `exiftool_metadata` sobre documentos públicos que el humano descargó.
9. **Intelligence e informe:** Origin → Impact → State con la plantilla de `osint-intelligence-reporte.md`.

**Ejemplo de prompt** (adaptar `TU-DOMINIO` al objetivo autorizado):

> Eres un analista OSINT. Objetivo autorizado: TU-DOMINIO. Usa solo técnicas pasivas: nada de
> transferencias de zona, escaneos ni accesos al objetivo. Si encuentras un bucket o servicio
> expuesto, documéntalo y detente. Usa solo las herramientas MCP de `openosint` y `osint-toolbox`.
> En cada hallazgo indica la herramienta y los argumentos, y no afirmes nada que no aparezca en una
> salida real. Si una herramienta falla, dilo en el informe. Guarda cada salida cruda en
> `evidencia/osint/`. Entrega la tabla de hallazgos, el cierre Origin → Impact → State y la lista de
> lo que decidiste no hacer.

## Evidencia y documentación

> **Regla de persistencia de evidencia (obligatoria):** la evidencia cruda **se guarda** en el
> workspace del proyecto, en `evidencia/osint/<objetivo>-<fecha>/`, nunca solo en `/tmp`. **Un
> archivo por llamada** en `herramientas/`, con herramienta, argumentos y fecha UTC, y la salida
> **literal**: sin resúmenes, sin notas de inferencia y sin combinar llamadas. La interpretación va
> solo en `informe.md`. Los documentos descargados van con su hash SHA-256.

El informe registra: alcance, hallazgos clasificados (hecho / inferencia / hipótesis), tabla de
infraestructura, dorks generados (no ejecutados por el agente), Origin → Impact → State, pendientes y
fallos de herramientas, decisiones de no hacer, recomendaciones y fuentes. Plantilla completa en
`osint-intelligence-reporte.md`.

## Errores comunes (resumen)

| Síntoma | Solución |
|---|---|
| `crt.sh answered HTTP 502` | Reintentar 1–2 veces; si persiste, pendiente en el informe. Nunca inventar datos. |
| `No RDAP server found for TLD` | Usar `search_whois` o `whois_lookup`. |
| El agente usa la búsqueda web del host | Pedir "solo herramientas MCP de openosint y osint-toolbox". |
| Primer arranque lento o timeout | Calentar la caché de `uvx` antes. |
| Kiro no encuentra `uvx` | Ruta absoluta de `which uvx` en `command`. |
| `search_dns` no reporta DKIM | Es activo; documentarlo como fuera de alcance. |

Detalle y más casos en `osint-herramientas-mcp.md`.

## Buenas prácticas

- **Nunca usar `--allow-active`** ni reactivar las CLIs del toolbox. Si un ejercicio necesita técnicas
  activas, es otra fase con otra autorización.
- **Aprobar cada llamada a mano** (sin `autoApprove`).
- **No ejecutar dorks de forma automatizada**: son URLs para que una persona las abra.
- **No instalar software** que el agente sugiera durante un ejercicio guiado.
- **No perfilar personas reales**: en el lab, solo identidades sintéticas del caso.
- **Ofuscar datos sensibles** (credenciales, datos personales) en el informe: se documenta su
  existencia, no su valor.
- **Tratar los hallazgos como indicadores de exposición**, no como vulnerabilidades confirmadas.

## Preguntas didácticas (úsalas en cada fase)

- ¿Qué afirmación **observaste** y cuál solo **inferiste**?
- ¿Qué salida de herramienta (o URL) respalda tu conclusión, y de qué fecha es?
- ¿Qué evidencia adicional confirmaría o refutaría la hipótesis? ¿Obtenerla sería pasivo?
- ¿Alguna consulta tocó al objetivo o a un tercero que escanea por encargo?
- ¿Cómo explicarías el riesgo al equipo técnico y a la dirección sin tecnicismos?

## MCP Config Placeholders

**No hay placeholders**: `mcp.json` usa paquetes públicos (`openosint`, `osint-toolbox-mcp`) vía `uvx`,
sin rutas ni credenciales del usuario.

## Referencias

- **Hack The Box Academy — "OSINT: Corporate Recon"** (base conceptual del power, incluye las
  categorías Company Information / Infrastructure / Leaks y el cierre Origin → Impact → State):
  <https://academy.hackthebox.com/course/preview/osint-corporate-recon/osint-methodology>.
- Metodología **OODA** (Observe–Orient–Decide–Act) aplicada al reconocimiento pasivo.
- Las guías de steering de este power son autocontenidas: metodología, categorías y flujo están en
  `steering/osint-*.md`.
- Paquetes de los servidores MCP: `openosint` y `osint-toolbox-mcp` (PyPI).

---

**Paquetes:** `openosint==2.36.1` (PyPI), `osint-toolbox-mcp@1.1.0` (PyPI)
**Servidores MCP:** `openosint`, `osint-toolbox`
