"""Redondeo al peso más cercano con aritmética entera."""
import pytest

from mercado_sabanero.redondeo import dividir_redondeando


@pytest.mark.parametrize(
    "numerador, denominador, esperado",
    [(10, 4, 3), (9, 4, 2), (11, 4, 3), (5, 2, 3), (0, 7, 0)],
)
def test_divide_redondeando_al_entero_mas_cercano(numerador, denominador, esperado):
    # Act
    resultado = dividir_redondeando(numerador, denominador)

    # Assert
    assert resultado == esperado
