"""HU-03: Descuento por volumen."""
import pytest

from mercado_sabanero.descuentos import porcentaje_descuento_volumen


# CA1, CA2 y CA3 con valores límite ----------------------------------------
@pytest.mark.parametrize(
    "subtotal, porcentaje_esperado",
    [
        (0, 0),
        (199_999, 0),      # CA1: justo debajo del primer umbral
        (200_000, 5),      # CA2: límite inferior
        (499_999, 5),      # CA2: límite superior
    ],
)
def test_aplica_el_porcentaje_de_descuento_segun_el_subtotal(
    subtotal, porcentaje_esperado
):
    # Act
    porcentaje = porcentaje_descuento_volumen(subtotal)

    # Assert
    assert porcentaje == porcentaje_esperado
