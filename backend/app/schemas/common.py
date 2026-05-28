from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResponseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class TimestampMixin(BaseModel):
    fecha_registro: datetime | None = None
