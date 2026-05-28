from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class TagReceta(Base):
    __tablename__ = "tag_receta"

    id_tag: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    recetas: Mapped[list["RecetaTag"]] = relationship("RecetaTag", back_populates="tag")
