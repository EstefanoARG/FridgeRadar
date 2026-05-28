from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.receta_favorita import RecetaFavorita
    from app.models.receta_ingrediente import RecetaIngrediente
    from app.models.receta_tag import RecetaTag
    from app.models.sugerencia import SugerenciaReceta
    from app.models.usuario import Usuario

from app.core.database import Base


class Receta(Base):
    __tablename__ = "receta"

    id_receta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario_creador: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instrucciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tiempo_preparacion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    dificultad: Mapped[str] = mapped_column(Enum("facil", "media", "dificil"), default="facil")
    porciones: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    imagen: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    calorias: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    es_publica: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario_creador: Mapped[Optional["Usuario"]] = relationship("Usuario", back_populates="recetas")
    tags: Mapped[list["RecetaTag"]] = relationship("RecetaTag", back_populates="receta")
    ingredientes: Mapped[list["RecetaIngrediente"]] = relationship("RecetaIngrediente", back_populates="receta")
    favoritos: Mapped[list["RecetaFavorita"]] = relationship("RecetaFavorita", back_populates="receta")
    sugerencias: Mapped[list["SugerenciaReceta"]] = relationship("SugerenciaReceta", back_populates="receta")
