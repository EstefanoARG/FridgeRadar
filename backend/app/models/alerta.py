from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.inventario import Inventario
    from app.models.usuario import Usuario


class Alerta(Base):
    __tablename__ = "alerta"

    id_alerta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_inventario: Mapped[int | None] = mapped_column(Integer, ForeignKey("inventario.id_inventario"), nullable=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str] = mapped_column(Enum("vencimiento", "desperdicio", "receta", "stock_bajo"), nullable=False)
    leida: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_alerta: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="alertas")
    inventario: Mapped[Optional["Inventario"]] = relationship("Inventario", back_populates="alertas")
