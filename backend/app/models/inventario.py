from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class Inventario(Base):
    __tablename__ = "inventario"

    id_inventario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_hogar: Mapped[int] = mapped_column(Integer, ForeignKey("hogar.id_hogar"), nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    id_estante: Mapped[int] = mapped_column(Integer, ForeignKey("estante.id_estante"), nullable=False)
    id_usuario_agrego: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False, default=1)
    fecha_compra: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_vencimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    abierto: Mapped[bool] = mapped_column(Boolean, default=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado_caducidad: Mapped[str] = mapped_column(Enum("verde", "amarillo", "rojo", "vencido"), default="verde")
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hogar: Mapped["Hogar"] = relationship("Hogar", back_populates="inventarios")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="inventarios")
    estante: Mapped["Estante"] = relationship("Estante", back_populates="inventarios")
    usuario_agrego: Mapped["Usuario"] = relationship("Usuario", back_populates="inventarios")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship("MovimientoInventario", back_populates="inventario")
    alertas: Mapped[list["Alerta"]] = relationship("Alerta", back_populates="inventario")
    desperdicios: Mapped[list["Desperdicio"]] = relationship("Desperdicio", back_populates="inventario")
