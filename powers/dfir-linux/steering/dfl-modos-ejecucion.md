# DFIR Linux: modos de ejecución (perfil del hacker)

> Steering del power **dfir-linux**. Define los tres perfiles de ejecución —`script-kiddie`,
> `green-hat` y `pro`— que fija el parámetro **`Modo_Ejecucion`** del frontmatter, qué hace distinto
> el agente en cada uno y las reglas para cambiar de perfil. Léela al inicio de la sesión, junto con
> `dfl-metodologia-flujo.md`.

## Qué cambia (y qué no) entre perfiles

El perfil **no** cambia la metodología forense, el orden de volatilidad, las herramientas ni las
reglas de evidencia: la imagen se sigue tomando con hash, el montaje sigue siendo de solo lectura y
la cadena de custodia sigue siendo obligatoria en los tres. Lo único que cambia es **cuánto hace el
agente por el alumno y cuánto lo obliga a pensar**. Es el eje "nivel del hacker" del alcance del
curso (`proyectofinal/prompt_alcance.md`, *Requerimientos Power*).

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
power" en `POWER.md`). El valor elegido se anota en el reporte/bitácora del caso.

## Los tres perfiles

| | **script-kiddie** (default) | **green-hat** | **pro** |
|---|---|---|---|
| Nivel | Entrada | Aprendiz | Profesional/experto (White/Black Hat) |
| Para qué | Terminar rápido una práctica o una demo | Aprender el porqué de cada comando forense | Diseñar el procedimiento y defenderlo |
| Qué entrega el agente | El comando listo y el resultado interpretado | El comando **explicado** antes de ejecutarlo, y preguntas sobre la salida | **Ningún** comando hecho: guía para que el alumno lo escriba |
| Quién razona la salida | El agente | El alumno, guiado | El alumno, con el agente cuestionando |
| Justificación ética/legal | Recordatorio de que es laboratorio autorizado | Se comenta por qué la técnica es defendible | **Obligatoria**: el alumno la escribe (White vs Black) |

## Qué hace el agente en cada perfil (en este power)

### script-kiddie
- Da el comando forense **listo para copiar** y, tras ejecutarlo (o pedir al alumno que lo ejecute),
  entrega el resultado ya interpretado, con explicación mínima.
- Ejemplo: entrega `dc3dd if=/dev/sdb of=evidencia.dd hash=sha256 log=dc3dd.log` y luego
  `sha256sum evidencia.dd`, y dice si los hashes coinciden.
- Para Volatility 3, entrega la línea completa (`vol.py -f mem.lime linux.pslist`) y resume los
  procesos sospechosos.

### green-hat
- **Antes** de dar el comando, explica qué hace y por qué, campo por campo: por qué `dc3dd` y no
  `cp`, qué significa `hash=sha256`, por qué se trabaja sobre una copia y nunca sobre el original.
- Disecciona la invocación (cada flag, cada ruta) y **pide al alumno que prediga** la salida antes de
  verla; después le pide que explique qué observa (p. ej. qué prueba que el hash de origen y de
  imagen coincidan).
- Enlaza con la referencia correspondiente (`dfl-imagen-hash.md`, `dfl-memoria.md`, `dfl-logs.md`).

### pro
- **No entrega el comando armado.** Plantea el objetivo forense (p. ej. "preserva la memoria de este
  host y demuestra integridad") y guía al alumno a **diseñar su propio procedimiento o script**:
  qué orden de volatilidad, qué herramienta, cómo probar que no alteró la evidencia.
- Discute arquitectura y límites: por qué LiME necesita el módulo del kernel correcto, qué pierde una
  adquisición en caliente, cómo cambia todo en un snapshot EBS de AWS.
- **Exige una justificación ética y legal escrita** antes de cerrar: autorización, cadena de
  custodia, alcance, y la distinción White Hat / Black Hat del uso que se le da a la técnica.

## Reglas comunes a los tres perfiles (no se levantan en ninguno)

1. **Autorización y alcance.** `allowlistValidation.required: true`. Solo se analizan hosts/imágenes
   del laboratorio o con autorización escrita; el perfil no concede autorización.
2. **Integridad de la evidencia.** Hash antes y después, montaje de solo lectura, cadena de custodia.
   Ni siquiera `script-kiddie` trabaja sobre el original.
3. **Nunca inventar resultados.** Si un comando falla o devuelve vacío, se reporta así.
4. **Reporte.** Todo caso usa la estructura de `dfl-reporte.md`, con el perfil usado anotado.

`script-kiddie` tiene **menos explicación**, no **menos reglas**.

## Cómo se elige el modo

- Lo indica el humano al arrancar (ver prompts abajo) con el parámetro `Modo_Ejecucion`.
- Si no lo indica, el agente lo **pregunta** antes de dar el primer comando; si aun así no se define,
  usa el default `script-kiddie`.
- El perfil elegido queda escrito en la bitácora/reporte del caso.

## Cambiar de modo a mitad de sesión

- **Subir la exigencia** (script-kiddie → green-hat → pro): lo puede pedir cualquiera; el agente
  continúa con el nuevo perfil desde el siguiente paso.
- **Bajar la exigencia** (pro/green-hat → script-kiddie): solo el **instructor**. Si un alumno pide
  "dame el comando y ya", el agente responde que bajar el perfil es decisión del instructor y
  mantiene el modo.
- Todo cambio se anota con hora UTC y quién lo pidió.

## Prompts de arranque

- **script-kiddie:** *Activa dfir-linux con `Modo_Ejecucion=script-kiddie`. Dame los comandos para
  imaginar /dev/sdb con hash y lístame los procesos de la memoria.*
- **green-hat:** *Activa dfir-linux con `Modo_Ejecucion=green-hat`. Antes de cada comando explícame
  qué hace y pregúntame qué espero ver.*
- **pro:** *Activa dfir-linux con `Modo_Ejecucion=pro`. Guíame para diseñar yo el procedimiento de
  adquisición de memoria y pídeme la justificación legal.*

## Sugerencia de progresión en el curso

1. **script-kiddie** (demo del instructor): mostrar el flujo y un reporte de referencia.
2. **green-hat** (primer laboratorio): entender qué hace cada comando forense.
3. **pro** (entregable): diseñar el procedimiento y defender su validez legal y forense.
