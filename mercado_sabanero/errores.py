"""Errores propios del dominio."""


class MercadoSabaneroError(Exception):
    """Clase base de todos los errores del módulo."""


class CantidadInvalidaError(MercadoSabaneroError, ValueError):
    """La cantidad no es un entero entre 1 y 50."""


class StockInsuficienteError(MercadoSabaneroError):
    """El inventario no tiene unidades suficientes."""


class CuponInvalidoError(MercadoSabaneroError):
    """El cupón no existe, está vencido o no aplica a la compra."""


class DatoInvalidoError(MercadoSabaneroError, ValueError):
    """Un dato de entrada (producto, municipio...) no es válido."""
