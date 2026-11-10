# Fase 1: Preparación

Dos objetivos:

1. **Crear la capacidad de respuesta** (personas, documentación, herramientas).
2. **Proteger y prevenir** con medidas técnicas. No es tarea directa del equipo de IH, pero el
   equipo debe conocerlas para saber dónde buscar evidencia y qué tan sofisticado es un ataque.

## Checklist de capacidad

### Personas

- [ ] Equipo de IH capacitado (puede ser tercerizado, pero con conocimiento interno básico).
- [ ] Incident manager definido, con mandato para pedir acciones a cualquier área.
- [ ] Personal general entrenado en concientización de seguridad.

### Documentación (actualizada)

- [ ] Contactos y roles del equipo de IH.
- [ ] Contactos de legal, cumplimiento, dirección, soporte TI, comunicación/prensa, autoridades, ISPs, instalaciones y equipo externo de IR.
- [ ] Política, plan y procedimientos de respuesta a incidentes.
- [ ] Política y procedimientos para compartir información del incidente.
- [ ] Baselines de sistemas y red a partir de una *golden image* (para detectar desviaciones).
- [ ] Diagramas de red.
- [ ] Inventario de activos de toda la organización.
- [ ] Cuentas privilegiadas de emergencia para el equipo: deshabilitadas por defecto, se habilitan al confirmar el incidente y se deshabilitan con reseteo de contraseña al cerrar.
- [ ] Procedimiento de compra urgente (hasta un monto) sin el proceso completo de adquisiciones.
- [ ] Cheat sheets forenses.
- [ ] Requisitos legales de notificación conocidos con legal (p. ej. GDPR fija plazos para brechas con datos personales).

### Jump bag (kit listo para salir)

- [ ] Laptop/estación forense por integrante (AV deshabilitado; aislada del dominio).
- [ ] Adquisición y análisis de imágenes de disco.
- [ ] Captura y análisis de memoria.
- [ ] Herramientas de live response.
- [ ] Análisis de logs y de tráfico de red.
- [ ] Cables de red, switch, cables de poder.
- [ ] Write blockers y discos para imágenes forenses.
- [ ] Destornilladores, pinzas y herramientas para desarmar hardware.
- [ ] Creador de IOCs y capacidad de buscarlos en toda la organización.
- [ ] Formularios de cadena de custodia.
- [ ] Software de cifrado.
- [ ] Sistema de tickets y de gestión de casos **independiente** de la infraestructura de la organización.
- [ ] Lugar seguro para almacenar evidencia e investigar.

### Durante el incidente

Documentar con calma: timestamp, actividad, resultado y quién la hizo. Responder quién, qué,
cuándo, dónde, por qué y cómo. La plantilla está en `ih-plantillas.md` (bitácora).

## Medidas de protección que el handler debe conocer

| Medida | Qué hace | Qué evidencia deja o qué cuidar |
|---|---|---|
| **DMARC** (sobre SPF y DKIM) | Rechaza correos que suplantan nuestro dominio. | Probar antes de aplicar `reject`: puede bloquear correo legítimo sin recuperarlo. Los envíos "en nombre de" fallan DMARC (falsos positivos). |
| Filtrado por header DMARC | Extiende la protección a dominios ajenos que fallan DMARC. | Requiere pruebas extensas. |
| Deshabilitar LLMNR/NetBIOS | Evita envenenamiento y robo de hashes en la red local. | — |
| LAPS y sin admin local | Contraseñas de admin local únicas; usuarios sin privilegios. | Limita el movimiento lateral. |
| PowerShell ConstrainedLanguage | Restringe funciones peligrosas de PowerShell. | Útil junto con logging de PowerShell (Script Block, Event 4104). |
| Reglas ASR (Defender) | Bloquea comportamientos comunes de malware. | Generan eventos de bloqueo que sirven de evidencia. |
| Allowlisting | Solo ejecuta software aprobado. Mínimo: bloquear ejecución desde Downloads, Desktop, AppData y scripts `.hta .vbs .cmd .bat .js`. | Cuidar los **LOLBins**, que se usan para evadirlo. |
| Firewall de host | Bloquea workstation-a-workstation y salida de LOLBins. | Corta movimiento lateral. |
| EDR con AMSI | Inspecciona scripts ofuscados antes de ejecutarse. | Fuente principal de telemetría en el endpoint. |
| Segmentación de red | Aísla sistemas críticos; nada interno expuesto salvo en DMZ. | Limita el alcance del incidente. |
| IDS/IPS con intercepción TLS | Detecta por contenido, no por reputación de IP. | — |
| 802.1x / Conditional Access | Solo dispositivos aprobados acceden a la red o a la nube. | — |
| MFA | Obligatorio al menos en todo acceso administrativo. | Su ausencia aparece en casi todos los casos del curso (Colonial Pipeline, Insight Nexus). |
| Passphrases | Contraseñas largas y fáciles de recordar (`i LIK3 my coffeE warm`). | `Password1!` o `Summer2021!` son "complejas" pero predecibles. |
| Escaneo de vulnerabilidades | Continuo; remediar al menos High y Critical. | Si no se puede parchear, segmentar. |
| Concientización | Entrenamiento y pruebas sorpresa (phishing mensual, USBs). | Los usuarios son una fuente de detección. |
| Evaluación de AD | Revisar AD como atacante para eliminar escalamientos de un paso. | Más pasos para el atacante = más probabilidad de detectarlo. |
| Purple team | Red team que comparte hallazgos con el blue team. | Prueba logging, detección y playbooks. |

## Preguntas del agente en esta fase (modo Respuesta)

Si se usa el modo Respuesta para evaluar la preparación de una organización de laboratorio, el
agente recorre el checklist y marca cada punto como *existe / no existe / desconocido*, y entrega
la lista de brechas ordenada por impacto.
