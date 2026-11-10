# Requirements Document

## Introduction

Este documento define los requisitos para convertir a Kiro en un **Agente de Ethical Hacking y Digital Forensics** orquestado por **subagentes** (Kiro custom agents) que cubren el ciclo de vida de EC-Council (Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks). El sistema es un proyecto final académico de la Universidad La Salle que integra el trabajo de 13 alumnos organizados en equipos (Líder Técnico, Red Team, Blue Team, Digital Forensics, GRC e Incident Responder).

Cada subagente se implementa como un Kiro custom agent y usa uno o más **Kiro Powers** que envuelven herramientas reales de Kali Linux (PenTest y Digital Forensics). El entorno objetivo es exclusivamente de laboratorio: aplicaciones DVWA (Damn Vulnerable Web Application) y servicios vulnerables ejecutados dentro de **contenedores Docker** sobre nodos EC2 con Debian, definidos mediante una allowlist de objetivos autorizados. Toda prueba de penetración se realiza sobre el contenedor Docker que expone el servicio, no sobre el host EC2 subyacente. El proceso de Digital Forensics sigue el flujo de seis fases (Detect → Isolate → Collect → Preserve → Analyze → Report) y los siete principios forenses de la presentación de La Salle 2026, con alcance limitado a Linux y nube (Windows fuera de alcance). La validación funcional del agente completo se realiza mediante un AWS GameDay de seguridad. El sistema aplica los principios éticos de la charla motivadora (Authorization First, Scope Discipline, Do No Harm, Confidentiality, Full Disclosure, Legal Compliance) y usa hooks `PreToolUse` para demostrar el patrón "Authorization First" de forma **simulada/didáctica** (no bloqueante estricto).

Este spec describe el comportamiento del sistema de agentes, subagentes, Powers, hooks y políticas; **no** incluye criterios de calificación ni rúbrica de evaluación de alumnos (gestionados por el docente fuera de este spec).

## Glossary

- **Agente_Orquestador**: Agente principal de Kiro (custom agent) que coordina el flujo del ciclo EC-Council, selecciona y delega en los subagentes de fase/rol, y consolida los entregables.
- **Subagente_Fase**: Kiro custom agent responsable de una fase ofensiva del ciclo EC-Council (Reconnaissance, Scanning, Gaining Access, Maintaining Access, Covering Tracks).
- **Subagente_Rol**: Kiro custom agent asociado a un equipo o rol (Red Team, Blue Team, Digital Forensics, GRC, Incident Responder).
- **Power**: Kiro Power que envuelve una o más herramientas de Kali Linux (PenTest o Digital Forensics) y expone su capacidad al subagente que lo usa.
- **Herramienta_Real**: Utilidad de Kali Linux u otra herramienta de seguridad operativa (p. ej. nmap, Metasploit, Volatility, Autopsy) invocada a través de un Power.
- **Allowlist_Objetivos**: Lista configurable de objetivos de laboratorio autorizados (contenedores Docker y, donde se indique, hosts EC2); única fuente de objetivos válidos.
- **Entorno_Laboratorio**: Conjunto de nodos EC2 con Debian que ejecutan, dentro de contenedores Docker, DVWA y los servicios vulnerables de referencia usados como objetivos autorizados.
- **Contenedor_Objetivo**: Contenedor Docker que ejecuta el servicio vulnerable sobre un nodo EC2 del Entorno_Laboratorio; es la unidad sobre la que se realiza la prueba de penetración autorizada.
- **DVWA**: Damn Vulnerable Web Application, aplicación web vulnerable intencionalmente, ejecutada dentro de un Contenedor_Objetivo en el Entorno_Laboratorio.
- **Hook_Autorizacion**: Hook `PreToolUse` que demuestra el patrón "Authorization First" (EH_GRANT_PATH del starter) de forma simulada; registra y advierte sin bloquear estrictamente.
- **Hook_Auditoria**: Hook `PostToolUse` que registra un resumen de la invocación de herramientas para trazabilidad.
- **Flujo_Investigacion**: Secuencia de investigación forense de seis fases Detect → Isolate → Collect → Preserve → Analyze → Report, según `digitalforensic/proceso-digital-forensic.md`.
- **Orden_Volatilidad**: Orden de recolección de evidencia de lo más volátil a lo menos volátil (RFC 3227) aplicado en la fase Collect del Flujo_Investigacion.
- **Cadena_Custodia**: Registro documentado de cada traspaso y transformación de evidencia digital.
- **Principios_Eticos**: Conjunto de seis principios: Authorization First, Scope Discipline, Do No Harm, Confidentiality, Full Disclosure, Legal Compliance.
- **Principios_Forenses**: Conjunto de siete principios que aplican en todas las fases del Flujo_Investigacion: Evidence Integrity, Chain of Custody, Reproducibility, Minimization, Objectivity, Documentation y Legal Admissibility.
- **Power_DFIR_Linux**: Power propuesto `dfir-linux` que guía el forense en host Linux (live response, sistemas de archivos, imagen `dd`/`dc3dd`, hashes, logs `auth`/`audit`/`wtmp`, persistencia, Autopsy), descrito en `digitalforensic/propuesta-powers-digital-forensic.md`.
- **Power_Network_Forensics**: Power propuesto `network-forensics` que guía el forense de red (tcpdump/Wireshark, filtros BPF, NetFlow con Suricata, Snort, TLS/SSL), descrito en `digitalforensic/propuesta-powers-digital-forensic.md`.
- **GameDay**: Ejercicio de aprendizaje interactivo, gamificado y por equipos de AWS que valida funcionalmente el sistema mediante escenarios "de la brecha a la solución" (breach-to-solution) sobre incidentes activos en la nube; no constituye rúbrica ni criterio de calificación.
- **Lider_Tecnico**: Rol de alumno responsable de integrar el Agente_Orquestador y todos los Powers de los demás alumnos.
- **Entregable**: Artefacto producido por un alumno o equipo (Power, custom agent, hook, reporte, artefacto de gobernanza o forense) que se integra al sistema.
- **Modo_Ejecucion**: Parámetro seleccionable de un Power que fija el nivel de profundidad y habilidad con que el Power ejecuta sus tareas; admite los valores `script-kiddie`, `green-hat` y `pro`.
- **Modo_Script_Kiddie**: Valor de Modo_Ejecucion de nivel de entrada; el Power depende por completo de herramientas automatizadas ajenas y ejecuta comandos predefinidos sin lógica propia de análisis.
- **Modo_Green_Hat**: Valor de Modo_Ejecucion de nivel aspirante; el Power usa herramientas de terceros pero expone y explica la lógica subyacente, con fundamentos de redes, sistemas operativos y scripting (Python, C, Bash) en desarrollo y uso acotado a laboratorio controlado.
- **Modo_Pro**: Valor de Modo_Ejecucion de nivel profesional/experto (Black Hat / White Hat en lo técnico, diferenciados solo por la ética y la legalidad); el Power aplica lógica propia avanzada, puede generar herramientas o scripts propios y razona sobre la arquitectura del sistema objetivo.
- **Artefactos_Documentacion**: Conjunto de artefactos de entrega que acompañan a cada Power y que comprenden el prompt de generación del Power, las sesiones de interacción con Kiro para probarlo y la realimentación del resultado al chat/contexto que creó el Power.
- **NIST_SP_800_61**: Guía de referencia *Computer Security Incident Handling Guide* del NIST (SP 800-61) que estructura el Proceso_Respuesta_Incidentes en cuatro fases: Preparation; Detection & Analysis; Containment, Eradication & Recovery; y Post-Incident Activity.
- **Proceso_Respuesta_Incidentes**: Proceso cíclico de respuesta a incidentes basado en NIST_SP_800_61 con cuatro fases (Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity), donde las fases de Detection & Analysis y de Containment, Eradication & Recovery son iterativas y las lecciones aprendidas retroalimentan la fase Preparation. Descrito en `incidentemanagement/notas-incident-handling.md`.
- **Power_Incident_Handling**: Power base `incident-handling-nist` que sirve de cimiento al Incident_Responder y guía el Proceso_Respuesta_Incidentes según NIST_SP_800_61.
- **IOC**: Indicador de compromiso; señal estructurada de que ocurrió un incidente (IPs, hashes, nombres de archivo, dominios), documentada y compartida en formatos como STIX, YARA u OpenIOC.
- **Contencion_Corto_Plazo**: Acción de contención con mínima huella orientada a ganar tiempo y preservar evidencia (aislar el sistema en una VLAN, desconectar la red, redirigir el DNS del C2), sin apagar el sistema.
- **Contencion_Largo_Plazo**: Acción de contención con cambios persistentes (cambio de contraseñas, reglas de firewall, parches, hardening, apagado autorizado de sistemas).
- **MITRE_ATTACK**: Base de conocimiento matricial de tácticas, técnicas y subtécnicas del comportamiento adversario, usada para mapear la actividad del incidente.
- **Cyber_Kill_Chain**: Modelo de siete etapas (Recon, Weaponize, Delivery, Exploitation, Installation, Command and Control, Actions on Objectives) que describe el ciclo de vida de un ataque.
- **NIST_CSF**: NIST Cybersecurity Framework 2.0 (NIST CSWP 29); taxonomía de resultados de ciberseguridad con seis funciones (GV Govern, ID Identify, PR Protect, DE Detect, RS Respond, RC Recover), 22 categorías y 106 subcategorías, usada como lenguaje común de GRC. Descrito en `grc/02-nist-csf-2.0.md`.
- **Power_GRC_CSF**: Power base `grc-nist-csf` que sirve de cimiento al Responsable_GRC y guía la gobernanza, el riesgo y el cumplimiento usando NIST_CSF como eje. Descrito en `grc/01-fundamentos-grc.md` y `grc/02-nist-csf-2.0.md`.
- **Registro_Riesgos**: Registro de riesgos que documenta cada riesgo con su probabilidad, impacto, dueño, opción de tratamiento (mitigar, transferir, aceptar o evitar) y riesgo residual, calculado con un método estandarizado conforme a GV.RM-06 del NIST_CSF.
- **Apetito_Riesgo**: Cantidad de riesgo que la organización está dispuesta a asumir para lograr sus objetivos; el riesgo residual del Registro_Riesgos debe mantenerse dentro del Apetito_Riesgo.
- **Perfil_CSF**: Perfil organizacional del NIST_CSF que describe el estado de los resultados del Core; comprende un perfil actual y un perfil objetivo cuya comparación produce el gap analysis y el plan de acción (POA&M).
- **POA_M**: Plan de acción e hitos (Plan of Action and Milestones) derivado del gap analysis entre el perfil actual y el perfil objetivo del Perfil_CSF.
- **Modelo_Tres_Lineas**: Modelo de gobierno (IIA, 2020) con órgano de gobierno, primera línea (operación), segunda línea (riesgos, cumplimiento, CISO) y tercera línea (auditoría interna); el trabajo técnico de Red/Blue/DF/VA aporta evidencia a la segunda y tercera línea.
- **Repositorio_Base**: Repositorio de GitHub mantenido por el docente (upstream) que contiene la estructura del agente integrado y del cual el Lider_Tecnico crea su fork; nivel superior de la topología de tres niveles.
- **Repositorio_Integracion**: Fork del Repositorio_Base creado y mantenido por el Lider_Tecnico; repositorio de integración de la clase que recibe las contribuciones de todos los alumnos mediante Pull Request y es la única fuente integrada de Entregables.
- **Fork_Alumno**: Fork del Repositorio_Integracion creado por un alumno; repositorio personal desde el cual el alumno abre Pull Request hacia el Repositorio_Integracion; nivel inferior de la topología de tres niveles.
- **Pull_Request**: Solicitud de integración de cambios desde una rama de un Fork_Alumno hacia el Repositorio_Integracion, sujeta a validación local y revisión humana del Lider_Tecnico antes de integrarse (merge).
- **CODEOWNERS**: Archivo de GitHub que asigna la propiedad de cada ruta del repositorio a un alumno o equipo responsable, de modo que las contribuciones a una ruta queden atribuidas a su dueño.
- **Validacion_Local**: Compuerta de calidad ejecutable de forma local mediante un único punto de entrada (objetivo de Make o script) que agrega las comprobaciones de integración del sistema y no depende de ningún servicio de integración continua remoto.
- **Catalogador**: Componente que genera el archivo de inventario de entregables (inventory.json) a partir del árbol de directorios `powers/`, sin edición manual.

## Requirements

### Requirement 1: Agente Orquestador del ciclo EC-Council

**User Story:** Como Lider_Tecnico, quiero un Agente_Orquestador que coordine las fases del ciclo EC-Council delegando en subagentes, para que el agente de Ethical Hacking tome forma como un sistema integrado.

#### Acceptance Criteria

1. THE Agente_Orquestador SHALL exponer las cinco fases del ciclo EC-Council (Reconnaissance, Scanning, Gaining Access, Maintaining Access, Covering Tracks) como etapas seleccionables del flujo de trabajo.
2. WHEN el usuario solicita iniciar o avanzar una fase del ciclo, THE Agente_Orquestador SHALL delegar la ejecución en el Subagente_Fase correspondiente a esa fase.
3. THE Agente_Orquestador SHALL mantener el orden secuencial de fases Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks como secuencia por defecto.
4. WHEN un Subagente_Fase finaliza su tarea, THE Agente_Orquestador SHALL consolidar los resultados de esa fase antes de ofrecer la transición a la fase siguiente.
5. WHERE el usuario solicita una fase específica fuera de orden, THE Agente_Orquestador SHALL registrar la solicitud e indicar las fases previas no completadas antes de delegar.
6. THE Agente_Orquestador SHALL identificar cada subagente invocado y la fase o rol que representa en la respuesta entregada al usuario.

### Requirement 2: Subagentes por fase ofensiva

**User Story:** Como miembro del Red Team, quiero que cada fase del ciclo EC-Council esté manejada por un Subagente_Fase dedicado implementado como Kiro custom agent, para que cada etapa tenga una capacidad especializada y trazable.

#### Acceptance Criteria

1. THE Agente_Orquestador SHALL disponer de un Subagente_Fase distinto para cada una de las cinco fases del ciclo EC-Council.
2. WHEN se activa el Subagente_Fase de Reconnaissance, THE Subagente_Fase SHALL usar al menos un Power de reconocimiento (p. ej. OSINT pasivo o footprinting) para reunir información del objetivo autorizado.
3. WHEN se activa el Subagente_Fase de Scanning, THE Subagente_Fase SHALL usar al menos un Power de descubrimiento y enumeración de puertos y servicios sobre objetivos de la Allowlist_Objetivos.
4. WHEN se activa el Subagente_Fase de Gaining Access, THE Subagente_Fase SHALL usar al menos un Power de evaluación de vulnerabilidades o explotación limitada a prueba de concepto contra el Entorno_Laboratorio.
5. WHEN se activa el Subagente_Fase de Maintaining Access, THE Subagente_Fase SHALL usar al menos un Power de gestión de persistencia o sesiones acotado al Entorno_Laboratorio.
6. WHEN se activa el Subagente_Fase de Covering Tracks, THE Subagente_Fase SHALL usar al menos un Power de análisis o manipulación de rastros acotado al Entorno_Laboratorio y SHALL registrar las acciones realizadas para trazabilidad.
7. THE Subagente_Fase SHALL declarar explícitamente el objetivo y el alcance de su actividad antes de invocar una Herramienta_Real.

### Requirement 3: Equipo Red Team

**User Story:** Como alumno del Red Team (3 integrantes), quiero implementar Powers ofensivos que cubran las cinco fases del ciclo EC-Council, para demostrar pruebas de seguridad autorizadas sobre el Entorno_Laboratorio.

#### Acceptance Criteria

1. THE Red_Team SHALL cubrir con sus Powers las cinco fases ofensivas del ciclo EC-Council.
2. THE Red_Team SHALL implementar un mínimo de dos Powers por cada integrante del equipo.
3. WHERE un Power del Red_Team usa una Herramienta_Real de PenTest, THE Power SHALL dirigir la herramienta únicamente a objetivos presentes en la Allowlist_Objetivos.
4. WHEN un Power del Red_Team ejecuta una acción ofensiva, THE Power SHALL producir un registro de la acción consumible por los subagentes de Blue Team y Digital Forensics.

### Requirement 4: Equipo Blue Team

**User Story:** Como alumno del Blue Team (3 integrantes), quiero implementar Powers defensivos y de detección, para identificar y analizar los ataques generados por el Red Team sobre el Entorno_Laboratorio.

#### Acceptance Criteria

1. THE Blue_Team SHALL implementar Powers de detección, análisis de logs y hardening del Entorno_Laboratorio.
2. THE Blue_Team SHALL implementar un mínimo de dos Powers por cada integrante del equipo.
3. WHEN una acción ofensiva del Red_Team genera registros, THE Blue_Team SHALL disponer de al menos un Power capaz de analizar esos registros para detectar la actividad.
4. WHERE un Power del Blue_Team identifica actividad sospechosa, THE Power SHALL producir un hallazgo de detección con la evidencia que lo sustenta.

### Requirement 5: Equipo Digital Forensics

**User Story:** Como alumno de Digital Forensics (4 integrantes), quiero implementar Powers que sigan el Flujo_Investigacion forense de seis fases y sus principios, para recolectar, preservar y analizar evidencia digital de forma íntegra.

#### Acceptance Criteria

1. THE Digital_Forensics_Team SHALL implementar Powers que cubran las seis fases del Flujo_Investigacion: Detect, Isolate, Collect, Preserve, Analyze y Report.
2. THE Digital_Forensics_Team SHALL implementar un mínimo de dos Powers por cada integrante del equipo.
3. WHEN un Power de Digital_Forensics_Team recolecta evidencia, THE Power SHALL calcular y registrar un hash de verificación de la evidencia recolectada.
4. THE Digital_Forensics_Team SHALL mantener una Cadena_Custodia que documente cada traspaso y transformación de la evidencia.
5. WHERE un Power de Digital_Forensics_Team usa una Herramienta_Real de forense (p. ej. análisis de memoria o de disco), THE Power SHALL operar siempre sobre una copia verificada por hash y SHALL abstenerse de alterar la evidencia original.
6. WHEN un Power de Digital_Forensics_Team recolecta evidencia en la fase Collect, THE Power SHALL seguir el Orden_Volatilidad (RFC 3227), recolectando primero la evidencia más volátil antes que la menos volátil.
7. THE Digital_Forensics_Team SHALL limitar su alcance a evidencia de sistemas Linux y de nube (AWS), y SHALL tratar los sistemas Windows como fuera de alcance.
8. THE Digital_Forensics_Team SHALL reconocer los Powers propuestos Power_DFIR_Linux (`dfir-linux`) y Power_Network_Forensics (`network-forensics`) como base para los Powers de forense de host y de red respectivamente.
9. WHERE la evidencia reside en un Contenedor_Objetivo, THE Digital_Forensics_Team SHALL tratarla como evidencia efímera y SHALL recolectarla mediante un procedimiento automatizado antes de que el contenedor desaparezca.
10. WHEN concluye una investigación, THE Digital_Forensics_Team SHALL producir un reporte que incluya los hallazgos, la evidencia asociada y la Cadena_Custodia.

### Requirement 6: Responsable de GRC

**User Story:** Como alumno responsable de GRC (1 integrante), quiero implementar Powers y artefactos de gobernanza, para asegurar la autorización, el alcance y el cumplimiento ético del engagement.

#### Acceptance Criteria

1. THE Responsable_GRC SHALL implementar Powers o artefactos que gestionen autorización, definición de alcance, cumplimiento ético y Cadena_Custodia.
2. THE Responsable_GRC SHALL implementar un mínimo de dos Powers que usen herramientas o artefactos verificables.
3. THE Responsable_GRC SHALL mantener la Allowlist_Objetivos como registro de los objetivos autorizados del Entorno_Laboratorio.
4. WHEN se define un nuevo engagement, THE Responsable_GRC SHALL registrar el alcance autorizado y los Principios_Eticos aplicables al engagement.
5. THE Responsable_GRC SHALL reconocer el Power_GRC_CSF (`grc-nist-csf`) como cimiento de sus Powers y artefactos de gobernanza.
6. THE Responsable_GRC SHALL usar NIST_CSF como lenguaje común para expresar los resultados de gobierno, riesgo y cumplimiento del engagement.
7. THE Responsable_GRC SHALL mantener un Registro_Riesgos que registre, por cada riesgo, su probabilidad, impacto, dueño, opción de tratamiento y riesgo residual.
8. WHEN el Responsable_GRC registra el riesgo residual de un riesgo, THE Responsable_GRC SHALL verificar que el riesgo residual queda dentro del Apetito_Riesgo definido para el engagement.
9. THE Responsable_GRC SHALL producir un Perfil_CSF con un perfil actual y un perfil objetivo, y SHALL derivar de su comparación un gap analysis con su POA_M.
10. WHEN el Red_Team, el Blue_Team, el Digital_Forensics_Team o una evaluación de vulnerabilidades produce un hallazgo, THE Responsable_GRC SHALL vincular el hallazgo a una subcategoría de NIST_CSF como evidencia.

### Requirement 7: Incident Responder

**User Story:** Como alumno Incident Responder (1 integrante), quiero implementar Powers que conecten la detección con el forense, para contener y responder a los incidentes detectados en el Entorno_Laboratorio.

#### Acceptance Criteria

1. THE Incident_Responder SHALL implementar Powers que vinculen los hallazgos de detección del Blue_Team con el Flujo_Investigacion del Digital_Forensics_Team.
2. THE Incident_Responder SHALL implementar un mínimo de dos Powers que usen herramientas de respuesta o contención.
3. WHEN el Blue_Team produce un hallazgo de detección, THE Incident_Responder SHALL disponer de un Power que inicie una acción de contención o respuesta acotada al Entorno_Laboratorio.
4. WHEN se ejecuta una acción de contención, THE Incident_Responder SHALL registrar la acción y notificar al Digital_Forensics_Team para la recolección de evidencia.
5. THE Incident_Responder SHALL reconocer el Power_Incident_Handling (`incident-handling-nist`) como cimiento de sus Powers.
6. THE Incident_Responder SHALL operar según las cuatro fases del Proceso_Respuesta_Incidentes (Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity) definido en NIST_SP_800_61.
7. WHEN el Incident_Responder ejecuta una acción de contención, THE Incident_Responder SHALL distinguir entre Contencion_Corto_Plazo, que aísla el sistema y preserva la evidencia sin apagarlo, y Contencion_Largo_Plazo, que aplica cambios persistentes.
8. THE Incident_Responder SHALL mantener los IOC del incidente y la Cadena_Custodia de la evidencia asociada.
9. IF el Incident_Responder detecta movimiento lateral hacia otro sistema o departamento, THEN THE Incident_Responder SHALL escalar el incidente y registrar el escalamiento.

### Requirement 8: Líder Técnico e integración

**User Story:** Como Lider_Tecnico (1 integrante), quiero integrar el Agente_Orquestador con todos los Powers y subagentes de los alumnos, para que el sistema funcione como un agente de Ethical Hacking y Digital Forensics unificado.

#### Acceptance Criteria

1. THE Lider_Tecnico SHALL integrar el Agente_Orquestador con los Powers y los custom agents producidos por todos los equipos.
2. WHEN un alumno entrega un Power conforme al modelo de Powers definido, THE Lider_Tecnico SHALL incorporar el Power al sistema de forma que quede disponible para el subagente correspondiente.
3. THE Lider_Tecnico SHALL verificar que cada fase del ciclo EC-Council y cada etapa del Flujo_Investigacion cuente con al menos un Power integrado.
4. IF un Entregable no cumple el modelo de Powers o la política ética definida, THEN THE Lider_Tecnico SHALL rechazar la integración del Entregable e indicar el incumplimiento.

### Requirement 9: Modelo de Powers y herramientas

**User Story:** Como alumno de cualquier equipo, quiero un modelo común de Powers que envuelvan herramientas reales de Kali, para que cada capacidad del sistema sea reutilizable por los subagentes.

#### Acceptance Criteria

1. THE Power SHALL envolver al menos una Herramienta_Real de Kali Linux de PenTest o Digital Forensics.
2. THE Power SHALL declarar la fase del ciclo EC-Council o la etapa del Flujo_Investigacion a la que contribuye.
3. THE Power SHALL ser invocable por al menos un Subagente_Fase o Subagente_Rol.
4. THE sistema SHALL reutilizar los Powers base existentes (osint-passive-recon, footprinting-enumeration, exploitation-metasploit, vulnerability-assessment) como referencia o cimiento de los Powers nuevos.
5. WHEN un Power invoca una Herramienta_Real, THE Power SHALL recibir como entrada el objetivo y validar que el objetivo pertenece a la Allowlist_Objetivos antes de ejecutar la herramienta.
6. THE cada alumno SHALL implementar un mínimo de dos Powers que usen Herramienta_Real.
7. THE Power SHALL aceptar un Modo_Ejecucion seleccionable con valores `script-kiddie`, `green-hat` y `pro` según se define en el Requirement 14.
8. THE Power SHALL entregar sus Artefactos_Documentacion asociados según se define en el Requirement 15.

### Requirement 10: Hooks de autorización simulada

**User Story:** Como docente, quiero hooks `PreToolUse` que demuestren el patrón "Authorization First" de forma didáctica, para enseñar el control de autorización sin bloquear el ejercicio en el aula.

#### Acceptance Criteria

1. WHEN un subagente va a invocar una Herramienta_Real a través de un Power, THE Hook_Autorizacion SHALL evaluar la autorización según el patrón EH_GRANT_PATH del starter y registrar el resultado de la evaluación.
2. WHERE la autorización simulada no está presente o no cubre el objetivo, THE Hook_Autorizacion SHALL emitir una advertencia didáctica sin bloquear estrictamente la ejecución.
3. THE Hook_Autorizacion SHALL identificar la Herramienta_Real y el objetivo declarado en el registro de evaluación.
4. WHEN se completa la invocación de una Herramienta_Real, THE Hook_Auditoria SHALL registrar un resumen de la invocación, incluyendo un hash de los datos recibidos, para trazabilidad.
5. THE hooks SHALL seguir el formato independiente `version: v1` de Kiro CLI V3 / IDE.

### Requirement 11: Política ética y seguridad de laboratorio

**User Story:** Como docente responsable del ejercicio, quiero que el sistema aplique los Principios_Eticos y restrinja la actividad al Entorno_Laboratorio, para garantizar un uso autorizado, acotado y seguro.

#### Acceptance Criteria

1. THE sistema SHALL dirigir toda actividad ofensiva y forense únicamente a objetivos presentes en la Allowlist_Objetivos.
2. IF un objetivo solicitado no pertenece a la Allowlist_Objetivos, THEN THE sistema SHALL rechazar la acción e indicar que el objetivo está fuera del alcance autorizado.
3. THE sistema SHALL tratar cualquier objetivo que no sea del Entorno_Laboratorio como producción no autorizada y SHALL abstenerse de actuar sobre él.
4. THE sistema SHALL dirigir toda prueba de penetración al Contenedor_Objetivo que expone el servicio y SHALL abstenerse de explotar el host EC2 subyacente, salvo que la Allowlist_Objetivos autorice ese host explícitamente.
5. THE sistema SHALL aplicar los Principios_Eticos (Authorization First, Scope Discipline, Do No Harm, Confidentiality, Full Disclosure, Legal Compliance) como restricciones de comportamiento del Agente_Orquestador y de los subagentes.
6. WHILE un engagement está activo, THE sistema SHALL mantener la actividad dentro del alcance autorizado registrado para ese engagement.
7. WHEN el sistema produce un hallazgo, THE sistema SHALL reportar el hallazgo de forma completa y honesta conforme al principio Full Disclosure.
8. THE sistema SHALL proteger la confidencialidad de los datos descubiertos durante el engagement conforme al principio Confidentiality.

### Requirement 12: Entorno objetivo DVWA en contenedores Docker sobre EC2 Debian

**User Story:** Como equipo del proyecto, quiero un Entorno_Laboratorio con DVWA y servicios vulnerables ejecutados en contenedores Docker sobre nodos EC2 Debian y los casos de referencia ya trabajados, para disponer de objetivos vulnerables autorizados y reproducibles.

#### Acceptance Criteria

1. THE Entorno_Laboratorio SHALL estar compuesto por nodos EC2 con Debian que ejecutan DVWA y los servicios vulnerables de referencia dentro de contenedores Docker.
2. THE sistema SHALL exponer cada servicio vulnerable como un Contenedor_Objetivo identificable sobre su nodo EC2 anfitrión.
3. WHEN un subagente realiza una prueba de penetración, THE sistema SHALL dirigir la actividad al Contenedor_Objetivo que expone el servicio y no al host EC2 subyacente, salvo autorización explícita en la Allowlist_Objetivos.
4. THE sistema SHALL reconocer los casos de referencia existentes (ethicalhacking, footprinting, nmap_enumeration) como fuentes de objetivos y escenarios del Entorno_Laboratorio.
5. THE Allowlist_Objetivos SHALL enumerar los Contenedores_Objetivo autorizados del Entorno_Laboratorio como único conjunto de objetivos válidos.
6. WHEN se agrega o retira un Contenedor_Objetivo o un nodo del Entorno_Laboratorio, THE Allowlist_Objetivos SHALL actualizarse para reflejar los objetivos autorizados vigentes.

### Requirement 13: Integración de entregables

**User Story:** Como Lider_Tecnico y docente, quiero que los Entregables de los alumnos se integren de forma consistente en el sistema, para que el agente completo refleje el trabajo de todos los equipos.

#### Acceptance Criteria

1. THE sistema SHALL organizar los Entregables por equipo y rol (Red Team, Blue Team, Digital Forensics, GRC, Incident Responder, Lider_Tecnico).
2. THE sistema SHALL asociar cada Power entregado con la fase del ciclo EC-Council o la etapa del Flujo_Investigacion que cubre.
3. WHEN todos los Entregables de una fase están integrados, THE sistema SHALL habilitar la fase correspondiente en el Agente_Orquestador.
4. THE sistema SHALL mantener un inventario de los Powers y custom agents integrados, con el equipo o alumno responsable de cada uno.
5. WHERE un Entregable es un reporte o artefacto de gobernanza o forense, THE sistema SHALL vincularlo con el engagement y con la Cadena_Custodia correspondiente.

### Requirement 14: Modos de ejecución por Power

**User Story:** Como alumno de cualquier equipo, quiero seleccionar el Modo_Ejecucion de un Power entre `script-kiddie`, `green-hat` y `pro`, para ejecutar la especialización técnica del Power al nivel de profundidad y habilidad que corresponda al ejercicio.

#### Acceptance Criteria

1. THE Power SHALL exponer el Modo_Ejecucion como parámetro seleccionable que admite exactamente los valores `script-kiddie`, `green-hat` y `pro`.
2. WHERE no se indica un Modo_Ejecucion al invocar el Power, THE Power SHALL aplicar el modo `script-kiddie` como valor por defecto.
3. WHILE el Modo_Ejecucion es `script-kiddie`, THE Power SHALL ejecutar la Herramienta_Real mediante comandos predefinidos automatizados sin añadir lógica propia de análisis.
4. WHILE el Modo_Ejecucion es `green-hat`, THE Power SHALL ejecutar la Herramienta_Real y SHALL incluir en su salida una explicación de la lógica subyacente de los comandos y herramientas empleados.
5. WHILE el Modo_Ejecucion es `pro`, THE Power SHALL aplicar lógica propia avanzada que razone sobre la arquitectura del objetivo y SHALL poder generar comandos o scripts propios además de invocar la Herramienta_Real.
6. WHEN el Power ejecuta una tarea, THE Power SHALL registrar el Modo_Ejecucion aplicado en el registro de ejecución consumible por el Hook_Auditoria.
7. IF se solicita un Modo_Ejecucion con un valor distinto de `script-kiddie`, `green-hat` o `pro`, THEN THE Power SHALL rechazar la invocación e indicar los valores de Modo_Ejecucion admitidos.
8. THE diferencia entre los perfiles Black Hat y White Hat SHALL representarse mediante la Política ética (Requirement 11) y no mediante el Modo_Ejecucion, de modo que el modo `pro` describa únicamente el nivel técnico.

### Requirement 15: Artefactos de documentación por Power

**User Story:** Como alumno de cualquier equipo, quiero documentar y entregar los Artefactos_Documentacion de cada Power que implemento, para evidenciar que entiendo lo que el Power genera.

#### Acceptance Criteria

1. THE alumno SHALL entregar, por cada Power implementado, los Artefactos_Documentacion que comprenden el prompt de generación del Power, las sesiones de interacción con Kiro para probar el Power y la realimentación del resultado al chat/contexto que creó el Power.
2. THE Artefactos_Documentacion SHALL incluir el prompt usado para generar el Power.
3. THE Artefactos_Documentacion SHALL incluir el registro de las sesiones de interacción con Kiro empleadas para probar el Power.
4. THE Artefactos_Documentacion SHALL incluir la realimentación del resultado devuelta al chat/contexto que creó el Power para su análisis.
5. THE sistema SHALL asociar los Artefactos_Documentacion con el Power al que corresponden y con el alumno responsable del Power.
6. WHERE un Power carece de alguno de los Artefactos_Documentacion requeridos, THE sistema SHALL señalar el artefacto faltante al integrar el Power.

### Requirement 16: Principios forenses transversales

**User Story:** Como alumno de Digital Forensics y como docente, quiero que los siete Principios_Forenses se apliquen como invariantes verificables en todas las fases del Flujo_Investigacion, para garantizar que la evidencia sea íntegra, reproducible y admisible.

#### Acceptance Criteria

1. THE Digital_Forensics_Team SHALL aplicar los siete Principios_Forenses (Evidence Integrity, Chain of Custody, Reproducibility, Minimization, Objectivity, Documentation, Legal Admissibility) en todas las fases del Flujo_Investigacion.
2. WHEN un Power de Digital_Forensics_Team analiza evidencia, THE Power SHALL operar sobre una copia verificada por hash conforme al principio Evidence Integrity.
3. WHEN la evidencia cambia de responsable o de ubicación, THE Digital_Forensics_Team SHALL registrar el traspaso en la Cadena_Custodia conforme al principio Chain of Custody.
4. THE Digital_Forensics_Team SHALL registrar por cada paso el comando, la hora en UTC, la herramienta, la versión y el resultado, de modo que otro analista reproduzca el mismo resultado conforme a los principios Documentation y Reproducibility.
5. THE Digital_Forensics_Team SHALL recolectar únicamente la evidencia necesaria para el alcance de la investigación conforme al principio Minimization.
6. WHEN el Digital_Forensics_Team documenta un hallazgo, THE Digital_Forensics_Team SHALL registrar también la evidencia que contradice la hipótesis conforme al principio Objectivity.
7. THE Digital_Forensics_Team SHALL preservar la evidencia con verificación de hash y almacenamiento de solo escritura única conforme al principio Legal Admissibility.
8. WHERE la evidencia proviene de un Contenedor_Objetivo, THE Digital_Forensics_Team SHALL recolectarla mediante un procedimiento automatizado que preserve su integridad antes de que el contenedor efímero desaparezca.

### Requirement 17: Validación mediante GameDay

**User Story:** Como docente y como Lider_Tecnico, quiero validar funcionalmente el agente completo en un AWS GameDay de seguridad, para comprobar que el sistema investiga incidentes, preserva evidencia y contiene amenazas sin interrumpir servicios.

#### Acceptance Criteria

1. THE sistema SHALL ser validado funcionalmente mediante un GameDay con escenarios "de la brecha a la solución" (breach-to-solution) sobre incidentes activos en la nube.
2. WHEN se ejecuta un escenario de GameDay, THE sistema SHALL investigar el incidente activo coordinando los Subagentes_Rol de Red Team, Blue Team, Digital Forensics, GRC e Incident Responder a través del Agente_Orquestador.
3. WHEN el sistema investiga un incidente de GameDay, THE sistema SHALL preservar la evidencia aplicando Evidence Integrity y Chain of Custody conforme al Requirement 16.
4. WHEN el sistema analiza un incidente de GameDay, THE sistema SHALL rastrear los indicadores de compromiso (IOCs) mediante análisis de logs.
5. WHEN el sistema responde a un incidente de GameDay, THE sistema SHALL aplicar contención y hardening de la infraestructura manteniendo disponibles los servicios afectados.
6. THE GameDay SHALL servir como escenario de validación funcional del sistema y no SHALL constituir rúbrica ni criterio de calificación de los alumnos.

### Requirement 18: Proceso de respuesta a incidentes (NIST SP 800-61)

**User Story:** Como Incident_Responder y como docente, quiero que la respuesta a incidentes siga el Proceso_Respuesta_Incidentes de NIST SP 800-61 con sus cuatro fases, para gestionar los incidentes del Entorno_Laboratorio de forma sistemática, coordinada y trazable.

#### Acceptance Criteria

1. THE sistema SHALL reconocer el Power_Incident_Handling (`incident-handling-nist`) como base del Proceso_Respuesta_Incidentes.
2. THE Proceso_Respuesta_Incidentes SHALL comprender las cuatro fases de NIST_SP_800_61: Preparation; Detection & Analysis; Containment, Eradication & Recovery; y Post-Incident Activity.
3. WHILE el Proceso_Respuesta_Incidentes está en la fase Preparation, THE Incident_Responder SHALL mantener disponibles la documentación, los contactos y las herramientas de respuesta antes de que ocurra un incidente.
4. WHEN el Blue_Team detecta un evento con consecuencia negativa, THE Incident_Responder SHALL iniciar la fase Detection & Analysis estableciendo el contexto y la línea de tiempo del incidente.
5. WHILE el Proceso_Respuesta_Incidentes está en la fase Detection & Analysis o en la fase Containment, Eradication & Recovery, THE Incident_Responder SHALL iterar entre crear y usar IOC, identificar nuevas pistas y sistemas impactados, y recolectar y analizar datos.
6. WHEN concluye la respuesta a un incidente, THE Incident_Responder SHALL ejecutar la fase Post-Incident Activity produciendo un reporte final y una sesión de lecciones aprendidas.
7. WHEN la fase Post-Incident Activity produce lecciones aprendidas, THE Incident_Responder SHALL retroalimentar la fase Preparation con esas lecciones, de modo que el Proceso_Respuesta_Incidentes sea cíclico.
8. WHEN el Proceso_Respuesta_Incidentes requiere datos de detección, THE Incident_Responder SHALL coordinarse con el Blue_Team, y WHEN requiere recolección o preservación de evidencia, THE Incident_Responder SHALL coordinarse con el Digital_Forensics_Team.
9. THE Incident_Responder SHALL documentar los IOC del incidente en al menos uno de los formatos STIX, YARA u OpenIOC.
10. WHEN el Incident_Responder analiza la actividad de un incidente, THE Incident_Responder SHALL mapear la actividad a tácticas y técnicas de MITRE_ATTACK y a etapas de la Cyber_Kill_Chain.
11. THE Proceso_Respuesta_Incidentes SHALL mantener coherencia con el flujo cruzado Red_Team → Blue_Team → Incident_Responder → Digital_Forensics_Team y SHALL ser ejercitable dentro de la validación mediante GameDay definida en el Requirement 17.

### Requirement 19: Gobernanza con NIST CSF 2.0

**User Story:** Como Responsable_GRC y como docente, quiero gobernar el engagement con NIST CSF 2.0, para registrar riesgos, medir brechas y aportar evidencia técnica a las líneas de defensa con un lenguaje común.

#### Acceptance Criteria

1. THE sistema SHALL reconocer el Power_GRC_CSF (`grc-nist-csf`) como base de la gobernanza con NIST_CSF.
2. WHEN el Responsable_GRC gestiona un requisito de ley, contrato, norma o política, THE Responsable_GRC SHALL mapear el requisito a una subcategoría de NIST_CSF, de esa subcategoría a un control y del control a su evidencia.
3. THE Responsable_GRC SHALL registrar cada riesgo en el Registro_Riesgos mediante un método estandarizado de cálculo, documentación, categorización y priorización conforme a GV.RM-06 del NIST_CSF.
4. WHEN el Responsable_GRC evalúa la postura del engagement, THE Responsable_GRC SHALL expresarla como un Perfil_CSF con perfil actual y perfil objetivo, y SHALL declarar el Tier objetivo entre los niveles 1 a 4.
5. WHEN la comparación entre el perfil actual y el perfil objetivo revela una brecha, THE Responsable_GRC SHALL registrar la brecha en el POA_M y SHALL registrar el riesgo asociado en el Registro_Riesgos.
6. THE Responsable_GRC SHALL aportar los hallazgos técnicos del Red_Team, el Blue_Team, el Digital_Forensics_Team y las evaluaciones de vulnerabilidades como evidencia a la segunda y tercera línea del Modelo_Tres_Lineas.
7. THE Responsable_GRC SHALL alinear la terminología de las funciones RS y RC del NIST_CSF con el Proceso_Respuesta_Incidentes del Power_Incident_Handling definido en el Requirement 18.

### Requirement 20: Colaboración y entrega mediante GitHub (fork + Pull Request) con validación local

**User Story:** Como Lider_Tecnico y como alumno de cualquier equipo, quiero un modelo de colaboración de tres niveles basado en forks y Pull Request de GitHub con una compuerta de validación local, para integrar el trabajo de los 13 alumnos en un agente unificado sin depender de integración continua remota.

#### Acceptance Criteria

1. THE sistema SHALL organizar la colaboración en una topología de tres niveles donde el docente mantiene el Repositorio_Base (upstream) con la estructura del agente, el Lider_Tecnico mantiene el Repositorio_Integracion como fork del Repositorio_Base, y cada alumno mantiene un Fork_Alumno creado a partir del Repositorio_Integracion.
2. THE alumno SHALL contribuir sus Entregables exclusivamente mediante Pull_Request desde su Fork_Alumno hacia el Repositorio_Integracion, sin disponer de permiso de escritura directa sobre el Repositorio_Integracion.
3. THE alumno SHALL realizar su trabajo en una rama propia con el patrón de nombre `power/<equipo>-<iniciales>-<nombre-power>` y SHALL abstenerse de trabajar sobre la rama base o de partida.
4. THE alumno SHALL ubicar cada Power contribuido en su propia carpeta `powers/<equipo>/<power>/`, y THE sistema SHALL asignar la propiedad de cada ruta a su alumno o equipo responsable mediante un archivo CODEOWNERS.
5. WHEN un alumno abre un Pull_Request de entrega de un Power, THE Pull_Request SHALL incluir el Power (su `plugin.json` o `POWER.md` con el contrato `x-ethack`), sus directorios `skills/` y `steering/`, y sus Artefactos_Documentacion (`docs/prompt.md`, `docs/sessions/` y `docs/feedback.md`) definidos en el Requirement 15.
6. THE sistema SHALL ofrecer una Validacion_Local ejecutable mediante un único punto de entrada (objetivo de Make o script) que agregue el adaptador de formatos, la comprobación de Artefactos_Documentacion, la guardia de Allowlist_Objetivos, la verificación de cobertura de fases del ciclo EC-Council y de etapas del Flujo_Investigacion, y el conteo de al menos dos Powers con Herramienta_Real por alumno, sin depender de un servicio de integración continua remoto.
7. WHEN un alumno va a abrir un Pull_Request, THE alumno SHALL ejecutar previamente la Validacion_Local, y WHEN el Lider_Tecnico va a integrar un Pull_Request, THE Lider_Tecnico SHALL ejecutar la Validacion_Local y revisar el Pull_Request antes de la integración.
8. IF un Pull_Request no pasa la Validacion_Local o no supera la revisión del Lider_Tecnico, THEN THE Lider_Tecnico SHALL abstenerse de integrar (merge) el Pull_Request e indicar el incumplimiento.
9. THE sistema SHALL generar el archivo de inventario de entregables `inventory.json` a partir del árbol `powers/` mediante el Catalogador, y THE sistema SHALL abstenerse de permitir su edición manual, para evitar conflictos de merge en archivos compartidos.
10. WHEN el docente publica actualizaciones del Repositorio_Base, THE Lider_Tecnico SHALL incorporarlas sincronizando el Repositorio_Integracion desde el upstream, y THE alumno SHALL sincronizar su Fork_Alumno desde el Repositorio_Integracion.
11. THE sistema SHALL mantener la compuerta de calidad como la Validacion_Local más la revisión del Lider_Tecnico, y SHALL abstenerse de depender de GitHub Actions o de cualquier otro servicio de integración continua remoto.
