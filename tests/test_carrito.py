"""HU-01: Agregar productos al carrito."""
import pytest

from mercado_sabanero.errores import CantidadInvalidaError, StockInsuficienteError


# CA1 ---------------------------------------------------------------------
@pytest.mark.parametrize("cantidad", [1, 2, 25, 49, 50])
def test_agrega_producto_con_stock_suficiente_y_queda_con_esa_cantidad(
    carrito, arroz, cantidad
):
    # Arrange: el inventario (mock) devuelve 100 unidades
    # Act
    carrito.agregar(arroz, cantidad)

    # Assert
    assert carrito.cantidad_de("ARR-01") == cantidad


# CA2 ---------------------------------------------------------------------
@pytest.mark.parametrize("cantidad", [0, -1, 51, 100])
def test_rechaza_cantidades_fuera_del_rango_de_1_a_50(carrito, arroz, cantidad):
    # Act + Assert
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar(arroz, cantidad)


@pytest.mark.parametrize("cantidad", [2.5, "3", None])
def test_rechaza_cantidades_que_no_son_enteros(carrito, arroz, cantidad):
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar(arroz, cantidad)


def test_no_modifica_el_carrito_cuando_la_cantidad_es_invalida(carrito, arroz):
    # Act
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar(arroz, 51)

    # Assert
    assert carrito.esta_vacio()


def test_no_consulta_el_inventario_cuando_la_cantidad_es_invalida(
    carrito, inventario, arroz
):
    # Act
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar(arroz, 0)

    # Assert: uso del doble de prueba
    inventario.obtener_stock.assert_not_called()


# CA3 ---------------------------------------------------------------------
def test_informa_stock_insuficiente_cuando_hay_menos_unidades_que_las_pedidas(
    carrito, inventario, licuadora
):
    # Arrange: el mock simula que solo quedan 3 licuadoras
    inventario.obtener_stock.return_value = 3

    # Act + Assert
    with pytest.raises(StockInsuficienteError, match="Stock insuficiente"):
        carrito.agregar(licuadora, 5)

    # Assert: se consultó el inventario con el código correcto
    inventario.obtener_stock.assert_called_once_with("LIC-01")
    assert carrito.esta_vacio()


def test_permite_agregar_exactamente_el_stock_disponible(carrito, inventario, licuadora):
    # Arrange
    inventario.obtener_stock.return_value = 3

    # Act
    carrito.agregar(licuadora, 3)

    # Assert
    assert carrito.cantidad_de("LIC-01") == 3


# CA4 ---------------------------------------------------------------------
def test_suma_las_cantidades_si_el_producto_ya_esta_en_el_carrito(carrito, cafe):
    # Arrange
    carrito.agregar(cafe, 2)

    # Act
    carrito.agregar(cafe, 3)

    # Assert
    assert carrito.cantidad_de("CAF-01") == 5
    assert len(carrito.items()) == 1


def test_stock_insuficiente_tiene_en_cuenta_lo_que_ya_esta_en_el_carrito(
    carrito, inventario, cafe
):
    # Arrange: stock 10, ya hay 6 en el carrito
    inventario.obtener_stock.return_value = 10
    carrito.agregar(cafe, 6)

    # Act + Assert: 6 + 6 = 12 > 10
    with pytest.raises(StockInsuficienteError):
        carrito.agregar(cafe, 6)
    assert carrito.cantidad_de("CAF-01") == 6
