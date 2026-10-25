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


# CA2 ---------------------------------------------------------------------
def test_enviogratis_marca_el_envio_como_gratuito():
    # Act
    cupon = validar_cupon("ENVIOGRATIS", 10_000, HOY)

    # Assert
    assert cupon.envio_gratis is True
    assert cupon.porcentaje == 0


# CA3 ---------------------------------------------------------------------
@pytest.mark.parametrize("codigo", ["NOEXISTE", "", None, "SABANERO20"])
def test_rechaza_cupones_inexistentes(codigo):
    with pytest.raises(CuponInvalidoError):
        validar_cupon(codigo, 100_000, HOY)


def test_el_codigo_del_cupon_no_distingue_mayusculas_ni_espacios():
    # Act
    cupon = validar_cupon("  sabanero10 ", 80_000, HOY)

    # Assert
    assert cupon.codigo == "SABANERO10"
