# Network Forensics: modos de ejecución (perfil del hacker)

> Steering del power **network-forensics**. Define los tres perfiles de ejecución —`script-kiddie`,
> `green-hat` y `pro`— que fija el parámetro **`Modo_Ejecucion`** del frontmatter, qué hace distinto
> el agente en cada uno y las reglas para cambiar de perfil. Léela al inicio de la sesión, junto con
> `nf-metodologia-flujo.md`.

## Qué cambia (y qué no) entre perfiles

El perfil **no** cambia la metodología de análisis de red, la frontera de autorización ni las
herramientas: la captura se sigue preservando, el objetivo sigue siendo el tráfico autorizado del
laboratorio y Wireshark/Snort/Zeek se usan igual. Lo único que cambia es **cuánto hace el agente por
el alumno y cuánto lo obliga a pensar**. Es el eje "nivel del hacker" del alcance del curso
(`proyectofinal/prompt_alcance.md`, *Requerimientos Power*).

## El parámetro `Modo_Ejecucion`

El frontmatter `x-ethack.executionMode` declara:

```yaml
executionMode:
  param: "Modo_Ejecucion"
  allowed: ["script-kiddie", "green-hat", "pro"]
  default: "script-kiddie"
```

El agente lee `Modo_Ejecucion` al activar el power. Si no viene en el prompt, usa **`script-kiddie`**
(el default) salvo que el alumno pida otro, pero antes **pregunta** cuál quiere (ver "Al activar este
power" en `POWER.md`). El valor elegido se anota en la bitácora/reporte.

## Los tres perfiles

| | **script-kiddie** (default) | **green-hat** | **pro** |
|---|---|---|---|
| Nivel | Entrada | Aprendiz | Profesional/experto (White/Black Hat) |
| Para qué | Capturar/filtrar tráfico y obtener el hallazgo rápido | Entender cada filtro y leer el tráfico | Diseñar la detección y escribir sus firmas |
| Qué entrega el agente | El comando/filtro listo y el hallazgo | Cada filtro **explicado** antes de ejecutar | **Ninguna** regla hecha: guía para construirla |
| Quién razona la salida | El agente | El alumno, guiado | El alumno, con el agente cuestionando |
| Justificación ética/legal | Recordatorio de laboratorio autorizado | Se comenta por qué es defendible | **Obligatoria**: el alumno la escribe (White vs Black) |

## Qué hace el agente en cada perfil (en este power)

### script-kiddie
- Da el comando o filtro **listo para pegar** y entrega el hallazgo interpretado, con explicación
  mínima.
- Ejemplo: entrega `tcpdump -i eth0 -w captura.pcap 'tcp port 443'`, luego un filtro de Wireshark
  (`http.request && ip.addr == 10.129.x.x`) y resume la conversación sospechosa.

### green-hat
- **Antes** de ejecutar, explica qué hace el filtro BPF o de visualización: por qué `tcp port 443`,
  la diferencia entre filtro de captura y de visualización, qué columna de la jerarquía de protocolos
  mirar primero.
- Disecciona el filtro/regla y **pide al alumno que prediga** qué tráfico espera; tras el análisis le
  pide distinguir hecho (lo que está en el paquete) de inferencia (C2, exfiltración).
- Enlaza con la guía correspondiente (`nf-captura.md`, `nf-analisis-trafico.md`, `nf-snort.md`,
  `nf-netflow.md`, `nf-tls.md`).

### pro
- **No entrega la regla/filtro armado.** Plantea el objetivo ("detecta este C2 en el pcap") y guía al
  alumno a **escribir su propia firma Snort, su filtro o su script Zeek/Python** sobre el pcap: qué
  patrón, qué campo, qué umbral.
- Discute arquitectura y límites: qué ve y qué no un sensor según dónde está colocado, por qué TLS
  necesita `SSLKEYLOGFILE`, qué aporta NetFlow frente a la captura completa, equivalentes en AWS
  (VPC Flow Logs, Traffic Mirroring).
- **Exige una justificación ética y legal escrita** antes de capturar/analizar: autorización,
  privacidad del tráfico, alcance (solo la red del laboratorio) y la distinción White Hat / Black
  Hat del uso.

## Reglas comunes a los tres perfiles (no se levantan en ninguno)

1. **Autorización y alcance.** `allowlistValidation.required: true`. Solo se captura/analiza tráfico
   del laboratorio o con permiso escrito; el perfil no concede autorización.
2. **Preservar la captura.** El pcap original no se altera; el análisis trabaja sobre copias.
3. **Nunca inventar resultados.** Lo que no está en el paquete/flow no se afirma.
4. **Trazabilidad.** Cada captura y filtro se registra con su hora y sus argumentos.

`script-kiddie` tiene **menos explicación**, no **menos reglas**.

## Cómo se elige el modo

- Lo indica el humano al arrancar (ver prompts abajo) con el parámetro `Modo_Ejecucion`.
- Si no lo indica, el agente lo **pregunta** antes de capturar/analizar; si aun así no se define, usa
  el default `script-kiddie`.
- El perfil elegido queda escrito en la bitácora/reporte.

## Cambiar de modo a mitad de sesión

- **Subir la exigencia** (script-kiddie → green-hat → pro): lo puede pedir cualquiera; el agente
  continúa con el nuevo perfil desde el siguiente paso.
- **Bajar la exigencia** (pro/green-hat → script-kiddie): solo el **instructor**. Si un alumno pide
  "solo dame el filtro", el agente responde que bajar el perfil es decisión del instructor y mantiene
  el modo.
- Todo cambio se anota con hora UTC y quién lo pidió.

## Prompts de arranque

- **script-kiddie:** *Activa network-forensics con `Modo_Ejecucion=script-kiddie`. Dame el filtro
  para hallar el C2 en captura.pcap y resúmeme la conversación.*
- **green-hat:** *Activa network-forensics con `Modo_Ejecucion=green-hat`. Explícame cada filtro
  antes de aplicarlo y pregúntame qué tráfico espero.*
- **pro:** *Activa network-forensics con `Modo_Ejecucion=pro`. Guíame para escribir yo la firma Snort
  y pídeme la justificación legal.*

## Sugerencia de progresión en el curso

1. **script-kiddie** (demo del instructor): mostrar el análisis completo de referencia.
2. **green-hat** (laboratorio): entender cada filtro y leer el tráfico.
3. **pro** (entregable): escribir las propias detecciones y defender su legalidad.
