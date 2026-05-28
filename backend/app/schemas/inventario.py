from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.common import ResponseBase


class InventarioCreate(BaseModel):
    id_producto:       int
    id_estante:        int
    cantidad:          float = 1.0
    fecha_compra:      date | None = None
    fecha_vencimiento: date | None = None
    abierto:           bool = False
    observaciones:     str | None = None


class InventarioUpdate(BaseModel):
    id_estante:        int | None = None
    cantidad:          float | None = None
    fecha_vencimiento: date | None = None
    abierto:           bool | None = None
    observaciones:     str | None = None


class InventarioResponse(ResponseBase):
    id_inventario:     int
    id_hogar:          int
    id_producto:       int
    id_estante:        int
    id_usuario_agrego: int
    cantidad:          float
    fecha_compra:      date | None
    fecha_vencimiento: date | None
    abierto:           bool
    observaciones:     str | None
    estado_caducidad:  str
    fecha_registro:    datetime


class MovimientoInventarioResponse(ResponseBase):
    id_movimiento:    int
    id_inventario:    int
    id_usuario:       int
    tipo_movimiento:  str
    cantidad:         float | None
    descripcion:      str | None
    fecha_movimiento: datetime
