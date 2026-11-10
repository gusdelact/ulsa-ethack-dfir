# Cyber Kill Chain, MITRE ATT&CK y pirámide del dolor

## Cyber Kill Chain (7 etapas)

Sirve para estimar qué tan avanzado está el atacante y a qué tiene acceso. **Objetivo del
defensor: detenerlo en la etapa más temprana posible.**

| # | Etapa | Qué hace el atacante | Dónde buscar evidencia |
|---|---|---|---|
| 1 | Recon | Elige objetivo; información pasiva (LinkedIn, ofertas de empleo, web) o activa (escaneos). | Logs de firewall/WAF, IDS, logs web |
| 2 | Weaponize | **Desarrolla el malware** y lo embebe en un exploit o payload, pensado para evadir el AV/EDR del objetivo. | Normalmente fuera de nuestra vista (threat intel) |
| 3 | Delivery | Phishing con adjunto o enlace, web falsa, llamada con pretexto, USB. | Gateway de correo, proxy, logs DNS |
| 4 | Exploitation | Se dispara el exploit o el usuario ejecuta el payload. | EDR, Sysmon 1, logs de aplicación |
| 5 | Installation | Stager, dropper, backdoor, rootkit; persistencia. | Sysmon 11/13, servicios (7045), tareas (4698) |
| 6 | Command & Control | Canal remoto; varias variantes para sobrevivir a la contención. | Sysmon 3, proxy, DNS, firewall |
| 7 | Actions on Objectives | Exfiltración, ransomware, máximo privilegio. | File server (5140/5145), DLP, proxy |

Los atacantes **no avanzan en línea recta**: tras Installation vuelven a Recon para moverse
lateralmente.

## MITRE ATT&CK

https://attack.mitre.org/matrices/enterprise/

| Nivel | Qué es | Ejemplo |
|---|---|---|
| Táctica | El objetivo del atacante en esa fase (columna de la matriz) | Initial Access, Persistence |
| Técnica | Método concreto | T1021 Remote Services |
| Sub-técnica | Implementación específica | T1021.001 Remote Desktop Protocol |

Reportar con sub-técnica cuando se conoce: "T1003.001 (LSASS Memory)" es más útil que "T1003".

Usos: entender intención y próximos pasos, priorizar alertas sobre activos críticos, elegir
mitigaciones que corten la cadena.

## Pirámide del dolor

| Nivel (de abajo a arriba) | Ejemplo | Costo para el atacante si lo bloqueamos |
|---|---|---|
| Hashes | MD5/SHA-256 de un payload | Trivial |
| Direcciones IP | IP del C2 | Fácil (cambia de servidor) |
| Dominios | Dominio del C2 | Simple |
| Artefactos de red/host | Claves de registro, mutex, nombres de archivo, user-agent (T1547.001) | Molesto |
| Herramientas | Mimikatz, Cobalt Strike | Difícil |
| TTPs | Abuso de PowerShell (T1059.001), inyección de procesos (T1055) | **Máximo**: debe cambiar cómo opera |

Detecciones por hash/IP se evaden fácil; detecciones por comportamiento (TTPs) son más duraderas.

## Regla de verificación (R10)

Antes de escribir un ID en el reporte:

1. Abrir `https://attack.mitre.org/techniques/<ID>/` (sub-técnicas: `T1003/001/`).
2. Confirmar que el **nombre** y la **táctica** coinciden con lo observado.
3. Si no se pudo verificar, escribir `T#### (por verificar)`.

Errores encontrados en el material del curso:

| En el curso | Problema | ID correcto |
|---|---|---|
| T1078.004 para credenciales por defecto | T1078.004 es *Cloud Accounts* | **T1078.001** Default Accounts |
| T1069 como persistencia | T1069 es *Permission Groups Discovery* (Discovery) | Para el MSI por GPO: **T1484.001** Group Policy Modification; para la tarea: **T1053.005** Scheduled Task |

## Técnicas frecuentes (referencia rápida)

| Táctica | ID | Nombre | Ejemplo de evidencia |
|---|---|---|---|
| Reconnaissance | T1595 | Active Scanning | Muchos 404 o puertos sondeados desde una IP |
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment | Adjunto ejecutado desde Outlook |
| Initial Access | T1566.002 | Phishing: Spearphishing Link | Clic a dominio recién registrado |
| Initial Access | T1190 | Exploit Public-Facing Application | Web shell tras explotación de app web |
| Initial Access | T1133 | External Remote Services | RDP/VPN expuestos a Internet |
| Initial Access / Persistence | T1078.001 | Valid Accounts: Default Accounts | Login con admin/admin |
| Initial Access / Persistence | T1078.002 | Valid Accounts: Domain Accounts | Logon con cuenta de dominio robada |
| Execution | T1204.002 | User Execution: Malicious File | Usuario abre el adjunto |
| Execution | T1059.001 | Command and Scripting Interpreter: PowerShell | `powershell -enc ...` |
| Execution / Lateral | T1072 | Software Deployment Tools | Despliegue con SCCM, ManageEngine |
| Persistence | T1547.001 | Registry Run Keys / Startup Folder | Clave en `HKCU\...\Run` |
| Persistence | T1543.003 | Create or Modify System Process: Windows Service | Event 7045 |
| Persistence | T1053.005 | Scheduled Task/Job: Scheduled Task | Event 4698 |
| Persistence | T1505.003 | Server Software Component: Web Shell | `.php`/`.jsp` nuevo en la raíz web |
| Persistence | T1136.002 | Create Account: Domain Account | Event 4720 en el DC |
| Privilege Esc. / Defense Evasion | T1484.001 | Domain or Tenant Policy Modification: Group Policy Modification | Event 5136 sobre objetos GPO |
| Defense Evasion | T1218.007 | System Binary Proxy Execution: Msiexec | `msiexec /i ... /quiet` |
| Defense Evasion | T1036 | Masquerading | `java-update.msi`, `diagnostics_data.zip` |
| Defense Evasion | T1027 | Obfuscated Files or Information | PowerShell en Base64 |
| Defense Evasion | T1070.001 | Indicator Removal: Clear Windows Event Logs | Event 1102 |
| Credential Access | T1003.001 | OS Credential Dumping: LSASS Memory | Mimikatz, Sysmon 10 sobre lsass.exe |
| Credential Access | T1555.004 | Credentials from Password Stores: Windows Credential Manager | Carga de `vaultcli.dll` por proceso raro |
| Credential Access | T1110 | Brute Force | Muchos 4625 seguidos |
| Discovery | T1087.002 | Account Discovery: Domain Account | Consultas LDAP masivas |
| Discovery | T1018 | Remote System Discovery | Enumeración de equipos |
| Discovery | T1135 | Network Share Discovery | Enumeración de shares |
| Lateral Movement | T1021.001 | Remote Services: RDP | 4624 tipo 10 |
| Lateral Movement | T1021.002 | Remote Services: SMB/Windows Admin Shares | Acceso a `ADMIN$`, `C$` |
| Lateral Movement | T1570 | Lateral Tool Transfer | Copia de binarios entre hosts |
| Collection | T1039 | Data from Network Shared Drive | 5140/5145 en el file server |
| Collection | T1560.001 | Archive Collected Data: Archive via Utility | `7z`, `Compress-Archive` |
| Command and Control | T1071.001 | Application Layer Protocol: Web Protocols | Beacons HTTPS periódicos |
| Command and Control | T1105 | Ingress Tool Transfer | `curl`, `wget`, `certutil` descargando |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | Subida grande al IP del C2 |
| Exfiltration | T1567 | Exfiltration Over Web Service | Subida a almacenamiento en la nube |
| Impact | T1486 | Data Encrypted for Impact | Ransomware |
| Impact | T1490 | Inhibit System Recovery | `vssadmin delete shadows` |

Los nombres y la táctica de cada ID deben confirmarse en attack.mitre.org antes de usarlos en un
entregable (R10); ATT&CK cambia entre versiones.

## Ejemplo de mapeo del curso (Confluence → LockBit)

| Táctica | Técnica | ID | Descripción |
|---|---|---|---|
| Initial Access | Exploit Public-Facing Application | T1190 | CVE de Confluence |
| Execution | PowerShell | T1059.001 | Descarga de payload |
| Persistence | Windows Service | T1543.003 | Servicio para persistencia |
| Credential Access | LSASS Memory | T1003.001 | Extracción de credenciales |
| Lateral Movement | Remote Desktop Protocol | T1021.001 | Movimiento lateral por RDP |
| Impact | Data Encrypted for Impact | T1486 | LockBit |

## Formato de `06-mitre.md`

| Hallazgo (con fuente) | Etapa Kill Chain | Táctica | ID | Nombre | Verificado |
|---|---|---|---|---|---|
| Sysmon 1 en DEV-021: `msiexec /i C:\Windows\Temp\java-update.msi /quiet` | Installation | Defense Evasion | T1218.007 | Msiexec | Sí (attack.mitre.org) |
