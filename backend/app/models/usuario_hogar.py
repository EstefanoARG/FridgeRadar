from datetime import datetime
from sqlalchemy import Integer, Enum, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class UsuarioHogar(Base):
    __tablename__ = "usuario_hogar"

    id_usuario_hogar: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_hogar: Mapped[int] = mapped_column(Integer, ForeignKey("hogar.id_hogar"), nullable=False)
    rol: Mapped[str] = mapped_column(Enum("owner", "admin", "miembro"), default="miembro")
    fecha_union: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_hogar", name="uq_usuario_hogar"),
    )

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="hogares")
    hogar: Mapped["Hogar"] = relationship("Hogar", back_populates="miembros")
