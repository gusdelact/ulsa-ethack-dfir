# Triage, enriquecimiento y correlación en TheHive

Flujo para un lote de alertas (p. ej. las del escenario Insight Nexus). Combina herramientas MCP y
pasos en la interfaz web, porque el servidor no cubre asignar, comentar ni vincular alertas a un
caso existente.

## 1. Inventario de alertas

1. `get_thehive_alerts` con `limit: 100`.
2. El agente arma una tabla en la bitácora:

| ID | Título | Severidad | Estado | Fuente | Fecha | ¿Escenario? |
|---|---|---|---|---|---|---|

3. Marcar las del escenario (p. ej. prefijo `[InsightNexus]` en el título). En modo Estudio, el
   alumno decide cuáles marcar y el agente revisa.

## 2. Detalle de cada alerta

Para cada alerta del escenario, `get_thehive_alert_by_id` con `alert_id` (formato `~123456`).
Extraer:

- Host, usuario, proceso, línea de comandos, IPs, hashes, regla (ID de Wazuh, p. ej. `92153`).
- Técnica MITRE si la alerta la trae (verificar el ID según R10).
- Observables ya existentes.

Registrar cada dato en `02-timeline.md` y `04-iocs.md` con la fuente
`thehive:<alert_id>` (R-LAB7).

## 3. Triage

Para cada alerta, decidir y anotar:

| Decisión | Cuándo |
|---|---|
| Verdadero positivo | Evidencia de actividad maliciosa |
| Falso positivo | Actividad legítima explicada (anotar por qué) |
| Requiere más datos | Falta contexto; anotar qué falta |

Prioridad según la matriz de `ih-02-deteccion-triage.md` del power `incident-handling-nist`.

## 4. Correlación

Agrupar alertas que comparten:

- Ventana de tiempo (mismos minutos u horas).
- Host, cuenta, IP o hash.
- Etapa de la Kill Chain consecutiva (p. ej. login → enumeración → creación de cuenta).

El agente propone los grupos y una hipótesis por grupo (marcada como hipótesis, R11).

## 5. Crear el caso (escritura, R-LAB2)

Dos caminos; el agente muestra los argumentos y pide confirmación antes de ejecutar:

**A. Promover la alerta principal**

```json
{ "alert_id": "~<id de la alerta principal>" }
```
con `promote_alert_to_case`.

**B. Crear un caso nuevo**

```json
{
  "title": "Insight Nexus — ManageEngine Compromise",
  "description": "Correlación de alertas: ...",
  "severity": 4,
  "tags": ["insightnexus", "manageengine", "exfiltration"],
  "tlp": 2,
  "pap": 2
}
```
con `create_thehive_case`.

Luego, **en la interfaz web** (el agente lo indica paso a paso):

- Alerts → seleccionar las alertas del escenario → **Merge into case** / vincular al caso creado.
- Asignarse las alertas y el caso.

## 6. Observables (escritura, R-LAB2)

Por cada IOC confirmado, `create_case_observable`:

```json
{
  "case_id": "<id del caso>",
  "data_type": "ip",
  "data": "103.112.60.117",
  "message": "C2 HTTPS desde java.exe de ManageEngine (Sysmon 3)",
  "ioc": true,
  "sighted": true,
  "tags": ["c2"]
}
```

Tipos válidos: `ip`, `domain`, `url`, `hash`, `mail`, `filename`, `fqdn`, `uri_path`,
`user-agent`, `autonomous-system`, `other`. Agrupar los IOCs y pedir **una** confirmación por lote.

## 7. Enriquecimiento

- Reputación con VirusTotal: `irl-enriquecimiento-virustotal.md`.
- El resultado se agrega como **comentario** en la alerta o el caso desde la interfaz web (el agente
  redacta el texto listo para pegar):

```text
[Enriquecimiento VT <fecha UTC>] 103.112.60.117
- Detecciones: <n>/<total> motores
- AS / país: <>
- Whois (OrgName/City): <>
- Archivos relacionados (referrer/communicating): <nombres>
- Conclusión: <hecho / inferencia>
```

## 8. Validar hallazgos de las notas

Si una alerta trae en notas salidas como `netstat`, el agente:

1. Extrae IPs y puertos remotos y el proceso (si viene `-b` u `-o`).
2. Separa IPs privadas de públicas.
3. Compara las públicas contra `04-iocs.md` y las enriquece.
4. Si un host **ya recuperado** sigue conectando a un IOC, lo marca y aplica R8 (volver a investigación).

## 9. Cierre (interfaz web)

Al terminar: resumen en el caso, lecciones aprendidas y estado. El agente redacta el resumen con la
plantilla de `08-reporte-final.md`.
