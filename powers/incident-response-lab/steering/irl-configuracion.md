# Configuración

## Prerrequisitos

| Componente | Para | Verificar |
|---|---|---|
| Node.js 20 o superior | `virustotal` (npx) | `node --version` |
| VPN de HTB conectada y target activo | `thehive` en el laboratorio | `curl -s -o /dev/null -w '%{http_code}\n' http://$TARGET_IP:9000` → `200` |
| API key de VirusTotal (cuenta gratuita) | `virustotal` | — |
| `jq` y Python 3 | Análisis de logs exportados | `jq --version`, `python3 --version` |
| Rust/cargo (opcional) | Compilar los binarios en lugar de descargarlos | `cargo --version` |

## 1. Instalar `mcp-server-thehive` (y `mcp-server-wazuh` si se usará)

### Opción A: binario publicado (macOS Apple Silicon)

```bash
mkdir -p ~/.local/bin
cd ~/.local/bin

curl -fL -o mcp-server-thehive \
  https://github.com/gbrigandi/mcp-server-thehive/releases/download/v0.1.1/mcp-server-thehive-macos-arm64
chmod +x mcp-server-thehive
xattr -d com.apple.quarantine mcp-server-thehive 2>/dev/null || true

# Solo si tienes un Wazuh propio:
curl -fL -o mcp-server-wazuh \
  https://github.com/gbrigandi/mcp-server-wazuh/releases/download/v0.3.0/mcp-server-wazuh-macos-arm64
chmod +x mcp-server-wazuh
xattr -d com.apple.quarantine mcp-server-wazuh 2>/dev/null || true
```

Otros sistemas: cambiar el sufijo por `macos-amd64`, `linux-amd64` o `windows-amd64.exe`. Las
releases no publican checksums; si eso importa, usar la opción B.

### Opción B: compilar desde el código (revisable)

```bash
git clone https://github.com/gbrigandi/mcp-server-thehive.git
cd mcp-server-thehive && git checkout v0.1.1 && cargo build --release
cp target/release/mcp-server-thehive ~/.local/bin/
```

### Que Kiro encuentre el binario

`mcp.json` usa `"command": "mcp-server-thehive"`, que debe estar en el PATH del proceso de Kiro.
Si Kiro no lo encuentra, editar `mcp.json` del power y poner la ruta absoluta, por ejemplo
`"/Users/<usuario>/.local/bin/mcp-server-thehive"`.

## 2. VirusTotal

No requiere instalación: `npx` descarga `@burtthecoder/mcp-virustotal@1.0.38` (versión fijada).

API key: crear cuenta en https://www.virustotal.com → menú de usuario → **API key** → copiar.
La cuenta pública permite 4 consultas por minuto y tiene límite diario.

## 3. Token de TheHive

1. Entrar a `http://<TARGET_IP>:9000` con las credenciales del laboratorio (`htb-analyst`).
2. Menú de usuario (arriba a la derecha) → **Settings** → **API Key** → **Create** / **Reveal**.
3. Copiar el token.

Si el usuario del laboratorio no tiene permiso para crear API keys, el servidor `thehive` no se
puede usar; el agente guía el trabajo en la interfaz web y usa solo VirusTotal y el análisis de
logs.

## 4. Variables de entorno

`mcp.json` no contiene secretos: usa `${VARIABLE}`. Exportarlas en la terminal:

```bash
export TARGET_IP=10.129.x.x                       # cambia en cada spawn del laboratorio
export THEHIVE_URL="http://$TARGET_IP:9000/api"   # termina en /api
export THEHIVE_API_TOKEN='<token de TheHive>'
export VIRUSTOTAL_API_KEY='<api key de VirusTotal>'

# Solo para Wazuh propio:
export WAZUH_API_HOST=... WAZUH_API_USERNAME=... WAZUH_API_PASSWORD=...
export WAZUH_INDEXER_HOST=... WAZUH_INDEXER_USERNAME=... WAZUH_INDEXER_PASSWORD=...
```

No escribir los valores en `mcp.json`, en archivos del repositorio ni en el chat (R-LAB5).

### Que Kiro vea las variables

1. Abrir Kiro **desde esa misma terminal** con el comando `kiro` (las apps abiertas desde el Dock en macOS no heredan las variables de la shell). Por ejemplo: `kiro /Users/<usuario>/Trabajo/ulsa/ethicalforensic`. Si `which kiro` no devuelve nada, instalarlo desde la paleta de comandos de Kiro: *Shell Command: Install 'kiro' command in PATH*. Cerrar antes cualquier ventana de Kiro abierta, porque una instancia ya abierta conserva su entorno.
2. En Kiro: *Settings* → buscar **Mcp Approved Env Vars** → agregar `THEHIVE_URL`, `THEHIVE_API_TOKEN`, `VIRUSTOTAL_API_KEY` (y las de Wazuh si aplica). Kiro solo expande variables aprobadas.

Cuando cambie `TARGET_IP` (nuevo spawn), actualizar `THEHIVE_URL` y reiniciar Kiro o el servidor
`thehive` desde el panel MCP.

## 5. Habilitar Wazuh (opcional)

En `mcp.json` del power, cambiar `"disabled": true` a `false` en `wazuh`. Con certificados
autofirmados de laboratorio se deja `WAZUH_VERIFY_SSL` en `false`; con un Wazuh de producción,
ponerlo en `true`.

## 6. Instalar el power

Kiro → panel **Powers** → **Add Custom Power** → **Local Directory** →
`/Users/awsgus/Trabajo/ulsa/ethicalforensic/powers/incident-response-lab`.

## 7. Verificar

Pedir al agente: *"Verifica los servidores del power incident-response-lab"*. Hace las pruebas de la
sección "Verificación" del `POWER.md` y reporta cuáles funcionan.
