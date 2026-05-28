from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import *


class RecetaTag(Base):
    __tablename__ = "receta_tag"

    id_receta_tag: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_receta: Mapped[int] = mapped_column(Integer, ForeignKey("receta.id_receta"), nullable=False)
    id_tag: Mapped[int] = mapped_column(Integer, ForeignKey("tag_receta.id_tag"), nullable=False)

    __table_args__ = (
        UniqueConstraint("id_receta", "id_tag", name="uq_receta_tag"),
    )

    receta: Mapped["Receta"] = relationship("Receta", back_populates="tags")
    tag: Mapped["TagReceta"] = relationship("TagReceta", back_populates="recetas")
