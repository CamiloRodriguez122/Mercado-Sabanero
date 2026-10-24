"""Errores propios del dominio."""


class MercadoSabaneroError(Exception):
    """Clase base de todos los errores del módulo."""


class CantidadInvalidaError(MercadoSabaneroError, ValueError):
    """La cantidad no es un entero entre 1 y 50."""
