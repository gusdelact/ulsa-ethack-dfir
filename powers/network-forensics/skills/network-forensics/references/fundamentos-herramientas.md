# Fundamentos y herramientas (secciones 1–2)

## Qué es el forense de red

Es la disciplina que detecta, monitorea y analiza delitos o violaciones de política a partir del tráfico y de los logs de red. Se usa para identificar el origen de ciberataques, DoS/DDoS, amenazas internas y otras actividades maliciosas, y para aportar evidencia en procesos legales.

El curso recomienda conocer antes: fundamentos de redes, protocolos, análisis de paquetes y análisis de logs de red.

## Principios

| Principio | Descripción |
|---|---|
| Recolección de datos | Monitoreo continuo del tráfico para registrarlo y analizarlo después: sniffers, servidores de logs, herramientas de monitoreo. |
| Investigación | Se analizan los datos para conocer el tipo de incidente, la hora, los sistemas afectados y el daño potencial. |
| Análisis | Examen detallado con herramientas y técnicas de análisis de red. |
| Reporte | Los hallazgos van a un reporte forense completo e imparcial, porque puede usarse en procesos legales. |

## Técnicas

| Técnica | Descripción |
|---|---|
| Software de análisis de paquetes | Wireshark y similares: análisis detallado del tráfico. |
| SIEM | Recolecta y analiza logs, y alerta cuando detecta una posible brecha. |
| Detección de anomalías | Análisis estadístico y modelos de aprendizaje automático que identifican comportamiento anormal. |

## Herramientas

### Wireshark

Analizador de protocolos que captura y examina tráfico en tiempo real.
- Interfaz gráfica y opciones de línea de comandos (`tshark`).
- Entiende cientos de protocolos.
- Filtros para encontrar los paquetes relevantes.
- Usos: investigación de brechas, problemas de rendimiento, examen de paquetes y flujos.

### tcpdump

Captura paquetes desde la línea de comandos y los muestra o guarda según criterios.
- Muy usado en Linux y Unix.
- Muchas opciones de filtrado y captura.
- Usos: análisis de bajo nivel, comportamiento de protocolos, auditorías y pruebas de penetración.

### Snort

IDS/IPS que monitorea el tráfico y alerta sobre amenazas analizando paquetes.
- Análisis en tiempo real y captura de paquetes.
- Conjunto amplio y personalizable de reglas y firmas.
- Usos: detectar y prevenir ataques, aplicar políticas, análisis de flujos.

### NetworkMiner

Herramienta pasiva de análisis forense de red: extrae archivos, sesiones y nombres de usuario del tráfico.
- Interfaz visual sencilla.
- Detecta actividad sospechosa.
- Usos: reunir información de dispositivos y usuarios de la red; analizar malware y sus comunicaciones.

### Otras mencionadas en el curso

| Herramienta | Uso |
|---|---|
| `ngrep` | Busca patrones de texto dentro del tráfico. |
| Suricata | IDS multihilo con firmas y detección de anomalías; genera NetFlow. |
| Zeek | Monitoreo de red con detección por firmas y por anomalías; adecuado para threat hunting y forense. |

## Tipos de evidencia de red

| Evidencia | Contenido | Ventaja | Límite |
|---|---|---|---|
| Captura completa (pcap) | Encabezados y contenido de cada paquete | Máximo detalle | Mucho espacio; contenido cifrado |
| Flujos (NetFlow, VPC Flow Logs) | Quién habló con quién, cuándo, cuánto | Poco espacio, retención larga | Sin contenido |
| Alertas de IDS | Coincidencias con firmas | Rápido para amenazas conocidas | No detecta lo desconocido (0-day) |
| Logs (proxy, DNS, firewall) | Eventos de cada servicio | Contexto de aplicación | Depende de la configuración |
