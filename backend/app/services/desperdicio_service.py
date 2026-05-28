from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.desperdicio import Desperdicio
from app.models.inventario import Inventario
from app.models.movimiento_inventario import MovimientoInventario
from app.schemas.desperdicio import DesperdicioCreate, DesperdicioResponse


class DesperdicioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def registrar(self, data: DesperdicioCreate, id_usuario: int) -> DesperdicioResponse:
        inventario = await self.db.get(Inventario, data.id_inventario)
        if not inventario:
            raise NotFoundError("Item de inventario no encontrado")

        desperdicio = Desperdicio(
            id_inventario=data.id_inventario,
            cantidad=data.cantidad or inventario.cantidad,
            motivo=data.motivo,
            comentario=data.comentario,
        )
        self.db.add(desperdicio)

        movimiento = MovimientoInventario(
            id_inventario=data.id_inventario,
            id_usuario=id_usuario,
            tipo_movimiento="eliminado",
            cantidad=data.cantidad or inventario.cantidad,
            descripcion=f"Registrado como desperdicio: {data.motivo or 'sin motivo'}",
        )
        self.db.add(movimiento)
        await self.db.flush()
        await self.db.refresh(desperdicio)
        return DesperdicioResponse.model_validate(desperdicio)

    async def listar_por_hogar(self, id_hogar: int) -> list[DesperdicioResponse]:
        stmt = (
            select(Desperdicio)
            .join(Inventario, Desperdicio.id_inventario == Inventario.id_inventario)
            .where(Inventario.id_hogar == id_hogar)
            .order_by(Desperdicio.fecha_desperdicio.desc())
        )
        result = await self.db.execute(stmt)
        desperdicios = result.scalars().all()
        return [DesperdicioResponse.model_validate(d) for d in desperdicios]

    async def obtener_metricas(self, id_hogar: int) -> dict:
        total = await self.db.execute(
            select(func.coalesce(func.sum(Desperdicio.cantidad), 0))
            .select_from(Desperdicio)
            .join(Inventario, Desperdicio.id_inventario == Inventario.id_inventario)
            .where(Inventario.id_hogar == id_hogar)
        )
        total_desperdiciado = float(total.scalar() or 0)

        por_motivo_result = await self.db.execute(
            select(
                Desperdicio.motivo,
                func.coalesce(func.sum(Desperdicio.cantidad), 0).label("total"),
                func.count(Desperdicio.id_desperdicio).label("conteo"),
            )
            .join(Inventario, Desperdicio.id_inventario == Inventario.id_inventario)
            .where(Inventario.id_hogar == id_hogar)
            .group_by(Desperdicio.motivo)
        )
        por_motivo = {}
        for row in por_motivo_result:
            por_motivo[row.motivo or "sin_motivo"] = {
                "total": float(row.total),
                "conteo": row.conteo,
            }

        total_items = await self.db.execute(
            select(func.count(Desperdicio.id_desperdicio))
            .join(Inventario, Desperdicio.id_inventario == Inventario.id_inventario)
            .where(Inventario.id_hogar == id_hogar)
        )
        total_count = total_items.scalar() or 0

        return {
            "total_desperdiciado": total_desperdiciado,
            "total_items": total_count,
            "por_motivo": por_motivo,
        }
