from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ResponseBase


class TagRecetaCreate(BaseModel):
    nombre: str
    color: str | None = None


class TagRecetaResponse(ResponseBase):
    id_tag: int
    nombre: str
    color: str | None


class RecetaIngredienteCreate(BaseModel):
    id_producto: int
    cantidad: float | None = None
    unidad_medida: str = "unidad"
    obligatorio: bool = True
    nota: str | None = None


class RecetaIngredienteResponse(ResponseBase):
    id_receta_ingrediente: int
    id_receta: int
    id_producto: int
    cantidad: float | None
    unidad_medida: str
    obligatorio: bool
    nota: str | None


class RecetaCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    instrucciones: str | None = None
    tiempo_preparacion: int | None = None
    dificultad: str = "facil"
    porciones: int | None = None
    imagen: str | None = None
    calorias: int | None = None
    es_publica: bool = True
    tags: list[int] = []
    ingredientes: list[RecetaIngredienteCreate] = []


class RecetaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    instrucciones: str | None = None
    tiempo_preparacion: int | None = None
    dificultad: str | None = None
    porciones: int | None = None
    imagen: str | None = None
    calorias: int | None = None
    es_publica: bool | None = None


class RecetaResponse(ResponseBase):
    id_receta: int
    id_usuario_creador: int | None
    nombre: str
    descripcion: str | None
    instrucciones: str | None
    tiempo_preparacion: int | None
    dificultad: str
    porciones: int | None
    imagen: str | None
    calorias: int | None
    es_publica: bool
    fecha_creacion: datetime


class RecetaDetalleResponse(RecetaResponse):
    tags: list[TagRecetaResponse] = []
    ingredientes: list[RecetaIngredienteResponse] = []


class RecetaFavoritaCreate(BaseModel):
    id_receta: int


class RecetaFavoritaResponse(ResponseBase):
    id_receta_favorita: int
    id_usuario: int
    id_receta: int
    fecha_guardado: datetime
