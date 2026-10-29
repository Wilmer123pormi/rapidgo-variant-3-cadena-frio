
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "docs" / "schemas" / "evento_cadena_frio.schema.json"

with SCHEMA_PATH.open(encoding="utf-8") as file:
    SCHEMA = json.load(file)

VALIDATOR = Draft202012Validator(
    SCHEMA,
    format_checker=FormatChecker(),
)


def evento_valido():
    return {
        "evento_id": "evt-0001",
        "pedido_id": "PED-001",
        "vehiculo_id": "VEH-001",
        "producto_tipo": "producto_refrigerado",
        "timestamp": "2026-10-21T10:30:00Z",
        "temperatura_c": 4.2,
        "humedad_pct": 50.0,
    }


def test_evento_valido_cumple_contrato():
    VALIDATOR.validate(evento_valido())


def test_falta_campo_obligatorio():
    evento = evento_valido()
    del evento["pedido_id"]

    with pytest.raises(ValidationError):
        VALIDATOR.validate(evento)


def test_pedido_id_con_formato_incorrecto():
    evento = evento_valido()
    evento["pedido_id"] = "PED-ABC"

    with pytest.raises(ValidationError):
        VALIDATOR.validate(evento)


def test_temperatura_fuera_del_limite_fisico():
    evento = evento_valido()
    evento["temperatura_c"] = 61

    with pytest.raises(ValidationError):
        VALIDATOR.validate(evento)


def test_humedad_fuera_del_limite_fisico():
    evento = evento_valido()
    evento["humedad_pct"] = 101

    with pytest.raises(ValidationError):
        VALIDATOR.validate(evento)


def test_rechaza_campos_no_definidos():
    evento = evento_valido()
    evento["campo_extra"] = "no permitido"

    with pytest.raises(ValidationError):
        VALIDATOR.validate(evento)


def test_timestamp_con_formato_invalido():
    evento = evento_valido()
    evento["timestamp"] = "fecha-invalida"

    with pytest.raises(ValidationError):
        VALIDATOR.validate(evento)
