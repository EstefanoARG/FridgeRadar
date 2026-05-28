import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.database import AsyncSessionLocal
from app.services.alerta_service import AlertaService

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(timezone="America/Lima")


@scheduler.scheduled_job(CronTrigger(hour=8, minute=0))
async def generar_alertas_batch():
    """Genera alertas masivas cada mañana."""
    async with AsyncSessionLocal() as db:
        service = AlertaService(db)
        logger.info("Tarea de generación de alertas ejecutada")
