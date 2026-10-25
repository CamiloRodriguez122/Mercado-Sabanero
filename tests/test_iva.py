"""HU-02: Calcular el IVA."""
import pytest

from mercado_sabanero.iva import calcular_iva


# CA1 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    "tarifa, iva_esperado", [(0, 0), (5, 5_000), (19, 19_000)]
)
def test_el_iva_corresponde_a_la_tarifa_del_producto(tarifa, iva_esperado):
    # Arrange
    valor = 100_000

    # Act
    iva = calcular_iva(valor, tarifa)

    # Assert
    assert iva == iva_esperado
