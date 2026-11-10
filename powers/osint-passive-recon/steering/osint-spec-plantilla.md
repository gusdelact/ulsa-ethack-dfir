# OSINT: plantilla del Spec de investigación

> Steering del power **osint-passive-recon**. Contiene la plantilla de los tres documentos del Spec
> de Kiro para una investigación OSINT. El proceso para crearlo con el alumno está en
> `osint-spec-investigacion.md`. **Léelo antes de usar esta plantilla.**
>
> El agente copia cada bloque a `.kiro/specs/osint-<objetivo>/` y **no rellena** los campos marcados
> `«ALUMNO: ...»`: los completa el alumno en el diálogo. El agente solo puede escribir lo que el
> alumno dijo, con sus palabras.

## `requirements.md`

```markdown
# Requisitos de inteligencia — <objetivo>

## Introducción

Pregunta del cliente: «ALUMNO: ¿qué quiere saber el cliente? Una frase. Ej.: ¿cuánto puede descubrir
alguien sobre la organización sin intentar entrar a sus sistemas?»

Alcance: ver `evidencia/osint/<objetivo>-<fecha>/00-alcance.md` (objetivo, quién autoriza, propósito).

## Requisitos

### Requisito 1 — Company Information

**Historia:** Como analista OSINT, quiero saber «ALUMNO: qué necesitas saber de la organización y su
personal», para «ALUMNO: para qué le sirve al cliente».

**Criterios de aceptación**

1. CUANDO termine la investigación, ENTONCES el informe SHALL responder «ALUMNO: pregunta concreta».
2. «ALUMNO: segundo criterio, si aplica»
3. SI un dato solo puede obtenerse tocando al objetivo o perfilando a una persona real, ENTONCES el
   informe SHALL dejarlo como "fuera de alcance" con la razón.

### Requisito 2 — Infrastructure

**Historia:** Como analista OSINT, quiero saber «ALUMNO: qué necesitas saber de dominios, DNS,
hosting, correo y terceros», para «ALUMNO: para qué».

**Criterios de aceptación**

1. CUANDO termine la investigación, ENTONCES el informe SHALL responder «ALUMNO».
2. «ALUMNO»
3. CUANDO un dato provenga de una sola fuente, ENTONCES el informe SHALL marcarlo como no contrastado.

### Requisito 3 — Leaks

**Historia:** Como analista OSINT, quiero saber «ALUMNO: qué información no destinada al público
podría existir», para «ALUMNO: para qué».

**Criterios de aceptación**

1. CUANDO termine la investigación, ENTONCES el informe SHALL responder «ALUMNO».
2. SI aparece una credencial o un dato personal, ENTONCES el informe SHALL documentar su existencia
   con el valor ofuscado, sin probarlo.

### Requisito 4 — Intelligence

**Historia:** Como analista OSINT, quiero conectar los hallazgos en cadenas Origin → Impact → State,
para explicar al cliente su exposición y no solo listar datos.

**Criterios de aceptación**

1. El informe SHALL incluir al menos «ALUMNO: cuántas» cadenas que unan hallazgos de dos categorías.
2. Cada eslabón SHALL marcarse como hecho, inferencia o hipótesis, con su fuente.
```

## `design.md`

```markdown
# Plan de investigación — <objetivo>

## Visión general

«ALUMNO: en 3–5 frases, qué crees que vas a encontrar y por qué. Es tu hipótesis inicial; está bien
equivocarse.»

## Frontera pasiva

- Permitido: «ALUMNO: lista las técnicas pasivas que usarás»
- Prohibido: «ALUMNO: lista lo que NO harás y por qué es activo»
- Regla de detención: si aparece un bucket, servicio expuesto u otro dominio/organización, documento
  y me detengo hasta que el humano decida.

## Matriz Core Elements × Information Resources

Para cada categoría: qué buscas (core element), de dónde lo sacas (resource) y con qué herramienta o
acción manual. Si no hay herramienta en el power, di quién lo hace (humano en navegador) o márcalo
fuera de alcance.

| Categoría | Qué busco (core element) | Fuente (resource) | Herramienta / acción | Hipótesis falsable |
|---|---|---|---|---|
| Company Information | «ALUMNO» | «ALUMNO» | «ALUMNO» | «ALUMNO» |
| Infrastructure | «ALUMNO» | «ALUMNO» | «ALUMNO» | «ALUMNO» |
| Leaks | «ALUMNO» | «ALUMNO» | «ALUMNO» | «ALUMNO» |

## Ciclos previstos

«ALUMNO: ¿qué hallazgo te haría abrir un nuevo ciclo? Ej.: "si crt.sh o Wayback dan un subdominio
nuevo, vuelvo a DNS sobre ese nombre".»

## Evidencia

- Carpeta: `evidencia/osint/<objetivo>-<fecha>[-runN]/`. Nunca se borra evidencia anterior.
- `herramientas/`: una salida literal por llamada. `bitacora-decisiones.md`: lo que decidiste y por qué.
```

## `tasks.md`

```markdown
# Tareas — <objetivo>

Modo de trabajo: Spec (ver `osint-modos-trabajo.md`).

El orden sigue a HTB (Company Information → Infrastructure → Leaks → Intelligence). Puede cambiarse
si el design.md lo justifica.

- [ ] 0. Alcance confirmado por el humano
  - Escribir `00-alcance.md` con las palabras del humano: objetivo, quién autoriza, propósito.
  - _Requisitos: todos_

- [ ] 1. Company Information
  - Antes: el alumno explica qué espera encontrar y qué le haría cambiar de idea.
  - Durante: `generate_dorks` (el humano abre las URLs), `search_github`; lectura manual de la web.
  - Después: el alumno clasifica hechos / inferencias / hipótesis y dice si se cumplen los criterios.
  - _Requisitos: 1.1, 1.2, 1.3_

- [ ] 2. Infrastructure
  - [ ] 2.1 Registro y DNS (`search_rdap`, `search_whois`, `search_dns`, `dns_lookup`)
  - [ ] 2.2 IP, ASN y proveedor (`search_ip`, `whois_lookup`)
  - [ ] 2.3 Subdominios (`crtsh_certificate_search`, `wayback_snapshots`) y nuevo ciclo de DNS
  - [ ] 2.4 Cloud y terceros (inferencia sobre 2.1–2.3; detenerse ante otro dominio)
  - Antes / después: igual que la tarea 1.
  - _Requisitos: 2.1, 2.2, 2.3_

- [ ] 3. Leaks
  - Durante: `wayback_snapshots` (robots.txt, contenido retirado), `search_paste`,
    `exiftool_metadata` sobre documentos públicos que el humano descargó.
  - Antes / después: igual que la tarea 1.
  - _Requisitos: 3.1, 3.2_

- [ ] 4. Intelligence e informe
  - El alumno propone las cadenas Origin → Impact → State; el agente revisa que cada eslabón tenga fuente.
  - Informe con la plantilla de `osint-intelligence-reporte.md`.
  - _Requisitos: 4.1, 4.2_
```
