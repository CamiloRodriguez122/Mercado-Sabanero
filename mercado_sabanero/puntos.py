"""HU-06: puntos de fidelidad."""
from mercado_sabanero.modelos import CategoriaCliente

PESOS_POR_PUNTO = 1_000


def calcular_puntos(total_sin_envio: int, categoria: CategoriaCliente) -> int:
    puntos = total_sin_envio // PESOS_POR_PUNTO
    return puntos * 2 if categoria is CategoriaCliente.ORO else puntos
