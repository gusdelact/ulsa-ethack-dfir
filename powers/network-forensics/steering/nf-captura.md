# Network Forensics: captura y preservación

> Guía de steering del power **network-forensics**, derivada de *Capturing Network Traffic* (HTB, sección 3). Detalle en `references/captura.md`.
>
> **Encuadre:** captura solo en redes propias o autorizadas. Una captura puede contener credenciales y datos personales: es evidencia sensible.

## Decisiones antes de capturar

| Decisión | Opciones | Criterio |
|---|---|---|
| Punto de captura | Host, SPAN del switch, TAP, Traffic Mirroring (AWS) | ¿Necesitas un host o un segmento entero? |
| Filtro de captura | Ninguno, por host, por puerto, por protocolo | Filtrar ahorra espacio, pero lo no capturado se pierde. En un incidente, captura amplio y filtra al analizar. |
| Duración y tamaño | Rotación por tamaño o tiempo | Archivos manejables para analizar y transportar. |
| Destino | Disco del equipo de captura, nunca el host sospechoso | Integridad. |

## Captura con tcpdump

```bash
mkdir -p /mnt/evidencia/caso01/pcap
sudo tcpdump -i eth0 -n -s 0 -C 100 -W 50 -w /mnt/evidencia/caso01/pcap/cap.pcap
```

- `-s 0` captura el paquete completo (es el valor por defecto en versiones modernas, pero explicítalo).
- `-C 100 -W 50` rota en 50 archivos de 100 MB.
- Para una captura acotada: `sudo tcpdump -i eth0 -n host 10.0.0.5 -w /mnt/evidencia/caso01/pcap/host5.pcap`.

## Captura con Wireshark

1. Selecciona la interfaz.
2. En **Capture → Options** define el filtro de captura (BPF) y la división en varios archivos (por paquetes, tamaño o tiempo).
3. Inicia, detén con **Stop** y guarda en `.pcapng`.

## En AWS

- **Traffic Mirroring:** sesión de mirroring desde la ENI de la instancia sospechosa hacia una instancia de análisis (destino ENI o NLB). Requiere instancias basadas en Nitro.
- **VPC Flow Logs:** actívalos en la VPC, subred o ENI si no lo estaban; solo registran desde ese momento.

## Preservación

```bash
cd /mnt/evidencia/caso01/pcap
sha256sum cap.pcap* > ../pcap.sha256
capinfos cap.pcap0* > ../pcap_capinfos.txt
```

Registro en la bitácora:

| Campo | Ejemplo |
|---|---|
| Host de captura | sensor01 |
| Interfaz | eth0 (SPAN del switch core) |
| Filtro de captura | ninguno |
| Inicio / fin (UTC) | 2026-11-05 10:00:00 / 12:00:00 |
| Archivos | cap.pcap00 … cap.pcap12 |
| SHA-256 | ver `pcap.sha256` |

Antes de cada análisis, verifica el hash (`sha256sum -c ../pcap.sha256`) y trabaja sobre una copia.

## Preguntas de control

- ¿El destino de la captura está fuera del host sospechoso?
- ¿Documentaste interfaz, filtro y horario?
- ¿Cada archivo tiene hash?
