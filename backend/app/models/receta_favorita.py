from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class RecetaFavorita(Base):
    __tablename__ = "receta_favorita"

    id_receta_favorita: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_receta: Mapped[int] = mapped_column(Integer, ForeignKey("receta.id_receta"), nullable=False)
    fecha_guardado: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_receta", name="uq_usuario_receta_favorita"),
    )

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="recetas_favoritas")
    receta: Mapped["Receta"] = relationship("Receta", back_populates="favoritos")
