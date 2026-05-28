from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class ListaCompraDetalle(Base):
    __tablename__ = "lista_compra_detalle"

    id_detalle: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_lista: Mapped[int] = mapped_column(Integer, ForeignKey("lista_compra.id_lista"), nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unidad: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    prioridad: Mapped[str] = mapped_column(Enum("alta", "media", "baja"), default="media")
    comprado: Mapped[bool] = mapped_column(Boolean, default=False)
    nota: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    lista: Mapped["ListaCompra"] = relationship("ListaCompra", back_populates="detalles")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="detalles_lista")
