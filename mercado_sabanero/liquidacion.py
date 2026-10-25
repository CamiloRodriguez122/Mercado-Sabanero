"""Liquidación completa de una compra (integra HU-01 a HU-06)."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from mercado_sabanero.carrito import Carrito
from mercado_sabanero.cupones import validar_cupon
from mercado_sabanero.descuentos import calcular_descuento, porcentaje_descuento_volumen
from mercado_sabanero.envio import calcular_envio
from mercado_sabanero.errores import CarritoVacioError
from mercado_sabanero.iva import calcular_iva
from mercado_sabanero.modelos import CategoriaCliente
from mercado_sabanero.puntos import calcular_puntos


@dataclass(frozen=True)
class LineaLiquidada:
    codigo: str
    valor: int
    iva: int


@dataclass(frozen=True)
class Liquidacion:
    subtotal: int
    porcentaje_descuento: int
    descuento: int
    iva: int
    envio: int
    total: int
    puntos: int
    lineas: tuple


def liquidar(
    carrito: Carrito,
    municipio: str,
    categoria: CategoriaCliente = CategoriaCliente.ESTANDAR,
    codigo_cupon: Optional[str] = None,
    hoy: Optional[date] = None,
) -> Liquidacion:
    if carrito.esta_vacio():
        raise CarritoVacioError("No se puede liquidar un carrito vacío")

    subtotal = carrito.subtotal()
    porcentaje_volumen = porcentaje_descuento_volumen(subtotal)
    porcentaje_cupon, cupon_envio_gratis = 0, False
    if codigo_cupon:
        cupon = validar_cupon(codigo_cupon, subtotal, hoy)
        porcentaje_cupon, cupon_envio_gratis = cupon.porcentaje, cupon.envio_gratis
    porcentaje = max(porcentaje_volumen, porcentaje_cupon)
    descuento = calcular_descuento(subtotal, porcentaje)
    lineas = tuple(
        LineaLiquidada(
            item.producto.codigo,
            item.valor,
            calcular_iva(item.valor, item.producto.tarifa_iva, porcentaje),
        )
        for item in carrito.items()
    )
    iva = sum(linea.iva for linea in lineas)
    valor_con_iva = sum(i.valor for i in carrito.items() if i.producto.tarifa_iva > 0)
    envio = calcular_envio(municipio, valor_con_iva, cupon_envio_gratis)
    return Liquidacion(
        subtotal=subtotal,
        porcentaje_descuento=porcentaje,
        descuento=descuento,
        iva=iva,
        envio=envio,
        total=subtotal - descuento + iva + envio,
        puntos=calcular_puntos(subtotal - descuento + iva, categoria),
        lineas=lineas,
    )
