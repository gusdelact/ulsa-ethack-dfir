# =============================================================================
# Makefile — punto de entrada único de la Validacion_Local (tarea 15.4)
# -----------------------------------------------------------------------------
# La compuerta de calidad del proyecto corre ENTERAMENTE en local: no depende de
# GitHub Actions ni de ningún servicio de integración continua remoto
# (Req 20.6, 20.11). El alumno ejecuta `make validate` antes de abrir su
# Pull_Request y el Líder Técnico lo ejecuta antes de integrar (Req 20.8, 20.9).
#
# Objetivos:
#   make validate   Validacion_Local completa: encadena adaptador de formatos,
#                   Artefactos_Documentacion (docStatus), guardia de la
#                   Allowlist_Objetivos, regeneración del inventario y
#                   cobertura + conteo por alumno. Exit 0 si la baseline es
#                   válida (con los 2 huecos esperados como pendientes).
#   make catalog    Regenera engagements/dvwa-lab-ulsa/inventory.json con el
#                   Catalogador (NO se edita a mano).
#   make coverage   Verifica cobertura de fases/etapas y responsables (consume
#                   el Catalogador).
# =============================================================================

PYTHON ?= python3

.PHONY: validate catalog coverage help

validate:
	$(PYTHON) agent_ethack_dfir/scripts/validate_all.py

catalog:
	$(PYTHON) agent_ethack_dfir/scripts/catalog.py

coverage:
	$(PYTHON) agent_ethack_dfir/scripts/check_coverage.py

help:
	@echo "Objetivos disponibles (todo corre en local, sin CI remota):"
	@echo "  make validate   Validacion_Local completa (único punto de entrada)"
	@echo "  make catalog     Regenera inventory.json con el Catalogador"
	@echo "  make coverage    Verifica cobertura de fases/etapas y responsables"
