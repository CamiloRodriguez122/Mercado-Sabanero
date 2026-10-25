"""HU-05: costo del envío."""
from mercado_sabanero.errores import DatoInvalidoError


def calcular_envio(
    municipio: str, valor_productos_con_iva: int, cupon_envio_gratis: bool = False
) -> int:
    nombre = (municipio or "").strip().casefold()
    if not nombre:
        raise DatoInvalidoError("El municipio de entrega es obligatorio")
    if cupon_envio_gratis or valor_productos_con_iva >= 150_000:
        return 0
    if nombre == "sincelejo":
        return 8_000
    return 15_000
