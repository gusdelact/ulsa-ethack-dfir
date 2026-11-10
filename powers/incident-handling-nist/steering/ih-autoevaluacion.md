# Autoevaluación (modo Estudio)

Instrucciones para el agente:

- Hacer **una pregunta a la vez** y esperar la respuesta.
- **No mostrar la respuesta ni el criterio** antes de que el alumno conteste (salvo que lo pida).
- Al corregir: decir si es correcta, parcialmente correcta o incorrecta, explicar con el criterio y citar la sección del curso.
- Las preguntas marcadas **[LAB]** no tienen respuesta aquí: indicar dónde encontrarla.

Tipos: **[C]** pregunta del curso · **[A]** pregunta de aplicación (situación del caso Insight Nexus).

---

## Fundamentos (secciones 1–3)

1. **[C]** ¿Qué diferencia hay entre un evento, un incidente y un incidente de seguridad TI?
   - *Criterio:* evento = cualquier acción en un sistema; incidente = evento con consecuencia negativa; incidente de seguridad = evento con intención clara de causar daño contra un sistema.
2. **[C]** ¿En qué etapa de la Cyber Kill Chain se desarrolla el malware?
   - *Respuesta:* **Weaponize.**
3. **[C]** Verdadero o falso: el incident handling tiene dos actividades principales, investigar y reportar.
   - *Respuesta:* **Falso.** Son investigar y recuperar.
4. **[C]** ¿Cuáles son las 4 etapas del proceso según NIST?
   - *Respuesta:* Preparación; Detección y análisis; Contención, erradicación y recuperación; Actividad post-incidente.
5. **[A]** Encontraste 10 equipos infectados. Tu compañero propone contener 5 hoy y erradicar esos mientras investigan los otros 5. ¿Qué respondes?
   - *Criterio:* no; hay que contener los 10 de forma coordinada antes de erradicar (R1, R2), porque se alerta al atacante.
6. **[C]** ¿Por qué el bloqueo de una IP de C2 causa poco "dolor" al atacante y qué conviene detectar en su lugar?
   - *Criterio:* cambia de IP fácilmente (base de la pirámide); detectar TTPs y artefactos de host.
7. **[C]** Diferencia entre táctica, técnica y sub-técnica en ATT&CK, con un ejemplo.
   - *Criterio:* objetivo / método / implementación; p. ej. Credential Access / T1003 / T1003.001.
8. **[LAB]** ID de la regla MITRE de la alerta 67c202 (LSASS Access) en TheHive.

## Preparación (secciones 4–5)

9. **[C]** ¿Qué debemos tener preparado y listo para "tomar y salir"?
   - *Respuesta:* **el jump bag.**
10. **[C]** Verdadero o falso: con baselines podemos descubrir desviaciones de la golden image.
    - *Respuesta:* **Verdadero.**
11. **[C]** ¿Por qué la documentación y la comunicación del incidente deben estar fuera de la infraestructura de la organización?
    - *Criterio:* asumir que el dominio está comprometido y que el atacante lee el correo; los sistemas pueden quedar indisponibles.
12. **[C]** ¿Qué mecanismo bloquea phishing que finge venir de nuestro dominio?
    - *Respuesta:* **DMARC** (sobre SPF y DKIM).
13. **[C]** Verdadero o falso: `Summer2021!` cumple los criterios de complejidad pero es fácil de adivinar.
    - *Respuesta:* **Verdadero.**
14. **[A]** Insight Nexus tenía ManageEngine expuesto con admin/admin y sin MFA. Nombra tres medidas de la fase de preparación que lo habrían evitado o detectado.
    - *Criterio:* cambiar credenciales por defecto, MFA, no exponer la consola (o WAF), enviar logons al SIEM, escaneo de vulnerabilidades.
15. **[C]** ¿Por qué hay que tener cuidado con los LOLBins al implementar allowlisting?
    - *Criterio:* son binarios legítimos permitidos que se usan para ejecutar código y evadir el allowlisting.

## Detección y análisis (secciones 6–7)

16. **[C]** Verdadero o falso: un proveedor externo puede ser la fuente de detección de un compromiso.
    - *Respuesta:* **Verdadero.**
17. **[C]** ¿Qué columnas debe tener la línea de tiempo del incidente?
    - *Respuesta:* fecha, hora del evento, hostname, descripción del evento, fuente de datos.
18. **[A]** Recibes: "cuenta admin se conectó a 10.0.5.20 a las 03:12". ¿Qué te falta saber antes de concluir algo?
    - *Criterio:* qué sistema es 10.0.5.20, zona horaria, si la cuenta suele hacerlo, desde dónde, qué hizo después.
19. **[C]** Menciona las 7 preguntas de severidad y alcance. ¿Cuáles indican la sofisticación del adversario?
    - *Criterio:* impacto, requisitos, sistemas críticos, remediación sugerida, número de sistemas, uso in the wild, capacidad de gusano; las dos últimas.
20. **[C]** Encontraste un archivo malicioso con MD5 `b40f6b2c167239519fcfb2028ab2524a`. ¿Cómo se llama ese valor en una investigación?
    - *Respuesta:* **IOC.**
21. **[C]** ¿Cuáles son los 3 pasos del ciclo de investigación?
    - *Respuesta:* crear y usar IOCs; identificar nuevas pistas y sistemas; recolectar y analizar datos.
22. **[A]** Necesitas revisar DEV-021 de forma remota con tu cuenta de Domain Admin. ¿Usas PsExec con `-u` y `-p`? ¿Por qué?
    - *Criterio:* no; PsExec con credenciales explícitas las deja cacheadas; usar WinRM o logon tipo 3 (R4).
23. **[C]** ¿Por qué apagar un equipo comprometido puede ser mala idea?
    - *Criterio:* se pierde lo que está solo en RAM (procesos, conexiones, claves, malware sin archivo).
24. **[C]** ¿Para qué sirve la cadena de custodia?
    - *Criterio:* que la evidencia sea admisible en juicio; registrar quién la tuvo y que no se alteró.
25. **[C]** Verdadero o falso: detectas movimiento lateral hacia sistemas de finanzas; como son de otro departamento, no escalas.
    - *Respuesta:* **Falso.** Se escala.
26. **[A]** La alerta `checkme.txt` parece de baja prioridad. ¿Qué buscarías para saber si es parte de algo mayor?
    - *Criterio:* correlacionar en la misma ventana y hosts: logins admin raros, conexiones salientes, procesos nuevos, cambios de GPO, enumeración, archivos comprimidos.
27. **[LAB]** Usuario que ejecutó Mimikatz según la alerta de TheHive (formato `dominio\usuario`).
28. **[LAB]** MD5 en la alerta con regla 92153 (VaultCli.dll).

## Contención, erradicación y recuperación (sección 8)

29. **[C]** Verdadero o falso: parchear un sistema es contención de corto plazo.
    - *Respuesta:* **Falso.** Es de largo plazo.
30. **[C]** Da tres ejemplos de contención de corto plazo.
    - *Criterio:* VLAN aislada, desconectar cable, sinkhole del DNS del C2, bloqueo de IP.
31. **[C]** Durante la recuperación siguen apareciendo IOCs de forma intermitente. ¿Recovery o Investigation?
    - *Respuesta:* **Investigation.**
32. **[A]** Ya se borró `checkme.txt` y se parchó el portal. ¿Se puede cerrar el caso? Justifica.
    - *Criterio:* no; Crimson Fox sigue con persistencia (GPO, tareas, cuenta Domain Admin, C2); falta erradicar y monitorear.
33. **[C]** ¿Qué eventos se vigilan en un sistema recién recuperado?
    - *Criterio:* logons inusuales, procesos inusuales, cambios de registro típicos de malware.

## Post-incidente (sección 9)

34. **[C]** Verdadero o falso: se debe entrenar a los miembros junior como parte de la actividad post-incidente.
    - *Respuesta:* **Verdadero.**
35. **[C]** ¿Qué preguntas debe responder el reporte final?
    - *Criterio:* qué pasó y cuándo; desempeño frente a planes; si el negocio respondió a tiempo; acciones de contención/erradicación; medidas preventivas; herramientas necesarias.
36. **[A]** Propón dos mejoras de detección para Insight Nexus a partir de las lecciones aprendidas.
    - *Criterio:* p. ej. regla Sigma de RDP desde IP pública; logons de ManageEngine al SIEM; filtrar ruido de creación de archivos; alertas por `msiexec` desplegado por GPO; egress a IPs raras.

## Insight Nexus y Skills Assessment (secciones 10–11)

37. **[C]** ¿Qué técnica de ATT&CK corresponde a descargar herramientas desde un C2 a la red de la víctima?
    - *Respuesta:* **T1105** (Ingress Tool Transfer).
38. **[A]** Mapea a la Kill Chain: adjunto abierto → downloader escribe `.exe` en `%AppData%` → clave `Run` → carga `VaultCli.dll` → envía credenciales a IP externa.
    - *Criterio:* Delivery/Exploitation → Installation → Installation (persistencia) → Actions on Objectives (credenciales) → Actions on Objectives (exfiltración).
39. **[A]** ¿Qué dos IDs del mapeo del curso para Insight Nexus son incorrectos y cuáles serían los adecuados?
    - *Criterio:* T1078.004 → T1078.001; T1069 → T1484.001 / T1053.005.
40. **[LAB]** Preguntas de `wazuh_export.zip` (proceso padre en 4688, imagePath de persistencia en DB01, IP de exfiltración de `diagnostics_data.zip`, usuario que accedió a `\\fs01\projects`).
41. **[LAB]** Preguntas del Skills Assessment (VirusTotal para las IPs 203.* y 198.*, ID MITRE de la regla 92153, IP y usuario del PowerShell en `logs-wazuh.zip`).

Para las preguntas [LAB], el power `incident-response-lab` guía la búsqueda paso a paso sin dar la
respuesta.
