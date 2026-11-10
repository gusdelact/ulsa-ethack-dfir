# Autoevaluación (modo Estudio)

Instrucciones para el agente:

- Hacer **una pregunta a la vez** y esperar la respuesta.
- **No mostrar la respuesta ni el criterio** antes de que el alumno conteste (salvo que lo pida).
- Al corregir: decir si es correcta, parcialmente correcta o incorrecta, explicar con el criterio y
  citar la guía de steering correspondiente.
- Al mencionar una subcategoría, mostrar su texto oficial desde `core/csf-2.0-core.csv`.

Tipos: **[C]** concepto · **[A]** aplicación (situación del caso Inlanefreight).

---

## Fundamentos de GRC (`grc-01-fundamentos.md`)

1. **[C]** ¿Qué pregunta responde cada componente de GRC?
   - *Criterio:* Gobierno: hacia dónde vamos, quién decide y cómo se rinde cuentas. Riesgo: qué puede impedir los objetivos y qué se hace. Cumplimiento: si se cumplen las obligaciones y cómo se demuestra.
2. **[C]** Verdadero o falso: si una organización pasa su auditoría de cumplimiento, está segura.
   - *Respuesta:* **Falso.** El cumplimiento es un piso mínimo; el riesgo define hasta dónde subir.
3. **[C]** Diferencia entre apetito y tolerancia al riesgo, con un ejemplo.
   - *Criterio:* apetito = cuánto riesgo se está dispuesto a asumir en general ("bajo en datos de clientes"); tolerancia = desviación medible ("máx. 8 h de caída al mes").
4. **[C]** Ordena de más general a más específico: procedimiento, política, guía, estándar.
   - *Respuesta:* Política → estándar → procedimiento; la guía es recomendación no obligatoria.
5. **[C]** ¿Qué hace la segunda línea en el modelo de las tres líneas?
   - *Criterio:* define marcos, asesora, monitorea y cuestiona a la primera línea (riesgos, cumplimiento, CISO).
6. **[A]** En Inlanefreight el CISO dice ser dueño de todos los riesgos. ¿Qué le respondes?
   - *Criterio:* el dueño es quien tiene autoridad sobre el proceso o activo de negocio (p. ej., Operaciones para `customers`); seguridad asesora y monitorea (R4).

## CSF 2.0: Core (`grc-02-csf-core.md`)

7. **[C]** ¿Cuáles son las seis funciones de CSF 2.0 y cuál es nueva respecto a la 1.1?
   - *Respuesta:* Govern, Identify, Protect, Detect, Respond, Recover; **Govern** es nueva.
8. **[C]** ¿Cuántas categorías y subcategorías tiene el Core de CSF 2.0?
   - *Respuesta:* **22 categorías y 106 subcategorías.** Comprobar con `core/csf-2.0-core.csv`.
9. **[C]** Verdadero o falso: CSF 2.0 dice qué producto o tecnología instalar para cada subcategoría.
   - *Respuesta:* **Falso.** Describe resultados; los controles vienen de catálogos como CIS, ISO o SP 800-53 (R8).
10. **[C]** Un compañero cita `PR.AC-01` en su reporte de CSF 2.0. ¿Qué está mal y cómo lo corriges?
    - *Criterio:* es un ID de la v1.1; en `core/withdrawn-v1.1.csv` aparece incorporado a **PR.AA-01** y **PR.AA-05** (R1).
11. **[C]** ¿Qué son los Implementation Examples del Core?
    - *Criterio:* ejemplos de acciones para lograr una subcategoría; orientan, no son requisitos.

## Govern (`grc-03-govern.md`)

12. **[C]** ¿Qué subcategoría de Govern trata los requisitos legales, regulatorios y contractuales?
    - *Respuesta:* **GV.OC-03.**
13. **[C]** ¿Qué subcategoría pide un método estandarizado para calcular y priorizar riesgos?
    - *Respuesta:* **GV.RM-06.**
14. **[C]** ¿Cuáles son las seis categorías de Govern?
    - *Respuesta:* GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, GV.SC.
15. **[A]** Inlanefreight tiene una política de seguridad firmada en un cajón que nadie ha leído. ¿Cumple GV.PO-01?
    - *Criterio:* parcialmente o no: la subcategoría exige que la política esté *"communicated and enforced"*.
16. **[C]** ¿Qué es un riesgo positivo y dónde aparece en CSF 2.0?
    - *Criterio:* una oportunidad estratégica; **GV.RM-07**.

## Perfiles y Tiers (`grc-04-perfiles-tiers.md`)

17. **[C]** ¿Cuáles son los cinco pasos para crear y usar un perfil?
    - *Respuesta:* alcance; recolectar información; crear el perfil (actual y objetivo); analizar brechas y crear plan de acción; implementar y actualizar.
18. **[C]** Nombra los cuatro Tiers en orden.
    - *Respuesta:* Partial, Risk Informed, Repeatable, Adaptive.
19. **[C]** Verdadero o falso: toda organización debe aspirar a Tier 4.
    - *Respuesta:* **Falso.** El objetivo se elige por riesgo y recursos (R9).
20. **[A]** ¿Qué Tier de gobierno le asignas a Inlanefreight hoy y por qué?
    - *Criterio:* Tier 1: no hay apetito, política vigente demostrada ni dueños; justificar con evidencia (R6).

## Riesgo (`grc-05-riesgo.md`)

21. **[C]** Escribe las cuatro partes de un escenario de riesgo.
    - *Respuesta:* amenaza, vulnerabilidad, activo, impacto.
22. **[C]** Diferencia entre riesgo inherente y residual.
    - *Criterio:* antes vs después de los controles; el residual debe quedar dentro del apetito o aceptarse formalmente.
23. **[C]** ¿Por qué un CVSS 9.8 no es automáticamente un riesgo crítico?
    - *Criterio:* CVSS mide severidad técnica; el riesgo depende del activo, la exposición, la probabilidad real y el impacto al negocio (R3).
24. **[A]** El reporte de footprinting calificó el AXFR abierto como Crítico. ¿Por qué el registro lo deja en Alto?
    - *Criterio:* por sí solo no expone datos personales; su impacto es facilitar otros ataques (I = 2). Ver `grc-caso-inlanefreight.md`.
25. **[C]** Nombra las cuatro opciones de tratamiento y qué exige la aceptación.
    - *Criterio:* mitigar, transferir, aceptar, evitar; aceptación con justificación, dueño, firma y vencimiento (R5).
26. **[C]** Escribe las fórmulas de SLE y ALE.
    - *Respuesta:* **SLE = AV × EF**; **ALE = SLE × ARO**.
27. **[A]** Un activo vale 1,000,000 MXN, EF = 0.4, ARO = 0.25. Calcula SLE y ALE.
    - *Respuesta:* SLE = 400,000 MXN; ALE = **100,000 MXN/año**.
28. **[A]** Un control cuesta 120,000 MXN/año y baja el ALE de 100,000 a 20,000 MXN/año. ¿Se justifica económicamente?
    - *Criterio:* 100,000 − 20,000 − 120,000 = −40,000 → **no** por ALE; podría justificarse por requisito legal o por riesgo reputacional no capturado. Explicar los límites del ALE.
29. **[C]** ¿Qué subcategoría cubre la gestión de excepciones?
    - *Respuesta:* **ID.RA-07.**

## Cumplimiento (`grc-06-cumplimiento.md`)

30. **[C]** ¿Qué diferencia hay entre evaluar el diseño y la efectividad de un control?
    - *Criterio:* diseño = existe y cubriría el requisito; efectividad = funciona en la práctica, en todo el alcance y en el periodo.
31. **[A]** Inlanefreight tiene un estándar de contraseñas, pero el footprinting encontró una cuenta de prueba con contraseña trivial en la base de clientes. ¿Qué resultado tiene L4?
    - *Criterio:* diseño posiblemente OK, efectividad NOK → **no cumple** (o *cumple parcialmente* si el estándar sí existe y está aprobado).
32. **[C]** ¿Por qué se usan CIS Controls IG1 en lugar de solo CSF?
    - *Criterio:* CSF dice qué resultado lograr; CIS IG1 da salvaguardas concretas y prácticas para lograrlo.
33. **[C]** ¿Qué hace el power antes de citar un artículo de la LFPDPPP?
    - *Criterio:* verificarlo en el texto vigente del DOF; mientras tanto redacción didáctica con la marca *a validar con legal* (R10).

## Monitoreo y mejora (`grc-07-monitoreo-mejora.md`)

34. **[C]** ¿Qué es un KRI? Da un ejemplo ligado a una tolerancia.
    - *Criterio:* indicador de riesgo con umbral; p. ej., "cuentas por defecto en sistemas con datos personales = 0".
35. **[C]** ¿Qué subcategoría recoge mejoras a partir de pruebas como un pentest?
    - *Respuesta:* **ID.IM-02.**
36. **[A]** Redacta en dos líneas, para la dirección de Inlanefreight, el riesgo R-01 sin jerga técnica ni datos sensibles.
    - *Criterio:* impacto de negocio (datos de clientes expuestos, obligación de notificar), sin usuario, contraseña ni nombres de servicios innecesarios (R11).
