"""HU-05: costo del envío."""
from mercado_sabanero.errores import DatoInvalidoError

COSTO_ENVIO_SINCELEJO = 8_000
COSTO_ENVIO_OTROS_MUNICIPIOS = 15_000
UMBRAL_ENVIO_GRATIS = 150_000


def calcular_envio(
    municipio: str, valor_productos_con_iva: int, cupon_envio_gratis: bool = False
) -> int:
    """Costo de envío.

    valor_productos_con_iva: suma de las líneas cuyo producto tiene tarifa > 0.
    """
    nombre = (municipio or "").strip().casefold()
    if not nombre:
        raise DatoInvalidoError("El municipio de entrega es obligatorio")
    if cupon_envio_gratis or valor_productos_con_iva >= UMBRAL_ENVIO_GRATIS:
        return 0
    if nombre == "sincelejo":
        return COSTO_ENVIO_SINCELEJO
    return COSTO_ENVIO_OTROS_MUNICIPIOS
