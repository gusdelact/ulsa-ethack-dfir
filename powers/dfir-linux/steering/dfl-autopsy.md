# DFIR en Linux: análisis de una imagen con Autopsy

> Guía de steering del power **dfir-linux**, derivada de *Linux Evidence Acquisition with Autopsy* (HTB, continuación, sección 7). Detalle en `references/autopsy-linux.md`.
>
> **Encuadre:** solo imágenes de sistemas propios o autorizados.

## Flujo

```
1. Imagen con hash          → dd/dc3dd + sha256sum (dfl-imagen-hash.md)
2. Iniciar Autopsy          → autopsy; abrir http://localhost:9999/autopsy
3. New Case                 → nombre, analista, número de caso, directorio
4. Host                     → datos del host analizado
5. Add Image                → ruta, tipo (disco o partición), importación, sistema de volúmenes
6. Verificar hash           → comparar con el registrado; si no coincide, detenerse
7. ANALYZE                  → menús de análisis
8. Reporte y cierre         → exportar y cerrar el caso
```

## Paso 7: orden de análisis sugerido

1. **File Analysis** en las rutas que señalan otras fuentes: `/etc` (cuentas, cron, sudoers), `/home/*` (historial, `.ssh`, `.bashrc`), `/var/log`, `/var/www`, `/tmp`.
2. **Archivos borrados:** en File Analysis aparecen marcados; extrae los relevantes.
3. **Keyword Search** con los IOCs que ya tienes: IPs, dominios, nombres de usuario, nombres de herramientas (`nc`, `mimikatz`, `linpeas`), cadenas de webshell (`eval(`, `base64_decode`, `system(`).
4. **File Type** (**Sort Files by Type**): ejecutables fuera de rutas estándar y archivos con extensión que no coincide con su tipo.
5. **Meta Data** de cada archivo relevante: timestamps, dueño, permisos, inodo.
6. **Data Unit** cuando necesites ver bytes crudos (archivos borrados, datos ocultos).
7. **Línea de tiempo** de la ventana del incidente.

## Registro

Por cada hallazgo, anota en `hallazgos.md`: ruta, inodo, timestamps MACB, hash del archivo extraído, menú de Autopsy usado y por qué es relevante.

## Preguntas de control

- ¿Verificaste el hash de la imagen dentro de Autopsy?
- ¿Las palabras clave salieron de evidencia previa y no de suposiciones?
- ¿Los archivos extraídos tienen hash y están fuera de la imagen?
- ¿El reporte de Autopsy está como anexo del reporte forense?
