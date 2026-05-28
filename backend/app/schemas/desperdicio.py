from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ResponseBase


class DesperdicioCreate(BaseModel):
    id_inventario: int
    cantidad: float | None = None
    motivo: str | None = None
    comentario: str | None = None


class DesperdicioResponse(ResponseBase):
    id_desperdicio: int
    id_inventario: int
    cantidad: float | None
    motivo: str | None
    comentario: str | None
    fecha_desperdicio: datetime
