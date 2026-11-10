---
name: TODO-skill-name
description: TODO — Describe qué hace este skill y CUÁNDO invocarlo. Debe envolver al menos una Herramienta_Real (Req 9.1) y operar solo sobre objetivos de la Allowlist_Objetivos del engagement. Use when el usuario pida <acción> en un laboratorio autorizado.
---

# TODO — Nombre del skill

> Esqueleto reutilizable del modelo estándar de Power. Copiar la carpeta
> `powers/_template/skills/<skill>/` a `powers/<equipo>/<power>/skills/<tu-skill>/`,
> renombrar y completar los TODO.

## Qué hace y cómo se invoca

TODO — Qué Herramienta_Real envuelve y qué entrega. El skill cubre **exactamente
una** ubicación del ciclo: una fase EC-Council **o** una etapa del
Flujo_Investigacion (la otra en `null` dentro de `x-ethack`).

## Modo_Ejecucion (Req 14.1–14.5)

El skill acepta el parámetro `Modo_Ejecucion` y lo resuelve con
`resolve_mode()` de `execution_mode.py` **antes** de tocar la Herramienta_Real:

- `script-kiddie` (default): comandos predefinidos automatizados, sin lógica propia.
- `green-hat`: ejecuta **y explica** la lógica subyacente.
- `pro`: lógica propia avanzada; puede generar scripts acotados al lab.

Si el valor es inválido, `resolve_mode()` lanza `InvalidModeError` y el skill
**no ejecuta** la herramienta (Req 14.7). El modo aplicado se registra para el
Hook_Auditoria (Req 14.6).

## Guardia de Allowlist_Objetivos (Req 9.5, 11.1–11.4)

Antes de ejecutar, resuelve y normaliza el objetivo y comprueba que pertenece a
la Allowlist_Objetivos (`allowlistValidation.source` del `plugin.json`). El
objetivo autorizado es el Contenedor_Objetivo; el host EC2 anfitrión queda
fuera de alcance salvo `host_is_target == true`. Nunca producción.

## Artefactos_Documentacion (Req 15.1)

Este Power entrega bajo `docs/`: `prompt.md`, `sessions/` y `feedback.md`.
