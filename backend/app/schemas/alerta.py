from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ResponseBase


class AlertaCreate(BaseModel):
    id_usuario: int
    id_inventario: int | None = None
    titulo: str
    mensaje: str
    tipo: str


class AlertaUpdate(BaseModel):
    leida: bool | None = None


class AlertaResponse(ResponseBase):
    id_alerta: int
    id_usuario: int
    id_inventario: int | None
    titulo: str
    mensaje: str
    tipo: str
    leida: bool
    fecha_alerta: datetime
