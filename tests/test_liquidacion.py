"""Pruebas de la liquidación completa (integra HU-02 a HU-06)."""
from datetime import date

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
