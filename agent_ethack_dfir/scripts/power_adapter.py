"""Adaptador de convivencia de los dos formatos de Power (`plugin.json` ↔ `POWER.md`).

En `powers/` conviven **dos formatos de empaquetado** del modelo estándar de Power
(Req 8.2): el estilo *agent-plugins.org* con `plugin.json` y el estilo `POWER.md`
(frontmatter YAML + sección "modos de trabajo"). Ambos declaran —explícita o
implícitamente— el mismo contrato lógico bajo la clave `x-ethack`. Este módulo
**normaliza los dos formatos a una vista común** de esos campos para que el
Líder Técnico pueda validar cualquier entregable con **criterios equivalentes**
(Req 8.4, 9.2): fase/etapa, `executionMode`, `documentation`, `allowlistValidation`,
`tools`, `owner`, `team` y `kind`.

Contrato lógico `x-ethack` (design.md "`plugin.json` extendido del proyecto"):
  - ``tools``             — Herramienta_Real envuelta, lista no vacía (Req 9.1).
  - ``ecCouncilPhase``    — una de las 5 fases EC-Council, o ``None`` si es forense.
  - ``forensicsStage``    — etapa del Flujo_Investigacion, o ``None`` si es ofensivo.
                            Exactamente uno de los dos (xor) (Req 9.2).
  - ``allowlistValidation`` — política de validación de objetivo; ``required == True``
                            apuntando al ``scope.yaml`` del engagement (Req 9.5, 11.1).
  - ``executionMode``     — Modo_Ejecucion: ``allowed == {script-kiddie, green-hat, pro}``
                            con ``default == script-kiddie`` (Req 9.7, 14.1, 14.2).
  - ``documentation``     — Artefactos_Documentacion bajo ``documentation.root`` (Req 9.8, 15.1).

Comportamiento con `POWER.md` (Req 8.2, 9.2):
  - Si el frontmatter declara un bloque ``x-ethack`` explícito, se usa tal cual
    (mismo contrato que ``plugin.json``).
  - Si **no** lo declara (caso de los Powers base de conocimiento), el adaptador
    extrae los campos equivalentes del frontmatter (``name``, ``author`` → ``owner``,
    ``keywords``) e **infiere de forma conservadora** lo que pueda (p. ej. ``kind``
    por *keywords*/rol). Lo que no es derivable **no se inventa**: se marca como
    faltante en ``missing`` para que :func:`validate_power` lo reporte. El adaptador
    **degrada con gracia** (nunca lanza excepción por un `x-ethack` incompleto),
    de modo que los 9 Powers reales se cargan sin romperse (Req 8.4).

Funciones públicas:
  - :func:`load_power` — ``load_power(power_dir) -> dict`` (vista común ``x-ethack``).
  - :func:`validate_power` — ``validate_power(view) -> (ok, problemas[])`` con los
    invariantes equivalentes para ambos formatos.
  - :func:`find_power_dirs` — conveniencia para el CLI (descubrimiento canónico de
    ambos layouts reside en el Catalogador, ``scripts/catalog.py``).

Referencia de diseño: design.md "`plugin.json` extendido del proyecto",
"Modo_Ejecucion — selección, validación y comportamiento por modo" y
"Validacion_Local: única compuerta automatizada".
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import yaml

# Invariantes del Modo_Ejecucion (design.md; Req 14.1, 14.2).
ALLOWED_MODES = ("script-kiddie", "green-hat", "pro")
DEFAULT_MODE = "script-kiddie"

# Artefactos_Documentacion mínimos esperados bajo documentation.root (Req 15.1).
REQUIRED_DOCS = ("prompt.md", "sessions/", "feedback.md")

# Pistas de keywords → kind, para inferencia conservadora cuando el POWER.md base
# no declara x-ethack (Req 9.2). Solo se usan para *sugerir* el kind; nunca para
# fabricar fase/etapa ni herramientas (eso se deja como faltante).
_KIND_HINTS: dict[str, tuple[str, ...]] = {
    "forensics": (
        "forensics", "dfir", "digital-forensics", "linux-forensics",
        "network-forensics", "pcap", "autopsy", "volatility", "wireshark",
        "tcpdump", "netflow", "log-analysis",
    ),
    "response": (
        "incident-handling", "incident-response", "incident-response-lab",
        "nist-800-61", "soc-triage", "thehive", "wazuh", "virustotal",
        "cyber-kill-chain", "mitre-attack",
    ),
    "governance": (
        "grc", "governance", "risk-management", "compliance", "nist-csf",
        "csf-2.0", "risk-register", "gap-analysis",
    ),
    "defensive": (
        "blue-team", "defense", "defensive", "hardening", "detection",
        "detección", "monitoring",
    ),
    "offensive": (
        "ethical-hacking", "pentest", "offensive", "red-team", "osint",
        "footprinting", "enumeration", "nmap", "scanning", "exploitation",
        "metasploit", "vulnerability-assessment", "vulnerability-scanning",
    ),
}


def _blank_view(power_dir: Path, fmt: Optional[str]) -> dict:
    """Devuelve una vista común vacía con los campos del contrato ``x-ethack``.

    Todos los campos del contrato arrancan en ``None``/vacío; :func:`load_power`
    los rellena desde el formato concreto. ``missing`` e ``inferred`` sirven para
    la degradación con gracia (Req 8.4): registran qué no se declaró y qué se
    dedujo de forma conservadora.
    """
    return {
        "power_dir": str(power_dir),
        "name": None,
        "format": fmt,              # "plugin.json" | "POWER.md" | None
        "declared": False,          # ¿había un bloque x-ethack explícito?
        "kind": None,               # offensive|defensive|forensics|governance|response
        "ecCouncilPhase": None,     # 5 fases EC-Council, o None si es forense
        "forensicsStage": None,     # etapa del Flujo_Investigacion, o None si ofensivo
        "track": None,              # GRC|IR para Powers que no caen en fase/etapa (Req 9.2)
        "team": None,
        "owner": None,
        "tools": [],                # Herramienta_Real envuelta (Req 9.1)
        "allowlistValidation": {},  # Req 9.5, 11.1
        "executionMode": {},        # Req 9.7, 14.1
        "documentation": {},        # Req 9.8, 15.1
        "producesActionLog": None,
        "inferred": [],             # campos deducidos conservadoramente
        "missing": [],              # campos del contrato no declarados/derivables
    }


def _infer_kind(keywords: list, name: str) -> Optional[str]:
    """Infiere ``kind`` de forma conservadora a partir de keywords/rol (Req 9.2).

    Recorre las pistas por categoría en orden de especificidad (forense, respuesta,
    gobernanza y defensa antes que ofensivo, que es el más genérico). Devuelve el
    primer ``kind`` cuya pista aparezca en las keywords o en el nombre del Power, o
    ``None`` si no hay señal suficiente (en cuyo caso el campo queda como faltante).
    """
    haystack = {str(k).strip().lower() for k in (keywords or [])}
    haystack.add((name or "").strip().lower())
    hay = " ".join(haystack)
    for kind in ("forensics", "response", "governance", "defensive", "offensive"):
        for hint in _KIND_HINTS[kind]:
            if hint in haystack or hint in hay:
                return kind
    return None


def _apply_xethack(view: dict, x: dict) -> None:
    """Copia un bloque ``x-ethack`` explícito (de ``plugin.json`` o frontmatter) a la vista.

    Es el camino común de ambos formatos cuando el contrato está declarado: el
    ``plugin.json`` siempre lo trae, y un ``POWER.md`` de alumno puede declararlo en
    su frontmatter. Los campos ausentes del bloque se dejan en su valor vacío para
    que :func:`validate_power` los reporte (Req 8.4).
    """
    view["declared"] = True
    view["kind"] = x.get("kind")
    view["ecCouncilPhase"] = x.get("ecCouncilPhase")
    view["forensicsStage"] = x.get("forensicsStage")
    view["track"] = x.get("track")
    view["team"] = x.get("team", view.get("team"))
    view["owner"] = x.get("owner", view.get("owner"))
    view["tools"] = x.get("tools") or []
    view["allowlistValidation"] = x.get("allowlistValidation") or {}
    view["executionMode"] = x.get("executionMode") or {}
    view["documentation"] = x.get("documentation") or {}
    view["producesActionLog"] = x.get("producesActionLog")


def _parse_frontmatter(text: str) -> dict:
    """Extrae y parsea el frontmatter YAML (``---`` ... ``---``) de un ``POWER.md``.

    Devuelve el mapa del frontmatter, o ``{}`` si el documento no tiene frontmatter
    o el YAML no es un mapeo. No lanza por YAML inválido: devuelve ``{}`` para que
    el adaptador degrade con gracia (Req 8.4).
    """
    if not text.startswith("---"):
        return {}
    # Separa el primer bloque fenced ---\n ... \n---.
    parts = text.split("\n")
    if parts[0].strip() != "---":
        return {}
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            block = "\n".join(parts[1:i])
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError:
                return {}
            return data if isinstance(data, dict) else {}
    return {}


def load_power(power_dir) -> dict:
    """Carga un Power y lo normaliza a la **vista común** del contrato ``x-ethack``.

    Detecta el formato por los ficheros presentes en ``power_dir`` y produce una
    única vista con los campos del contrato, cualquiera que sea el empaquetado
    (Req 8.2, 9.2):

    - ``plugin.json`` (estilo agent-plugins.org): lee el bloque ``x-ethack``.
    - ``POWER.md`` (frontmatter YAML + "modos de trabajo"): si el frontmatter
      declara ``x-ethack``, se usa; si no, se extraen los equivalentes del
      frontmatter (``name``, ``author`` → ``owner``, ``keywords``) y se **infiere
      de forma conservadora** lo derivable (p. ej. ``kind`` por keywords/rol),
      marcando en ``missing`` lo que no se declara para que la validación lo
      reporte (Req 8.4).

    La función **degrada con gracia**: nunca lanza por un ``x-ethack`` incompleto o
    ausente, de modo que los 9 Powers reales de ``powers/`` se cargan sin romperse.
    Solo señala formato desconocido si el directorio no contiene ni ``plugin.json``
    ni ``POWER.md``.

    Args:
        power_dir: Ruta del directorio del Power (``powers/<nombre>/`` o
            ``powers/<equipo>/<power>/``).

    Returns:
        La vista común ``x-ethack`` como ``dict`` (ver :func:`_blank_view`), con
        ``missing`` e ``inferred`` poblados según lo encontrado.
    """
    power_dir = Path(power_dir)
    plugin = power_dir / "plugin.json"
    power_md = power_dir / "POWER.md"

    if plugin.is_file():
        view = _blank_view(power_dir, "plugin.json")
        try:
            data = json.loads(plugin.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            view["missing"].append("x-ethack")
            view["missing"].append(f"plugin.json ilegible: {exc}")
            return view
        view["name"] = data.get("name")
        author = data.get("author")
        if isinstance(author, dict):
            view["owner"] = author.get("name")
        elif isinstance(author, str):
            view["owner"] = author
        x = data.get("x-ethack")
        if isinstance(x, dict):
            _apply_xethack(view, x)
        else:
            view["missing"].append("x-ethack")
        return view

    if power_md.is_file():
        view = _blank_view(power_dir, "POWER.md")
        try:
            text = power_md.read_text(encoding="utf-8")
        except OSError as exc:
            view["missing"].append("x-ethack")
            view["missing"].append(f"POWER.md ilegible: {exc}")
            return view
        fm = _parse_frontmatter(text)
        view["name"] = fm.get("name") or fm.get("displayName")
        author = fm.get("author")
        if isinstance(author, str):
            view["owner"] = author
        elif isinstance(author, dict):
            view["owner"] = author.get("name")

        x = fm.get("x-ethack")
        if isinstance(x, dict):
            # POWER.md de alumno con contrato explícito: mismo camino que plugin.json.
            _apply_xethack(view, x)
            if not view.get("team"):
                view["team"] = fm.get("team")
            return view

        # POWER.md base sin x-ethack: extraer equivalentes + inferencia conservadora.
        view["declared"] = False
        if fm.get("team"):
            view["team"] = fm.get("team")
        kind = _infer_kind(fm.get("keywords") or [], view["name"] or "")
        if kind:
            view["kind"] = kind
            view["inferred"].append("kind")
        else:
            view["missing"].append("kind")
        # Lo demás no es derivable del POWER.md de conocimiento: se marca faltante
        # (no se inventa) para que validate_power lo reporte con criterio equivalente.
        if not view["tools"]:
            view["missing"].append("tools")
        view["missing"].append("ecCouncilPhase|forensicsStage")
        view["missing"].append("allowlistValidation")
        view["missing"].append("executionMode")
        view["missing"].append("documentation")
        if not view["owner"]:
            view["missing"].append("owner")
        if not view["team"]:
            view["missing"].append("team")
        return view

    # Ni plugin.json ni POWER.md: formato desconocido (degradación con gracia).
    view = _blank_view(power_dir, None)
    view["missing"].append("plugin.json|POWER.md")
    return view


def validate_power(view: dict) -> tuple[bool, list[str]]:
    """Valida la vista común contra los invariantes del modelo de Power (Req 9, 14).

    Aplica —con **criterios equivalentes** para ``plugin.json`` y ``POWER.md``— los
    invariantes del contrato ``x-ethack`` (design.md "Reglas del modelo"):

    1. ``tools`` no vacío — cada Power envuelve ≥1 Herramienta_Real (Req 9.1).
    2. ``ecCouncilPhase`` **xor** ``forensicsStage`` — exactamente una ubicación en
       el ciclo (Req 9.2). **Excepción (tarea 1.11):** los Powers que no caen en
       ninguno de los dos ejes —gobernanza (GRC) y respuesta a incidentes (IR)—
       declaran ``kind ∈ {governance, response}`` y ambos ejes en ``null``; en ese
       caso se exige en su lugar un ``track ∈ {GRC, IR}`` que los ubique. Cualquier
       otra combinación (ambos declarados, o ambos ``null`` sin ``track`` válido)
       sigue siendo inválida.
    3. ``allowlistValidation.required == True`` — validación de objetivo obligatoria
       contra la Allowlist_Objetivos (Req 9.5, 11.1).
    4. ``executionMode.allowed == {script-kiddie, green-hat, pro}`` con
       ``default == script-kiddie`` (Req 9.7, 14.1, 14.2).
    5. Artefactos_Documentacion presentes — ``documentation`` con ``root`` y lista
       ``required`` (Req 9.8, 15.1).

    No lanza excepciones: un Power incompleto (p. ej. un ``POWER.md`` base sin
    ``x-ethack``) produce ``ok == False`` y la lista de problemas, de modo que la
    Validacion_Local pueda **reportar** el incumplimiento en lugar de romperse
    (Req 8.4).

    Args:
        view: Vista común devuelta por :func:`load_power`.

    Returns:
        Tupla ``(ok, problemas)`` donde ``ok`` es ``True`` solo si no hay problemas.
    """
    problems: list[str] = []
    name = view.get("name") or view.get("power_dir") or "<power>"

    if view.get("format") is None:
        problems.append(f"{name}: sin plugin.json ni POWER.md (formato de Power desconocido)")
        return False, problems

    if not view.get("declared"):
        problems.append(
            f"{name}: no declara el contrato x-ethack "
            f"(faltan: {', '.join(view.get('missing') or ['x-ethack'])})"
        )

    # 1) tools no vacío (Req 9.1).
    tools = view.get("tools") or []
    if not isinstance(tools, list) or len(tools) == 0:
        problems.append(f"{name}: 'tools' vacío — un Power debe envolver ≥1 Herramienta_Real (Req 9.1)")

    # 2) ecCouncilPhase xor forensicsStage (Req 9.2), con excepción governance/response.
    #    Tarea 1.11: GRC e IR no son fase EC-Council ni etapa forense. Para esos Powers
    #    (kind ∈ {governance, response}) se admite que AMBOS ejes sean null siempre que
    #    declaren un 'track' ∈ {GRC, IR} que los ubique. El resto de combinaciones
    #    (ambos declarados, o ambos null sin track válido) sigue siendo inválido.
    _GOVRESP_KINDS = {"governance", "response"}
    _VALID_TRACKS = {"GRC", "IR"}
    phase = view.get("ecCouncilPhase")
    stage = view.get("forensicsStage")
    has_phase = phase is not None and str(phase).strip() != ""
    has_stage = stage is not None and str(stage).strip() != ""
    kind = view.get("kind")
    track = view.get("track")
    has_track = track is not None and str(track).strip() in _VALID_TRACKS
    is_govresp = kind in _GOVRESP_KINDS
    if has_phase and has_stage:
        problems.append(
            f"{name}: declara ecCouncilPhase Y forensicsStage — debe ser exactamente uno (xor) (Req 9.2)"
        )
    elif not has_phase and not has_stage:
        # Caso especial: gobernanza/respuesta con track en lugar de fase/etapa.
        if is_govresp and has_track:
            pass  # ubicación válida por 'track' (GRC/IR)
        elif is_govresp and not has_track:
            problems.append(
                f"{name}: kind '{kind}' sin ecCouncilPhase/forensicsStage debe declarar "
                f"un 'track' ∈ {{GRC, IR}} que lo ubique (Req 9.2)"
            )
        else:
            problems.append(
                f"{name}: no declara ni ecCouncilPhase ni forensicsStage — falta la ubicación en el ciclo (Req 9.2)"
            )

    # 3) allowlistValidation.required == true (Req 9.5, 11.1).
    av = view.get("allowlistValidation") or {}
    if not isinstance(av, dict) or av.get("required") is not True:
        problems.append(
            f"{name}: 'allowlistValidation.required' debe ser true (validación de objetivo obligatoria) (Req 9.5, 11.1)"
        )

    # 4) executionMode.allowed == {script-kiddie, green-hat, pro} con default script-kiddie (Req 9.7, 14.1).
    em = view.get("executionMode") or {}
    allowed = em.get("allowed") if isinstance(em, dict) else None
    if not isinstance(allowed, (list, tuple)) or set(allowed) != set(ALLOWED_MODES):
        problems.append(
            f"{name}: 'executionMode.allowed' debe ser exactamente {{{', '.join(ALLOWED_MODES)}}} (Req 14.1)"
        )
    if not isinstance(em, dict) or em.get("default") != DEFAULT_MODE:
        problems.append(
            f"{name}: 'executionMode.default' debe ser '{DEFAULT_MODE}' (Req 14.2)"
        )

    # 5) Artefactos_Documentacion presentes (Req 9.8, 15.1).
    doc = view.get("documentation") or {}
    if not isinstance(doc, dict) or not doc.get("root") or not doc.get("required"):
        problems.append(
            f"{name}: 'documentation' debe declarar 'root' y 'required' (Artefactos_Documentacion) (Req 9.8, 15.1)"
        )

    return (len(problems) == 0), problems


def find_power_dirs(powers_root) -> list[Path]:
    """Descubre directorios de Power en **ambos layouts** (conveniencia del CLI).

    Busca carpetas que contengan ``plugin.json`` o ``POWER.md`` tanto en un nivel
    (``powers/<nombre>/``, Powers base) como en dos (``powers/<equipo>/<power>/``,
    Powers de alumnos), ignorando la plantilla ``_template``. El descubrimiento
    **canónico** para el inventario reside en el Catalogador (``scripts/catalog.py``,
    ``discover_powers()``); esta función solo sirve al modo CLI de este adaptador.

    Args:
        powers_root: Ruta de la carpeta ``powers/``.

    Returns:
        Lista ordenada de rutas de directorios de Power.
    """
    powers_root = Path(powers_root)
    found: set[Path] = set()
    for marker in ("plugin.json", "POWER.md"):
        for hit in powers_root.rglob(marker):
            d = hit.parent
            if d.name == "_template" or "_template" in d.parts:
                continue
            found.add(d)
    return sorted(found)


def _main(argv: list[str]) -> int:
    """CLI: carga y valida los Powers bajo ``powers/`` (o rutas dadas) e informa.

    Uso:
        python scripts/power_adapter.py [powers_root_o_power_dirs...]

    Sin argumentos, usa ``powers/`` relativo a la raíz del repositorio. Imprime,
    por Power, el formato, la ubicación en el ciclo, el ``kind`` (y si fue inferido)
    y el resultado de :func:`validate_power`. Devuelve 0 siempre que la *carga* no
    rompa (la validez de cada Power se reporta, no aborta): así se demuestra la
    degradación con gracia sobre los 9 Powers reales (Req 8.4).
    """
    repo_root = Path(__file__).resolve().parent.parent
    args = argv[1:]
    if not args:
        targets = find_power_dirs(
            repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")
    else:
        targets = []
        for a in args:
            p = Path(a)
            if (p / "plugin.json").is_file() or (p / "POWER.md").is_file():
                targets.append(p)
            else:
                targets.extend(find_power_dirs(p))

    ok_count = 0
    for d in targets:
        view = load_power(d)
        ok, problems = validate_power(view)
        ok_count += 1 if ok else 0
        loc = view.get("ecCouncilPhase") or view.get("forensicsStage") or "—"
        kind = view.get("kind") or "—"
        kind_note = " (inferido)" if "kind" in view.get("inferred", []) else ""
        status = "OK" if ok else "!OK"
        rel = Path(view["power_dir"]).relative_to(repo_root) if str(view["power_dir"]).startswith(str(repo_root)) else view["power_dir"]
        print(f"[{status}] {rel}  fmt={view.get('format')}  kind={kind}{kind_note}  ciclo={loc}")
        for prob in problems:
            print(f"        - {prob}")
    print(f"\nCargados {len(targets)} Powers; válidos {ok_count}/{len(targets)} "
          f"(los no válidos se reportan, no rompen — Req 8.4).")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
