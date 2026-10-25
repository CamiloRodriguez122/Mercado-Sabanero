"""Pruebas de la liquidación completa (integra HU-02 a HU-06)."""
from datetime import date

import pytest

from mercado_sabanero.errores import CarritoVacioError, CuponInvalidoError
from mercado_sabanero.liquidacion import liquidar
from mercado_sabanero.modelos import CategoriaCliente, Producto

HOY = date(2026, 10, 23)


def test_ejemplo_del_enunciado_cliente_estandar_en_sincelejo_sin_cupon(
    carrito, licuadora, cafe, arroz
):
    # Arrange: 1 licuadora, 2 cafés y 4 arroces
    carrito.agregar(licuadora, 1)
    carrito.agregar(cafe, 2)
    carrito.agregar(arroz, 4)

    # Act
    liq = liquidar(carrito, "Sincelejo", CategoriaCliente.ESTANDAR, hoy=HOY)

    # Assert
    assert liq.subtotal == 228_000
    assert liq.descuento == 11_400
    assert liq.iva == 33_915
    assert liq.envio == 0
    assert liq.total == 250_515
    assert liq.puntos == 250


def test_el_iva_por_producto_usa_el_valor_con_descuento(
    carrito, licuadora, cafe, arroz
):
    # Arrange
    carrito.agregar(licuadora, 1)
    carrito.agregar(cafe, 2)
    carrito.agregar(arroz, 4)

    # Act
    liq = liquidar(carrito, "Sincelejo", hoy=HOY)

    # Assert
    iva_por_codigo = {linea.codigo: linea.iva for linea in liq.lineas}
    assert iva_por_codigo == {"LIC-01": 32_490, "CAF-01": 1_425, "ARR-01": 0}


def test_total_es_subtotal_menos_descuento_mas_iva_mas_envio(carrito):
    # Arrange: 1 producto de $100.000 con IVA 19 %, envío a Sincelejo
    carrito.agregar(Producto("VEN-01", "Ventilador", 100_000, 19), 1)

    # Act
    liq = liquidar(carrito, "Sincelejo", hoy=HOY)

    # Assert: 100.000 - 0 + 19.000 + 8.000
    assert (liq.subtotal, liq.descuento, liq.iva, liq.envio) == (
        100_000, 0, 19_000, 8_000,
    )
    assert liq.total == 127_000


def test_cupon_sabanero10_aplica_10_por_ciento_cuando_no_hay_descuento_por_volumen(
    carrito, arroz
):
    # Arrange: subtotal 90.000 (< 200.000, sin descuento por volumen)
    carrito.agregar(arroz, 20)

    # Act
    liq = liquidar(carrito, "Sincelejo", codigo_cupon="SABANERO10", hoy=HOY)

    # Assert
    assert liq.porcentaje_descuento == 10
    assert liq.descuento == 9_000


def test_con_descuento_por_volumen_mayor_el_cupon_sabanero10_no_se_suma(carrito):
    # Arrange: subtotal 500.000 -> volumen 10 %; el cupón también es 10 %
    carrito.agregar(Producto("TV-02", "Televisor", 500_000, 19), 1)

    # Act
    liq = liquidar(carrito, "Sincelejo", codigo_cupon="SABANERO10", hoy=HOY)

    # Assert: 10 % (50.000), no 20 %
    assert liq.porcentaje_descuento == 10
    assert liq.descuento == 50_000


def test_con_descuento_por_volumen_menor_se_aplica_el_cupon_porque_es_el_mayor(carrito):
    # Arrange: subtotal 300.000 -> volumen 5 %; el cupón da 10 %
    carrito.agregar(Producto("NEV-01", "Nevera pequeña", 300_000, 19), 1)

    # Act
    liq = liquidar(carrito, "Sincelejo", codigo_cupon="SABANERO10", hoy=HOY)

    # Assert
    assert liq.porcentaje_descuento == 10
    assert liq.descuento == 30_000


def test_cupon_enviogratis_deja_el_envio_en_cero_en_la_liquidacion(carrito, arroz):
    # Arrange: compra pequeña a otro municipio (costaría $15.000)
    carrito.agregar(arroz, 2)

    # Act
    liq = liquidar(carrito, "Corozal", codigo_cupon="ENVIOGRATIS", hoy=HOY)

    # Assert
    assert liq.envio == 0
    assert liq.total == 9_000


def test_los_puntos_se_calculan_sin_incluir_el_envio(carrito):
    # Arrange: total 127.000 = 119.000 de compra + 8.000 de envío
    carrito.agregar(Producto("VEN-01", "Ventilador", 100_000, 19), 1)

    # Act
    liq = liquidar(carrito, "Sincelejo", hoy=HOY)

    # Assert: 119.000 / 1.000 = 119 puntos
    assert liq.total == 127_000
    assert liq.puntos == 119


def test_cliente_oro_recibe_el_doble_de_puntos_en_la_liquidacion(carrito, arroz):
    # Arrange
    carrito.agregar(arroz, 10)  # 45.000 + 8.000 de envío

    # Act
    liq = liquidar(carrito, "Sincelejo", CategoriaCliente.ORO, hoy=HOY)

    # Assert: 45.000 / 1.000 = 45 -> x2
    assert liq.puntos == 90


def test_rechaza_liquidar_un_carrito_vacio(carrito):
    with pytest.raises(CarritoVacioError):
        liquidar(carrito, "Sincelejo", hoy=HOY)


def test_rechaza_liquidar_con_un_cupon_inexistente(carrito, arroz):
    # Arrange
    carrito.agregar(arroz, 1)

    # Act + Assert
    with pytest.raises(CuponInvalidoError):
        liquidar(carrito, "Sincelejo", codigo_cupon="FALSO", hoy=HOY)


def test_rechaza_liquidar_con_un_cupon_vencido(carrito, arroz):
    # Arrange
    carrito.agregar(arroz, 20)

    # Act + Assert
    with pytest.raises(CuponInvalidoError, match="vencido"):
        liquidar(carrito, "Sincelejo", codigo_cupon="SABANERO10", hoy=date(2027, 1, 2))
