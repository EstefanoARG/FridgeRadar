from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ResponseBase


class HogarCreate(BaseModel):
    nombre: str
    codigo_invitacion: str | None = None


class HogarUpdate(BaseModel):
    nombre: str | None = None


class HogarResponse(ResponseBase):
    id_hogar: int
    nombre: str
    codigo_invitacion: str | None
    fecha_creacion: datetime


class UsuarioHogarCreate(BaseModel):
    id_usuario: int
    id_hogar: int
    rol: str = "miembro"


class UsuarioHogarResponse(ResponseBase):
    id_usuario_hogar: int
    id_usuario: int
    id_hogar: int
    rol: str
    fecha_union: datetime
