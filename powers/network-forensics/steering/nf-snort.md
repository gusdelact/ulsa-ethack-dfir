# Network Forensics: detección por firmas con Snort

> Guía de steering del power **network-forensics**, derivada de *Signature-based Detection* (HTB, sección 5). Detalle en `references/deteccion-firmas.md`.
>
> **Encuadre:** pcaps de redes propias o autorizadas. Las firmas detectan lo conocido; la ausencia de alertas no prueba que no haya ataque.

## Flujo

```
1. Verificar      → snort -V; reglas actualizadas; hash del pcap
2. Ejecutar       → snort -r sobre una copia, salida en evidencia/<caso>/ids/
3. Agrupar        → por firma, clase y prioridad
4. Validar        → cada alerta relevante se confirma en el pcap con Wireshark
5. Registrar      → alerta, SID, origen, destino, hora, confirmación
```

## Ejecutar

```bash
mkdir -p /mnt/evidencia/caso01/ids
sha256sum -c /mnt/evidencia/caso01/pcap.sha256
snort -q -r captura.pcap -c /etc/snort/snort.conf -l /mnt/evidencia/caso01/ids -A fast -k none
ls /mnt/evidencia/caso01/ids
```

Si usas la configuración del sistema sin `-l`, las alertas quedan en `/var/log/snort/` (`alert.fast` o `snort.alert.fast`, según la salida configurada).

## Agrupar

```bash
A=/mnt/evidencia/caso01/ids/alert
grep -oP '\] \K[^\[]+(?= \[\*\*\])' "$A" | sort | uniq -c | sort -rn        # por firma
grep -oP 'Classification: \K[^\]]+' "$A" | sort | uniq -c | sort -rn        # por clase
grep "Priority: 1" "$A"                                                     # prioridad alta
```

## Validar

Para cada alerta: toma IPs, puertos y hora; filtra en Wireshark (`ip.addr==<origen> && tcp.port==<puerto>`), ve el paquete y el stream. Clasifica como **confirmada**, **falso positivo** o **sin determinar**.

## Leer la alerta

`[GID:SID:REV] descripción [Classification: ...] [Priority: N] {PROTO} origen:puerto -> destino:puerto`

El SID permite buscar la regla exacta (`grep "sid:<SID>;" /etc/snort/rules/*.rules`) para entender qué disparó la alerta.

## Alternativas

- **Suricata:** `suricata -r captura.pcap -l /mnt/evidencia/caso01/ids/` genera `fast.log` y `eve.json` (que incluye flujos para `nf-netflow.md`).
- **Zeek:** `zeek -r captura.pcap` genera logs por protocolo (`conn.log`, `dns.log`, `http.log`) útiles para el análisis.

## Preguntas de control

- ¿Las reglas estaban actualizadas? ¿Anotaste la versión?
- ¿Validaste en el pcap cada alerta que reportas?
- ¿Documentaste los falsos positivos y por qué lo son?
