"""Contrato del servicio externo de inventario.

En producción lo implementaría un cliente HTTP; en las pruebas se
reemplaza por un doble de prueba (Mock).
"""
from abc import ABC, abstractmethod


class Inventario(ABC):
    @abstractmethod
    def obtener_stock(self, codigo_producto: str) -> int:
        """Devuelve las unidades disponibles del producto."""
