# Spark Structured Streaming - Cadena de frío

Consume el tópico `eventos-cadena-frio` desde Kafka, procesa los eventos y los guarda en el Data Lake en formato Parquet.

## Ejecutar (Docker)
1. Levantar Kafka y crear el tópico (solo la primera vez), como indica el README principal:
   ```bash
   docker compose up -d zookeeper kafka
   docker exec -it rapidgo-variant-3-cadena-frio-kafka-1 kafka-topics --create --topic eventos-cadena-frio --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
   ```
2. En una terminal, arrancar el job de Spark (la primera vez descarga el conector de Kafka, necesita internet):
   ```bash
   docker compose up spark-job
   ```
3. En otra terminal, arrancar el productor:
   ```bash
   python producer/producer.py
   ```
4. Ver los resultados (Parquet en `datalake/`):
   ```bash
   docker compose run --rm --no-deps spark-job /opt/spark/bin/spark-submit --master local[1] /app/spark/mostrar_resultados.py
   ```
5. Recuperación: con `Ctrl+C` se detiene el job; al volver a ejecutar `docker compose up spark-job` continúa desde el checkpoint, sin reprocesar lo ya guardado.

## Variables de entorno (se definen en `docker-compose.yml`)
| Variable | Defecto | Uso |
|---|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:9092` | Broker de Kafka (en Docker: `kafka:29092`) |
| `KAFKA_TOPIC` | `eventos-cadena-frio` | Tópico a consumir |
| `DATALAKE_PATH` | `datalake` | Raíz del Data Lake |
| `STARTING_OFFSETS` | `earliest` | Desde dónde leer la primera vez |
| `TRIGGER_SEGUNDOS` | `10` | Cada cuánto procesa (0 = procesa lo disponible y termina) |
| `WATERMARK` | `2 minutes` | Tolerancia a eventos tardíos |
| `EXPOSICION_MINUTOS` | `10` | Minutos fuera de rango para la alerta de exposición prolongada |
| `MUESTREO_SEGUNDOS` | `60` | Segundos entre eventos de un mismo pedido (para estimar minutos fuera de rango) |

## Qué escribe (Parquet)
| Ruta en `datalake/` | Contenido |
|---|---|
| `raw/eventos` | Mensajes tal como llegan de Kafka (key, value, partition, offset) |
| `processed/eventos` | Eventos validados con marcas de fuera de rango y temperatura crítica |
| `curated/kpis_ventana` | KPIs por pedido y ventana de 5 min (tiempo fuera de rango, % dentro de rango, temperatura media) |
| `curated/alertas_temperatura_critica` | Alerta 1 |
| `curated/alertas_exposicion_prolongada` | Alerta 2 |
| `checkpoints/<capa>` | Checkpoints de Spark (recuperación del streaming) |

## Transformaciones
1. `validar_eventos`: castea el timestamp y descarta eventos incompletos o con valores imposibles.
2. `marcar_fuera_de_rango`: marca temperatura y humedad fuera del rango permitido.
3. `marcar_temperatura_critica`: marca temperatura crítica y agrega la columna `fecha` (partición).
4. Agregación por ventana: `kpis_por_ventana` (ventana de 5 minutos por pedido).

## Limitaciones conocidas
- Los resultados por ventana aparecen cuando el *watermark* cierra la ventana: hacen falta eventos posteriores para ver la última.
- La alerta de exposición prolongada se calcula con una ventana deslizante de (`EXPOSICION_MINUTOS` + 1) minutos y paso de 1 minuto: dispara si todos los eventos del pedido en la ventana están fuera de rango y abarcan `EXPOSICION_MINUTOS` o más. Mientras la exposición continúa puede repetirse en cada ventana.
- Los umbrales viven en `spark/transformaciones.py` y son provisionales (ver `docs/kpi_alertas.md`).

## Pruebas
```bash
pytest -v
```
Las pruebas de `tests/test_spark_transformaciones.py` no necesitan Kafka (requieren Java instalado).
