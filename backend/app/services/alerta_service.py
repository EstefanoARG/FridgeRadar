from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.alerta import Alerta
from app.schemas.alerta import AlertaCreate, AlertaResponse


class AlertaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, data: AlertaCreate) -> AlertaResponse:
        alerta = Alerta(
            id_usuario=data.id_usuario,
            id_inventario=data.id_inventario,
            titulo=data.titulo,
            mensaje=data.mensaje,
            tipo=data.tipo,
        )
        self.db.add(alerta)
        await self.db.flush()
        await self.db.refresh(alerta)
        return AlertaResponse.model_validate(alerta)

    async def listar(
        self, id_usuario: int, solo_no_leidas: bool = False
    ) -> list[AlertaResponse]:
        stmt = (
            select(Alerta)
            .where(Alerta.id_usuario == id_usuario)
            .order_by(Alerta.fecha_alerta.desc())
        )
        if solo_no_leidas:
            stmt = stmt.where(Alerta.leida == False)
        result = await self.db.execute(stmt)
        alertas = result.scalars().all()
        return [AlertaResponse.model_validate(a) for a in alertas]

    async def marcar_leida(self, id_alerta: int, id_usuario: int | None = None) -> AlertaResponse:
        alerta = await self.db.get(Alerta, id_alerta)
        if not alerta:
            raise NotFoundError("Alerta no encontrada")
        alerta.leida = True
        await self.db.flush()
        await self.db.refresh(alerta)
        return AlertaResponse.model_validate(alerta)

    async def contar_no_leidas(self, id_usuario: int) -> int:
        stmt = select(func.count(Alerta.id_alerta)).where(
            Alerta.id_usuario == id_usuario, Alerta.leida == False
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def obtener(self, id_alerta: int) -> AlertaResponse:
        alerta = await self.db.get(Alerta, id_alerta)
        if not alerta:
            raise NotFoundError("Alerta no encontrada")
        return AlertaResponse.model_validate(alerta)

    async def eliminar(self, id_alerta: int, id_usuario: int | None = None) -> None:
        alerta = await self.db.get(Alerta, id_alerta)
        if not alerta:
            raise NotFoundError("Alerta no encontrada")
        await self.db.delete(alerta)
        await self.db.flush()
