# HANDOFF — Traspaso al Líder Técnico

> Documento de traspaso del **Repositorio_Base** al Líder Técnico del curso.
> Reemplaza los marcadores antes de usar:
> - `<USUARIO_LT>` = usuario de GitHub del Líder Técnico (se define en la clase de la noche).
> - Owner del Repositorio_Base: **`gusdelact`** (https://github.com/gusdelact).

## 1. Qué es esto

El **Repositorio_Base** del Agente de Ethical Hacking y Digital Forensics. Contiene
**el Spec** (`.kiro/specs/ethical-hacking-forensics-agent/`) y **la línea base ya
construida por el docente**. El trabajo colaborativo consiste en **completar las
tareas pendientes del Spec** entre docente y alumnos, vía git + Pull Request.

## 2. Estado al momento del traspaso

- `make validate`: **VERDE** (2 huecos de cobertura esperados, no son error).
- **Tareas baseline del docente completas** (27 subtareas no opcionales): base común,
  orquestador, 5 subagentes de fase, cableado de los 5 subagentes de rol a los 9
  Powers base, hooks, integración y colaboración (Tasks 1, 3, 4, 6.1, 7.1, 8.1,
  10.1-cableado, 11.1-cableado, 12, 13, 15).
- **Ejemplo resuelto** incluido en
  `agent_ethack_dfir/engagements/dvwa-lab-ulsa/_ejemplo-resuelto/`: un ciclo completo
  contra DVWA (scanning → gaining → maintaining → forense → incidente → GRC) con
  evidencia, cadena de custodia, incidente NIST y artefactos GRC reales, más
  `reporte-ciclo-completo.md`. Úsalo como referencia de calidad con los alumnos.

## 3. Tareas pendientes (el trabajo colaborativo)

Fuente de verdad: `.kiro/specs/ethical-hacking-forensics-agent/tasks.md`.
Orden según el `Task Dependency Graph` del propio `tasks.md` (olas 5-11).

| Task | Equipo | Qué falta | Nota |
|---|---|---|---|
| **6.2** | Red Team (3) | Extender Powers ofensivos + **crear Power nuevo de Covering Tracks** | Cierra 1 de los 2 huecos |
| **7.2** | Blue Team (3) | **Crear Powers de detección/hardening desde cero** | Cierra el 2º hueco; cierra la brecha `DE.CM-01` del ejemplo resuelto |
| **8.2** | Digital Forensics (4) | Collect/Preserve sobre `dfir-linux`/`network-forensics` | — |
| **8.4** | Digital Forensics | Detect/Isolate/Analyze sin alterar evidencia | — |
| **8.6** | Digital Forensics | Cadena_Custodia + Power de reporte | — |
| **8.8** | Digital Forensics | Principios_Forenses como invariantes | — |
| **10.1** (ext.) | GRC (1) | Poblar artefactos GRC sobre el Power `grc-nist-csf` cableado | ≥2 Powers con herramienta/artefacto |
| **11.1** (ext.) | Incident Responder (1) | Poblar incidentes sobre `incident-handling-nist` | — |
| **16** | Todos | Checkpoint final — ensamblaje completo | — |

Tareas marcadas con `*` en `tasks.md` son property tests **opcionales** (pueden posponerse).

**Regla transversal:** cada alumno entrega ≥2 Powers con Herramienta_Real (Req 9.6).
`make validate` lo cuenta por `owner` (`count_tooled_by_owner`).

## 4. Topología de colaboración (ya documentada en CONTRIBUTING.md)

```
Repositorio_Base (gusdelact)  ──upstream──┐
                                           │ fork
             Repositorio_Integracion (<USUARIO_LT>)  ← docente + LT colaboran aquí
                                           │ fork
                          Fork_Alumno × 13  ← cada alumno toma una task
```

### Para que el docente y el Líder Técnico colaboren
Dos opciones (elige una):

- **A (simple):** el LT es **colaborador Maintain** del Repositorio_Base; ambos trabajan
  con ramas + PR sobre el mismo repo. Los alumnos forkean del Base.
- **B (fiel al Spec):** el LT **forkea** el Base → su fork es el `Repositorio_Integracion`;
  el LT invita al docente como **Maintain**; los alumnos forkean del Integracion.

### Rutas de propiedad (CODEOWNERS)
Las rutas compartidas (`agent_ethack_dfir/agents/orquestador/`, `scripts/`,
`engagements/`, y **el Spec** en `.kiro/specs/`) son del Líder Técnico: nadie las
edita sin su revisión. Las rutas `powers/<equipo>/` son de cada equipo.

## 5. Flujo para avanzar una tarea

```bash
git checkout -b task/7.2-blueteam-deteccion      # o power/<equipo>-<iniciales>-<nombre>
# ...ejecutar la task con Kiro (abrir el Spec) o implementarla a mano...
# marcar la task [x] en tasks.md EN EL MISMO COMMIT
make validate                                     # compuerta local, debe ir VERDE
git add . && git commit -m "feat(task-7.2): deteccion Blue Team; cierra hueco DE.CM-01"
git push origin task/7.2-blueteam-deteccion
# abrir PR al Repositorio_Integracion → revisa el LT → merge
```

## 6. Operación diaria

```bash
make validate     # compuerta completa (adaptador, docs, allowlist, cobertura, conteo)
make catalog      # regenera inventory.json (NO se edita a mano)
make coverage     # cobertura de fases/etapas + conteo por responsable
```

## 7. Laboratorio AWS (credenciales por canal privado)

El engagement de referencia apunta a un lab de AWS (Kali + DVWA). **Las IPs,
instance-IDs y la llave SSH NO están en este repo** y se entregan por canal privado.
Para una pasada real, el responsable actualiza `scope.yaml` (`authorized_window` y
los endpoints del asset `dvwa-01`) y verifica con la guardia antes de operar. Ver el
`_ejemplo-resuelto/reporte-ciclo-completo.md` para el procedimiento exacto que siguió
el docente.

## 8. Powers de alumno en repos aparte (decisión para la siguiente iteración)

Se decidió que los Powers nuevos de alumno vivirán en **repos de git propios** (cada
alumno publica el suyo). El mecanismo de integración (un manifest tipo
`powers.lock.yaml` + `bootstrap.sh` que clona los Powers aprobados en `powers/`)
**aún no está implementado**: debe añadirse como **tarea nueva al Spec**. Mientras
tanto, los 9 Powers base viajan dentro de este monorepo, como define el Spec actual.

## 9. Checklist de publicación (en la laptop con acceso a GitHub)

Ver `PUBLICAR.md` (incluido en el ZIP de entrega). Resumen:
1. Descomprimir el ZIP del Repositorio_Base.
2. `make validate` → confirmar VERDE.
3. `git init` + commit + tag `v0.1.0-baseline` + push a `github.com/gusdelact/ulsa-ethack-dfir`.
4. Invitar al Líder Técnico (`<USUARIO_LT>`) como colaborador Maintain (opción A).
5. Publicar los 9 repos de Powers base + `power-template` (ZIPs aparte).
