# Fase 3: Contención, erradicación y recuperación

Se entra cuando la investigación explica el tipo de incidente y su impacto en el negocio.

## Contención

**Coordinada y simultánea en todos los sistemas (R2).** Si se contiene por partes, el atacante se
da cuenta y cambia de técnicas o activa otra persistencia.

### Corto plazo

Mínima huella en los sistemas; gana tiempo y preserva evidencia.

- Mover el sistema a una VLAN aislada.
- Desconectar el cable de red.
- Redirigir el DNS del C2 a un sistema propio (sinkhole) o a uno inexistente.
- Bloquear la IP/dominio del C2 en el perímetro.

Aprovechar para tomar imágenes forenses si no se hizo (*backup substage*). Apagar un sistema
requiere comunicarlo al negocio y tener autorización (R12).

### Largo plazo

Cambios persistentes:

- Cambiar contraseñas y revocar sesiones activas.
- Reglas de firewall.
- Instalar un HIDS.
- **Aplicar parches** (es contención de largo plazo, no de corto).
- Apagar sistemas.

Mantener informados al negocio y a los interesados. Que el sistema esté parchado no significa que
el incidente terminó.

### Checklist antes de contener

- [ ] Lista completa de sistemas, cuentas e IOCs confirmados (`03-sistemas.md`, `04-iocs.md`).
- [ ] Evidencia volátil capturada o decisión documentada de no capturarla.
- [ ] Ventana de ejecución acordada para que todas las acciones ocurran al mismo tiempo.
- [ ] Responsables por acción y canal de coordinación fuera de banda (R5).
- [ ] Autorización del negocio para apagados o aislamientos (R12).
- [ ] Plan para la reacción del atacante (otra persistencia, otra IP de C2).

## Erradicación

Eliminar la causa raíz y lo que quede del atacante:

- [ ] Remover malware y herramientas del atacante.
- [ ] Eliminar persistencia: servicios, tareas programadas, claves `Run`, GPOs, web shells, cuentas creadas por el atacante.
- [ ] Reconstruir sistemas o restaurarlos desde un backup **anterior** al compromiso (validar con el timeline).
- [ ] Cerrar el vector de entrada (parche, credencial por defecto, servicio expuesto).
- [ ] Parches adicionales no urgentes.
- [ ] Hardening adicional, en el sistema afectado y a veces en toda la red.
- [ ] Si hubo compromiso de dominio: considerar el reseteo doble de `krbtgt` y la rotación de cuentas de servicio (complemento, no del curso; validarlo con el equipo de AD).

## Recuperación

1. El negocio verifica que el sistema funciona y tiene todos sus datos.
2. Se pasa a producción.
3. **Monitoreo intensivo**, porque los sistemas comprometidos suelen ser atacados otra vez. Vigilar:
   - Logons inusuales (cuentas que nunca habían iniciado sesión ahí).
   - Procesos inusuales.
   - Cambios en claves de registro usadas por malware.
   - Conexiones a los IOCs del caso.
4. En incidentes grandes, recuperar por fases: primero quick wins, luego cambios permanentes de largo plazo. Puede tardar meses.

### Regla R8

**Si durante la recuperación aparecen IOCs, se vuelve a la fase de investigación.** Ejemplo del
Skills Assessment: un host que volvió al dominio tras la recuperación sigue conectándose a una IP
externa (visto con `netstat`). Eso indica persistencia no erradicada.

## Criterios para cerrar la fase

- [ ] Todos los sistemas restaurados y verificados por el negocio.
- [ ] Periodo de monitoreo intensivo acordado y cumplido sin IOCs.
- [ ] Cuentas de emergencia del equipo deshabilitadas y con contraseña reseteada.
- [ ] Bitácora y timeline actualizados.

Siguiente: `ih-05-post-incidente.md`.
