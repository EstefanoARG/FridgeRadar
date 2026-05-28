from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictError, NotFoundError
from app.models.receta import Receta
from app.models.receta_favorita import RecetaFavorita
from app.models.receta_ingrediente import RecetaIngrediente
from app.models.receta_tag import RecetaTag
from app.models.tag_receta import TagReceta
from app.schemas.receta import (
    RecetaCreate,
    RecetaDetalleResponse,
    RecetaIngredienteResponse,
    RecetaResponse,
    RecetaUpdate,
    TagRecetaCreate,
    TagRecetaResponse,
)


class RecetaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, data: RecetaCreate, id_usuario: int) -> RecetaDetalleResponse:
        receta = Receta(
            id_usuario_creador=id_usuario,
            nombre=data.nombre,
            descripcion=data.descripcion,
            instrucciones=data.instrucciones,
            tiempo_preparacion=data.tiempo_preparacion,
            dificultad=data.dificultad,
            porciones=data.porciones,
            imagen=data.imagen,
            calorias=data.calorias,
            es_publica=data.es_publica,
        )
        self.db.add(receta)
        await self.db.flush()

        for ing_data in data.ingredientes:
            ingrediente = RecetaIngrediente(
                id_receta=receta.id_receta,
                id_producto=ing_data.id_producto,
                cantidad=ing_data.cantidad,
                unidad_medida=ing_data.unidad_medida,
                obligatorio=ing_data.obligatorio,
                nota=ing_data.nota,
            )
            self.db.add(ingrediente)

        for id_tag in data.tags:
            tag = await self.db.get(TagReceta, id_tag)
            if tag:
                receta_tag = RecetaTag(id_receta=receta.id_receta, id_tag=id_tag)
                self.db.add(receta_tag)

        await self.db.flush()
        return await self._cargar_detalle(receta.id_receta)

    async def obtener(self, id_receta: int) -> RecetaDetalleResponse:
        return await self._cargar_detalle(id_receta)

    async def listar_publicas(self, q: str | None = None) -> list[RecetaResponse]:
        if q:
            return await self.buscar(q)
        stmt = (
            select(Receta)
            .where(Receta.es_publica == True)
            .order_by(Receta.fecha_creacion.desc())
        )
        result = await self.db.execute(stmt)
        recetas = result.scalars().all()
        return [RecetaResponse.model_validate(r) for r in recetas]

    async def buscar(self, nombre: str) -> list[RecetaResponse]:
        stmt = (
            select(Receta)
            .where(Receta.es_publica == True, Receta.nombre.ilike(f"%{nombre}%"))
            .order_by(Receta.nombre)
        )
        result = await self.db.execute(stmt)
        recetas = result.scalars().all()
        return [RecetaResponse.model_validate(r) for r in recetas]

    async def actualizar(
        self, id_receta: int, data: RecetaUpdate, id_usuario: int | None = None
    ) -> RecetaDetalleResponse:
        receta = await self.db.get(Receta, id_receta)
        if not receta:
            raise NotFoundError("Receta no encontrada")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(receta, key, value)
        await self.db.flush()
        return await self._cargar_detalle(id_receta)

    async def eliminar(self, id_receta: int, id_usuario: int | None = None) -> None:
        receta = await self.db.get(Receta, id_receta)
        if not receta:
            raise NotFoundError("Receta no encontrada")

        await self.db.execute(
            delete(RecetaIngrediente).where(RecetaIngrediente.id_receta == id_receta)
        )
        await self.db.execute(
            delete(RecetaTag).where(RecetaTag.id_receta == id_receta)
        )
        await self.db.execute(
            delete(RecetaFavorita).where(RecetaFavorita.id_receta == id_receta)
        )
        await self.db.delete(receta)
        await self.db.flush()

    async def agregar_favorito(self, id_usuario: int, id_receta: int) -> None:
        receta = await self.db.get(Receta, id_receta)
        if not receta:
            raise NotFoundError("Receta no encontrada")

        stmt = select(RecetaFavorita).where(
            RecetaFavorita.id_usuario == id_usuario,
            RecetaFavorita.id_receta == id_receta,
        )
        result = await self.db.execute(stmt)
        if result.scalar_one_or_none():
            raise ConflictError("La receta ya está en favoritos")

        favorita = RecetaFavorita(id_usuario=id_usuario, id_receta=id_receta)
        self.db.add(favorita)
        await self.db.flush()

    async def marcar_favorito(self, id_receta: int, id_usuario: int) -> None:
        await self.agregar_favorito(id_usuario, id_receta)

    async def quitar_favorito(self, id_receta: int, id_usuario: int) -> None:
        stmt = select(RecetaFavorita).where(
            RecetaFavorita.id_usuario == id_usuario,
            RecetaFavorita.id_receta == id_receta,
        )
        result = await self.db.execute(stmt)
        favorita = result.scalar_one_or_none()
        if not favorita:
            raise NotFoundError("Favorito no encontrado")
        await self.db.delete(favorita)
        await self.db.flush()

    async def listar_favoritos(self, id_usuario: int) -> list[RecetaResponse]:
        stmt = (
            select(Receta)
            .join(RecetaFavorita, Receta.id_receta == RecetaFavorita.id_receta)
            .where(RecetaFavorita.id_usuario == id_usuario)
            .order_by(RecetaFavorita.fecha_guardado.desc())
        )
        result = await self.db.execute(stmt)
        recetas = result.scalars().all()
        return [RecetaResponse.model_validate(r) for r in recetas]

    async def crear_tag(self, data: TagRecetaCreate) -> TagRecetaResponse:
        tag = TagReceta(nombre=data.nombre, color=data.color)
        self.db.add(tag)
        await self.db.flush()
        await self.db.refresh(tag)
        return TagRecetaResponse.model_validate(tag)

    async def listar_tags(self) -> list[TagRecetaResponse]:
        result = await self.db.execute(select(TagReceta).order_by(TagReceta.nombre))
        tags = result.scalars().all()
        return [TagRecetaResponse.model_validate(t) for t in tags]

    async def _cargar_detalle(self, id_receta: int) -> RecetaDetalleResponse:
        stmt = (
            select(Receta)
            .where(Receta.id_receta == id_receta)
            .options(
                selectinload(Receta.ingredientes),
                selectinload(Receta.tags).selectinload(RecetaTag.tag),
            )
        )
        result = await self.db.execute(stmt)
        receta = result.scalar_one_or_none()
        if not receta:
            raise NotFoundError("Receta no encontrada")

        tags = [
            TagRecetaResponse.model_validate(rt.tag) for rt in receta.tags
        ]
        ingredientes = [
            RecetaIngredienteResponse.model_validate(i) for i in receta.ingredientes
        ]

        response = RecetaDetalleResponse.model_validate(receta)
        response.tags = tags
        response.ingredientes = ingredientes
        return response
