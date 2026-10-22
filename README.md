# RapidGo - Pipeline Big Data (Variante 3: Cadena de Frío)

**Integrantes:**
- [Wilmer Leon]
- [Nicolas Martinez]
- [Yair Mora]

## 1. Objetivo del Proyecto
RapidGo es una plataforma de entregas que requiere monitorear productos sensibles. Este proyecto construye un pipeline Big Data End-to-End para capturar eventos de temperatura y humedad durante el reparto, procesarlos en tiempo real y generar alertas si la cadena de frío se rompe.

## 2. Arquitectura Inicial
El flujo de datos planificado para las próximas semanas es el siguiente:
`Productor de Eventos (Python) -> Apache Kafka -> Spark Structured Streaming -> Data Lake (Parquet) -> Apache Airflow (Orquestación)`

## 3. Organización del Repositorio
- `airflow/`: DAGs para orquestación (Semana 3).
- `producer/`: Código del generador de eventos (Semana 2).
- `spark/`: Scripts de procesamiento en streaming (Semana 2).
- `tests/`: Pruebas automatizadas.
- `samples/`: Ejemplos de contratos JSON.
- `datalake/`: Almacenamiento local (Raw, Processed, Curated).
- `docs/`: Documentación, ADRs y checkpoints semanales.

## 4. Requisitos Previos y Ejecución (Estado Semana 1)
**Requisitos:**
- Docker Desktop (con Docker Compose v2)
- Python 3.11+

**Pasos previstos:**
1. Clonar el repositorio.
2. Validar sintaxis de Docker: `docker compose config`
3. (A partir de Semana 2) Levantar servicios: `docker compose up -d`
