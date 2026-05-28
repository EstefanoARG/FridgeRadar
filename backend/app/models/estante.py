from typing import Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class Estante(Base):
    __tablename__ = "estante"

    id_estante: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_zona: Mapped[int] = mapped_column(Integer, ForeignKey("zona.id_zona"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    posicion_vertical: Mapped[int] = mapped_column(Integer, nullable=False)
    color_ui: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    zona: Mapped["Zona"] = relationship("Zona", back_populates="estantes")
    inventarios: Mapped[list["Inventario"]] = relationship("Inventario", back_populates="estante")
