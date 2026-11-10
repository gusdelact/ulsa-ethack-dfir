---
name: "incident-response-lab"
displayName: "Incident Response Lab"
description: "Laboratorio de respuesta a incidentes con TheHive (alertas, casos y observables), VirusTotal (reputación de IPs, dominios y hashes) y Wazuh (alertas, agentes y logs), más recetas para analizar logs exportados de Windows/Sysmon y decodificar PowerShell. Pensado para el módulo Incident Handling Process de HTB Academy y para laboratorios propios. Se usa junto con el power incident-handling-nist."
keywords: ["thehive", "wazuh", "virustotal", "soc-triage", "sysmon", "incident-response-lab"]
author: "Gustavo De la Cruz Tovar"
x-ethack:
  kind: "response"
  ecCouncilPhase: null
  forensicsStage: null
  track: "IR"
  team: "incident-responder"
  owner: "Gustavo De la Cruz Tovar"
  tools: ["TheHive", "VirusTotal", "Wazuh", "Sysmon"]
  allowlistValidation:
    required: true
    source: "engagements/${ENGAGEMENT_ID}/scope.yaml#assets"
    targetParams: ["target", "host", "hostname", "domain", "url"]
  executionMode:
    param: "Modo_Ejecucion"
    allowed: ["script-kiddie", "green-hat", "pro"]
    default: "script-kiddie"
  documentation:
    root: "powers/incident-response-lab/docs"
    required: ["prompt.md", "sessions/", "feedback.md"]
---

# Incident Response Lab

## Al activar este power (obligatorio, en este orden)

1. **Objetivo de la sesión.** Si el prompt no lo indica, preguntar y esperar:
   > ¿Qué quieres hacer en esta sesión?
   > - **Estudio:** te guío para que encuentres tú las respuestas del laboratorio; no te las doy.
   > - **Respuesta:** hago el triage y el enriquecimiento contigo y registro todo en la carpeta del caso.
2. **Perfil de ejecución (`Modo_Ejecucion`).** Lee el parámetro `Modo_Ejecucion` del frontmatter
   (`x-ethack.executionMode`, valores `script-kiddie` | `green-hat` | `pro`, default
   `script-kiddie`). Define **cuánta autonomía y profundidad** tiene la guía de triage/enriquecimiento
   (ver "Modos de ejecución (perfil del hacker)" abajo). Si el prompt no lo indica, se pregunta junto
   con el objetivo; si no se define, se usa `script-kiddie`.
3. **Alcance (R-LAB1).** Confirmar que el objetivo es un laboratorio autorizado (HTB, laboratorio
   propio o asignado) y anotar `TARGET_IP` o la URL de TheHive/Wazuh.
4. **Verificar servidores.** Comprobar qué servidores MCP responden (ver "Verificación" abajo). Si
   alguno falla, cargar `irl-configuracion.md`. Los logs exportados se pueden analizar sin ningún MCP.
5. **Cargar la guía de la tarea** (tabla de steering) y, si está instalado, el power
   `incident-handling-nist` para la carpeta del caso, las reglas R1–R12 y la equivalencia de perfiles
   de `ih-modos-trabajo.md`.

## Overview

| Servidor MCP | Paquete | Para qué | Estado por defecto |
|---|---|---|---|
| `thehive` | [gbrigandi/mcp-server-thehive](https://github.com/gbrigandi/mcp-server-thehive) v0.1.1 (binario) | Leer alertas y casos, promover alertas a caso, crear casos y observables | Habilitado |
| `virustotal` | [`@burtthecoder/mcp-virustotal@1.0.38`](https://github.com/w0h1v/mcp-virustotal) (npm) | Reputación y relaciones de IPs, dominios, URLs y hashes | Habilitado |
| `wazuh` | [gbrigandi/mcp-server-wazuh](https://github.com/gbrigandi/mcp-server-wazuh) v0.3.0 (binario) | Alertas, agentes, procesos, puertos, reglas y logs de un Wazuh en vivo | **Deshabilitado**: el laboratorio de HTB entrega los logs de Wazuh como `.zip`, no un Wazuh en vivo. Habilitarlo solo con un Wazuh propio. |

Además, `irl-analisis-logs-exportados.md` trae recetas con `jq` y Python para los archivos
`logs-wazuh.zip` y `wazuh_export.zip` del curso, que no necesitan MCP.

> Base didáctica: módulo [Incident Handling Process](https://academy.hackthebox.com/module/details/148)
> de HTB Academy. Creado para el curso de Ingeniería Cibernética (ULSA) con asistencia de Kiro.

## Reglas del laboratorio

Además de R1–R12 de `incident-handling-nist`:

| # | Regla |
|---|---|
| R-LAB1 | Solo instancias autorizadas (laboratorio HTB activo, laboratorio propio o asignado). |
| R-LAB2 | **Escrituras con confirmación.** `promote_alert_to_case`, `create_thehive_case` y `create_case_observable` se ejecutan solo después de mostrar los argumentos y recibir un "sí". Ninguna herramienta va en `autoApprove`. |
| R-LAB3 | **VirusTotal es un tercero.** Consultar un indicador lo revela a VirusTotal. No enviar URLs, dominios o hashes internos de un caso real sin autorización (TLP). `get_url_report` **envía la URL a escanear** si no está en caché. |
| R-LAB4 | Cuota de VirusTotal pública: 4 consultas/minuto y límite diario. Agrupar consultas y no repetirlas. |
| R-LAB5 | Credenciales y tokens solo en variables de entorno; nunca en `mcp.json`, en la bitácora ni en el chat. |
| R-LAB6 | En modo **Estudio**, no dar la respuesta de preguntas [LAB]: guiar con el método y dejar que el alumno lea el dato. |
| R-LAB7 | Todo resultado de herramienta se registra en la carpeta del caso con la fuente (`thehive: get_thehive_alert_by_id ~123`), según R11. |

## Herramientas disponibles

### `thehive`

| Herramienta | Parámetros | Escribe |
|---|---|---|
| `get_thehive_alerts` | `limit` (int, opcional, 100) | No |
| `get_thehive_alert_by_id` | `alert_id` (string, requerido, p. ej. `~123456`) | No |
| `get_thehive_cases` | `limit` (int, opcional, 100) | No |
| `get_thehive_case_by_id` | `case_id` (string, requerido) | No |
| `promote_alert_to_case` | `alert_id` (string, requerido) | **Sí** |
| `create_thehive_case` | `title`, `description` (requeridos); `severity` (1 baja–4 crítica), `tags`, `tlp` (0–3), `pap` (0–3), `status`, `assignee`, `case_template`, `start_date` (ms) | **Sí** |
| `create_case_observable` | `case_id`, `data_type` (`ip`, `domain`, `url`, `hash`, `mail`, `filename`, `fqdn`, `uri_path`, `user-agent`, `autonomous-system`, `other`), `data` (requeridos); `message`, `tlp`, `pap`, `ioc` (bool), `sighted` (bool), `tags` | **Sí** |

No hay herramientas para **asignarse una alerta, comentar, vincular una alerta a un caso existente
ni cerrar casos**. Eso se hace en la interfaz web; el agente indica el paso.

### `virustotal`

| Herramienta | Parámetros |
|---|---|
| `get_ip_report` | `ip` |
| `get_ip_relationship` | `ip`, `relationship` (p. ej. `referrer_files`, `communicating_files`, `downloaded_files`, `resolutions`, `urls`), `limit` (1–40), `cursor` |
| `get_domain_report` | `domain`, `relationships` (array, opcional) |
| `get_domain_relationship` | `domain`, `relationship` (p. ej. `subdomains`, `resolutions`, `communicating_files`), `limit`, `cursor` |
| `get_file_report` | `hash` (MD5, SHA-1 o SHA-256) |
| `get_file_relationship` | `hash`, `relationship` (p. ej. `contacted_ips`, `contacted_domains`, `dropped_files`), `limit`, `cursor` |
| `get_file_behaviour_summary` | `hash` |
| `get_url_report` | `url` (**envía a escanear si no hay caché**, R-LAB3) |
| `get_url_relationship` | `url`, `relationship`, `limit`, `cursor` |
| `search_vt` | `query` (hash, IP, dominio, URL o modificadores VTI), `limit`, `cursor` |
| `get_collection` | `id`, `relationships` (opcional) |

### `wazuh` (deshabilitado por defecto)

`get_wazuh_alert_summary` (`limit`), `get_wazuh_agents` (`limit`, `status`, `name`, `ip`, `group`,
`os_platform`, `version`), `get_wazuh_agent_processes` (`agent_id`, `limit`, `search`),
`get_wazuh_agent_ports` (`agent_id`, `limit`, `protocol`, `state`), `get_wazuh_rules_summary`
(`limit`, `level`, `group`, `filename`), `get_wazuh_vulnerability_summary`,
`get_wazuh_critical_vulnerabilities`, `search_wazuh_manager_logs`, `get_wazuh_manager_error_logs`,
`get_wazuh_weekly_stats`, `get_wazuh_remoted_stats`, `get_wazuh_log_collector_stats`,
`get_wazuh_cluster_health`, `get_wazuh_cluster_nodes`. Todas de solo lectura. Detalle en
`irl-wazuh-en-vivo.md`.

## Cómo está organizado el conocimiento (steering/)

| Guía | Contenido |
|---|---|
| `irl-configuracion.md` | Instalación de los binarios y el paquete npm, variables de entorno, aprobación en Kiro, verificación, errores comunes. |
| `irl-triage-thehive.md` | Flujo de triage, enriquecimiento y correlación en TheHive con las herramientas MCP y la interfaz web. |
| `irl-enriquecimiento-virustotal.md` | Cómo enriquecer IPs, dominios y hashes, qué mirar en cada reporte y cómo registrarlo. |
| `irl-analisis-logs-exportados.md` | Reconocer el formato de los `.zip`, normalizar con `jq`/Python, filtros por Event ID, decodificar PowerShell. |
| `irl-wazuh-en-vivo.md` | Uso del servidor Wazuh con una instancia propia. |
| `irl-sigma-detecciones.md` | Reglas Sigma de referencia para lo que se ve en el curso y cómo probarlas. |
| `irl-skills-assessment.md` | Guía del Skills Assessment y de las preguntas de Insight Nexus, sin respuestas. |

## Verificación

Con los servidores configurados, el agente prueba en este orden y reporta qué funciona:

1. `thehive` → `get_thehive_alerts` con `limit: 5`. Esperado: lista de alertas.
2. `virustotal` → `get_file_report` con el SHA-256 de EICAR
   `275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f`. Esperado: reporte con detecciones.
3. `wazuh` (si se habilitó) → `get_wazuh_agents` con `limit: 5`.

## Modos de ejecución (perfil del hacker)

Este power tiene **dos ejes** que conviven:

- **Objetivo de la sesión** (qué se produce): Estudio o Respuesta.
- **Perfil de ejecución** (cuánta autonomía y profundidad), fijado por el parámetro
  **`Modo_Ejecucion`** del frontmatter (`x-ethack.executionMode`:
  `allowed: ["script-kiddie", "green-hat", "pro"]`, `default: "script-kiddie"`).

Como el trabajo es triage y enriquecimiento con TheHive, VirusTotal y Wazuh (más logs exportados),
los **tres** perfiles expresan cuánto ejecuta el agente y cuánto hace razonar al alumno:

| `Modo_Ejecucion` | Perfil | Qué hace el agente en incident-response-lab |
|---|---|---|
| `script-kiddie` *(default)* | Nivel de entrada | Ejecuta las consultas MCP listas (`get_thehive_alerts`, `get_file_report`, filtros de logs), entrega el veredicto y registra, con explicación mínima. Avanzar rápido. |
| `green-hat` | Aprendiz | Antes de cada consulta explica qué herramienta usa y por qué, disecciona los parámetros y **pide al alumno interpretar** el reporte (reputación, relaciones, Event IDs). Es el espíritu del modo **Estudio**, que no da la respuesta. |
| `pro` | Profesional/experto (White/Black Hat) | No entrega la consulta hecha: guía al alumno a **diseñar su propio flujo de triage, sus reglas Sigma y su correlación**, discute arquitectura y límites (cuota y TLP de VirusTotal R-LAB3/4, qué ve Wazuh) y exige la **justificación ética y legal** (autorización R-LAB1, no exponer indicadores de terceros, cadena de custodia R-LAB7). |

**Equivalencia con los modos existentes:** el modo **Estudio** es trabajo de perfil `green-hat`
(reforzado por R-LAB6: no dar la respuesta de preguntas `[LAB]`); el modo **Respuesta** puede
ejecutarse en cualquiera de los tres perfiles. Así los tres perfiles del `Modo_Ejecucion` quedan
cubiertos. La equivalencia detallada vive en `ih-modos-trabajo.md` del power `incident-handling-nist`,
con el que este laboratorio se usa en conjunto.

**Prompts de arranque por perfil:**

- **script-kiddie:** *Activa incident-response-lab con `Modo_Ejecucion=script-kiddie`. Haz el triage de las alertas y dame el veredicto.*
- **green-hat:** *Activa incident-response-lab con `Modo_Ejecucion=green-hat`. Explícame cada consulta antes de ejecutarla y pídeme interpretar el reporte.*
- **pro:** *Activa incident-response-lab con `Modo_Ejecucion=pro`. Guíame para diseñar yo el flujo de triage y las reglas Sigma, y pídeme la justificación legal.*

## Prompts de arranque

- *Activa el power incident-response-lab en modo Estudio. Laboratorio HTB, TheHive en http://10.129.x.x:9000. Quiero hacer el Skills Assessment.*
- *Activa incident-response-lab en modo Respuesta. Haz el triage de las alertas [InsightNexus] y propón el caso.*
- *Con incident-response-lab, analiza `~/Downloads/logs-wazuh.zip` y encuentra el PowerShell sospechoso.*

## Troubleshooting

| Error | Causa probable | Solución |
|---|---|---|
| `command not found: mcp-server-thehive` | Binario no instalado o no está en el PATH de Kiro | Ver `irl-configuracion.md`; o poner la ruta absoluta en `command`. |
| macOS: "no se puede abrir porque es de un desarrollador no identificado" | Cuarentena de Gatekeeper | `xattr -d com.apple.quarantine <binario>` |
| TheHive: `401` / authentication failed | Token incorrecto o sin permisos | Crear otro API key; ver `irl-configuracion.md`. |
| TheHive: connection refused / timeout | VPN de HTB caída, `TARGET_IP` cambió o falta `/api` en la URL | Reconectar la VPN, actualizar `THEHIVE_URL`, reiniciar el servidor MCP. |
| Variables `${...}` vacías | Kiro no aprobó la variable o no la ve en su entorno | Aprobarlas en *Mcp Approved Env Vars* y abrir Kiro desde una terminal donde estén exportadas. |
| VirusTotal: `429` | Cuota pública agotada | Esperar 1 minuto; agrupar consultas (R-LAB4). |
| VirusTotal: `401` / `WrongCredentialsError` | API key mal copiada | La key tiene 64 caracteres, sin comillas ni espacios. |
