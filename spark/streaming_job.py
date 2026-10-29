"""Kafka -> Spark Structured Streaming -> Data Lake (Parquet).

Capas del Data Lake (DATALAKE_PATH):
  raw/eventos                          mensajes tal como llegan de Kafka
  processed/eventos                    eventos validados y con marcas de rango
  curated/kpis_ventana                 KPIs por pedido y ventana de 5 min
  curated/alertas_temperatura_critica  alerta 1
  curated/alertas_exposicion_prolongada alerta 2
Checkpoints en DATALAKE_PATH/checkpoints/<capa>.

Variables de entorno (todas opcionales):
  KAFKA_BOOTSTRAP_SERVERS (kafka:9092)  KAFKA_TOPIC (eventos-cadena-frio)
  DATALAKE_PATH (datalake)              STARTING_OFFSETS (earliest)
  TRIGGER_SEGUNDOS (10; 0 = procesar lo disponible y terminar)
  WATERMARK (2 minutes)
  EXPOSICION_MINUTOS (10)  MUESTREO_SEGUNDOS (60)   # ver transformaciones.py
"""
import os

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from transformaciones import (
    alertas_exposicion_prolongada,
    alertas_temperatura_critica,
    kpis_por_ventana,
    procesar_eventos,
)


def crear_spark() -> SparkSession:
    return (
        SparkSession.builder.appName("rapidgo-cadena-frio")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def leer_kafka(spark: SparkSession, servidores: str, topic: str, offsets: str) -> DataFrame:
    return (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", servidores)
        .option("subscribe", topic)
        .option("startingOffsets", offsets)
        .option("failOnDataLoss", "false")
        .load()
    )


def _escribir(df: DataFrame, datalake: str, capa: str, trigger_seg: int, particion=None):
    escritor = (
        df.writeStream.format("parquet")
        .outputMode("append")
        .option("path", f"{datalake}/{capa}")
        .option("checkpointLocation", f"{datalake}/checkpoints/{capa}")
    )
    if particion:
        escritor = escritor.partitionBy(particion)
    if trigger_seg > 0:
        escritor = escritor.trigger(processingTime=f"{trigger_seg} seconds")
    else:
        escritor = escritor.trigger(availableNow=True)
    return escritor.start()


def iniciar_pipeline(df_kafka: DataFrame, datalake: str, trigger_seg: int = 10,
                     watermark: str = "2 minutes") -> list:
    """Arranca las 5 consultas de streaming a partir de un DataFrame con el
    formato de la fuente Kafka (key, value, topic, partition, offset, timestamp)."""
    raw = df_kafka.select(
        F.col("key").cast("string").alias("key"),
        F.col("value").cast("string").alias("value"),
        "topic", "partition", "offset",
        F.col("timestamp").alias("kafka_timestamp"),
    )
    procesados = procesar_eventos(df_kafka)

    return [
        _escribir(raw, datalake, "raw/eventos", trigger_seg),
        _escribir(procesados, datalake, "processed/eventos", trigger_seg, "fecha"),
        _escribir(kpis_por_ventana(procesados, watermark=watermark),
                  datalake, "curated/kpis_ventana", trigger_seg),
        _escribir(alertas_temperatura_critica(procesados),
                  datalake, "curated/alertas_temperatura_critica", trigger_seg, "fecha"),
        _escribir(alertas_exposicion_prolongada(procesados, watermark=watermark),
                  datalake, "curated/alertas_exposicion_prolongada", trigger_seg, "fecha"),
    ]


def main():
    spark = crear_spark()
    spark.sparkContext.setLogLevel("WARN")
    df_kafka = leer_kafka(
        spark,
        os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        os.getenv("KAFKA_TOPIC", "eventos-cadena-frio"),
        os.getenv("STARTING_OFFSETS", "earliest"),
    )
    iniciar_pipeline(
        df_kafka,
        os.getenv("DATALAKE_PATH", "datalake"),
        int(os.getenv("TRIGGER_SEGUNDOS", "10")),
        os.getenv("WATERMARK", "2 minutes"),
    )
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
