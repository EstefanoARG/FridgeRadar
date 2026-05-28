from typing import Optional
from sqlalchemy import String, Integer, Enum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class Zona(Base):
    __tablename__ = "zona"

    id_zona: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_hogar: Mapped[int] = mapped_column(Integer, ForeignKey("hogar.id_hogar"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo: Mapped[str] = mapped_column(
        Enum("refrigerador", "congelador", "alacena", "cajon", "puerta_refri"), nullable=False
    )
    icono: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    temperatura_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    temperatura_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    hogar: Mapped["Hogar"] = relationship("Hogar", back_populates="zonas")
    estantes: Mapped[list["Estante"]] = relationship("Estante", back_populates="zona")
