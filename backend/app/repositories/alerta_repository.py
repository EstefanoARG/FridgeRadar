
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alerta import Alerta


class AlertaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        id_usuario: int,
        titulo: str,
        mensaje: str,
        tipo: str,
        id_inventario: int | None = None,
    ) -> Alerta:
        alerta = Alerta(
            id_usuario=id_usuario,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            id_inventario=id_inventario,
        )
        self.db.add(alerta)
        await self.db.flush()
        await self.db.refresh(alerta)
        return alerta

    async def get_by_id(self, id_alerta: int) -> Alerta | None:
        result = await self.db.execute(
            select(Alerta).where(Alerta.id_alerta == id_alerta)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Alerta]:
        result = await self.db.execute(select(Alerta))
        return result.scalars().all()

    async def list_by_usuario(
        self, id_usuario: int, solo_no_leidas: bool = False
    ) -> list[Alerta]:
        stmt = select(Alerta).where(Alerta.id_usuario == id_usuario)
        if solo_no_leidas:
            stmt = stmt.where(Alerta.leida == False)
        stmt = stmt.order_by(Alerta.fecha_alerta.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_tipo(
        self, id_usuario: int, tipo: str
    ) -> list[Alerta]:
        result = await self.db.execute(
            select(Alerta)
            .where(Alerta.id_usuario == id_usuario, Alerta.tipo == tipo)
            .order_by(Alerta.fecha_alerta.desc())
        )
        return result.scalars().all()

    async def count_no_leidas(self, id_usuario: int) -> int:
        result = await self.db.execute(
            select(func.count())
            .where(Alerta.id_usuario == id_usuario, Alerta.leida == False)
        )
        return result.scalar() or 0

    async def marcar_como_leida(self, id_alerta: int) -> Alerta | None:
        alerta = await self.get_by_id(id_alerta)
        if alerta is None:
            return None
        alerta.leida = True
        await self.db.flush()
        await self.db.refresh(alerta)
        return alerta

    async def update(self, id_alerta: int, **kwargs) -> Alerta | None:
        alerta = await self.get_by_id(id_alerta)
        if alerta is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(alerta, key, value)
        await self.db.flush()
        await self.db.refresh(alerta)
        return alerta

    async def delete(self, id_alerta: int) -> bool:
        alerta = await self.get_by_id(id_alerta)
        if alerta is None:
            return False
        await self.db.delete(alerta)
        await self.db.flush()
        return True
