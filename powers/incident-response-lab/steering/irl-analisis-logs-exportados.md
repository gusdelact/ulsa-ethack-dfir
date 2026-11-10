# Análisis de logs exportados (sin MCP)

Para `logs-wazuh.zip` (Skills Assessment) y `wazuh_export.zip` (Insight Nexus), o cualquier
exportación de alertas de Wazuh con eventos de Windows/Sysmon.

Reglas: trabajar sobre una **copia**; calcular el hash del `.zip` original y registrarlo en
`05-evidencia-custodia.md` (R7). En modo Estudio, el agente da los comandos y explica qué buscar,
pero **el alumno lee el valor** (R-LAB6).

## 1. Preparar y reconocer el formato

```bash
CASE=incidentes/IR-2025-001          # carpeta del caso
mkdir -p "$CASE/evidencia" && cp ~/Downloads/logs-wazuh.zip "$CASE/evidencia/"
cd "$CASE/evidencia"
shasum -a 256 logs-wazuh.zip         # anotar en 05-evidencia-custodia.md
unzip -o logs-wazuh.zip -d logs-wazuh
find logs-wazuh -type f -exec file {} \; | head
head -c 1500 "$(find logs-wazuh -type f | head -1)"; echo
```

| Lo que se ve al inicio | Formato | Cómo leerlo |
|---|---|---|
| `{"timestamp":...}` una línea por evento | JSON Lines (como `alerts.json` de Wazuh) | `jq -c '.' archivo` |
| `[{"_index":...,"_source":{...}}` | Exportación del indexer/dashboard | `jq -c '.[] | ._source // .' archivo` |
| `{"hits":{"hits":[...]}}` | Respuesta de búsqueda del indexer | `jq -c '.hits.hits[] | ._source' archivo` |
| Encabezados separados por comas | CSV del dashboard | Python `csv` (ver paso 3, variante CSV) |
| `ElfFile` / `.evtx` | Log nativo de Windows | `python-evtx` o `chainsaw`/`hayabusa`; fuera de este flujo |

## 2. Normalizar a una línea por evento

Deja todo en `eventos.jsonl` con el contenido del evento (sin envoltorios):

```bash
find logs-wazuh -type f \( -name '*.json' -o -name '*.jsonl' -o -name '*.log' \) -print0 |
while IFS= read -r -d '' f; do
  jq -c 'if type=="array" then .[] elif (type=="object" and has("hits")) then .hits.hits[] else . end | ._source // .' "$f"
done > eventos.jsonl
wc -l eventos.jsonl
```

Ver la estructura de un evento de Windows:

```bash
jq -c 'select(.data.win != null)' eventos.jsonl | head -1 | jq '{timestamp, agent: .agent.name, rule: .rule.id, desc: .rule.description, system: .data.win.system, eventdata: .data.win.eventdata}'
```

En alertas de Wazuh, los campos de Windows están en `data.win.system.*` (`eventID`, `systemTime`,
`computer`, `channel`) y `data.win.eventdata.*` en camelCase (`commandLine`, `image`,
`parentImage`, `targetUserName`, `subjectUserName`, `ipAddress`, `logonType`, `shareName`,
`imagePath`, `serviceName`, `destinationIp`, `targetFilename`, `imageLoaded`). **Confirmarlo con el
primer evento**: si los nombres cambian, ajustar los filtros.

## 3. Tabla resumen

```bash
jq -r '[.timestamp, .agent.name, .rule.id, (.data.win.system.eventID // ""), .rule.description] | map(tostring) | join("\t")' eventos.jsonl \
  | sort > resumen.tsv
cut -f4 resumen.tsv | sort | uniq -c | sort -rn      # cuántos eventos por Event ID
cut -f3,5 resumen.tsv | sort | uniq -c | sort -rn | head -30   # reglas más frecuentes
```

Variante CSV:

```bash
python3 - <<'PY' logs-wazuh/*.csv
import csv, sys, collections
c = collections.Counter()
for p in sys.argv[1:]:
    with open(p, newline='', encoding='utf-8', errors='replace') as fh:
        r = csv.DictReader(fh)
        print("Columnas:", r.fieldnames)
        for row in r:
            c[row.get('data.win.system.eventID') or row.get('rule.id')] += 1
print(c.most_common(20))
PY
```

## 4. Filtros por pregunta de investigación

Definir una función para no repetir el `select`:

```bash
ev() { jq -c --arg id "$1" 'select((.data.win.system.eventID|tostring) == $id)' eventos.jsonl; }
```

| Pregunta | Event ID |
|---|---|
| ¿Qué procesos se crearon y quién los lanzó? | 4688 (Security), 1 (Sysmon) |
| ¿Hubo volcado de credenciales? | 4688/1 con herramientas conocidas; 10 (Sysmon, acceso a LSASS) |
| ¿Qué persistencia se creó? | 7045 (servicio), 4697, 4698 (tarea), 13 (Sysmon, registro) |
| ¿Quién inició sesión y desde dónde? | 4624 / 4625 |
| ¿Quién accedió a un share? | 5140 / 5145 |
| ¿A dónde se conectó un proceso? | 3 (Sysmon) |
| ¿Qué archivos se crearon? | 11 (Sysmon) |
| ¿Qué DLL cargó un proceso? | 7 (Sysmon) |
| ¿Hubo PowerShell sospechoso? | 4104 (Script Block), 4688/1 (ver paso 5) |
| ¿Se borraron logs? | 1102 |

```bash
row='map(tostring) | join("\t")'
E='.data.win.eventdata'

# Procesos (Security 4688 y Sysmon 1)
ev 4688 | jq -r "[.timestamp, .agent.name, $E.subjectDomainName+\"\\\\\"+$E.subjectUserName, $E.parentProcessName, $E.newProcessName, $E.commandLine] | $row"
ev 1    | jq -r "[.timestamp, .agent.name, $E.user, $E.parentImage, $E.image, $E.commandLine] | $row"

# Volcado de credenciales (cualquier evento que mencione herramientas o LSASS)
jq -r "select(tostring | test(\"mimikatz|sekurlsa|procdump|lsass|comsvcs\"; \"i\")) | [.timestamp, .agent.name, .rule.id, .rule.description] | $row" eventos.jsonl

# Persistencia: servicios nuevos y tareas programadas
ev 7045 | jq -r "[.timestamp, .agent.name, $E.serviceName, $E.imagePath] | $row"
ev 4698 | jq -r "[.timestamp, .agent.name, $E.subjectUserName, $E.taskName] | $row"

# Logons
ev 4624 | jq -r "[.timestamp, .agent.name, $E.targetDomainName+\"\\\\\"+$E.targetUserName, $E.logonType, $E.ipAddress] | $row"

# Acceso a shares
ev 5140 | jq -r "[.timestamp, .agent.name, $E.subjectDomainName+\"\\\\\"+$E.subjectUserName, $E.shareName, $E.ipAddress] | $row"

# Conexiones de red
ev 3 | jq -r "[.timestamp, .agent.name, $E.image, $E.destinationIp, $E.destinationPort] | $row" | sort -u

# Archivos creados
ev 11 | jq -r "[.timestamp, .agent.name, $E.image, $E.targetFilename] | $row"

# DLL cargadas (ej. vaultcli.dll)
ev 7 | jq -r "select($E.imageLoaded | test(\"vaultcli\"; \"i\")) | [.timestamp, .agent.name, $E.image, $E.imageLoaded] | $row"

# Borrado de logs
ev 1102 | jq -r "[.timestamp, .agent.name, .rule.description] | $row"
```

Búsqueda libre de un indicador (archivo, IP, usuario) en cualquier campo:

```bash
ioc() { jq -c --arg q "$1" 'select(tostring|test($q;"i"))' eventos.jsonl | jq -r '[.timestamp,.agent.name,.rule.id,.rule.description]|map(tostring)|join("\t")'; }
ioc 'diagnostics_data\.zip'
ioc 'projects'
```

Se usa `join("\t")` en lugar de `@tsv` porque `@tsv` duplica las barras invertidas (`INSIGHT\\jdoe` en lugar de `INSIGHT\jdoe`).

Si un campo no aparece, buscar su nombre real: `jq -r '.data.win.eventdata|keys[]' eventos.jsonl | sort | uniq -c`.

## 5. PowerShell codificado

Localizar comandos con `-enc`, `-e`, `-EncodedCommand` o `FromBase64String`:

```bash
jq -r 'select(tostring|test("-e(nc|ncodedcommand)?\\s|frombase64string";"i"))
       | [.timestamp, .agent.name,
          (.data.win.eventdata.subjectDomainName // "") + "\\" + (.data.win.eventdata.subjectUserName // .data.win.eventdata.user // ""),
          (.data.win.eventdata.commandLine // .data.win.eventdata.scriptBlockText // "")] | map(tostring) | join("\t")' eventos.jsonl > powershell.tsv
cat powershell.tsv
```

Decodificar (el argumento de `-EncodedCommand` es Base64 de texto **UTF-16LE**). La salida se guarda
en `decodificado.txt`:

```bash
python3 - <<'PY' | tee decodificado.txt
import base64, re, csv, sys
pat = re.compile(r'-(?:e|en|enc|encodedcommand)\s+["\']?([A-Za-z0-9+/=]{16,})', re.I)
for row in csv.reader(open('powershell.tsv', encoding='utf-8'), delimiter='\t'):
    ts, host, user, cmd = (row + ['']*4)[:4]
    for b64 in pat.findall(cmd):
        raw = base64.b64decode(b64 + '=' * (-len(b64) % 4))
        try:
            txt = raw.decode('utf-16-le')
        except UnicodeDecodeError:
            txt = raw.decode('utf-8', 'replace')
        print(f'{ts}\t{host}\t{user}\n  {txt}\n')
PY
```

Si el resultado contiene otra capa (`FromBase64String('...')`, `-join`, `[char]`), decodificar esa
capa también. Extraer IOCs del texto decodificado:

```bash
python3 - decodificado.txt <<'PY'
import re, sys
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
print("IPs:", sorted(set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', t))))
print("URLs:", sorted(set(re.findall(r'https?://[^\s\'")]+', t, re.I))))
print("Archivos:", sorted(set(re.findall(r'[\w\\/.:-]+\.(?:exe|dll|ps1|bat|vbs|hta|msi|zip)\b', t, re.I))))
PY
```

El usuario que ejecutó el comando está en el mismo evento: `subjectDomainName\subjectUserName`
(4688), `user` (Sysmon 1) o el contexto del 4104. Formato de respuesta habitual: `dominio\usuario`.

## 6. Al terminar

- Cada hallazgo a `02-timeline.md` (con Event ID y archivo como fuente) y cada IOC a `04-iocs.md`.
- Mapear a ATT&CK con `ih-mapeo-killchain-mitre.md` del power `incident-handling-nist` (R10).
- Proponer detecciones con `irl-sigma-detecciones.md`.
