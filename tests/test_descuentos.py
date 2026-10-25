"""HU-03: Descuento por volumen."""
import pytest

from mercado_sabanero.descuentos import calcular_descuento, porcentaje_descuento_volumen


# CA1, CA2 y CA3 con valores límite ----------------------------------------
@pytest.mark.parametrize(
    "subtotal, porcentaje_esperado",
    [
        (0, 0),
        (199_999, 0),      # CA1: justo debajo del primer umbral
        (200_000, 5),      # CA2: límite inferior
        (499_999, 5),      # CA2: límite superior
        (500_000, 10),     # CA3: límite inferior
        (2_000_000, 10),
    ],
)
def test_aplica_el_porcentaje_de_descuento_segun_el_subtotal(
    subtotal, porcentaje_esperado
):
    # Act
    porcentaje = porcentaje_descuento_volumen(subtotal)

    # Assert
    assert porcentaje == porcentaje_esperado


def test_el_descuento_en_pesos_del_ejemplo_del_enunciado_es_11400():
    # Arrange: subtotal 228.000 con 5 %
    # Act
    descuento = calcular_descuento(228_000, 5)

    # Assert
    assert descuento == 11_400


def test_el_descuento_se_redondea_al_peso_mas_cercano():
    # Arrange: 5 % de 200.010 = 10.000,5 -> 10.001
    # Act
    descuento = calcular_descuento(200_010, 5)

    # Assert
    assert descuento == 10_001
