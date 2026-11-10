# Guía de contribución

Este proyecto se construye de forma colaborativa entre el docente, el Líder
Técnico y los 13 alumnos. La integración se hace **exclusivamente por Pull
Request** (modelo fork + PR de GitHub) con una **compuerta de validación
local**, sin depender de ningún servicio de integración continua remoto.

> Requisitos cubiertos por este documento: **20.1, 20.2, 20.3, 20.7, 20.10,
> 20.11**. El protocolo de compuerta (validación local + revisión humana) se
> detalla en la **sección 5**.

---

## 1. Topología de tres niveles

La colaboración se organiza en tres niveles de repositorio. El flujo de código
sube de abajo hacia arriba por Pull Request, y las actualizaciones del docente
bajan por sincronización `upstream`.

```
┌──────────────────────────────────────────────────────────────┐
│  Nivel 1 — Repositorio_Base (docente)            [upstream]    │
│  Mantiene la estructura del agente y la línea base del proyecto│
└───────────────▲───────────────────────────────┬──────────────┘
                │ (el Líder Técnico sincroniza)  │ fork
                │                                 ▼
┌───────────────┴───────────────────────────────────────────────┐
│  Nivel 2 — Repositorio_Integracion (Líder Técnico)  [upstream  │
│  del alumno]  Fork del Repositorio_Base. Aquí se integran los   │
│  Pull Request de los 13 alumnos tras pasar la compuerta.        │
└───────────────▲───────────────────────────────┬───────────────┘
                │ Pull Request (entrega)          │ fork
                │ desde el Fork_Alumno            ▼
┌───────────────┴───────────────────────────────────────────────┐
│  Nivel 3 — Fork_Alumno (cada alumno)                            │
│  Fork del Repositorio_Integracion. El alumno trabaja aquí en    │
│  su rama propia y abre el PR hacia el Repositorio_Integracion.  │
└────────────────────────────────────────────────────────────────┘
```

Reglas de la topología (Req 20.1, 20.2):

- El **docente** mantiene el `Repositorio_Base` como `upstream` del proyecto.
- El **Líder Técnico** mantiene el `Repositorio_Integracion` como **fork del
  `Repositorio_Base`**. Es el punto único de integración del trabajo de todos.
- Cada **alumno** mantiene su `Fork_Alumno` como **fork del
  `Repositorio_Integracion`** (no del repo del docente).
- Los alumnos contribuyen **solo por Pull Request** desde su `Fork_Alumno` hacia
  el `Repositorio_Integracion`. **Ningún alumno tiene permiso de escritura
  directa** sobre el `Repositorio_Integracion`.

---

## 2. Rama de trabajo por alumno

Cada alumno trabaja en **su propia rama**, nunca sobre la rama base/de partida
(Req 20.3).

- Patrón obligatorio de nombre de rama:

  ```
  power/<equipo>-<iniciales>-<nombre-power>
  ```

  - `<equipo>`: `red-team`, `blue-team`, `digital-forensics`, `grc`, `ir`.
  - `<iniciales>`: iniciales del alumno.
  - `<nombre-power>`: nombre corto del Power en `kebab-case`.

- Ejemplos:

  ```
  power/red-team-jlp-covering-tracks
  power/blue-team-amr-log-detection
  power/digital-forensics-sgc-memory-acquisition
  ```

- **Prohibido** commitear directamente sobre la rama base (p. ej. `main` /
  `mainline`) tanto en el `Fork_Alumno` como en el `Repositorio_Integracion`.
  La rama base se usa solo como punto de partida y para sincronizar.

---

## 3. Pasos de git para el alumno (estilo ejercicio FlowSync)

Flujo completo, desde el fork hasta abrir el Pull Request. Sustituye las URLs
por las reales del `Repositorio_Integracion` del Líder Técnico y de tu
`Fork_Alumno`.

### 3.1 Fork y clonado

1. En GitHub, haz **fork del `Repositorio_Integracion`** (el repo del Líder
   Técnico). Esto crea tu `Fork_Alumno`.
2. Clona tu `Fork_Alumno` en tu máquina:

   ```bash
   git clone https://github.com/<tu-usuario>/<repo-integracion>.git
   cd <repo-integracion>
   ```

   Al clonar, el remoto `origin` apunta a tu `Fork_Alumno`.

### 3.2 Añadir el upstream (Repositorio_Integracion)

3. Registra el `Repositorio_Integracion` del Líder Técnico como `upstream`:

   ```bash
   git remote add upstream https://github.com/<lider-tecnico>/<repo-integracion>.git
   git remote -v   # verifica: origin = tu fork, upstream = repo de integración
   ```

### 3.3 Traer la rama base y crear la rama de trabajo

4. Trae la rama base actualizada desde el `upstream`:

   ```bash
   git fetch upstream
   git checkout main
   git merge --ff-only upstream/main
   ```

5. Crea tu **rama de trabajo** a partir de la base (nunca trabajes sobre `main`):

   ```bash
   git checkout -b power/<equipo>-<iniciales>-<nombre-power>
   ```

### 3.4 Trabajar, commitear y empujar al fork

6. Coloca tu Power en `powers/<equipo>/<power>/` con su `plugin.json` o
   `POWER.md` (contrato `x-ethack`), sus `skills/`, `steering/` y los
   Artefactos_Documentacion bajo `docs/`.
7. Commitea tus cambios:

   ```bash
   git add powers/<equipo>/<power>/
   git commit -m "feat(<equipo>): agrega Power <nombre-power>"
   ```

8. Empuja tu rama a **tu fork** (`origin`):

   ```bash
   git push -u origin power/<equipo>-<iniciales>-<nombre-power>
   ```

### 3.5 Abrir el Pull Request hacia el Repositorio_Integracion

9. En GitHub, abre un **Pull Request** con:
   - **Base repository:** el `Repositorio_Integracion` del **Líder Técnico**
     (no tu fork), rama base `main`.
   - **Head repository:** tu `Fork_Alumno`, rama
     `power/<equipo>-<iniciales>-<nombre-power>`.

   > Cuidado: GitHub a veces preselecciona como base tu propio fork. Cambia el
   > *base repository* al repo del Líder Técnico antes de crear el PR.

10. Antes de abrir el PR debes haber corrido la compuerta local (ver sección 5).

---

## 4. Sincronización upstream en dos sentidos

Las actualizaciones del docente se propagan hacia abajo en dos saltos
(Req 20.10).

### 4.1 Líder Técnico: sincroniza Integración ← Base (docente)

El Líder Técnico mantiene el `Repositorio_Base` del docente como su `upstream`:

```bash
# En el clon del Repositorio_Integracion del Líder Técnico
git remote add upstream https://github.com/<docente>/<repo-base>.git   # una sola vez
git fetch upstream
git checkout main
git merge --ff-only upstream/main      # incorpora la línea base del docente
git push origin main                   # publica en el Repositorio_Integracion
```

### 4.2 Alumno: sincroniza Fork ← Integración (Líder Técnico)

Cuando el `Repositorio_Integracion` recibe novedades (del docente o de otros
PR ya integrados), cada alumno actualiza su `Fork_Alumno`:

```bash
# En el clon del Fork_Alumno; upstream = Repositorio_Integracion (sección 3.2)
git fetch upstream
git checkout main
git merge --ff-only upstream/main      # actualiza la base local
git push origin main                   # actualiza la rama base de tu fork

# Lleva las novedades a tu rama de trabajo (rebase recomendado)
git checkout power/<equipo>-<iniciales>-<nombre-power>
git rebase main
```

Resumen del doble sentido:

| Actor          | Sincroniza          | Desde (upstream)        | Hacia (origin)          |
|----------------|---------------------|-------------------------|-------------------------|
| Líder Técnico  | `Repositorio_Integracion` | `Repositorio_Base` (docente) | `Repositorio_Integracion` |
| Alumno         | `Fork_Alumno`       | `Repositorio_Integracion` | `Fork_Alumno`           |

---

## 5. Protocolo de compuerta (validación local + revisión humana)

La integración de cada Power pasa por una **única compuerta de calidad**
compuesta por dos partes: la **Validacion_Local** (`make validate`) y la
**revisión humana** del Líder Técnico. **No hay CI remota ni GitHub Actions**:
toda comprobación corre en la máquina de quien contribuye y de quien integra
(Req 20.7, 20.11).

### 5.1 El alumno valida antes de abrir el PR

Antes de abrir el Pull Request (paso 10 de la sección 3.5), el alumno ejecuta la
Validacion_Local desde la raíz del repositorio:

```bash
make validate
```

- **Solo abre el PR si `make validate` corre en verde.** Si falla, corrige lo
  que indique el agregador y vuelve a ejecutarlo hasta que pase.
- No se abre ni se pide revisión de un PR cuya Validacion_Local está en rojo.

### 5.2 El Líder Técnico valida y revisa antes de integrar

Antes de hacer *merge* del PR en el `Repositorio_Integracion`, el Líder Técnico:

1. Trae la rama del PR y ejecuta `make validate` él mismo (no confía solo en la
   captura del alumno).
2. **Revisa el PR** (revisión humana): contrato del Power, ubicación en
   `powers/<equipo>/<power>/`, rama `power/<equipo>-<iniciales>-<nombre-power>`,
   Artefactos_Documentacion y cumplimiento de la política ética/de laboratorio.
3. Integra **solo si** la Validacion_Local corre en verde **y** la revisión se
   supera.

### 5.3 Qué comprueba `make validate`

`make validate` es el **punto de entrada único** de la Validacion_Local
(`agent_ethack_dfir/scripts/validate_all.py`, tarea 15.4). No reimplementa lógica: **encadena**
componentes ya existentes e **invoca el Catalogador**:

- **Adaptador de formatos** (`agent_ethack_dfir/scripts/power_adapter.py`, tarea 1.10): normaliza
  Powers en `plugin.json` y en `POWER.md` a la vista común `x-ethack`, de modo
  que ambos se validen con criterios equivalentes (`tools` no vacío,
  `ecCouncilPhase` xor `forensicsStage`, `allowlistValidation.required == true`,
  `executionMode.allowed == {script-kiddie, green-hat, pro}` con default
  `script-kiddie`).
- **docStatus** (`agent_ethack_dfir/scripts/check_power_docs.py`, tarea 13.1): verifica la
  presencia de los Artefactos_Documentacion bajo `docs/` (`prompt.md`,
  `sessions/`, `feedback.md`) y lista los faltantes.
- **Guardia de la Allowlist_Objetivos** (`validate_target.py`, tarea 1.3):
  confirma que la validación de alcance está cableada, de modo que cada Power
  dirija su Herramienta_Real únicamente a objetivos autorizados (Contenedor_
  Objetivo) y nunca al host subyacente salvo autorización explícita.
- **Cobertura y conteo vía Catalogador** (`agent_ethack_dfir/scripts/catalog.py`, tarea 1.9):
  regenera `inventory.json` con `build_inventory()` (también disponible como
  `make catalog`, nunca se edita a mano) y usa `coverage_gaps()` (cobertura de
  las 5 fases EC-Council y las 6 etapas del Flujo_Investigacion) y
  `count_tooled_by_owner()` (mínimo de **≥2 Powers con Herramienta_Real por
  alumno**, Req 9.6).

### 5.4 Qué pasa cuando la compuerta no se supera

- Si la **Validacion_Local falla** o la **revisión del Líder Técnico no se
  supera**, el **PR no se integra**. El Líder Técnico indica el incumplimiento
  concreto: qué **regla del modelo** de Power o qué **política** (ética/de
  laboratorio) falló, para que el alumno lo corrija y vuelva a solicitar la
  integración.
- **Excepción esperada (no es fallo):** la línea base deja **dos huecos de
  cobertura** conocidos —**Covering Tracks** (Red Team) y
  **detección/hardening del Blue Team**— que `coverage_gaps()` marca con
  `gap: true`. Estos dos huecos de baseline **no cuentan como fallo** de la
  compuerta; se reportan como pendientes hasta que exista un Power nuevo que los
  cubra.
