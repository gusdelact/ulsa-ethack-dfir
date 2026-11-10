#!/usr/bin/env python3
# scripts/gate_mcp_sim.py  — variante DIDACTICA, no bloqueante (Req 10.1-10.3)
#
# Contraste con el gate_mcp.py "fail-closed" del starter:
#   - El starter aplica "Authorization First" de forma estricta: si la invocacion
#     de la Herramienta_Real no esta cubierta por la autorizacion (EH_GRANT_PATH),
#     ABORTA con `exit 2` y el evento NO se ejecuta (fail-closed).
#   - Esta variante del aula evalua las MISMAS condiciones y conserva el mismo
#     registro de evaluacion (herramienta + objetivo + resultado de cada
#     condicion), pero SOLO emite una advertencia didactica y SIEMPRE retorna
#     `exit 0`: nunca bloquea el ejercicio. Sirve para que el alumno vea el
#     razonamiento de autorizacion sin frenar el laboratorio.
#
# Decision "autorizada" (Req 10.1, 10.3): se cumple si y solo si TODAS las
# condiciones de `reasons` son verdaderas:
#   - grant presente y legible (EH_GRANT_PATH absoluto, existe y es JSON valido)
#   - status == "approved"
#   - NO caducado: si el grant declara expiracion/ventana, debe estar vigente;
#     si no declara expiracion, no se bloquea por ello pero se registra en notes
#     (comprobacion defensiva, Req 10.3)
#   - herramienta declarada presente en allowed_tools
#   - objetivo declarado presente en los targets de esa herramienta
import datetime, json, os, sys, urllib.parse
from pathlib import Path


def warn(msg):  # advertencia didactica, NO bloquea
    print(f"[AUTORIZACION SIMULADA] {msg}", file=sys.stderr)


def normalize_target(v):
    # Normaliza host/IP/URL a una forma comparable (misma logica que el gate
    # fail-closed del starter) para que "entrenamiento.lab" y "https://Entrenamiento.lab/"
    # se reconozcan como el mismo objetivo. Devuelve None si no es un string util.
    if not isinstance(v, str) or not v.strip():
        return None
    v = v.strip()
    if "://" in v:
        try:
            u = urllib.parse.urlsplit(v)
            if u.scheme not in ("http", "https") or u.username or u.password or not u.hostname:
                return None
            v = u.hostname
        except ValueError:
            return None
    return v.strip("[]").rstrip(".").lower()


def _check_expiry(grant, reasons, notes):
    # Comprobacion de caducidad defensiva (Req 10.3):
    #   - acepta `expires_at` (ISO-8601) o `authorized_window.end`
    #   - si NO hay campo de expiracion: no se agrega condicion a `reasons`
    #     (no bloquea) pero se deja constancia en `notes`
    #   - si hay expiracion ilegible o sin zona horaria: condicion `no_caducado`
    #     en False (grant malformado => no autorizado, con nota explicativa)
    raw = grant.get("expires_at")
    if raw is None:
        win = grant.get("authorized_window")
        if isinstance(win, dict):
            raw = win.get("end")
    if raw is None:
        notes.append("grant sin campo de expiracion; no se bloquea por caducidad (Req 10.3)")
        return
    try:
        expiry = datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        reasons["no_caducado"] = False
        notes.append(f"expiracion ilegible: {raw!r}")
        return
    if expiry.tzinfo is None:
        reasons["no_caducado"] = False
        notes.append("expiracion sin zona horaria; se trata como invalida")
        return
    now = datetime.datetime.now(datetime.timezone.utc)
    reasons["no_caducado"] = expiry > now
    if not reasons["no_caducado"]:
        notes.append(f"grant caducado el {expiry.isoformat()}")


def evaluate(evt):
    tool = evt.get("tool_name", "")
    params = evt.get("tool_input", {}) if isinstance(evt.get("tool_input"), dict) else {}
    # Objetivo declarado en el evento (se identifica para el registro, Req 10.3)
    target = next((params[k] for k in ("target", "host", "hostname", "domain", "url") if k in params), None)
    reasons = {}
    notes = []
    # EH_GRANT_PATH: autorizacion externa, fuera del workspace, custodiada por el docente.
    path = os.environ.get("EH_GRANT_PATH")
    grant = {}
    if path and os.path.isabs(path) and os.path.exists(path):
        try:
            grant = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            reasons["grant_legible"] = False
    else:
        reasons["grant_presente"] = False
    if not isinstance(grant, dict):
        reasons["grant_legible"] = False
        grant = {}
    reasons["aprobado"] = grant.get("status") == "approved"
    allowed = grant.get("allowed_tools") or {}
    reasons["tool_permitido"] = tool in allowed
    accepted = ((allowed.get(tool) or {}).get("targets") or []) if isinstance(allowed, dict) else []
    norm_target = normalize_target(target)
    accepted_norm = {normalize_target(x) for x in accepted if isinstance(x, str)}
    accepted_norm.discard(None)
    reasons["objetivo_cubierto"] = bool(norm_target and norm_target in accepted_norm)
    _check_expiry(grant, reasons, notes)
    return tool, target, reasons, notes


def main():
    try:
        evt = json.load(sys.stdin)
    except (ValueError, UnicodeDecodeError):
        warn("evento JSON invalido")
        return 0
    if not isinstance(evt, dict):
        warn("evento con formato inesperado")
        return 0
    tool, target, reasons, notes = evaluate(evt)
    autorizado = all(reasons.values())
    record = {
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tool": tool,
        "target": target,
        "reasons": reasons,
        "notes": notes,
        "authorized": autorizado,
    }
    Path("local-audit").mkdir(exist_ok=True)
    (Path("local-audit") / "authz.jsonl").open("a", encoding="utf-8").write(
        json.dumps(record, ensure_ascii=False) + "\n")
    if not autorizado:
        warn(f"'{tool}' sobre '{target}' no esta cubierto por la autorizacion simulada. "
             "En produccion esto se bloquearia (fail-closed, exit 2).")
    return 0  # modo didactico: NUNCA bloquea


if __name__ == "__main__":
    sys.exit(main())
