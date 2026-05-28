from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.categoria_producto import CategoriaProducto
    from app.models.inventario import Inventario
    from app.models.lista_compra_detalle import ListaCompraDetalle
    from app.models.receta_ingrediente import RecetaIngrediente


class Producto(Base):
    __tablename__ = "producto"

    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    id_categoria: Mapped[int | None] = mapped_column(Integer, ForeignKey("categoria_producto.id_categoria"), nullable=True)
    codigo_barras: Mapped[str | None] = mapped_column(String(50), nullable=True)
    unidad_medida: Mapped[str] = mapped_column(
        Enum("unidad", "kg", "g", "litro", "ml", "paquete", "lata", "botella", "taza", "cucharada"),
        default="unidad",
    )
    perecible: Mapped[bool] = mapped_column(Boolean, default=True)
    dias_promedio_vencimiento: Mapped[int | None] = mapped_column(Integer, nullable=True)
    imagen: Mapped[str | None] = mapped_column(String(255), nullable=True)

    categoria: Mapped[Optional["CategoriaProducto"]] = relationship("CategoriaProducto", back_populates="productos")
    inventarios: Mapped[list["Inventario"]] = relationship("Inventario", back_populates="producto")
    ingredientes_receta: Mapped[list["RecetaIngrediente"]] = relationship("RecetaIngrediente", back_populates="producto")
    detalles_lista: Mapped[list["ListaCompraDetalle"]] = relationship("ListaCompraDetalle", back_populates="producto")
