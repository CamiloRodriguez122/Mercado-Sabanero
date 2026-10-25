"""HU-04: cupones de descuento."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from mercado_sabanero.errores import CuponInvalidoError


@dataclass(frozen=True)
class Cupon:
    codigo: str
    vence: date
    porcentaje: int = 0
    envio_gratis: bool = False
    subtotal_minimo: int = 0


CUPONES = {
    "SABANERO10": Cupon(
        "SABANERO10", vence=date(2026, 12, 31), porcentaje=10, subtotal_minimo=50_000
    ),
    "ENVIOGRATIS": Cupon("ENVIOGRATIS", vence=date(2026, 12, 31), envio_gratis=True),
}


def validar_cupon(codigo: str, subtotal: int, hoy: Optional[date] = None) -> Cupon:
    """Devuelve el cupón si es aplicable; si no, lanza CuponInvalidoError."""
    hoy = hoy or date.today()
    cupon = CUPONES.get((codigo or "").strip().upper())
    if cupon is None:
        raise CuponInvalidoError(f"El cupón '{codigo}' no existe")
    if hoy > cupon.vence:
        raise CuponInvalidoError(f"El cupón '{cupon.codigo}' está vencido")
    if subtotal < cupon.subtotal_minimo:
        raise CuponInvalidoError(
            f"El cupón '{cupon.codigo}' requiere un subtotal de al menos "
            f"${cupon.subtotal_minimo:,}"
        )
    return cupon
