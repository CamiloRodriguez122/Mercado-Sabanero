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


# CA2 ---------------------------------------------------------------------
def test_el_iva_se_calcula_sobre_el_valor_con_el_descuento_aplicado():
    # Arrange: $200.000 con 5 % de descuento = $190.000 -> IVA 19 % = $36.100
    # Act
    iva = calcular_iva(200_000, 19, porcentaje_descuento=5)

    # Assert
    assert iva == 36_100


# Redondeo (regla del alcance: al peso más cercano) -----------------------
@pytest.mark.parametrize(
    "valor, iva_esperado",
    [
        (1_000, 50),   # 50,00  -> 50
        (1_001, 50),   # 50,05  -> 50  (baja)
        (1_010, 51),   # 50,50  -> 51  (la mitad sube)
        (1_011, 51),   # 50,55  -> 51  (sube)
    ],
)
def test_el_iva_se_redondea_al_peso_mas_cercano(valor, iva_esperado):
    # Act
    iva = calcular_iva(valor, 5)

    # Assert
    assert iva == iva_esperado
