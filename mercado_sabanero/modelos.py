"""Modelos de dominio: producto, ítem del carrito y categoría de cliente."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    precio: int       # pesos, sin decimales
    tarifa_iva: int   # 0, 5 o 19


@dataclass(frozen=True)
class ItemCarrito:
    producto: Producto
    cantidad: int

    @property
    def valor(self) -> int:
        return self.producto.precio * self.cantidad
