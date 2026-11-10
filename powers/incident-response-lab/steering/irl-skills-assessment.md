# Guía del Skills Assessment y de las preguntas de Insight Nexus

Esta guía da el **método**, no las respuestas (R-LAB6). El agente propone el paso, el alumno lo
ejecuta o lo lee, y el agente verifica que el razonamiento sea correcto. En modo Respuesta el agente
puede ejecutar las herramientas, pero igual deja que el alumno lea y escriba el valor final.

Antes de empezar: target activo, VPN conectada, `THEHIVE_URL` actualizado (ver `irl-configuracion.md`)
y carpeta del caso creada (`incident-handling-nist`, `ih-plantillas.md`).

---

## Parte A: Skills Assessment (sección 11)

### Triage en TheHive

| Tarea | Método |
|---|---|
| 1. Crear un caso y vincular las alertas de Insight Nexus | `get_thehive_alerts` → filtrar por `[InsightNexus]` en el título → `create_thehive_case` o `promote_alert_to_case` (con confirmación, R-LAB2) → vincular el resto en la interfaz web. Ver `irl-triage-thehive.md`, pasos 1–5. |
| 2. Triage, enriquecimiento y correlación | Pasos 3, 4 y 7 de `irl-triage-thehive.md`. Anotar en las notas de cada alerta. |
| 3. Validar la salida de `netstat` | Paso 8 de `irl-triage-thehive.md`. Si el host ya recuperado sigue conectando a una IP externa, aplicar R8. |

### Preguntas

| # | Pregunta (resumen) | Método |
|---|---|---|
| Q1 | Archivo que empieza con "Mango" en *Files Referring* de la IP `203.*` | 1) `get_thehive_alert_by_id` de "[InsightNexus] Admin Login via ManageEngine Web Console" y leer los comentarios para encontrar la IP `203.*`. 2) `get_ip_relationship` con `relationship: "referrer_files"` (equivale a *Files Referring*). 3) El alumno busca el nombre que empieza con "Mango". 4) Redactar el comentario de enriquecimiento (plantilla del paso 7) y pegarlo en la alerta desde la interfaz web. |
| Q2 | Ciudad en *Whois Lookup* de la IP `198.*` | `get_ip_report` con la IP; buscar la línea `City:` del WHOIS. Si no aparece (formato del registro regional), verla en la web de VirusTotal: *Details → Whois Lookup*. |
| Q3 | Técnica de transferencia de herramientas desde un C2 | Consultar la tabla de `ih-mapeo-killchain-mitre.md` (táctica Command and Control). Verificar en attack.mitre.org. |
| Q4 | Técnica MITRE de la regla 92153 (VaultCli.dll) | `get_thehive_alerts` / `get_thehive_alert_by_id` para encontrar la alerta con la regla 92153; leer el campo MITRE o los tags de la alerta. Comparar con la técnica de Credential Access que corresponde a `vaultcli.dll` y verificar (R10). |
| Q5 | IP sospechosa en el PowerShell decodificado de `logs-wazuh.zip` | `irl-analisis-logs-exportados.md`, pasos 1, 2 y 5: normalizar, localizar `-enc`, decodificar UTF-16LE, extraer IPs. Si hay varias capas, decodificar todas. |
| Q6 | Usuario que ejecutó ese PowerShell (`dominio\usuario`) | Mismo evento del paso anterior: `subjectDomainName\subjectUserName` (4688) o `user` (Sysmon 1). |

### Mapeo a la Kill Chain

Cadena: adjunto abierto → downloader escribe `.exe` en `%AppData%` → clave `Run` → carga
`VaultCli.dll` con herramienta sospechosa → credenciales a IP externa.

El alumno llena la tabla y el agente revisa con `ih-mapeo-killchain-mitre.md`:

| Paso | Etapa Kill Chain | Táctica ATT&CK | ID (verificado) |
|---|---|---|---|
| Abre el adjunto |  |  |  |
| Descarga y escribe el `.exe` |  |  |  |
| Crea la clave `Run` |  |  |  |
| Carga `VaultCli.dll` |  |  |  |
| Envía credenciales a IP externa |  |  |  |

Tarea 2: buscar la alerta de Mimikatz en TheHive y leer su ID de técnica.

---

## Parte B: preguntas de "Analysis of Insight Nexus Breach" (sección 10)

Archivo: `wazuh_export.zip`. Seguir `irl-analisis-logs-exportados.md` (pasos 1–3) y luego:

| # | Pregunta (resumen) | Método |
|---|---|---|
| B1 | Ruta completa del **proceso padre** que ejecutó una herramienta de volcado de credenciales (Event ID 4688) | Filtro de "volcado de credenciales" y luego `ev 4688` sobre esos eventos; leer `parentProcessName`. El formato de respuesta del curso empieza con `C:\\Pr...` (barras dobles, como en JSON). |
| B2 | `imagePath` de un mecanismo de persistencia en **DB01** | `ev 7045` (y 4697) filtrando `agent.name` o `computer` = DB01; leer `imagePath`. |
| B3 | IP externa a la que se subió `diagnostics_data.zip` | `ioc 'diagnostics_data'` y revisar los eventos de red cercanos en tiempo y host (Sysmon 3, logs de firewall o proxy); separar IPs privadas de públicas. |
| B4 | Usuario que intentó conectarse a `\\fs01\projects` | `ev 5140` / `ev 5145` o `ioc 'projects'`; leer `subjectDomainName\subjectUserName`. |

Cada respuesta se registra en `02-timeline.md` con su Event ID y archivo como fuente, y las IPs o
archivos nuevos en `04-iocs.md`.
