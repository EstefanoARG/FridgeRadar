from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class Hogar(Base):
    __tablename__ = "hogar"

    id_hogar: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_invitacion: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    miembros: Mapped[list["UsuarioHogar"]] = relationship("UsuarioHogar", back_populates="hogar")
    zonas: Mapped[list["Zona"]] = relationship("Zona", back_populates="hogar")
    inventarios: Mapped[list["Inventario"]] = relationship("Inventario", back_populates="hogar")
    listas_compra: Mapped[list["ListaCompra"]] = relationship("ListaCompra", back_populates="hogar")
    sugerencias: Mapped[list["SugerenciaReceta"]] = relationship("SugerenciaReceta", back_populates="hogar")
