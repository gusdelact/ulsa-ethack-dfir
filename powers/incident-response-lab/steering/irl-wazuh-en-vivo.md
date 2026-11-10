# Wazuh en vivo (instancia propia)

El laboratorio de HTB entrega los logs de Wazuh como `.zip`; para eso usar
`irl-analisis-logs-exportados.md`. Esta guía es para cuando tienes un Wazuh propio (por ejemplo, un
laboratorio local con agentes Windows y Sysmon). El servidor viene **deshabilitado**; activarlo según
`irl-configuracion.md`, sección 5.

Todas las herramientas son de solo lectura.

## Herramientas y uso en un incidente

| Herramienta | Parámetros | Uso en la respuesta |
|---|---|---|
| `get_wazuh_alert_summary` | `limit` (por defecto 100) | Últimas alertas del indexer: punto de partida del triage. No filtra por regla ni por host; el agente filtra el resultado. |
| `get_wazuh_agents` | `limit`, `status` (`active`, `disconnected`, `pending`, `never_connected`), `name`, `ip`, `group`, `os_platform`, `version` | Inventario y cobertura: ¿qué hosts no tienen agente o están desconectados? (en Insight Nexus la cobertura era parcial). |
| `get_wazuh_agent_processes` | `agent_id` (requerido), `limit`, `search` | Live response básico: procesos en ejecución de un host sospechoso. |
| `get_wazuh_agent_ports` | `agent_id` (requerido), `limit`, `protocol`, `state` | Puertos abiertos y conexiones: buscar el C2 o servicios expuestos (p. ej. 3389). |
| `get_wazuh_rules_summary` | `limit`, `level`, `group`, `filename` | Ver qué detecta Wazuh y con qué nivel (p. ej. `group: "sysmon"`). |
| `get_wazuh_vulnerability_summary` | `agent_id` (requerido), `limit`, `severity`, `cve` | Vector de entrada probable; prioridad de parches. |
| `get_wazuh_critical_vulnerabilities` | `agent_id` (requerido), `limit` | Solo críticas de un agente. |
| `search_wazuh_manager_logs` | `limit`, `offset`, `level`, `tag`, `search_term` | Logs del manager (no son los eventos de Windows). |
| `get_wazuh_manager_error_logs` | `limit` | Errores del manager: pérdida de eventos, agentes caídos. |
| `get_wazuh_log_collector_stats` | `agent_id` (requerido) | ¿El agente está enviando sus logs? |
| `get_wazuh_remoted_stats`, `get_wazuh_weekly_stats` | — | Volumen de eventos; caídas bruscas pueden indicar un agente detenido por el atacante. |
| `get_wazuh_cluster_health`, `get_wazuh_cluster_nodes` | `limit`, `offset`, `node_type` | Salud del clúster. |

## Flujo sugerido

1. `get_wazuh_alert_summary` → identificar hosts y reglas de interés.
2. `get_wazuh_agents` con `name` → obtener `agent_id` del host.
3. `get_wazuh_agent_processes` y `get_wazuh_agent_ports` → procesos y conexiones actuales (registrar como evidencia volátil con hora, R3/R7).
4. `get_wazuh_vulnerability_summary` → posible vector.
5. `get_wazuh_log_collector_stats` → confirmar que no hay huecos de telemetría.

Para consultas por Event ID o por campo, el servidor no tiene una herramienta de búsqueda en el
indexer: usar Discover en el dashboard de Wazuh o exportar los eventos y seguir
`irl-analisis-logs-exportados.md`.
