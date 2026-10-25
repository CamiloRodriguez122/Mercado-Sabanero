"""Modelos de dominio: producto, ítem del carrito y categoría de cliente."""
from dataclasses import dataclass

from mercado_sabanero.errores import DatoInvalidoError

TARIFAS_IVA_VALIDAS = (0, 5, 19)


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    precio: int       # pesos, sin decimales
    tarifa_iva: int   # 0, 5 o 19

    def __post_init__(self):
        if not isinstance(self.precio, int) or self.precio <= 0:
            raise DatoInvalidoError("El precio debe ser un entero positivo")
        if self.tarifa_iva not in TARIFAS_IVA_VALIDAS:
            raise DatoInvalidoError(
                f"Tarifa de IVA inválida: {self.tarifa_iva}. "
                f"Use una de {TARIFAS_IVA_VALIDAS}"
            )


@dataclass(frozen=True)
class ItemCarrito:
    producto: Producto
    cantidad: int

    @property
    def valor(self) -> int:
        return self.producto.precio * self.cantidad
