# Reporte — Ciclo completo contra DVWA (`dvwa-lab-ulsa`)

**Engagement:** `dvwa-lab-ulsa` · **Fecha:** 2026-11-10 (UTC 18:53 → 19:03) · **Resultado:** `make validate` **VERDE** (2 huecos esperados)
**Objetivo:** `dvwa-01` → DVWA v1.10 sobre Apache 2.4.25 (Debian), EC2 `i-0b173b90eb54b63cb`, privada `10.50.0.224:80`
**Atacante:** Kali `i-0d16e800fbba08eac` con nmap 7.99 y curl 8.17.0
**Modo de los Powers:** `script-kiddie` (default, nivel de entrada)

> El pentest no es un atacante automático: es un orquestador determinista que delega en subagentes, respeta una `Allowlist_Objetivos` y produce artefactos verificables. La "velocidad" del script-kiddie es en explicación, no en reglas.

---

## 1. Flujo ejecutado (8 fases)

| # | Fase | Subagente/Power | Qué se hizo | Evidencia nueva |
|---|---|---|---|---|
| 1 | Reconnaissance | fase-recon + `osint-passive-recon` | Reutilizado del estado previo | — |
| 2 | **Scanning** | fase-scanning + `footprinting-enumeration` | `nmap -Pn -sV -p80 --script=http-title,http-server-header,http-headers 10.50.0.224` | `evidence/scan-dvwa-01-0001/` |
| 3 | **Gaining Access** | fase-gaining + `exploitation-metasploit` | PoC CWE-78 con `ip=127.0.0.1;id` → `uid=33(www-data)` | `evidence/webex-dvwa-01-0001/raw/gaining/` |
| 4 | **Maintaining Access** | fase-maintaining | Cookie `PHPSESSID` reutilizada 2m07s después sin re-login; `;hostname` → `1288e81c1735`; `ls` confirma no-persistencia | `evidence/webex-dvwa-01-0001/raw/maintaining/` |
| 5 | Covering Tracks | — | **Parada controlada**: hueco de baseline (`gap: true`, pending_team=`red-team`) | registro de parada |
| 6 | **Digital Forensics** | rol `digital-forensics` + `dfir-linux`, `network-forensics` | Collect (`scp`) → Preserve (`chmod a-w`, hash MATCH) → Analyze (IoCs) → Report (`record.json` + chain) | 2 piezas, cadena enlazada OK |
| 7 | **Incident Responder** | rol `incident-responder` | `incidents/inc-0002/incident.json`, NIST 800-61 fase **Detection & Analysis** | 6 IoCs ATT&CK verificados |
| 8 | **GRC** | rol `grc` + Power `grc-nist-csf` | 4 riesgos + perfil CSF + POA&M; ALE del crítico | `grc/*.real.json` |

Plantillas (`mem-dvwa-01-0001/`, `inc-0001/`, `grc/*.json` sin `.real`) y `state.json`: **intactos**.

---

## 2. Scope y guardia (`authorization-first`)

`scope.yaml` ajustado a la pasada real:

```yaml
authorized_window: { start: 2026-11-10T00:00:00Z, end: 2026-11-10T23:59:59Z }
assets:
  - id: dvwa-01
    target_host: 100.31.187.69          # publica (prefix list alumnos-ethack)
    target_hostname: 10.50.0.224        # privada (via Kali, misma VPC)
    target_port: 80
    host_is_target: false               # EC2 anfitriona NO es objetivo
prohibited_actions: [acceder_a_produccion, persistencia_oculta, exfiltracion, denegacion_de_servicio]
```

**`validate_target.py` self-check:**

| Objetivo | ¿En alcance? |
|---|---|
| `http://100.31.187.69/login.php` / `10.50.0.224` | sí |
| `44.213.147.197` (Kali, no es objetivo) | no |
| `10.0.10.21` (EC2 original del scope previo) | no |
| `attacker.example.com` | no |

---

## 3. Evidencia (cadena de custodia)

```
evidence/
├── mem-dvwa-01-0001/      PLANTILLA (intacta)
├── scan-dvwa-01-0001/
│   ├── record.json        sha256 d52839...287f51  (nmap xml principal)
│   ├── chain_of_custody.jsonl   seq 0..3  collect→transfer→preserve→analyze  (OK)
│   └── raw/               4 archivos nmap, write-once
└── webex-dvwa-01-0001/
    ├── record.json        sha256 3975c3...0331b9  (exec_post.html: prueba uid=www-data)
    ├── chain_of_custody.jsonl   seq 0..4  (+collect-additional de maintaining)  (OK)
    └── raw/
        ├── gaining/       7 HTTP crudos + SHA256SUMS
        └── maintaining/   5 HTTP crudos + SHA256SUMS
```

**Regla:** rango de volatilidad 5 (disco) con nota de origen de red; `prev_sha256` enlaza cada eslabón al anterior; `chmod a-w` fija write-once. **Discrepancia de hash = cadena rota**.

---

## 4. Incidente — `inc-0002`

**NIST SP 800-61:** `Preparation` → `Detection & Analysis` (actual). `Containment` pendiente para Blue Team (hueco).

**IoCs mapeados a MITRE ATT&CK (verificados):**

| # | Tipo | Valor | Kill Chain | ATT&CK |
|---|---|---|---|---|
| ioc-01 | URL | `/vulnerabilities/exec/` | Exploitation | **T1190** Exploit Public-Facing Application |
| ioc-02 | payload | `ip=127.0.0.1;id` | Exploitation | **T1059** Command and Scripting Interpreter |
| ioc-03 | process | `uid=33(www-data)` | Exploitation | **T1033** System Owner/User Discovery |
| ioc-04 | hostname | `1288e81c1735` (Docker) | Exploitation | **T1082** System Information Discovery |
| ioc-05 | cookie | `PHPSESSID` sin HttpOnly/Secure | C2 | **T1550.004** Web Session Cookie |
| ioc-06 | scan | `nmap --script=http-*` | Reconnaissance | **T1595.002** Vulnerability Scanning |

---

## 5. GRC — 4 riesgos, invariante OK

**INVARIANTE verificada automáticamente** (`gaps == POA&M == risks`):

```
{DE.CM-01, PR.AA-05, PR.PS-01, PR.PS-06}   ← subcategorías con gap==true
{DE.CM-01, PR.AA-05, PR.PS-01, PR.PS-06}   ← csf_subcategory del POA&M
{DE.CM-01, PR.AA-05, PR.PS-01, PR.PS-06}   ← csf_subcategory de los riesgos
```

| Riesgo | Escenario (una línea) | P×I | Residual | CSF | ALE |
|---|---|---|---|---|---|
| r-01 | CWE-78 explotable como `www-data` | 5×4=20 Crítico | 1×3=3 Bajo | **PR.PS-06** | **1.225 M MXN/año** justifica control |
| r-02 | `PHPSESSID` sin flags → hijacking | 4×4=16 Crítico | 2×3=6 Medio | **PR.AA-05** | — |
| r-03 | Sin cabeceras HTTP ni HTTPS | 4×3=12 Alto | 2×2=4 Bajo | **PR.PS-01** | — |
| r-04 | Sin monitoreo/detección | 5×4=20 Crítico | 2×3=6 Medio | **DE.CM-01** | — |

Apetito propuesto: `max_residual_score ≤ 8`. Los 4 quedan `within_appetite`.

**Subcategorías CSF ya logradas (sin gap):** `GV.OC-03` (scope ético documentado), `RS.AN-03` (análisis de incidente), `RS.AN-07` (cadena de custodia).

**Target tier:** 3 (Repeatable) en 12 meses. Actual: 1 en gobierno y en gestión.

---

## 6. Las 3 paradas que definen el agente

1. **Guardia de allowlist:** si un objetivo no normaliza a un endpoint autorizado → `OutOfScopeError` y no se ejecuta la herramienta.
2. **Orden canónico EC-Council:** si pides una fase saltándote predecesoras → el orquestador reporta `pending_previous` y no delega.
3. **Hueco de baseline:** si una fase/etapa no tiene Power que la cubra (Covering Tracks, Blue Team) → `enabled=false`, el orquestador no delega y el hueco queda registrado como pendiente del alumno.

---

## 7. Comandos clave (reproducibles)

```bash
# Validación local completa (compuerta)
make validate

# Allowlist self-check
python3 -c "import sys,yaml;sys.path.insert(0,'agent_ethack_dfir/scripts');\
  import validate_target as vt;\
  a=yaml.safe_load(open('agent_ethack_dfir/engagements/dvwa-lab-ulsa/scope.yaml'))['assets'];\
  print(sorted(vt.scope_endpoints(a)))"

# Verificar invariante GRC (gaps == POA&M == risks)
python3 - <<'PY'
import json; grc='agent_ethack_dfir/engagements/dvwa-lab-ulsa/grc/'
rr=json.load(open(grc+'risk_register.real.json'))
cp=json.load(open(grc+'csf_profile.real.json'))
g={s['id'] for s in cp['subcategories'] if s['gap']}
p={x['csf_subcategory'] for x in cp['poam']}
r={x['csf_subcategory'] for x in rr['risks']}
print('invariante:', g==p==r, '->', sorted(g))
PY

# Verificar cadena de custodia enlazada por prev_sha256
python3 -c "import json,pathlib;[(print(d.name, all(l['prev_sha256']==prev or (l['seq']==0 and l['prev_sha256'] is None) for prev,l in zip([None]+[json.loads(x)['sha256'] for x in open(d/'chain_of_custody.jsonl')], [json.loads(x) for x in open(d/'chain_of_custody.jsonl')])))) for d in sorted(pathlib.Path('agent_ethack_dfir/engagements/dvwa-lab-ulsa/evidence').iterdir()) if (d/'chain_of_custody.jsonl').exists()]"
```

---

## 8. Qué pide el proyecto final del alumno (los 2 huecos)

El agente está construido de modo que el alumno no empieza de cero: hereda la máquina de estados, la guardia, el inventario y los Powers base. Lo que falta son **las dos piezas que cierran el ciclo**:

| Hueco | Lo que debe aportar el alumno | Lo cierra por |
|---|---|---|
| **Covering Tracks** (`red-team`) | Power(s) con herramienta real: tampering de logs del propio objetivo *demostrado y reversible*, mapeado a **T1070** y **T1562** | Sube `enabled=true` en `state.json` |
| **Blue Team detection/hardening** (`blue-team`) | Power(s) con herramienta real: ingesta de logs al SIEM, reglas de detección para los IoCs ioc-01..06, hardening HTTP | **Cierra la brecha `DE.CM-01` que este reporte deja abierta** |

**Req 9.6** exige ≥2 Powers con herramienta real por alumno; `make validate` lo cuenta.

---

## 9. Lo que NO hicimos (por disciplina de PoC)

- No se abrió shell reversa, no se escaló a root, no se leyeron `/etc/shadow` ni otros archivos sensibles.
- No se dejó webshell ni cron ni usuario nuevo. **Verificado** por el propio PoC (`ls /var/www/html/vulnerabilities/exec/` → solo `help`, `index.php`, `source`).
- No se probaron los niveles Medium/High de DVWA (fuera de alcance didáctico para la primera iteración).
- No se tocó la EC2 anfitriona (fuera de alcance, `host_is_target: false`).
- No se ejecutó Metasploit; curl bastó para el PoC. Metasploit queda como ejercicio del alumno para el PoC del propio hueco Covering Tracks.

---

## 10. Firmas (artefactos clave)

```
evidence/scan-dvwa-01-0001/record.json         (nmap xml)      d52839283661afda4707e9f9f79e3966c0bc44b7d4556c141bd539965e287f51
evidence/webex-dvwa-01-0001/record.json        (exec_post.html) 3975c375303c02496490be3775a7d4a870df08132bf96261ef62b5ba5b0331b9
incidents/inc-0002/incident.json                                (nist_phase=Detection & Analysis, 6 IoCs ATT&CK)
grc/risk_register.real.json                                     (4 riesgos, ALE para r-01)
grc/csf_profile.real.json                                       (target_tier=3, 4 gaps = 4 POA&M)
scope.yaml                                                      (ventana 2026-11-10; objetivos localhost→cloud ajustados)
```

---

*Reporte generado por el agente Ethical Hacking + DFIR + GRC (ULSA, ciclo 2026).*
*Metodología: EC-Council · NIST SP 800-61 · NIST CSF 2.0 · RFC 3227 · MITRE ATT&CK.*
