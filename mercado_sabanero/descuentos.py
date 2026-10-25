"""HU-03: descuento por volumen."""
from mercado_sabanero.redondeo import dividir_redondeando


def porcentaje_descuento_volumen(subtotal: int) -> int:
    if subtotal >= 500_000:
        return 10
    if subtotal >= 200_000:
        return 5
    return 0


def calcular_descuento(subtotal: int, porcentaje: int) -> int:
    return dividir_redondeando(subtotal * porcentaje, 100)
