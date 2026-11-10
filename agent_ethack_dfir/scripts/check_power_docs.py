"""Estado de los Artefactos_Documentacion de un Power — `scripts/check_power_docs.py` (tarea 13.1).

Al **incorporar** un Power, el Líder Técnico calcula su ``docStatus``: marca cada
Artefacto_Documentacion presente/ausente bajo ``docs/`` y, si falta alguno, deja
``complete: false`` con la lista ``missing`` para **señalar los artefactos
faltantes** (Req 15.6). La integración **no se bloquea** por documentación
incompleta: el Power se registra marcado como "documentación incompleta" hasta que
se complete (design.md "Convención de integración de Powers", paso 4).

Artefactos_Documentacion requeridos (Req 15.1, 15.6):

  - ``docs/prompt.md``   — el prompt de generación del Power.
  - ``docs/sessions/``   — las sesiones de interacción con Kiro para probarlo.
  - ``docs/feedback.md`` — la realimentación del resultado al chat/contexto.

Este módulo expone una **función reutilizable** :func:`doc_status` (consumida por
`scripts/integrate_power.py` y por el agregador de la Validacion_Local, design.md
paso 2 de "Validacion_Local") y un **CLI** para inspeccionar uno o más Powers.

Requisitos: 15.5, 15.6.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Artefactos_Documentacion mínimos bajo docs/ (Req 15.1). El sufijo "/" marca el
# artefacto que es un directorio (sessions/), coincidiendo con la etiqueta usada en
# el Catalogador (scripts/catalog.py) para que 'missing' sea consistente en todo el
# sistema.
REQUIRED_DOCS = ("prompt.md", "sessions/", "feedback.md")


def doc_status(power_dir) -> dict:
    """Calcula el ``docStatus`` de un Power a partir de su carpeta ``docs/`` (Req 15.6).

    Comprueba la presencia de los tres Artefactos_Documentacion requeridos bajo
    ``<power_dir>/docs``: ``prompt.md`` (fichero), ``sessions/`` (directorio) y
    ``feedback.md`` (fichero). ``complete`` es ``True`` solo si están los tres;
    ``missing`` es exactamente el complemento de los presentes (las etiquetas de
    :data:`REQUIRED_DOCS`), de modo que la integración pueda **señalar** lo que falta
    sin bloquearse.

    No lanza excepciones: si ``docs/`` no existe, los tres artefactos se reportan
    como ausentes.

    Args:
        power_dir: Ruta del directorio del Power (``powers/<nombre>/`` o
            ``powers/<equipo>/<power>/``).

    Returns:
        ``dict`` con las claves ``root`` (ruta de ``docs/``), ``prompt``,
        ``sessions``, ``feedback`` (booleanos de presencia), ``complete`` (bool) y
        ``missing`` (lista de etiquetas faltantes). La forma coincide con la que
        produce el Catalogador para cada entrada de ``inventory.json``.
    """
    docs = Path(power_dir) / "docs"
    has_prompt = (docs / "prompt.md").is_file()
    has_sessions = (docs / "sessions").is_dir()
    has_feedback = (docs / "feedback.md").is_file()
    present = {
        "prompt.md": has_prompt,
        "sessions/": has_sessions,
        "feedback.md": has_feedback,
    }
    missing = [name for name in REQUIRED_DOCS if not present[name]]
    return {
        "root": str(docs),
        "prompt": has_prompt,
        "sessions": has_sessions,
        "feedback": has_feedback,
        "complete": not missing,
        "missing": missing,
    }


def _resolve_targets(args: list[str]) -> list[Path]:
    """Resuelve los argumentos del CLI a directorios de Power.

    Cada argumento puede ser el directorio de un Power (contiene ``plugin.json`` o
    ``POWER.md``) o una carpeta ``powers/`` que se recorre con el descubrimiento de
    ambos layouts del adaptador (``power_adapter.find_power_dirs``), reutilizado para
    no duplicar la lógica de descubrimiento.
    """
    try:
        from scripts import power_adapter
    except ImportError:  # pragma: no cover - ejecución como script suelto
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import power_adapter  # type: ignore

    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if (p / "plugin.json").is_file() or (p / "POWER.md").is_file():
            targets.append(p)
        else:
            targets.extend(power_adapter.find_power_dirs(p))
    return targets


def _main(argv: list[str]) -> int:
    """CLI: reporta el ``docStatus`` de uno o más Powers (no bloquea, Req 15.6).

    Uso:
        python scripts/check_power_docs.py <power_dir|powers_root> [más...]

    Sin argumentos usa ``powers/`` relativo a la raíz del repositorio. Imprime, por
    Power, si la documentación está completa y, si no, los artefactos faltantes.
    Devuelve 0 siempre (señalar documentación incompleta **no** es un fallo que
    aborte la integración); el código 0 refleja que el check corrió, no que todo
    esté completo.
    """
    repo_root = Path(__file__).resolve().parent.parent
    args = argv[1:] or [str(
        repo_root / "powers" if (repo_root / "powers").is_dir() else repo_root.parent / "powers")]
    targets = _resolve_targets(args)

    if not targets:
        print("check_power_docs: no se encontraron Powers en las rutas dadas.")
        return 0

    incomplete = 0
    for d in targets:
        st = doc_status(d)
        rel = d.relative_to(repo_root) if str(d).startswith(str(repo_root)) else d
        if st["complete"]:
            print(f"[docs OK  ] {rel}  (prompt.md, sessions/, feedback.md)")
        else:
            incomplete += 1
            print(f"[docs FALTA] {rel}  faltan: {', '.join(st['missing'])}")

    print(f"\n{len(targets)} Powers revisados; {incomplete} con documentación incompleta "
          f"(se señalan al integrar, no bloquean — Req 15.6).")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
