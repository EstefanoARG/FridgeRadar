from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class RecetaIngrediente(Base):
    __tablename__ = "receta_ingrediente"

    id_receta_ingrediente: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_receta: Mapped[int] = mapped_column(Integer, ForeignKey("receta.id_receta"), nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unidad_medida: Mapped[str] = mapped_column(
        Enum("unidad", "kg", "g", "litro", "ml", "taza", "cucharada", "pizca"), default="unidad"
    )
    obligatorio: Mapped[bool] = mapped_column(Boolean, default=True)
    nota: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    receta: Mapped["Receta"] = relationship("Receta", back_populates="ingredientes")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="ingredientes_receta")
