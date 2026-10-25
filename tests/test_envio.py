"""HU-05: Calcular el envío."""
import pytest

from mercado_sabanero.envio import calcular_envio


# CA1 ---------------------------------------------------------------------
@pytest.mark.parametrize("municipio", ["Sincelejo", "SINCELEJO", "  sincelejo "])
def test_envio_dentro_de_sincelejo_cuesta_8000(municipio):
    # Act
    envio = calcular_envio(municipio, valor_productos_con_iva=50_000)

    # Assert
    assert envio == 8_000
