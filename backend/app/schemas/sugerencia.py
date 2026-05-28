from app.schemas.common import ResponseBase


class SugerenciaResponse(ResponseBase):
    id_receta:               int
    nombre:                  str
    descripcion:             str | None = None
    tiempo_preparacion:      int | None = None
    dificultad:              str
    porciones:               int | None = None
    imagen:                  str | None = None
    calorias:                int | None = None
    porcentaje_match:        float
    usa_criticos:            bool
