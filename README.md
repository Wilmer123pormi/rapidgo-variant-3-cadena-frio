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

### 4. Requisitos Previos y Ejecución

**Requisitos:**
- Docker Desktop (con Docker Compose v2)
- Python 3.11+

**Pasos generales de validación:**
1. Clonar el repositorio.
2. Validar sintaxis de Docker: `docker compose config`

**Ejecución del Pipeline (Estado Semana 2):**
1. Instalar dependencias de Python:
   pip install -r requirements.txt
2. Levantar los servicios de infraestructura (Kafka y Zookeeper):
   docker compose up -d zookeeper kafka
3. Crear el Topic en Kafka (solo la primera vez):
   docker exec -it rapidgo-variant-3-cadena-frio-kafka-1 kafka-topics --create --topic eventos-cadena-frio --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
4. Ejecutar el Productor de eventos:
   python producer/producer.py
5. Comprobar que los eventos llegan a Kafka (en una segunda terminal):
   docker exec -it rapidgo-variant-3-cadena-frio-kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic eventos-cadena-frio --from-beginning --property print.key=true

## 5. Contrato del Evento
El contrato oficial se encuentra documentado en `samples/evento_cadena_frio.json`. Los campos principales son:
- `event_id`: Identificador único del evento.
- `equipo`: Identificador del equipo ("equipo-7").
- `pedido_id`: Identificador del pedido (usado como Key en Kafka).
- `vehiculo_id`: Identificador del vehículo.
- `timestamp`: Fecha y hora.
- `temperatura_c`: Temperatura en grados Celsius.
- `humedad_pct`: Porcentaje de humedad.
- `estado`: Estado del pedido ("EN_RUTA").