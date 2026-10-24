"""HU-01: carrito de compras."""
from mercado_sabanero.errores import CantidadInvalidaError
from mercado_sabanero.inventario import Inventario
from mercado_sabanero.modelos import ItemCarrito, Producto


class Carrito:
    def __init__(self, inventario: Inventario):
        self._inventario = inventario
        self._items: dict[str, ItemCarrito] = {}

    def agregar(self, producto: Producto, cantidad: int) -> None:
        if not isinstance(cantidad, int) or not 1 <= cantidad <= 50:
            raise CantidadInvalidaError("La cantidad debe ser un entero entre 1 y 50")
        self._items[producto.codigo] = ItemCarrito(producto, cantidad)

    def cantidad_de(self, codigo_producto: str) -> int:
        item = self._items.get(codigo_producto)
        return item.cantidad if item else 0

    def esta_vacio(self) -> bool:
        return not self._items
