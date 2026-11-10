#!/usr/bin/env python3
# scripts/audit_event.py  — Hook_Auditoria (PostToolUse)
# Resumen + sha256 del evento, anotando el Modo_Ejecucion aplicado (Req 10.4, 14.6).
#
# Registra en local-audit/events.jsonl un record con time_utc, tool, mode y sha256.
# Es trazabilidad didactica, no evidencia forense inmutable; la evidencia forense
# real se preserva aparte (Req 5.4, 5.5).
import datetime, hashlib, json, sys
from pathlib import Path

DEFAULT_MODE = "script-kiddie"


def extract_mode(evt: dict) -> str:
    """Modo_Ejecucion aplicado; cae al default si el evento no lo declara (Req 14.2, 14.6)."""
    ti = evt.get("tool_input") if isinstance(evt.get("tool_input"), dict) else {}
    return evt.get("mode") or ti.get("Modo_Ejecucion") or DEFAULT_MODE


def main() -> int:
    try:
        evt = json.load(sys.stdin)
    except (ValueError, UnicodeDecodeError):
        return 0
    payload = json.dumps(evt, ensure_ascii=False, sort_keys=True)
    record = {
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tool": evt.get("tool_name", ""),
        "mode": extract_mode(evt),                                      # Modo_Ejecucion aplicado  Req 14.6
        "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),  # Req 10.4
    }
    Path("local-audit").mkdir(exist_ok=True)
    (Path("local-audit") / "events.jsonl").open("a", encoding="utf-8").write(
        json.dumps(record, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
