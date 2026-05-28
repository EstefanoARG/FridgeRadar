from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.zona import Zona
from app.schemas.zona import ZonaCreate, ZonaResponse, ZonaUpdate


class ZonaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, data: ZonaCreate) -> ZonaResponse:
        zona = Zona(
            id_hogar=data.id_hogar,
            nombre=data.nombre,
            tipo=data.tipo,
            icono=data.icono,
            temperatura_min=data.temperatura_min,
            temperatura_max=data.temperatura_max,
        )
        self.db.add(zona)
        await self.db.flush()
        await self.db.refresh(zona)
        return ZonaResponse.model_validate(zona)

    async def listar(self, id_hogar: int | None = None) -> list[ZonaResponse]:
        stmt = select(Zona)
        if id_hogar is not None:
            stmt = stmt.where(Zona.id_hogar == id_hogar)
        result = await self.db.execute(stmt)
        zonas = result.scalars().all()
        return [ZonaResponse.model_validate(z) for z in zonas]

    async def obtener(self, id_zona: int) -> ZonaResponse:
        zona = await self.db.get(Zona, id_zona)
        if not zona:
            raise NotFoundError("Zona no encontrada")
        return ZonaResponse.model_validate(zona)

    async def actualizar(self, id_zona: int, data: ZonaUpdate) -> ZonaResponse:
        zona = await self.db.get(Zona, id_zona)
        if not zona:
            raise NotFoundError("Zona no encontrada")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(zona, key, value)
        await self.db.flush()
        await self.db.refresh(zona)
        return ZonaResponse.model_validate(zona)

    async def eliminar(self, id_zona: int) -> None:
        zona = await self.db.get(Zona, id_zona)
        if not zona:
            raise NotFoundError("Zona no encontrada")
        await self.db.delete(zona)
        await self.db.flush()
