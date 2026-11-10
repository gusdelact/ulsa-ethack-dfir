# Fase 2b: Investigación

Objetivo: entender **qué pasó y cómo pasó**. Sin saber cómo entró el atacante y qué afectó, la
remediación no impide que vuelva a entrar por el mismo camino. Reconstruir sistemas sin investigar
no es suficiente.

La investigación debe encontrar:

- El **patient zero** (primera víctima) y la línea de tiempo.
- Las herramientas y el malware usados.
- Los sistemas comprometidos y lo que hizo el atacante en cada uno.

## Ciclo de investigación

```
1. Crear y usar IOCs ─► 2. Identificar nuevas pistas y sistemas ─► 3. Recolectar y analizar ─┐
        ▲                                                                                    │
        └────────────────────────────────────────────────────────────────────────────────────┘
```

No enfocarse en un solo hallazgo (p. ej. "es Mimikatz"). Eso produce conclusiones prematuras y un
impacto incompleto. El equipo debe proponer pistas nuevas en cada vuelta.

## 1. IOCs

Un IOC es una señal estructurada de que ocurrió un incidente: IPs, dominios, hashes, nombres de
archivo, claves de registro, mutex, user-agents, cuentas.

| Formato / herramienta | Uso |
|---|---|
| OpenIOC | Documentar y compartir IOCs |
| YARA | Reglas para identificar archivos o memoria por patrones |
| Mandiant IOC Editor | Crear y editar IOCs |
| STIX 2.1 (JSON) | Intercambiar CTI; lo publica CISA en sus avisos |
| Sigma | Reglas de detección sobre logs, portables entre SIEMs |

Registro en `04-iocs.md`: tipo, valor, fuente, primera/última vez visto, estado (activo, falso
positivo, descartado) y dónde se buscó.

Recordar la **pirámide del dolor** (`ih-mapeo-killchain-mitre.md`): los hashes e IPs se cambian
fácil; priorizar también artefactos de host y TTPs.

Para buscar IOCs a escala en Windows se usa WMI o PowerShell (o el EDR/SIEM).

## Credenciales del investigador (R4)

Al conectarse a sistemas posiblemente comprometidos, **no dejar credenciales privilegiadas en
memoria**:

| Método | ¿Cachea credenciales en el remoto? |
|---|---|
| WinRM / PowerShell Remoting (logon tipo 3) | No, normalmente |
| PsExec sin credenciales (usa la sesión actual) | No |
| **PsExec con `-u`/`-p` explícitos** | **Sí** |
| **RDP con cuenta de dominio (logon tipo 10)** | **Sí** |
| Logon interactivo en consola (tipo 2) | Sí |

La misma herramienta deja huellas distintas según cómo se use: conocer las herramientas.

## 2. Nuevas pistas y sistemas impactados

- Un IOC muy genérico da hits no relacionados: **eliminar falsos positivos** antes de ampliar el alcance.
- Con muchos hits, priorizar los que puedan dar pistas nuevas tras un análisis forense.
- Cada sistema nuevo se agrega a `03-sistemas.md` con su estado.

## 3. Recolección y análisis

### Live response vs apagar (R3)

| | Live response | Apagar y analizar |
|---|---|---|
| Cuándo | Lo más común; se recolecta un conjunto predefinido de artefactos | Cuando el riesgo de mantenerlo encendido es mayor |
| Ventaja | Conserva memoria, conexiones y procesos | Disco estable para imagen forense |
| Riesgo | Alterar evidencia si se interactúa de más | **Se pierde todo lo que está solo en RAM** |

Interactuar lo mínimo con el sistema en ambos casos.

### Orden de volatilidad (complemento, RFC 3227)

Recolectar de lo más volátil a lo menos volátil:

1. Registros y caché de CPU, tabla de procesos, conexiones de red, memoria RAM.
2. Archivos temporales, swap/pagefile.
3. Disco.
4. Logs remotos y datos de monitoreo.
5. Configuración física y topología de red.
6. Medios de respaldo.

### Análisis

- Lo más común: **análisis de malware** y **forense de disco**.
- **Forense de memoria**: cada vez más relevante contra ataques avanzados.
- Suele ser la parte que más tiempo toma.
- Cada pista validada se agrega a `02-timeline.md`.

### Cadena de custodia (R7)

Para que la evidencia sea admisible en juicio, registrar en `05-evidencia-custodia.md`: qué es,
hash (SHA-256), quién la recolectó, cuándo, de dónde, dónde se guarda y cada transferencia.

## IA en detección y respuesta

- Automatiza la revisión de logs y alertas, reduce tiempos y detecta anomalías de comportamiento.
- Ejemplo: **Elastic Security Attack Discovery** usa LLMs para agrupar alertas en una historia de ataque con usuarios, hosts y mapeo a ATT&CK.
- Usos: triage y priorización automática, correlación y reconstrucción del timeline, playbooks automáticos, apoyo en lecciones aprendidas.
- La salida de la IA es una **inferencia** (R11): se valida contra la fuente antes de usarla.

## Correlación

En el caso Insight Nexus, una alerta de baja prioridad (`checkme.txt`) se volvió crítica al
correlacionarla en la misma ventana de tiempo con logins admin desde IPs extranjeras, `msiexec` en
muchos hosts, enumeración LDAP, cambios de GPO, compresión de archivos y HTTPS saliente raro.
Buscar siempre otros eventos en la misma ventana de tiempo y en los mismos hosts o cuentas.

## Siguiente paso

Cuando se cumplen los criterios de avance (tipo, vector, sistemas, impacto), pasar a
`ih-04-contencion-erradicacion-recuperacion.md`.
