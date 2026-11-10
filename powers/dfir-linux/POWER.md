---
name: "dfir-linux"
displayName: "Digital Forensics on Linux"
description: "Cursos Digital Forensics on Linux y su continuación (HTB Academy, 14 secciones): live response y datos volátiles, sistemas de archivos EXT/XFS/Btrfs, imagen con dd y dc3dd, hashes, montaje de solo lectura, recuperación de borrados, persistencia (cron, systemd, authorized_keys, .bashrc, sudoers, SUID/SGID), análisis de logs (syslog, auth, auditd, boot, dmesg, faillog, wtmp/btmp), adquisición con comandos, Autopsy y memoria con LiME y Volatility 3, con equivalentes en AWS (snapshots EBS). Para laboratorios autorizados. Incluye guías de steering por fase, cargables bajo demanda."
keywords: ["digital-forensics", "dfir", "linux-forensics", "live-response", "log-analysis", "auditd", "autopsy"]
author: "Gustavo De la Cruz Tovar"
x-ethack:
  kind: "forensics"
  ecCouncilPhase: null
  forensicsStage: "Analyze"
  team: "digital-forensics"
  owner: "Gustavo De la Cruz Tovar"
  tools: ["dd", "dc3dd", "LiME", "Volatility 3", "Autopsy", "auditd"]
  allowlistValidation:
    required: true
    source: "engagements/${ENGAGEMENT_ID}/scope.yaml#assets"
    targetParams: ["target", "host", "hostname", "domain", "url"]
  executionMode:
    param: "Modo_Ejecucion"
    allowed: ["script-kiddie", "green-hat", "pro"]
    default: "script-kiddie"
  documentation:
    root: "powers/dfir-linux/docs"
    required: ["prompt.md", "sessions/", "feedback.md"]
---

# Digital Forensics on Linux

## Al activar este power (obligatorio, en este orden)

1. **Modo de ejecución (perfil).** Lee el parámetro `Modo_Ejecucion` del frontmatter
   (`x-ethack.executionMode`, valores `script-kiddie` | `green-hat` | `pro`, default
   `script-kiddie`). Si el prompt no lo indica, el agente **pregunta** cuál perfil usar antes de dar
   el primer comando; si aun así no se define, usa el default `script-kiddie`:
   > ¿Con qué perfil trabajamos?
   > - **script-kiddie:** te doy el comando listo y el resultado, con explicación mínima.
   > - **green-hat:** antes de cada comando te explico qué hace y te pido razonar la salida.
   > - **pro:** no te doy el comando hecho; te guío a diseñar tu procedimiento y te pido la
   >   justificación ética y legal.
2. **Cargar `dfl-modos-ejecucion.md`** (detalle de los tres perfiles y reglas de cambio de modo).
3. **Cargar `dfl-metodologia-flujo.md`** y seguir el flujo forense según el perfil elegido.

## Overview

Este power de conocimiento empaqueta los cursos **Digital Forensics on Linux** y su continuación de
**Hack The Box Academy** (14 secciones) y los convierte en un flujo forense que el agente puede
seguir en un laboratorio autorizado:

- **Live response y datos volátiles** en un sistema Linux.
- **Sistemas de archivos** EXT, XFS y Btrfs.
- **Imagen forense** con `dd` y `dc3dd`, hashes, montaje de solo lectura y recuperación de borrados.
- **Persistencia**: cron, systemd, `authorized_keys`, `.bashrc`, `sudoers`, SUID/SGID.
- **Análisis de logs**: syslog, auth, auditd, boot, dmesg, faillog, wtmp/btmp.
- **Adquisición** con comandos y con **Autopsy**.
- **Memoria** con LiME y Volatility 3.
- **Equivalentes en AWS** (snapshots EBS) para escenarios en la nube.

> **Encuadre:** material didáctico para laboratorios autorizados o equipos propios. El power no
> concede autorización por sí mismo. Base: módulos de DFIR de HTB Academy. Creado para el curso de
> Ingeniería Cibernética (ULSA) con asistencia de Kiro.

## Cómo está organizado el conocimiento (steering/)

Las guías se cargan **bajo demanda** (acción `readSteering`): lee solo la que necesites según la fase.

| Guía | Contenido |
|---|---|
| `dfl-modos-ejecucion.md` | **Léela al inicio.** Los perfiles script-kiddie, green-hat y pro del parámetro `Modo_Ejecucion`, qué cambia el agente en cada uno y las reglas de cambio. |
| `dfl-metodologia-flujo.md` | **Léela primero.** Metodología y flujo del análisis forense en Linux. |
| `dfl-live-response.md` | Live response y recolección de datos volátiles. |
| `dfl-imagen-hash.md` | Imagen con `dd`/`dc3dd`, hashes, montaje de solo lectura y recuperación de borrados. |
| `dfl-persistencia.md` | Persistencia: cron, systemd, `authorized_keys`, `.bashrc`, `sudoers`, SUID/SGID. |
| `dfl-logs.md` | Análisis de logs: syslog, auth, auditd, boot, dmesg, faillog, wtmp/btmp. |
| `dfl-memoria.md` | Captura y análisis de memoria con LiME y Volatility 3. |
| `dfl-autopsy.md` | Adquisición y análisis con Autopsy. |
| `dfl-reporte.md` | Estructura del reporte forense. |

## Modos de ejecución (perfil del hacker)

Además del flujo técnico, este power se ejecuta en uno de **tres perfiles** que definen cuánto hace
el agente por ti y cuánto te hace pensar. El perfil se fija con el parámetro **`Modo_Ejecucion`** del
frontmatter (`x-ethack.executionMode`: `allowed: ["script-kiddie", "green-hat", "pro"]`,
`default: "script-kiddie"`). No cambian la metodología, las herramientas ni las reglas de evidencia;
cambia la profundidad de la explicación y quién razona. Detalle y reglas de cambio en
`steering/dfl-modos-ejecucion.md`.

| `Modo_Ejecucion` | Perfil | Qué hace el agente en dfir-linux |
|---|---|---|
| `script-kiddie` *(default)* | Nivel de entrada | Da el comando listo (p. ej. `dc3dd ... hash=sha256`, `vol.py ... linux.pslist`) y entrega el resultado interpretado, con explicación mínima. Para terminar rápido. |
| `green-hat` | Aprendiz | Antes de ejecutar, explica qué hace el comando y por qué (cada flag, por qué solo lectura), disecciona la invocación y te pide predecir y leer la salida. Para aprender en el laboratorio. |
| `pro` | Profesional/experto (White/Black Hat) | No da el comando hecho: te guía a diseñar tu propio procedimiento/script de adquisición o análisis, discute arquitectura y límites (LiME, orden de volatilidad, EBS) y exige una justificación ética y legal escrita. |

**Prompts de arranque:**

- **script-kiddie:** *Activa dfir-linux con `Modo_Ejecucion=script-kiddie`. Dame los comandos para imaginar /dev/sdb con hash y listar procesos de memoria.*
- **green-hat:** *Activa dfir-linux con `Modo_Ejecucion=green-hat`. Explícame cada comando antes de ejecutarlo y pregúntame qué espero ver.*
- **pro:** *Activa dfir-linux con `Modo_Ejecucion=pro`. Guíame para diseñar yo el procedimiento de adquisición y pídeme la justificación legal.*

**Elección y cambio de modo:** si el humano no indica el perfil, el agente lo pregunta antes del
primer comando (default `script-kiddie`). Subir la exigencia (script-kiddie → green-hat → pro) lo
pide cualquiera; bajarla (→ script-kiddie) solo el **instructor**. El perfil usado se anota en la
bitácora/reporte.

## Configuration

**No requiere configuración.** Es un power de conocimiento: no tiene `mcp.json` ni API keys.
