"""HU-01: Agregar productos al carrito."""
import pytest

from mercado_sabanero.errores import CantidadInvalidaError


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
