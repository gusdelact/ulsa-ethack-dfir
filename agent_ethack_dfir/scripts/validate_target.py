"""Guardia de la Allowlist_Objetivos — utilidad compartida de alcance.

Esta utilidad resuelve y valida el objetivo de cada acción ofensiva o forense
contra la ``Allowlist_Objetivos`` del engagement **antes** de que un Power
ejecute su Herramienta_Real. La invoca cada Power como paso previo obligatorio
(Req 9.5: "WHEN un Power invoca una Herramienta_Real, THE Power SHALL ... validar
que el objetivo pertenece a la Allowlist_Objetivos antes de ejecutar la
herramienta").

Modelo de alcance (Req 11.4, 12.2, 12.3): los ``assets`` del ``scope.yaml``
modelan el **Contenedor_Objetivo** que expone el servicio sobre su host EC2
anfitrión. El objetivo autorizado es el contenedor/servicio
(``target_host``/``target_hostname``); el host EC2 subyacente
(``ec2_host``/``ec2_hostname``) queda **fuera de alcance** salvo que el asset lo
autorice explícitamente con ``host_is_target == true``.

Principios_Eticos aplicados:
  - Scope Discipline (Req 11.1, 11.2): toda actividad se dirige únicamente a
    objetivos presentes en la Allowlist_Objetivos; un objetivo fuera de ella se
    rechaza indicando que está fuera del alcance autorizado.
  - Nunca producción (Req 11.3): cualquier objetivo que no resuelva a un
    Contenedor_Objetivo autorizado se trata como producción no autorizada y el
    sistema se abstiene de actuar sobre él.
  - Contenedor, no host (Req 11.4): la prueba de penetración apunta al
    Contenedor_Objetivo; el host EC2 no es objetivo salvo autorización explícita.

Referencia de diseño: design.md, sección "Validación de la Allowlist_Objetivos
en el Power". La lógica de normalización reutiliza la del starter (``gate_mcp.py``).
"""

from __future__ import annotations

import ipaddress
import urllib.parse
from typing import Callable, Optional


class OutOfScopeError(Exception):
    """El objetivo no pertenece a la Allowlist_Objetivos autorizada.

    Se lanza cuando un objetivo no resuelve a un Contenedor_Objetivo autorizado
    (ni a un host EC2 explícitamente autorizado). El Power no ejecuta la
    Herramienta_Real e informa el alcance autorizado (Req 11.2, 11.3, 11.4).
    """


def normalize_target(v: str) -> Optional[str]:
    """Normaliza un objetivo (host, IP o URL) a su forma canónica comparable.

    Acepta host/IP/URL y devuelve una forma normalizada: en minúsculas, sin
    punto final, sin corchetes IPv6 y usando únicamente el ``hostname`` cuando
    la entrada es una URL. Devuelve ``None`` cuando la entrada no es un objetivo
    de red válido y comparable, de modo que la guardia lo trate como fuera de
    alcance (Req 11.1, 11.2).

    Reglas de rechazo (devuelven ``None``):
      - Entrada vacía o que no es ``str``.
      - URL con esquema distinto de ``http``/``https`` (Req 11.1: solo se admite
        tráfico web de laboratorio por nombre de host).
      - URL que incluye credenciales embebidas (``user``/``password``): se
        rechazan por higiene de alcance y para no filtrar secretos.
      - URL sin ``hostname``.
      - Host (no URL) que contiene separadores de ruta/consulta/credenciales o
        espacios (``/ \\ ? # @ ; `` y espacio), que indicarían algo distinto de
        un host plano.
      - IPv6 sin corchetes que no sea una dirección IP válida.

    Args:
        v: Objetivo en bruto tal como lo recibe el Power (host, IP o URL).

    Returns:
        El objetivo normalizado, o ``None`` si no es válido/comparable.
    """
    if not isinstance(v, str) or not v.strip():
        return None
    v = v.strip()
    if "://" in v:
        u = urllib.parse.urlsplit(v)
        # Solo http(s), sin credenciales embebidas y con hostname presente.
        if u.scheme not in ("http", "https") or u.username or u.password or not u.hostname:
            return None
        v = u.hostname
    else:
        # Un host plano no debe contener separadores de ruta/consulta/credenciales.
        if any(c in v for c in "/\\?#@; "):
            return None
        # Un IPv6 sin corchetes debe ser una dirección IP válida; en caso
        # contrario se descarta (ValueError -> fuera de alcance).
        if ":" in v and not v.startswith("["):
            try:
                ipaddress.ip_address(v)
            except ValueError:
                return None
    return v.strip("[]").rstrip(".").lower()


def scope_endpoints(assets: list[dict]) -> set[str]:
    """Resuelve el alcance autorizado al Contenedor_Objetivo de cada asset.

    Construye el conjunto de endpoints válidos a partir de
    ``target_host``/``target_hostname`` de cada asset e **incluye el host EC2
    anfitrión** (``ec2_host``/``ec2_hostname``) **solo si** el asset declara
    ``host_is_target == true`` (Req 11.4, 12.2, 12.3). Así, apuntar al host EC2
    subyacente de un servicio en contenedor queda fuera de alcance a menos que
    la Allowlist lo autorice explícitamente.

    Args:
        assets: Lista de assets de la Allowlist_Objetivos (``scope.yaml.assets``),
            cada uno modelado como Contenedor_Objetivo sobre su host EC2.

    Returns:
        Conjunto de endpoints normalizados que están dentro del alcance
        autorizado.
    """
    allowed: set[str] = set()
    for a in assets:
        # Objetivo autorizado = contenedor/servicio que expone el asset.
        for key in ("target_host", "target_hostname"):
            n = normalize_target(a.get(key, ""))
            if n:
                allowed.add(n)
        # Host EC2 anfitrión: dentro de alcance solo si está autorizado explícito.
        if a.get("host_is_target") is True:
            for key in ("ec2_host", "ec2_hostname"):
                n = normalize_target(a.get(key, ""))
                if n:
                    allowed.add(n)
    return allowed


def target_in_scope(target: str, assets: list[dict]) -> bool:
    """Indica si ``target`` resuelve a un endpoint autorizado de la allowlist.

    Normaliza el objetivo y comprueba su pertenencia al conjunto resuelto por
    :func:`scope_endpoints` (Req 11.1, 11.2). Un objetivo que no normaliza
    (``None``) nunca está en alcance.

    Args:
        target: Objetivo solicitado (host, IP o URL).
        assets: Lista de assets de la Allowlist_Objetivos.

    Returns:
        ``True`` si el objetivo normalizado pertenece al alcance autorizado.
    """
    t = normalize_target(target)
    return t is not None and t in scope_endpoints(assets)


def run_tool_guarded(
    target: str,
    assets: list[dict],
    run_tool: Callable[[str], object],
) -> object:
    """Ejecuta la Herramienta_Real solo si el objetivo está en alcance.

    Punto de entrada que cada Power usa para envolver la invocación de su
    Herramienta_Real. Si el objetivo no resuelve a un Contenedor_Objetivo
    autorizado (ni a un host EC2 explícitamente autorizado) de la allowlist,
    lanza :class:`OutOfScopeError` y **no** ejecuta la herramienta, informando el
    alcance autorizado (Req 11.2, 11.3, 11.4).

    Args:
        target: Objetivo solicitado (host, IP o URL).
        assets: Lista de assets de la Allowlist_Objetivos.
        run_tool: Callable que ejecuta la Herramienta_Real sobre el objetivo.

    Returns:
        El resultado de ``run_tool(target)`` cuando el objetivo está en alcance.

    Raises:
        OutOfScopeError: Si el objetivo está fuera del alcance autorizado.
    """
    if not target_in_scope(target, assets):
        raise OutOfScopeError(
            f"Objetivo fuera de alcance autorizado (contenedor/servicio): {target!r}"
        )
    return run_tool(target)
