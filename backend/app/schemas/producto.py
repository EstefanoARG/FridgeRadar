from pydantic import BaseModel

from app.schemas.common import ResponseBase


class CategoriaProductoCreate(BaseModel):
    nombre: str
    icono: str | None = None
    color: str | None = None


class CategoriaProductoResponse(ResponseBase):
    id_categoria: int
    nombre: str
    icono: str | None
    color: str | None


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    id_categoria: int | None = None
    codigo_barras: str | None = None
    unidad_medida: str = "unidad"
    perecible: bool = True
    dias_promedio_vencimiento: int | None = None
    imagen: str | None = None


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    id_categoria: int | None = None
    codigo_barras: str | None = None
    unidad_medida: str | None = None
    perecible: bool | None = None
    dias_promedio_vencimiento: int | None = None
    imagen: str | None = None


class ProductoResponse(ResponseBase):
    id_producto: int
    nombre: str
    descripcion: str | None
    id_categoria: int | None
    codigo_barras: str | None
    unidad_medida: str
    perecible: bool
    dias_promedio_vencimiento: int | None
    imagen: str | None


class ProductoConCategoriaResponse(ProductoResponse):
    categoria: CategoriaProductoResponse | None = None
