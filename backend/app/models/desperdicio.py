from datetime import datetime
from typing import Optional

from app.models import *
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Desperdicio(Base):
    __tablename__ = "desperdicio"

    id_desperdicio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_inventario: Mapped[int] = mapped_column(Integer, ForeignKey("inventario.id_inventario"), nullable=False)
    cantidad: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    motivo: Mapped[Optional[str]] = mapped_column(Enum("vencido", "mal_estado", "olvido", "otro"), nullable=True)
    comentario: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fecha_desperdicio: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    inventario: Mapped["Inventario"] = relationship("Inventario", back_populates="desperdicios")
