from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.schemas.common import ResponseBase


class UsuarioCreate(BaseModel):
    nombres:       str
    apellidos:     str | None = None
    correo:        EmailStr
    password:      str


class UsuarioUpdate(BaseModel):
    nombres:       str | None = None
    apellidos:     str | None = None
    correo:        EmailStr | None = None
    password:      str | None = None
    estado:        str | None = None


class UsuarioResponse(ResponseBase):
    id_usuario:     int
    nombres:        str
    apellidos:      str | None
    correo:         str
    fecha_registro: datetime | None = None
    estado:         str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
