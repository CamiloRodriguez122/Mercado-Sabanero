"""HU-02: cálculo del IVA por producto."""


def calcular_iva(valor: int, tarifa: int) -> int:
    return valor * tarifa // 100
