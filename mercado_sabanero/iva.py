"""HU-02: cálculo del IVA por producto."""
from mercado_sabanero.redondeo import dividir_redondeando


def calcular_iva(valor: int, tarifa: int, porcentaje_descuento: int = 0) -> int:
    base = dividir_redondeando(valor * (100 - porcentaje_descuento), 100)
    return dividir_redondeando(base * tarifa, 100)
