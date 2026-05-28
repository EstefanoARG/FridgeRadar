from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class ListaCompra(Base):
    __tablename__ = "lista_compra"

    id_lista: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_hogar: Mapped[int] = mapped_column(Integer, ForeignKey("hogar.id_hogar"), nullable=False)
    nombre: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    estado: Mapped[str] = mapped_column(Enum("activa", "completada"), default="activa")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hogar: Mapped["Hogar"] = relationship("Hogar", back_populates="listas_compra")
    detalles: Mapped[list["ListaCompraDetalle"]] = relationship("ListaCompraDetalle", back_populates="lista")
