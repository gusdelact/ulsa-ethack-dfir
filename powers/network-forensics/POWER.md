---
name: "network-forensics"
displayName: "Network Forensics"
description: "Curso Introduction to Network Forensics (HTB Academy, 7 secciones): principios y herramientas (Wireshark, tcpdump, Snort, NetworkMiner), captura con filtros BPF y de visualización, análisis de tráfico (jerarquía de protocolos, conversaciones, C2, exfiltración, amenazas internas, escaneos, ARP spoofing), NetFlow con Suricata, detección por firmas con Snort y análisis de TLS/SSL con SSLKEYLOGFILE, con equivalentes en AWS (VPC Flow Logs, Traffic Mirroring). Para laboratorios autorizados. Incluye guías de steering por fase, cargables bajo demanda."
keywords: ["network-forensics", "dfir", "wireshark", "tcpdump", "netflow", "snort", "pcap"]
author: "Gustavo De la Cruz Tovar"
x-ethack:
  kind: "forensics"
  ecCouncilPhase: null
  forensicsStage: "Collect"
  team: "digital-forensics"
  owner: "Gustavo De la Cruz Tovar"
  tools: ["Wireshark", "tcpdump", "Snort", "Suricata", "Zeek"]
  allowlistValidation:
    required: true
    source: "engagements/${ENGAGEMENT_ID}/scope.yaml#assets"
    targetParams: ["target", "host", "hostname", "domain", "url"]
  executionMode:
    param: "Modo_Ejecucion"
    allowed: ["script-kiddie", "green-hat", "pro"]
    default: "script-kiddie"
  documentation:
    root: "powers/network-forensics/docs"
    required: ["prompt.md", "sessions/", "feedback.md"]
---

# Network Forensics

## Al activar este power (obligatorio, en este orden)

1. **Modo de ejecución (perfil).** Lee el parámetro `Modo_Ejecucion` del frontmatter
   (`x-ethack.executionMode`, valores `script-kiddie` | `green-hat` | `pro`, default
   `script-kiddie`). Si el prompt no lo indica, el agente **pregunta** cuál perfil usar antes de
   capturar o analizar; si aun así no se define, usa el default `script-kiddie`:
   > ¿Con qué perfil trabajamos?
   > - **script-kiddie:** te doy el comando/filtro listo y el hallazgo, con explicación mínima.
   > - **green-hat:** antes de ejecutar te explico cada filtro y te pido razonar el tráfico.
   > - **pro:** no te doy la regla hecha; te guío a escribir tu firma/filtro y te pido la
   >   justificación ética y legal.
2. **Cargar `nf-modos-ejecucion.md`** (detalle de los tres perfiles y reglas de cambio de modo).
3. **Cargar `nf-metodologia-flujo.md`** y seguir el flujo de análisis según el perfil elegido.

## Overview

Este power de conocimiento empaqueta el módulo **Introduction to Network Forensics** de
**Hack The Box Academy** (7 secciones) y lo convierte en un flujo de análisis que el agente puede
seguir en un laboratorio autorizado:

- **Principios y herramientas**: Wireshark, tcpdump, Snort y NetworkMiner.
- **Captura** con filtros BPF y filtros de visualización.
- **Análisis de tráfico**: jerarquía de protocolos, conversaciones, C2, exfiltración, amenazas
  internas, escaneos y ARP spoofing.
- **NetFlow** con Suricata.
- **Detección por firmas** con Snort.
- **Análisis de TLS/SSL** con `SSLKEYLOGFILE`.
- **Equivalentes en AWS**: VPC Flow Logs y Traffic Mirroring.

> **Encuadre:** material didáctico para laboratorios autorizados o equipos propios. El power no
> concede autorización por sí mismo. Creado para el curso de Ingeniería Cibernética (ULSA) con
> asistencia de Kiro.

## Cómo está organizado el conocimiento (steering/)

Las guías se cargan **bajo demanda** (acción `readSteering`): lee solo la que necesites según la fase.

| Guía | Contenido |
|---|---|
| `nf-modos-ejecucion.md` | **Léela al inicio.** Los perfiles script-kiddie, green-hat y pro del parámetro `Modo_Ejecucion`, qué cambia el agente en cada uno y las reglas de cambio. |
| `nf-metodologia-flujo.md` | **Léela primero.** Metodología y flujo del análisis de red. |
| `nf-captura.md` | Captura con filtros BPF y de visualización. |
| `nf-analisis-trafico.md` | Análisis de tráfico: protocolos, conversaciones, C2, exfiltración, escaneos, ARP spoofing. |
| `nf-netflow.md` | NetFlow con Suricata. |
| `nf-snort.md` | Detección por firmas con Snort. |
| `nf-tls.md` | Análisis de TLS/SSL con `SSLKEYLOGFILE`. |
| `nf-reporte.md` | Estructura del reporte. |

## Modos de ejecución (perfil del hacker)

Además del flujo técnico, este power se ejecuta en uno de **tres perfiles** que definen cuánto hace
el agente por ti y cuánto te hace pensar. El perfil se fija con el parámetro **`Modo_Ejecucion`** del
frontmatter (`x-ethack.executionMode`: `allowed: ["script-kiddie", "green-hat", "pro"]`,
`default: "script-kiddie"`). No cambian la metodología, las herramientas ni la frontera de
autorización; cambia la profundidad de la explicación y quién razona. Detalle y reglas de cambio en
`steering/nf-modos-ejecucion.md`.

| `Modo_Ejecucion` | Perfil | Qué hace el agente en network-forensics |
|---|---|---|
| `script-kiddie` *(default)* | Nivel de entrada | Da el comando/filtro listo (p. ej. `tcpdump -i eth0 -w captura.pcap 'tcp port 443'`, filtro de Wireshark) y resume el hallazgo, con explicación mínima. Para terminar rápido. |
| `green-hat` | Aprendiz | Antes de ejecutar, explica el filtro BPF o de visualización (captura vs visualización, qué mirar primero), disecciona el filtro y te pide predecir e interpretar el tráfico. Para aprender en el laboratorio. |
| `pro` | Profesional/experto (White/Black Hat) | No da la regla hecha: te guía a escribir tu propia firma Snort, filtro o script Zeek/Python, discute arquitectura y límites (colocación del sensor, TLS con `SSLKEYLOGFILE`, NetFlow, VPC Flow Logs) y exige una justificación ética y legal escrita. |

**Prompts de arranque:**

- **script-kiddie:** *Activa network-forensics con `Modo_Ejecucion=script-kiddie`. Dame el filtro para hallar el C2 en captura.pcap y resúmeme la conversación.*
- **green-hat:** *Activa network-forensics con `Modo_Ejecucion=green-hat`. Explícame cada filtro antes de aplicarlo y pregúntame qué tráfico espero.*
- **pro:** *Activa network-forensics con `Modo_Ejecucion=pro`. Guíame para escribir yo la firma Snort y pídeme la justificación legal.*

**Elección y cambio de modo:** si el humano no indica el perfil, el agente lo pregunta antes de
capturar/analizar (default `script-kiddie`). Subir la exigencia (script-kiddie → green-hat → pro) lo
pide cualquiera; bajarla (→ script-kiddie) solo el **instructor**. El perfil usado se anota en la
bitácora/reporte.

## Configuration

**No requiere configuración.** Es un power de conocimiento: no tiene `mcp.json` ni API keys.
