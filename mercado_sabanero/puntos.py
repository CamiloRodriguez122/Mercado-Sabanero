"""HU-06: puntos de fidelidad."""
from mercado_sabanero.modelos import CategoriaCliente


def calcular_puntos(total_sin_envio: int, categoria: CategoriaCliente) -> int:
    puntos = total_sin_envio // 1_000
    return puntos * 2 if categoria is CategoriaCliente.ORO else puntos
