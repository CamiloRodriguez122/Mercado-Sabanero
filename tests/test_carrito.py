"""HU-01: Agregar productos al carrito."""
import pytest


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
