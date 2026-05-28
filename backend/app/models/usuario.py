from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    correo: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ultimo_acceso: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    estado: Mapped[str] = mapped_column(Enum("activo", "suspendido", "eliminado"), default="activo")

    hogares: Mapped[list["UsuarioHogar"]] = relationship("UsuarioHogar", back_populates="usuario")
    inventarios: Mapped[list["Inventario"]] = relationship("Inventario", back_populates="usuario_agrego")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship("MovimientoInventario", back_populates="usuario")
    recetas: Mapped[list["Receta"]] = relationship("Receta", back_populates="usuario_creador")
    alertas: Mapped[list["Alerta"]] = relationship("Alerta", back_populates="usuario")
    sugerencias: Mapped[list["SugerenciaReceta"]] = relationship("SugerenciaReceta", back_populates="usuario")
    recetas_favoritas: Mapped[list["RecetaFavorita"]] = relationship("RecetaFavorita", back_populates="usuario")
