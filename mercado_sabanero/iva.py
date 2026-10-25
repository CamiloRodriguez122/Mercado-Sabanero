"""HU-02: cálculo del IVA por producto."""


def calcular_iva(valor: int, tarifa: int, porcentaje_descuento: int = 0) -> int:
    base = valor * (100 - porcentaje_descuento) // 100
    return base * tarifa // 100
