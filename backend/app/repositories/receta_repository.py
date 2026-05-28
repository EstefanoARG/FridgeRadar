from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.receta import Receta
from app.models.receta_favorita import RecetaFavorita
from app.models.receta_ingrediente import RecetaIngrediente
from app.models.receta_tag import RecetaTag
from app.models.tag_receta import TagReceta


class RecetaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, nombre: str, **kwargs) -> Receta:
        receta = Receta(nombre=nombre, **kwargs)
        self.db.add(receta)
        await self.db.flush()
        await self.db.refresh(receta)
        return receta

    async def get_by_id(self, id_receta: int) -> Receta | None:
        result = await self.db.execute(
            select(Receta).where(Receta.id_receta == id_receta)
        )
        return result.scalar_one_or_none()

    async def get_with_ingredientes(self, id_receta: int) -> Receta | None:
        stmt = (
            select(Receta)
            .where(Receta.id_receta == id_receta)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_tags(self, id_receta: int) -> Receta | None:
        stmt = (
            select(Receta)
            .where(Receta.id_receta == id_receta)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def search_by_nombre(self, nombre: str) -> list[Receta]:
        result = await self.db.execute(
            select(Receta).where(Receta.nombre.ilike(f"%{nombre}%"))
        )
        return result.scalars().all()

    async def list_publicas(self) -> list[Receta]:
        result = await self.db.execute(
            select(Receta).where(Receta.es_publica == True)
        )
        return result.scalars().all()

    async def list_all(self) -> list[Receta]:
        result = await self.db.execute(select(Receta))
        return result.scalars().all()

    async def update(self, id_receta: int, **kwargs) -> Receta | None:
        receta = await self.get_by_id(id_receta)
        if receta is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(receta, key, value)
        await self.db.flush()
        await self.db.refresh(receta)
        return receta

    async def delete(self, id_receta: int) -> bool:
        receta = await self.get_by_id(id_receta)
        if receta is None:
            return False
        await self.db.delete(receta)
        await self.db.flush()
        return True

    # ── RecetaIngrediente ──────────────────────────────────────────────────

    async def add_ingrediente(
        self,
        id_receta: int,
        id_producto: int,
        cantidad: float | None = None,
        unidad_medida: str = "unidad",
        obligatorio: bool = True,
        nota: str | None = None,
    ) -> RecetaIngrediente:
        ingrediente = RecetaIngrediente(
            id_receta=id_receta,
            id_producto=id_producto,
            cantidad=cantidad,
            unidad_medida=unidad_medida,
            obligatorio=obligatorio,
            nota=nota,
        )
        self.db.add(ingrediente)
        await self.db.flush()
        await self.db.refresh(ingrediente)
        return ingrediente

    async def get_ingrediente_by_id(
        self, id_receta_ingrediente: int
    ) -> RecetaIngrediente | None:
        result = await self.db.execute(
            select(RecetaIngrediente).where(
                RecetaIngrediente.id_receta_ingrediente == id_receta_ingrediente
            )
        )
        return result.scalar_one_or_none()

    async def list_ingredientes(self, id_receta: int) -> list[RecetaIngrediente]:
        result = await self.db.execute(
            select(RecetaIngrediente).where(
                RecetaIngrediente.id_receta == id_receta
            )
        )
        return result.scalars().all()

    async def update_ingrediente(
        self, id_receta_ingrediente: int, **kwargs
    ) -> RecetaIngrediente | None:
        ingrediente = await self.get_ingrediente_by_id(id_receta_ingrediente)
        if ingrediente is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(ingrediente, key, value)
        await self.db.flush()
        await self.db.refresh(ingrediente)
        return ingrediente

    async def delete_ingrediente(self, id_receta_ingrediente: int) -> bool:
        ingrediente = await self.get_ingrediente_by_id(id_receta_ingrediente)
        if ingrediente is None:
            return False
        await self.db.delete(ingrediente)
        await self.db.flush()
        return True

    # ── TagReceta ──────────────────────────────────────────────────────────

    async def create_tag(
        self, nombre: str, color: str | None = None
    ) -> TagReceta:
        tag = TagReceta(nombre=nombre, color=color)
        self.db.add(tag)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag

    async def get_tag_by_id(self, id_tag: int) -> TagReceta | None:
        result = await self.db.execute(
            select(TagReceta).where(TagReceta.id_tag == id_tag)
        )
        return result.scalar_one_or_none()

    async def get_tag_by_nombre(self, nombre: str) -> TagReceta | None:
        result = await self.db.execute(
            select(TagReceta).where(TagReceta.nombre == nombre)
        )
        return result.scalar_one_or_none()

    async def list_tags(self) -> list[TagReceta]:
        result = await self.db.execute(select(TagReceta))
        return result.scalars().all()

    async def update_tag(self, id_tag: int, **kwargs) -> TagReceta | None:
        tag = await self.get_tag_by_id(id_tag)
        if tag is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(tag, key, value)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag

    async def delete_tag(self, id_tag: int) -> bool:
        tag = await self.get_tag_by_id(id_tag)
        if tag is None:
            return False
        await self.db.delete(tag)
        await self.db.flush()
        return True

    # ── RecetaTag ──────────────────────────────────────────────────────────

    async def add_tag_to_receta(
        self, id_receta: int, id_tag: int
    ) -> RecetaTag:
        rt = RecetaTag(id_receta=id_receta, id_tag=id_tag)
        self.db.add(rt)
        await self.db.flush()
        await self.db.refresh(rt)
        return rt

    async def get_receta_tag(self, id_receta_tag: int) -> RecetaTag | None:
        result = await self.db.execute(
            select(RecetaTag).where(RecetaTag.id_receta_tag == id_receta_tag)
        )
        return result.scalar_one_or_none()

    async def list_tags_of_receta(self, id_receta: int) -> list[RecetaTag]:
        result = await self.db.execute(
            select(RecetaTag).where(RecetaTag.id_receta == id_receta)
        )
        return result.scalars().all()

    async def remove_tag_from_receta(self, id_receta_tag: int) -> bool:
        rt = await self.get_receta_tag(id_receta_tag)
        if rt is None:
            return False
        await self.db.delete(rt)
        await self.db.flush()
        return True

    # ── RecetaFavorita ─────────────────────────────────────────────────────

    async def add_favorito(
        self, id_usuario: int, id_receta: int
    ) -> RecetaFavorita:
        fav = RecetaFavorita(id_usuario=id_usuario, id_receta=id_receta)
        self.db.add(fav)
        await self.db.flush()
        await self.db.refresh(fav)
        return fav

    async def get_favorito_by_id(
        self, id_receta_favorita: int
    ) -> RecetaFavorita | None:
        result = await self.db.execute(
            select(RecetaFavorita).where(
                RecetaFavorita.id_receta_favorita == id_receta_favorita
            )
        )
        return result.scalar_one_or_none()

    async def list_favoritos_by_usuario(
        self, id_usuario: int
    ) -> list[RecetaFavorita]:
        result = await self.db.execute(
            select(RecetaFavorita).where(
                RecetaFavorita.id_usuario == id_usuario
            )
        )
        return result.scalars().all()

    async def list_favoritos_by_receta(
        self, id_receta: int
    ) -> list[RecetaFavorita]:
        result = await self.db.execute(
            select(RecetaFavorita).where(
                RecetaFavorita.id_receta == id_receta
            )
        )
        return result.scalars().all()

    async def remove_favorito(self, id_receta_favorita: int) -> bool:
        fav = await self.get_favorito_by_id(id_receta_favorita)
        if fav is None:
            return False
        await self.db.delete(fav)
        await self.db.flush()
        return True
