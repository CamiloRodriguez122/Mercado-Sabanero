"""HU-01: carrito de compras."""
from mercado_sabanero.errores import CantidadInvalidaError, StockInsuficienteError
from mercado_sabanero.inventario import Inventario
from mercado_sabanero.modelos import ItemCarrito, Producto

CANTIDAD_MINIMA = 1
CANTIDAD_MAXIMA = 50


class Carrito:
    def __init__(self, inventario: Inventario):
        self._inventario = inventario
        self._items: dict[str, ItemCarrito] = {}

    def agregar(self, producto: Producto, cantidad: int) -> None:
        self._validar_cantidad(cantidad)
        cantidad_total = self.cantidad_de(producto.codigo) + cantidad
        stock = self._inventario.obtener_stock(producto.codigo)
        if stock < cantidad_total:
            raise StockInsuficienteError(
                f"Stock insuficiente de {producto.nombre}: "
                f"disponibles {stock}, solicitadas {cantidad_total}"
            )
        self._items[producto.codigo] = ItemCarrito(producto, cantidad_total)

    def cantidad_de(self, codigo_producto: str) -> int:
        item = self._items.get(codigo_producto)
        return item.cantidad if item else 0

    def items(self) -> list[ItemCarrito]:
        return list(self._items.values())

    def esta_vacio(self) -> bool:
        return not self._items

    def subtotal(self) -> int:
        return sum(item.valor for item in self._items.values())

    @staticmethod
    def _validar_cantidad(cantidad: int) -> None:
        if not isinstance(cantidad, int) or not CANTIDAD_MINIMA <= cantidad <= CANTIDAD_MAXIMA:
            raise CantidadInvalidaError(
                f"La cantidad debe ser un entero entre {CANTIDAD_MINIMA} "
                f"y {CANTIDAD_MAXIMA}"
            )
