"""Validaciones del modelo Producto (soporte de HU-02 CA1: tarifas 0, 5 y 19)."""
import pytest

from mercado_sabanero.errores import DatoInvalidoError
from mercado_sabanero.modelos import Producto


@pytest.mark.parametrize("tarifa", [0, 5, 19])
def test_acepta_las_tarifas_de_iva_permitidas(tarifa):
    # Act
    producto = Producto("X-01", "Producto", 1_000, tarifa)

    # Assert
    assert producto.tarifa_iva == tarifa


@pytest.mark.parametrize("tarifa", [1, 10, 16, -5, 100])
def test_rechaza_tarifas_de_iva_no_permitidas(tarifa):
    with pytest.raises(DatoInvalidoError):
        Producto("X-01", "Producto", 1_000, tarifa)


@pytest.mark.parametrize("precio", [0, -1_000, 99.5])
def test_rechaza_precios_que_no_son_enteros_positivos(precio):
    with pytest.raises(DatoInvalidoError):
        Producto("X-01", "Producto", precio, 19)
