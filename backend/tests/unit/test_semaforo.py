from datetime import date, timedelta

from app.utils.semaforo import calcular_estado, dias_restantes, es_critico


def test_verde():
    hoy = date.today()
    futuro = hoy + timedelta(days=10)
    assert calcular_estado(futuro) == "verde"


def test_amarillo():
    hoy = date.today()
    futuro = hoy + timedelta(days=5)
    assert calcular_estado(futuro) == "amarillo"


def test_rojo():
    hoy = date.today()
    futuro = hoy + timedelta(days=1)
    assert calcular_estado(futuro) == "rojo"


def test_vencido():
    hoy = date.today()
    pasado = hoy - timedelta(days=1)
    assert calcular_estado(pasado) == "vencido"


def test_none():
    assert calcular_estado(None) == "verde"


def test_es_critico():
    assert es_critico("amarillo") is True
    assert es_critico("rojo") is True
    assert es_critico("verde") is False
    assert es_critico("vencido") is False


def test_dias_restantes():
    hoy = date.today()
    futuro = hoy + timedelta(days=5)
    assert dias_restantes(futuro) == 5
    assert dias_restantes(None) is None
