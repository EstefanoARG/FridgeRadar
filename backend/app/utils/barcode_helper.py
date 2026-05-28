import re


def validar_codigo_barras(codigo: str) -> bool:
    """Valida un código de barras EAN-13 o UPC."""
    if not re.match(r"^\d{8,13}$", codigo):
        return False
    return True


def formatear_codigo_barras(codigo: str) -> str:
    """Limpia y normaliza un código de barras."""
    return codigo.strip()


def sugerir_unidad_por_categoria(id_categoria: int | None) -> str:
    """Sugiere una unidad de medida según la categoría del producto."""
    sugerencias = {
        1: "litro",   # Lácteos
        2: "kg",      # Carnes
        3: "kg",      # Verduras
        4: "kg",      # Frutas
        5: "litro",   # Bebidas
        6: "unidad",  # Snacks
        7: "ml",      # Condimentos
        8: "kg",      # Granos
        9: "unidad",  # Congelados
        10: "unidad", # Panadería
    }
    return sugerencias.get(id_categoria, "unidad")
