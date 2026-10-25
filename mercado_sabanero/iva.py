"""HU-02: cálculo del IVA por producto."""
from mercado_sabanero.redondeo import dividir_redondeando


def calcular_iva(valor: int, tarifa: int, porcentaje_descuento: int = 0) -> int:
    """IVA de una línea, calculado sobre el valor ya descontado.

    base = valor * (100 - descuento) / 100
    iva  = base * tarifa / 100  ->  se hace en un solo paso entero.
    """
    return dividir_redondeando(valor * (100 - porcentaje_descuento) * tarifa, 10_000)
