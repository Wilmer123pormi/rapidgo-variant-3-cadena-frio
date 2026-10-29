def esta_fuera_de_rango(temperatura_c, humedad_pct):
    return not (
        2 <= temperatura_c <= 8
        and 35 <= humedad_pct <= 65
    )


def es_temperatura_critica(temperatura_c):
    return temperatura_c >= 10 or temperatura_c <= 0


def test_evento_dentro_de_rango():
    assert not esta_fuera_de_rango(4.2, 50.0)


def test_temperatura_superior_al_rango():
    assert esta_fuera_de_rango(9.0, 50.0)


def test_humedad_inferior_al_rango():
    assert esta_fuera_de_rango(4.2, 30.0)


def test_temperatura_critica_por_calor():
    assert es_temperatura_critica(10.0)


def test_temperatura_critica_por_frio():
    assert es_temperatura_critica(0.0)


def test_temperatura_no_critica():
    assert not es_temperatura_critica(4.2)
