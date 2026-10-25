"""HU-05: costo del envío."""


def calcular_envio(municipio: str, valor_productos_con_iva: int) -> int:
    nombre = (municipio or "").strip().casefold()
    if valor_productos_con_iva >= 150_000:
        return 0
    if nombre == "sincelejo":
        return 8_000
    return 15_000
