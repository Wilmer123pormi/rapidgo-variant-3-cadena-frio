# Checkpoint — Semana 2: Streaming y validaciones

## 1. Objetivo

Automatizar las validaciones básicas del contrato de eventos y comprobar las reglas iniciales de negocio de la cadena de frío.

## 2. Actividades realizadas

- Se configuró GitHub Actions mediante `.github/workflows/ci.yml`.
- Se crearon pruebas automatizadas del contrato JSON en `tests/test_evento_schema.py`.
- Se añadieron pruebas auxiliares de reglas de temperatura y humedad en `tests/test_reglas_negocio.py`.
- Se comprobaron las condiciones de temperatura crítica y exposición prolongada fuera de rango.
- Se documentó la decisión técnica en `docs/decisions/ADR-002.md`.

## 3. Evidencias de validación

La ejecución de GitHub Actions finalizó correctamente con **17 pruebas aprobadas y ningún fallo**:

- 7 pruebas del contrato JSON.
- 6 pruebas de las reglas básicas de temperatura y humedad.
- 4 pruebas de exposición prolongada.

## 4. Pendientes

- Integrar las reglas con el procesamiento de eventos de Spark Structured Streaming.
- Implementar y validar los cálculos temporales de los KPI.
- Comprobar el comportamiento con datos de prueba integrados en el pipeline.
- Revisar los resultados de las validaciones automáticas durante futuros cambios.

## 5. Estado del checkpoint

Se completó una primera etapa de validación automatizada. Las pruebas actuales verifican el contrato JSON y funciones auxiliares; no representan todavía una implementación integrada del procesamiento de eventos y alertas.
