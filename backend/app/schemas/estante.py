from pydantic import BaseModel

from app.schemas.common import ResponseBase


class EstanteCreate(BaseModel):
    id_zona: int
    nombre: str
    posicion_vertical: int
    color_ui: str | None = None


class EstanteUpdate(BaseModel):
    nombre: str | None = None
    posicion_vertical: int | None = None
    color_ui: str | None = None


class EstanteResponse(ResponseBase):
    id_estante: int
    id_zona: int
    nombre: str
    posicion_vertical: int
    color_ui: str | None
