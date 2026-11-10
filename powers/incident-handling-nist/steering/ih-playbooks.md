# Playbooks por tipo de incidente

Cada playbook sigue las fases de NIST y respeta las reglas R1–R12. Son una base para laboratorio y
clase; una organización real los adapta a sus herramientas y políticas.

Elegir el playbook según el tipo de incidente de la investigación inicial. Si hay varios (p. ej.
phishing que termina en ransomware), seguir el más grave y usar el otro para la fase de entrada.

---

## 1. Phishing

**Casos del curso:** U.S. Interior (evil twin), Twitter 2020 (ingeniería social).

| Fase | Pasos |
|---|---|
| Detección | Reporte del usuario o del gateway. Obtener el correo **con headers** (.eml). Revisar SPF/DKIM/DMARC, remitente real, `Reply-To`, enlaces y adjuntos (hash, sin abrirlos). |
| Alcance | Buscar el mismo remitente, asunto, URL o hash en todos los buzones. ¿Quién hizo clic? ¿Quién ejecutó el adjunto? ¿Quién ingresó credenciales? |
| Contención | Purgar el correo de todos los buzones. Bloquear remitente, dominio y URL. Para quien ingresó credenciales: reset y revocar sesiones (ver playbook 3). Para quien ejecutó el adjunto: aislar el equipo (ver playbook 2 si hay malware). |
| Erradicación | Eliminar reglas de buzón creadas por el atacante (reenvío, borrado). Eliminar el payload y su persistencia. |
| Recuperación | Monitorear las cuentas afectadas (logons nuevos, reglas de buzón). |
| Post-incidente | ¿DMARC está en `reject`? ¿El usuario reportó rápido? Usar el caso en la concientización. |

ATT&CK típico: T1566.001/.002, T1204.002, T1078.

---

## 2. Malware / ransomware

**Casos del curso:** WannaCry, Colonial Pipeline, Confluence → LockBit.

| Fase | Pasos |
|---|---|
| Detección | Alerta de AV/EDR, archivos cifrados, nota de rescate, `vssadmin delete shadows`. Anotar hora y primer host. |
| Contención (urgente) | Aislar los hosts afectados **sin apagarlos** si es posible (R3: la clave de cifrado puede estar en RAM). Bloquear el C2. Deshabilitar las cuentas usadas para propagar. Cortar shares y backups en línea para protegerlos. En ransomware, la contención de corto plazo va antes que una investigación completa, pero coordinada (R2). |
| Investigación | Patient zero, vector de entrada, cuentas comprometidas, alcance de la exfiltración previa (la doble extorsión es común). |
| Erradicación | Reconstruir desde imagen limpia en lugar de "limpiar". Eliminar persistencia y cuentas del atacante en todo el dominio. Cerrar el vector. |
| Recuperación | Restaurar desde backups **anteriores al compromiso** y verificados libres de malware. Por fases y priorizando sistemas críticos. |
| Post-incidente | Pagar el rescate no se recomienda; la decisión es de la dirección con legal. Revisar backups offline, segmentación, parches. |

ATT&CK típico: T1486, T1490, T1021.002, T1570, T1003.001.

---

## 3. Credenciales comprometidas

**Casos del curso:** Colonial Pipeline (VPN sin MFA), Mirai y LogicMonitor (credenciales por defecto).

| Fase | Pasos |
|---|---|
| Detección | Logon desde ubicación o IP rara, viaje imposible, MFA rechazado repetido, credenciales en una filtración. |
| Alcance | Todos los logons de la cuenta en la ventana de tiempo: hosts, IPs, tipo de logon. ¿Qué hizo con ella? ¿Creó cuentas o tokens? |
| Contención | Reset de contraseña, **revocar sesiones y tokens**, deshabilitar la cuenta si es necesario, bloquear IP de origen. Coordinar si hay varias cuentas (R2). |
| Erradicación | Eliminar cuentas, claves de API, apps OAuth o dispositivos MFA agregados por el atacante. Cambiar credenciales por defecto en todo lo expuesto. |
| Recuperación | Habilitar la cuenta con MFA. Monitorear logons. |
| Post-incidente | MFA en todo acceso remoto y administrativo. Eliminar cuentas inactivas (la VPN de Colonial era de una cuenta inactiva). |

ATT&CK típico: T1078.001/.002, T1110, T1133.

---

## 4. Insider

**Caso del curso:** Cash App / Block (exempleado con acceso a datos de clientes).

| Fase | Pasos |
|---|---|
| Detección | Acceso a datos fuera de su función, descargas masivas, acceso tras la baja. |
| Confidencialidad | **Need-to-know estricto (R6)**; involucrar a RR. HH. y legal desde el inicio. No alertar a la persona. |
| Investigación | Preservar evidencia con cadena de custodia (R7), porque es probable un proceso legal. Revisar accesos, correos, USB, nube personal. |
| Contención | Coordinada con RR. HH. y legal: revocar todos los accesos al mismo tiempo. |
| Erradicación / recuperación | Revisar cuentas compartidas o credenciales que conocía; rotarlas. |
| Post-incidente | Mínimo privilegio, revisión periódica de accesos, baja inmediata de cuentas al salir, monitoreo de accesos a datos sensibles. |

ATT&CK típico: T1078, T1039, T1567, T1052 (exfiltración por medio físico).

---

## 5. Aplicación expuesta a Internet

**Casos del curso:** Equifax (Struts sin parchear), Insight Nexus (ManageEngine con admin/admin y portal PHP con upload vulnerable).

| Fase | Pasos |
|---|---|
| Detección | Archivos nuevos en la raíz web, procesos hijos raros del servidor web/Java, conexiones salientes del servidor, logins admin desde IPs extranjeras. |
| Investigación | Logs de acceso web (IPs, user-agents, rutas, POST a uploads), logs de auditoría de la app, Sysmon en el servidor. Buscar web shells. Revisar qué credenciales o integraciones tenía la app (ManageEngine administraba AD). |
| Contención | Restringir la app a acceso interno o bajarla. Bloquear IPs de origen y del C2. Rotar credenciales que la app almacenaba o usaba. |
| Erradicación | Parchear, cambiar credenciales por defecto, eliminar web shells, revisar cuentas creadas desde la app. |
| Recuperación | Publicar detrás de WAF y con MFA. Logs de la app al SIEM. |
| Post-incidente | Escaneo periódico de vulnerabilidades en lo expuesto. Inventario de servicios publicados. |

ATT&CK típico: T1190, T1078.001, T1505.003, T1071.001.

---

## 6. Cadena de suministro

**Caso del curso:** SolarWinds Orion.

| Fase | Pasos |
|---|---|
| Detección | Aviso del proveedor, de un CERT o de threat intel (fuente: tercero). |
| Alcance | ¿Qué versiones del software tenemos y dónde? ¿Qué cuentas y accesos tiene ese software? Buscar los IOCs publicados (STIX de CISA) en todo el periodo desde la instalación. |
| Contención | Aislar o apagar el software afectado según la guía del proveedor/CERT. Rotar las credenciales que usaba. |
| Erradicación | Actualizar a versión limpia o reemplazar. Buscar persistencia secundaria (el atacante pudo haber ido más allá). |
| Recuperación | Monitorear las cuentas e integraciones del software. |
| Post-incidente | Inventario de software de terceros con acceso privilegiado; mínimo privilegio para herramientas de administración. |

ATT&CK típico: T1195.002 (Compromise Software Supply Chain), T1078, T1071.
