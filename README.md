# Agente de Ethical Hacking y Digital Forensics — ULSA

Sistema de agentes de Kiro para conducir, de forma **autorizada y trazable**, el
ciclo completo de **pentest (EC-Council)** + **forense (Flujo_Investigacion)** +
**respuesta a incidentes (NIST SP 800-61)** + **gobernanza (NIST CSF 2.0)** sobre
un laboratorio controlado.

Este repositorio es el **Repositorio_Base** del curso de Ingeniería Cibernética
(ULSA). Contiene **el Spec** (lo que hay que construir) y **la línea base ya
construida por el docente** (el resultado de ejecutar las primeras tareas).
Alumnos y docente lo **evolucionan en colaboración** completando las tareas
pendientes del Spec.

## Qué hay aquí

| Ruta | Qué es |
|---|---|
| `.kiro/specs/ethical-hacking-forensics-agent/` | **El Spec**: `requirements.md`, `design.md`, `tasks.md`. Es el objeto de trabajo colaborativo. |
| `.kiro/hooks/`, `.kiro/settings/`, `.kiro/steering/` | Hooks de gobernanza/auditoría, config MCP (sin secretos) y steering. |
| `agent_ethack_dfir/agents/` | Agente_Orquestador + 5 subagentes de fase + 5 subagentes de rol (custom agents de Kiro). |
| `agent_ethack_dfir/scripts/` | Guardia de allowlist, catalogador, adaptador de Powers, validación local. |
| `agent_ethack_dfir/engagements/dvwa-lab-ulsa/` | Engagement de referencia: `scope.yaml`, `state.json`, `inventory.json`, evidencia, incidentes, GRC. |
| `agent_ethack_dfir/engagements/dvwa-lab-ulsa/_ejemplo-resuelto/` | **Ejemplo resuelto por el docente**: un ciclo completo contra DVWA con evidencia, incidente y artefactos GRC reales. Material de estudio. |
| `powers/` | Los **9 Powers base** (cimiento, formato `POWER.md`) + `powers/_template/` + carpetas por equipo (`red-team/`, `blue-team/`, ...). |
| `Makefile` | Punto de entrada único de la Validacion_Local. |
| `CONTRIBUTING.md` | Flujo de colaboración (fork de 3 niveles + PR) y protocolo de compuerta. |
| `CODEOWNERS` | Propiedad por ruta. |
| `.github/pull_request_template.md` | Contrato de entrega de un Power. |
| `HANDOFF.md` | Traspaso al Líder Técnico: estado, pendientes y operación. |

## Requisitos

- Python 3.12+
- [Kiro](https://kiro.dev) (para ejecutar el Spec y los custom agents)
- `make`
- Para la **pasada real** contra el laboratorio: acceso al lab AWS (Kali + DVWA).
  Las credenciales del lab se entregan **por canal privado**, nunca en este repo.

## Arranque rápido

```bash
# 1. Validar la línea base (compuerta local; no necesita el lab ni red)
make validate            # debe terminar en VERDE con 2 huecos esperados

# 2. Regenerar el inventario de Powers (no se edita a mano)
make catalog

# 3. Ver cobertura de fases/etapas y conteo por responsable
make coverage
```

`make validate` corre **enteramente en local**: no depende de GitHub Actions ni
de CI remota (decisión de diseño, Req 20.6/20.11).

## Cómo se trabaja el Spec (resumen)

1. Elige una tarea pendiente en `.kiro/specs/ethical-hacking-forensics-agent/tasks.md`.
2. Crea una rama: `task/<n>-<descripcion>` o `power/<equipo>-<iniciales>-<nombre>`.
3. Ejecútala con Kiro (abre el Spec y pídele ejecutar esa tarea), o impleméntala a mano.
4. Marca la tarea `[x]` en `tasks.md` en el mismo commit que la implementa.
5. `make validate` en verde **antes** de abrir el Pull Request.
6. PR al Repositorio_Integracion del Líder Técnico. Él revisa y mergea.

El detalle completo del flujo de forks y la compuerta está en **`CONTRIBUTING.md`**.

## Estado actual

- **Línea base del docente: completa.** Orquestador, 5 subagentes de fase, 5
  subagentes de rol cableados a los 9 Powers base, scripts de integración y
  colaboración. `make validate` en VERDE.
- **Pendiente (trabajo de alumnos):** tareas **6.2** (Red Team + Covering Tracks),
  **7.2** (Blue Team detección/hardening), **8.2/8.4/8.6/8.8** (Digital Forensics),
  extensión de **10.1** (GRC) y **11.1** (Incident Responder), y el checkpoint **16**.
- **2 huecos de cobertura conocidos y esperados:** `Covering Tracks` (red-team) y
  `Blue Team detección/hardening`. `make validate` los reporta como pendientes, no
  como error.

## Alcance ético

Toda actividad se dirige **únicamente** a los objetivos de la `Allowlist_Objetivos`
(`scope.yaml`), nunca a producción, con autorización documentada. El sistema
distingue el **Contenedor_Objetivo** del **host anfitrión** (que no es objetivo
salvo autorización explícita). Las acciones prohibidas (exfiltración, persistencia
oculta, denegación de servicio) están declaradas y la guardia las bloquea.

---

*Curso de Ingeniería Cibernética — Universidad La Salle. Metodologías: EC-Council ·
NIST SP 800-61 · NIST CSF 2.0 · RFC 3227 · MITRE ATT&CK.*
