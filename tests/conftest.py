"""Fixtures compartidas por todas las pruebas."""
from unittest.mock import Mock

import pytest

from mercado_sabanero.carrito import Carrito
from mercado_sabanero.inventario import Inventario
from mercado_sabanero.modelos import Producto


@pytest.fixture
def inventario():
    """Doble de prueba del servicio externo de inventario (100 unidades de todo)."""
    doble = Mock(spec=Inventario)
    doble.obtener_stock.return_value = 100
    return doble


@pytest.fixture
def carrito(inventario):
    return Carrito(inventario)


@pytest.fixture
def licuadora():
    return Producto("LIC-01", "Licuadora", 180_000, 19)


@pytest.fixture
def cafe():
    return Producto("CAF-01", "Café", 15_000, 5)


@pytest.fixture
def arroz():
    return Producto("ARR-01", "Arroz", 4_500, 0)
