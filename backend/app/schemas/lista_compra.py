from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ResponseBase


class ListaCompraDetalleCreate(BaseModel):
    id_producto: int
    cantidad: float | None = None
    unidad: str | None = None
    prioridad: str = "media"
    nota: str | None = None


class ListaCompraDetalleUpdate(BaseModel):
    cantidad: float | None = None
    unidad: str | None = None
    prioridad: str | None = None
    comprado: bool | None = None
    nota: str | None = None


class ListaCompraDetalleResponse(ResponseBase):
    id_detalle: int
    id_lista: int
    id_producto: int
    cantidad: float | None
    unidad: str | None
    prioridad: str
    comprado: bool
    nota: str | None


class ListaCompraCreate(BaseModel):
    id_hogar: int
    nombre: str | None = None
    items: list[ListaCompraDetalleCreate] = []


class ListaCompraUpdate(BaseModel):
    nombre: str | None = None
    estado: str | None = None


class ListaCompraResponse(ResponseBase):
    id_lista: int
    id_hogar: int
    nombre: str | None
    estado: str
    fecha_creacion: datetime
    items: list[ListaCompraDetalleResponse] = []
