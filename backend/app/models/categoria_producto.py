from typing import Optional

from app.models.producto import Producto
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CategoriaProducto(Base):
    __tablename__ = "categoria_producto"

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    icono: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    productos: Mapped[list["Producto"]] = relationship("Producto", back_populates="categoria")
