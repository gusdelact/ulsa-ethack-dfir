# Plantillas de la carpeta del caso

El agente copia cada plantilla al archivo correspondiente en `incidentes/<ID>/` y la llena con lo
que diga el usuario y lo que se encuentre. Todas las horas en UTC salvo que se indique otra zona.

---

## `00-alcance.md`

```markdown
# <ID> — Alcance

- **Entorno:** <laboratorio HTB / simulado / real asignado>
- **Autoriza:** <nombre y rol>
- **Incident manager:** <nombre>
- **Roles:** Triage: <> · Forense: <> · Contención: <> · Comunicación: <>
- **Apertura del caso (UTC):** <AAAA-MM-DD HH:MM>

## Reporte inicial
- **Detectado por / reportado por:** <>
- **Fecha y hora del reporte:** <>
- **Cómo se detectó:** <alerta, usuario, tercero, hunting>
- **Qué se observó (palabras del reportante):** <>
- **¿Sigue activo?:** <sí / no / desconocido>
- **Acciones ya tomadas y por quién:** <>

## Fuentes de evidencia disponibles
| Fuente | Zona horaria | Retención | Acceso |
|---|---|---|---|

## Clasificación inicial
- **Tipo:** <phishing / malware / credenciales / insider / app expuesta / supply chain / otro>
- **Playbook:** <>
- **Prioridad:** <Baja / Media / Alta / Crítica> — **Motivo:** <>
- **Expectativas:** <tiempo estimado, qué se espera poder determinar>
```

---

## `01-bitacora.md`

```markdown
# <ID> — Bitácora

| Hora (UTC) | Quién | Fase | Acción | Resultado | Reglas aplicadas |
|---|---|---|---|---|---|
| 2025-10-07 14:02 | analista1 | Detección | Revisión de la alerta checkme.txt en TheHive | Archivo en raíz web de portal; correlación pendiente | — |
```

---

## `02-timeline.md`

```markdown
# <ID> — Línea de tiempo (ordenada por hora del evento)

| Fecha | Hora (UTC) | Hostname | Descripción del evento | Fuente | Tipo (hecho/inferencia) | Etapa Kill Chain |
|---|---|---|---|---|---|---|
```

---

## `03-sistemas.md`

```markdown
# <ID> — Sistemas afectados

| Hostname | IP | Función | Dueño | SO | Criticidad | Evidencia de compromiso | Estado | Evidencia recolectada |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  | sospechoso / confirmado / contenido / erradicado / recuperado |  |

## Cuentas involucradas
| Cuenta | Tipo (usuario/servicio/admin) | Uso observado | Estado |
|---|---|---|---|
```

---

## `04-iocs.md`

```markdown
# <ID> — IOCs

| Tipo | Valor | Contexto | Fuente | Primera vez | Última vez | Estado | Buscado en |
|---|---|---|---|---|---|---|---|
| ipv4 |  |  |  |  |  | activo / falso positivo / descartado |  |
| sha256 |  |  |  |  |  |  |  |
| filename |  |  |  |  |  |  |  |
| registry |  |  |  |  |  |  |  |
| account |  |  |  |  |  |  |  |
```

---

## `05-evidencia-custodia.md`

```markdown
# <ID> — Evidencia y cadena de custodia

## Inventario
| ID evidencia | Descripción | Origen (host/ruta) | Método de adquisición | SHA-256 | Recolectó | Fecha/hora (UTC) | Ubicación de almacenamiento |
|---|---|---|---|---|---|---|---|
| EV-001 |  |  |  |  |  |  |  |

## Transferencias
| ID evidencia | Fecha/hora (UTC) | Entrega | Recibe | Motivo | Hash verificado |
|---|---|---|---|---|---|
```

Para calcular el hash: `shasum -a 256 <archivo>` (macOS) o `sha256sum <archivo>` (Linux) o
`Get-FileHash <archivo> -Algorithm SHA256` (Windows).

---

## `06-mitre.md`

```markdown
# <ID> — Mapeo Kill Chain / MITRE ATT&CK

| Hallazgo (con fuente) | Etapa Kill Chain | Táctica | ID | Nombre | Verificado |
|---|---|---|---|---|---|
```

---

## `07-comunicaciones.md`

```markdown
# <ID> — Comunicaciones

| Fecha/hora (UTC) | De | Para | Canal (fuera de banda) | Contenido resumido | Aprobado por |
|---|---|---|---|---|---|
```

### Mensaje de actualización a la dirección (modelo)

```text
Asunto: [<ID>] Actualización <n> — <prioridad>

Estado: <fase actual>
Qué sabemos: <2–3 hechos>
Impacto en el negocio: <sistemas/servicios, datos>
Qué estamos haciendo: <acciones en curso>
Qué necesitamos: <decisiones o recursos>
Próxima actualización: <hora>
```

---

## `08-reporte-final.md`

```markdown
# Reporte de incidente <ID>

## 1. Resumen ejecutivo
<qué pasó, impacto, estado actual, en 5–8 líneas>

## 2. Datos del caso
- Periodo del incidente (primer evento del atacante → cierre):
- Detección (fecha, fuente):
- Tiempo hasta detectar / hasta contener:
- Prioridad:
- Equipo:

## 3. Línea de tiempo resumida
| Fecha/hora (UTC) | Evento | Fuente |
|---|---|---|

## 4. Análisis técnico por fase del atacante
### 4.1 Acceso inicial
### 4.2 Ejecución y persistencia
### 4.3 Escalamiento y movimiento lateral
### 4.4 Recolección y exfiltración
### 4.5 Impacto
(cada afirmación con su fuente; hechos, inferencias e hipótesis separados)

## 5. Mapeo MITRE ATT&CK
<tabla de 06-mitre.md, solo IDs verificados o marcados "(por verificar)">

## 6. IOCs
<tabla de 04-iocs.md con estado "activo">

## 7. Respuesta
- Contención (corto y largo plazo):
- Erradicación:
- Recuperación:

## 8. Evaluación de la respuesta
- ¿Cómo se desempeñó el equipo respecto a planes, playbooks y procedimientos?
- ¿El negocio entregó la información a tiempo? ¿Qué mejorar?

## 9. Lecciones aprendidas y recomendaciones
| # | Recomendación | Prioridad | Responsable | Fecha |
|---|---|---|---|---|

## 10. Herramientas y recursos necesarios

## Anexos
- Bitácora (01), evidencia y custodia (05), comunicaciones (07)
```
