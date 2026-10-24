"""HU-01: carrito de compras."""
from mercado_sabanero.inventario import Inventario
from mercado_sabanero.modelos import ItemCarrito, Producto


class Carrito:
    def __init__(self, inventario: Inventario):
        self._inventario = inventario
        self._items: dict[str, ItemCarrito] = {}

    def agregar(self, producto: Producto, cantidad: int) -> None:
        self._items[producto.codigo] = ItemCarrito(producto, cantidad)

    def cantidad_de(self, codigo_producto: str) -> int:
        item = self._items.get(codigo_producto)
        return item.cantidad if item else 0
