from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Float, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class MovimientoInventario(Base):
    __tablename__ = "movimiento_inventario"

    id_movimiento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_inventario: Mapped[int] = mapped_column(Integer, ForeignKey("inventario.id_inventario"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    tipo_movimiento: Mapped[str] = mapped_column(
        Enum("agregado", "movido", "consumido", "eliminado", "vencido"), nullable=False
    )
    cantidad: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fecha_movimiento: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    inventario: Mapped["Inventario"] = relationship("Inventario", back_populates="movimientos")
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="movimientos")
