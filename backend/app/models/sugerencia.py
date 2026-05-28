from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class SugerenciaReceta(Base):
    __tablename__ = "sugerencia_receta"

    id_sugerencia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_hogar: Mapped[int] = mapped_column(Integer, ForeignKey("hogar.id_hogar"), nullable=False)
    id_receta: Mapped[int] = mapped_column(Integer, ForeignKey("receta.id_receta"), nullable=False)
    porcentaje_coincidencia: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    usa_productos_criticos: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_sugerencia: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="sugerencias")
    hogar: Mapped["Hogar"] = relationship("Hogar", back_populates="sugerencias")
    receta: Mapped["Receta"] = relationship("Receta", back_populates="sugerencias")
