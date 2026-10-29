"""Pruebas de las transformaciones y alertas (no requieren Kafka)."""
import json
import os
import sys
from datetime import datetime, timedelta

import pytest
from pyspark.sql import SparkSession

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "spark"))
import transformaciones as t  # noqa: E402


@pytest.fixture(scope="module")
def spark():
    s = (
        SparkSession.builder.master("local[1]").appName("tests-cadena-frio")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    yield s
    s.stop()


def _evento(i, pedido, minuto, temp, hum=50.0):
    base = datetime(2026, 10, 21, 10, 0, 0)
    return {
        "evento_id": f"evt-{pedido}-{i}", "pedido_id": pedido, "vehiculo_id": "VEH-001",
        "producto_tipo": "producto_refrigerado",
        "timestamp": (base + timedelta(minutes=minuto)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "temperatura_c": temp, "humedad_pct": hum,
    }


def _kafka_df(spark, eventos):
    """Simula la salida de la fuente Kafka (value en JSON + partition/offset)."""
    filas = [(0, i, json.dumps(e) if isinstance(e, dict) else e) for i, e in enumerate(eventos)]
    return spark.createDataFrame(filas, "partition int, offset long, value string")


def test_descarta_eventos_invalidos(spark):
    df = _kafka_df(spark, [
        _evento(1, "PED-001", 0, 5.0),
        "esto no es json",
        _evento(2, "PED-001", 1, 500.0),            # temperatura imposible
    ])
    assert t.procesar_eventos(df).count() == 1


def test_marcas_de_rango_y_temperatura_critica(spark):
    df = _kafka_df(spark, [
        _evento(1, "PED-001", 0, 5.0, 50.0),        # normal
        _evento(2, "PED-001", 1, 11.8, 50.0),       # crítica por calor
        _evento(3, "PED-001", 2, 0.0, 50.0),        # crítica por frío (<= 0)
        _evento(4, "PED-001", 3, 1.0, 50.0),        # fuera de rango, no crítica
        _evento(5, "PED-001", 4, 5.0, 70.0),        # humedad fuera de rango
    ])
    filas = {r["evento_id"]: r for r in t.procesar_eventos(df).collect()}
    assert not filas["evt-PED-001-1"]["fuera_de_rango"]
    assert filas["evt-PED-001-2"]["alerta_temperatura_critica"]
    assert filas["evt-PED-001-3"]["alerta_temperatura_critica"]
    assert filas["evt-PED-001-4"]["fuera_de_rango"] and not filas["evt-PED-001-4"]["alerta_temperatura_critica"]
    assert filas["evt-PED-001-5"]["hum_fuera_rango"] and not filas["evt-PED-001-5"]["alerta_temperatura_critica"]
    assert t.alertas_temperatura_critica(t.procesar_eventos(df)).count() == 2


def test_kpis_por_ventana(spark):
    temps = [4.0, 5.0, 6.0, 9.0]  # el último está fuera de rango
    df = _kafka_df(spark, [_evento(i, "PED-001", i, v) for i, v in enumerate(temps)])
    fila = t.kpis_por_ventana(t.procesar_eventos(df)).collect()[0]
    assert fila["eventos"] == 4 and fila["eventos_fuera_rango"] == 1
    assert fila["temp_media_c"] == 6.0
    assert fila["pct_dentro_rango"] == 75.0
    assert fila["minutos_fuera_rango_estimado"] == 1.0


def test_alerta_exposicion_prolongada(spark):
    larga = [_evento(i, "PED-LARGA", i, 9.5) for i in range(13)]      # 13 min fuera de rango
    corta = [_evento(i, "PED-CORTA", i, 9.5) for i in range(5)]       # solo 5 min
    normal = [_evento(i, "PED-OK", i, 5.0) for i in range(13)]
    df = t.procesar_eventos(_kafka_df(spark, larga + corta + normal))
    pedidos = {r["pedido_id"] for r in t.alertas_exposicion_prolongada(df).collect()}
    assert pedidos == {"PED-LARGA"}


def test_timestamp_con_microsegundos_y_offset(spark):
    """El productor usa datetime.isoformat(): 2026-10-21T10:30:00.123456+00:00."""
    e = _evento(1, "PED-001", 0, 5.0)
    e["timestamp"] = "2026-10-21T10:30:00.123456+00:00"
    filas = t.procesar_eventos(_kafka_df(spark, [e])).collect()
    assert len(filas) == 1
    assert filas[0]["timestamp"].year == 2026
