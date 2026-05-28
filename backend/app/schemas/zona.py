from pydantic import BaseModel

from app.schemas.common import ResponseBase


class ZonaCreate(BaseModel):
    id_hogar: int
    nombre: str
    tipo: str
    icono: str | None = None
    temperatura_min: float | None = None
    temperatura_max: float | None = None


class ZonaUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    icono: str | None = None
    temperatura_min: float | None = None
    temperatura_max: float | None = None


class ZonaResponse(ResponseBase):
    id_zona: int
    id_hogar: int
    nombre: str
    tipo: str
    icono: str | None
    temperatura_min: float | None
    temperatura_max: float | None
