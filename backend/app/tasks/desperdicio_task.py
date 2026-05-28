import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.desperdicio import Desperdicio
from app.models.inventario import Inventario

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(timezone="America/Lima")


@scheduler.scheduled_job(CronTrigger(hour=2, minute=0))
async def marcar_vencidos_como_desperdicio():
    """Marca automáticamente productos vencidos como desperdicio."""
    async with AsyncSessionLocal() as db:
        stmt = select(Inventario).where(Inventario.estado_caducidad == "vencido")
        result = await db.execute(stmt)
        vencidos = result.scalars().all()

        count = 0
        for item in vencidos:
            existing = await db.execute(
                select(Desperdicio).where(Desperdicio.id_inventario == item.id_inventario)
            )
            if not existing.scalar_one_or_none():
                desperdicio = Desperdicio(
                    id_inventario=item.id_inventario,
                    cantidad=item.cantidad,
                    motivo="vencido",
                    comentario="Marcado automáticamente por tarea programada",
                )
                db.add(desperdicio)
                count += 1

        await db.commit()
        logger.info("Marcados %d productos vencidos como desperdicio", count)
