"""HU-04: Usar cupones."""
from datetime import date

import pytest

from mercado_sabanero.cupones import validar_cupon
from mercado_sabanero.errores import CuponInvalidoError

HOY = date(2026, 10, 23)


# CA1 ---------------------------------------------------------------------
@pytest.mark.parametrize("subtotal", [50_000, 50_001, 1_000_000])
def test_sabanero10_otorga_10_por_ciento_con_subtotal_de_al_menos_50000(subtotal):
    # Act
    cupon = validar_cupon("SABANERO10", subtotal, HOY)

    # Assert
    assert cupon.porcentaje == 10


def test_sabanero10_se_rechaza_con_subtotal_menor_a_50000():
    with pytest.raises(CuponInvalidoError, match="subtotal"):
        validar_cupon("SABANERO10", 49_999, HOY)
