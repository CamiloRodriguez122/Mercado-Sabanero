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


@pytest.mark.parametrize("municipio", ["Corozal", "Sampués", "San Marcos"])
def test_envio_a_otros_municipios_de_sucre_cuesta_15000(municipio):
    # Act
    envio = calcular_envio(municipio, valor_productos_con_iva=50_000)

    # Assert
    assert envio == 15_000


# CA2: valores límite ------------------------------------------------------
@pytest.mark.parametrize(
    "valor_con_iva, envio_esperado",
    [
        (0, 8_000),
        (149_999, 8_000),   # un peso menos: se cobra
        (150_000, 0),       # límite: gratis
        (150_001, 0),
    ],
)
def test_envio_es_gratis_desde_150000_en_productos_con_iva(
    valor_con_iva, envio_esperado
):
    # Act
    envio = calcular_envio("Sincelejo", valor_con_iva)

    # Assert
    assert envio == envio_esperado


def test_envio_gratis_por_umbral_tambien_aplica_a_otros_municipios():
    # Act
    envio = calcular_envio("Corozal", valor_productos_con_iva=150_000)

    # Assert
    assert envio == 0


def test_cupon_enviogratis_deja_el_envio_en_cero_aunque_la_compra_sea_pequena():
    # Act
    envio = calcular_envio("Corozal", 10_000, cupon_envio_gratis=True)

    # Assert
    assert envio == 0
