from datetime import date, datetime


def formatear_fecha(fecha: date | None) -> str | None:
    if fecha is None:
        return None
    return fecha.strftime("%d/%m/%Y")


def parsear_fecha(cadena: str) -> date | None:
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
    for fmt in formatos:
        try:
            return datetime.strptime(cadena, fmt).date()
        except ValueError:
            continue
    return None


def dias_hasta(fecha: date | None) -> int | None:
    if fecha is None:
        return None
    return (fecha - date.today()).days


def esta_vencido(fecha: date | None) -> bool:
    if fecha is None:
        return False
    return fecha < date.today()


def es_hoy(fecha: date | None) -> bool:
    if fecha is None:
        return False
    return fecha == date.today()


def dentro_de_dias(fecha: date | None, dias: int) -> bool:
    if fecha is None:
        return False
    return 0 <= (fecha - date.today()).days <= dias
