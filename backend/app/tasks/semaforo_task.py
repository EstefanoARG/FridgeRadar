import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.database import AsyncSessionLocal
from app.services.semaforo_service import SemaforoService

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(timezone="America/Lima")


@scheduler.scheduled_job(CronTrigger(hour=0, minute=5))
async def actualizar_semaforos():
    """Recalcula el estado de todos los productos cada medianoche."""
    async with AsyncSessionLocal() as db:
        service = SemaforoService(db)
        total = await service.recalcular_todos()
        logger.info(f"Semáforo actualizado: {total} productos procesados")


@scheduler.scheduled_job(CronTrigger(hour=8, minute=0))
async def generar_alertas_diarias():
    """Genera alertas de vencimiento cada mañana a las 8 AM."""
    async with AsyncSessionLocal() as db:
        service = SemaforoService(db)
        alertas = await service.generar_alertas_vencimiento()
        logger.info(f"Alertas generadas: {alertas}")
