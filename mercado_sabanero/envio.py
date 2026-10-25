"""HU-05: costo del envío."""


def calcular_envio(
    municipio: str, valor_productos_con_iva: int, cupon_envio_gratis: bool = False
) -> int:
    nombre = (municipio or "").strip().casefold()
    if cupon_envio_gratis or valor_productos_con_iva >= 150_000:
        return 0
    if nombre == "sincelejo":
        return 8_000
    return 15_000
