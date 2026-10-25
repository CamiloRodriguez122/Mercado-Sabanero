"""Aritmética entera para dinero (pesos sin decimales)."""


def dividir_redondeando(numerador: int, denominador: int) -> int:
    """Divide y redondea al entero más cercano (la mitad sube).

    Se usan solo enteros para evitar los errores de redondeo de float.
    """
    return (2 * numerador + denominador) // (2 * denominador)
