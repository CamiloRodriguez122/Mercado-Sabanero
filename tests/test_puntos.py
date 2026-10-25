"""HU-06: Acumular puntos."""
import pytest

from mercado_sabanero.modelos import CategoriaCliente
from mercado_sabanero.puntos import calcular_puntos


# CA1 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    "total, puntos_esperados",
    [
        (0, 0),
        (999, 0),          # no completa los $1.000
        (1_000, 1),
        (1_999, 1),        # solo cuentan los miles completos
        (250_515, 250),    # ejemplo del enunciado
    ],
)
def test_cliente_estandar_recibe_1_punto_por_cada_1000_completos(
    total, puntos_esperados
):
    # Act
    puntos = calcular_puntos(total, CategoriaCliente.ESTANDAR)

    # Assert
    assert puntos == puntos_esperados
