from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventario import Inventario
from app.models.movimiento_inventario import MovimientoInventario


class InventarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        id_hogar: int,
        id_producto: int,
        id_estante: int,
        id_usuario_agrego: int,
        cantidad: float = 1,
        **kwargs,
    ) -> Inventario:
        inventario = Inventario(
            id_hogar=id_hogar,
            id_producto=id_producto,
            id_estante=id_estante,
            id_usuario_agrego=id_usuario_agrego,
            cantidad=cantidad,
            **kwargs,
        )
        self.db.add(inventario)
        await self.db.flush()
        await self.db.refresh(inventario)
        return inventario

    async def get_by_id(self, id_inventario: int) -> Inventario | None:
        result = await self.db.execute(
            select(Inventario).where(Inventario.id_inventario == id_inventario)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Inventario]:
        result = await self.db.execute(select(Inventario))
        return result.scalars().all()

    async def list_by_hogar(
        self, id_hogar: int, estado_caducidad: str | None = None
    ) -> list[Inventario]:
        stmt = select(Inventario).where(Inventario.id_hogar == id_hogar)
        if estado_caducidad is not None:
            stmt = stmt.where(Inventario.estado_caducidad == estado_caducidad)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, id_inventario: int, **kwargs) -> Inventario | None:
        inventario = await self.get_by_id(id_inventario)
        if inventario is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(inventario, key, value)
        await self.db.flush()
        await self.db.refresh(inventario)
        return inventario

    async def delete(self, id_inventario: int) -> bool:
        inventario = await self.get_by_id(id_inventario)
        if inventario is None:
            return False
        await self.db.delete(inventario)
        await self.db.flush()
        return True

    async def get_movimientos(
        self, id_inventario: int
    ) -> list[MovimientoInventario]:
        result = await self.db.execute(
            select(MovimientoInventario).where(
                MovimientoInventario.id_inventario == id_inventario
            )
        )
        return result.scalars().all()

    async def get_vencimientos_proximos(
        self, id_hogar: int, dias: int
    ) -> list[Inventario]:
        today = datetime.utcnow().date()
        target = today + timedelta(days=dias)
        stmt = (
            select(Inventario)
            .where(
                Inventario.id_hogar == id_hogar,
                Inventario.fecha_vencimiento <= target,
                Inventario.fecha_vencimiento >= today,
                Inventario.estado_caducidad.in_(["verde", "amarillo", "rojo"]),
            )
            .order_by(Inventario.fecha_vencimiento.asc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
