"""Muestra qué hay en cada capa del Data Lake (sirve como evidencia para el checkpoint).

Uso dentro de Docker:
  docker compose run --rm --no-deps spark-job /opt/spark/bin/spark-submit --master local[1] /app/spark/mostrar_resultados.py
"""
import os

from pyspark.sql import SparkSession

DATALAKE = os.getenv("DATALAKE_PATH", "datalake")
CAPAS = [
    "raw/eventos",
    "processed/eventos",
    "curated/kpis_ventana",
    "curated/alertas_temperatura_critica",
    "curated/alertas_exposicion_prolongada",
]

spark = SparkSession.builder.appName("mostrar-resultados").config("spark.sql.session.timeZone", "UTC").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
for capa in CAPAS:
    ruta = f"{DATALAKE}/{capa}"
    try:
        df = spark.read.parquet(ruta)
    except Exception:
        print(f"\n=== {capa}: sin datos todavía")
        continue
    print(f"\n=== {capa}: {df.count()} filas")
    df.orderBy(*df.columns[:1]).show(5, truncate=False)
