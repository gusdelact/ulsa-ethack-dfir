# Fase 2a: Detección y triage

Incluye sensores, logs, personal entrenado, intercambio de información, threat intelligence con
contexto, segmentación y visibilidad de la red.

## Fuentes de detección

- Un empleado que nota un comportamiento anormal.
- Una alerta de herramienta: EDR, IDS, firewall, SIEM.
- Threat hunting.
- Una **notificación de un tercero** (proveedor, CERT, cliente, autoridad).

## Niveles de detección

| Nivel | Herramientas | Ejemplo de señal |
|---|---|---|
| Perímetro | Firewall, NIDS/NIPS, DMZ | Conexiones salientes a una IP rara por 443 |
| Red interna | Firewalls locales, HIDS/HIPS | Tráfico SMB entre estaciones de trabajo |
| Endpoint | AV, EDR | Mimikatz detectado, acceso a LSASS |
| Aplicación | Logs de aplicación y servicios | Login admin exitoso desde IP extranjera |

## Investigación inicial

Antes de convocar a todo el equipo, establecer contexto. Una cuenta admin conectándose a una IP a
las HH:MM:SS no significa nada sin saber qué hay en esa IP ni la zona horaria.

Datos a reunir (van a `00-alcance.md` y `03-sistemas.md`):

- [ ] Fecha y hora del reporte; quién detectó y quién reportó.
- [ ] Cómo se detectó.
- [ ] Qué tipo de incidente parece (phishing, indisponibilidad, malware, acceso no autorizado…).
- [ ] Lista de sistemas impactados.
- [ ] Quién accedió a esos sistemas y qué acciones se tomaron.
- [ ] ¿Sigue activo o ya se detuvo?
- [ ] Por sistema: ubicación física, SO, IP, hostname, dueño, propósito, estado actual.
- [ ] Si hay malware: IPs, fecha/hora de detección, tipo, sistemas afectados, copia del archivo y hashes.

El contexto cambia la respuesta: la laptop del CEO no se trata igual que la de un practicante.

## Línea de tiempo

Se inicia desde la investigación inicial y se actualiza durante todo el caso.

| Date | Time (con zona) | Hostname | Event description | Data source |
|---|---|---|---|---|
| 09/09/2021 | 13:31 CET | SQLServer01 | Hacker tool 'Mimikatz' was detected | Antivirus Software |

- Ordenar por **hora del evento**, no por hora del hallazgo.
- Se centra en el comportamiento del atacante: conexiones, descargas, ejecuciones, cuentas creadas.
- Sirve para decidir si una evidencia nueva pertenece al incidente (p. ej. el "payload inicial" ya estaba en otro equipo dos semanas antes).

## Severidad y alcance

| Pregunta | Por qué importa |
|---|---|
| ¿Cuál es el impacto de la explotación? | Define la prioridad. |
| ¿Qué requisitos tiene la explotación? | Indica qué otros sistemas son vulnerables. |
| ¿Puede afectar sistemas críticos para el negocio? | Escala la prioridad. |
| ¿Hay pasos de remediación sugeridos? | Acelera la contención. |
| ¿Cuántos sistemas están impactados? | Muchos sistemas obligan a escalar. |
| ¿El exploit se usa *in the wild*? | Indica sofisticación y urgencia. |
| ¿Tiene capacidades de gusano? | Indica sofisticación y riesgo de propagación. |

### Matriz de prioridad sugerida

No viene del curso; es una ayuda para ordenar la decisión. Ajustar a la política de la organización.

| Impacto \ Alcance | 1 sistema | Varios sistemas | Muchos o críticos |
|---|---|---|---|
| **Bajo** (sin datos sensibles, sin interrupción) | Baja | Media | Alta |
| **Medio** (datos internos, interrupción parcial) | Media | Alta | Crítica |
| **Alto** (datos de clientes, exfiltración, ransomware, cuentas de dominio) | Alta | Crítica | Crítica |

En el caso Insight Nexus la prioridad fue **Critical** por exfiltración confirmada.

## Escalamiento (R9)

Escalar al incident manager cuando:

- La prioridad es Alta o Crítica.
- Hay muchos sistemas afectados o crece el número.
- El movimiento lateral alcanza sistemas de **otra área** (finanzas, RR. HH.). Que sean de otro departamento **no** es motivo para no escalar.
- Hay datos personales o de clientes involucrados (posible obligación legal de notificar).
- Se sospecha de un insider.

## Confidencialidad y comunicación (R6)

- Información en **need-to-know**; el atacante puede ser un empleado.
- La comunicación interna y externa la hace la persona designada junto con legal.
- Al abrir la investigación, fijar expectativas: tipo de incidente, fuentes de evidencia, tiempo estimado y probabilidad de identificar al adversario.
- Mantener informada a la dirección de avances y cambios de expectativa (registrar en `07-comunicaciones.md`).

## Trabajo en la plataforma de casos (TheHive u otra)

1. Asignarse la alerta.
2. Crear el caso (o promover la alerta a caso) y vincular las alertas relacionadas.
3. Agregar IOCs en *Observables*.
4. Documentar hallazgos en notas y comentarios.
5. Cerrar con resumen y lecciones aprendidas.

Para hacerlo con herramientas MCP, usar el power `incident-response-lab`.

## Siguiente paso

Cuando hay contexto suficiente, pasar a `ih-03-investigacion.md`.
