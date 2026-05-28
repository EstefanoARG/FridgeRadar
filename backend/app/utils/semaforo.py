from datetime import date

VERDE    = "verde"
AMARILLO = "amarillo"
ROJO     = "rojo"
VENCIDO  = "vencido"


def calcular_estado(fecha_vencimiento: date | None) -> str:
    """Calcula el estado del semáforo según la fecha de vencimiento."""
    if fecha_vencimiento is None:
        return VERDE

    dias = (fecha_vencimiento - date.today()).days

    if dias > 7:
        return VERDE
    elif dias >= 3:
        return AMARILLO
    elif dias >= 0:
        return ROJO
    else:
        return VENCIDO


def es_critico(estado: str) -> bool:
    """True si el producto está en amarillo o rojo."""
    return estado in (AMARILLO, ROJO)


def dias_restantes(fecha_vencimiento: date | None) -> int | None:
    if fecha_vencimiento is None:
        return None
    return (fecha_vencimiento - date.today()).days
