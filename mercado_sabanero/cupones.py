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


def validar_cupon(codigo: str, subtotal: int, hoy: Optional[date] = None) -> Cupon:
    codigo_normalizado = (codigo or "").strip().upper()
    if codigo_normalizado == "SABANERO10":
        if subtotal < 50_000:
            raise CuponInvalidoError(
                "El cupón 'SABANERO10' requiere un subtotal de al menos $50,000"
            )
        return Cupon("SABANERO10", vence=date(2026, 12, 31), porcentaje=10, subtotal_minimo=50_000)
    if codigo_normalizado == "ENVIOGRATIS":
        return Cupon("ENVIOGRATIS", vence=date(2026, 12, 31), envio_gratis=True)
    raise CuponInvalidoError(f"El cupón '{codigo}' no existe")
